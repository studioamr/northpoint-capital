#!/usr/bin/env swift
//  ═══════════════════════════════════════════════════════════════
//  NORTHPOINT · CORTADOR DE CLIPS
//
//  Toma la grabación del stream + el .json del marcador y saca solo:
//    · un clip VERTICAL 1080x1920 por cada marca  → TikTok / Reels / Shorts
//    · un RESUMEN horizontal con todos los momentos → YouTube
//
//  Usa AVFoundation, que ya viene en macOS: cero instalaciones, cero
//  dependencias, cero descargas. Corre con `swift cortar.swift`.
//
//  Uso:
//    swift cortar.swift stream.mkv marcas-2026-08-13.json
//    swift cortar.swift stream.mp4 marcas.json --solo-clips
//    swift cortar.swift stream.mp4 marcas.json --solo-resumen
//
//  OJO CON EL FORMATO: AVFoundation NO lee .mkv. En OBS graba en .mp4
//  o .mov (Ajustes → Salida → Formato de grabación). Si ya tienes un
//  .mkv, OBS lo remuxea sin recomprimir: Archivo → Remuxear grabaciones.
//  ═══════════════════════════════════════════════════════════════

import AVFoundation
import Foundation
import CoreImage
import CoreMedia
import QuartzCore

// ── marca del json ──
struct Marca: Codable {
    let t: Double
    let tipo: String
    var auto: Bool?
    var nota: String?
    // zona a recortar, en FRACCIONES del frame [x, y, ancho, alto].
    // Sin esto, un stream de tres pantallas queda ilegible en un celular:
    // el clip vertical enseña sólo el panel que importa.
    var zona: [Double]?
}
struct Marcas: Codable {
    let sesion: String
    var antes: Double?
    var despues: Double?
    let marcas: [Marca]
}

let args = CommandLine.arguments
guard args.count >= 3 else {
    print("""
    NORTHPOINT · cortador de clips

      swift cortar.swift <video> <marcas.json> [--solo-clips|--solo-resumen]

    El video debe ser .mp4 o .mov (AVFoundation no lee .mkv).
    """)
    exit(1)
}
let rutaVideo = URL(fileURLWithPath: args[1])
let rutaJSON  = URL(fileURLWithPath: args[2])
let soloClips   = args.contains("--solo-clips")
let soloResumen = args.contains("--solo-resumen")

guard FileManager.default.fileExists(atPath: rutaVideo.path) else {
    print("✗ No encuentro el video: \(rutaVideo.path)"); exit(1)
}
guard let datos = try? Data(contentsOf: rutaJSON),
      let M = try? JSONDecoder().decode(Marcas.self, from: datos) else {
    print("✗ No pude leer el json de marcas: \(rutaJSON.path)"); exit(1)
}

let ANTES   = M.antes ?? 25
let DESPUES = M.despues ?? 20

// carpeta de salida junto al video: ./clips-<sesion>/
let salida = rutaVideo.deletingLastPathComponent()
    .appendingPathComponent("clips-\(M.sesion)")
try? FileManager.default.createDirectory(at: salida, withIntermediateDirectories: true)

let asset = AVURLAsset(url: rutaVideo)
let sem = DispatchSemaphore(value: 0)

// ── datos del video (duración y pista) ──
var duracion = CMTime.zero
var pistaV: AVAssetTrack?
var pistaA: AVAssetTrack?
var tamano = CGSize(width: 1920, height: 1080)

Task {
    duracion = (try? await asset.load(.duration)) ?? .zero
    pistaV = try? await asset.loadTracks(withMediaType: .video).first
    pistaA = try? await asset.loadTracks(withMediaType: .audio).first
    if let p = pistaV {
        let n = (try? await p.load(.naturalSize)) ?? tamano
        let tr = (try? await p.load(.preferredTransform)) ?? .identity
        tamano = CGSize(width: abs(n.applying(tr).width), height: abs(n.applying(tr).height))
    }
    sem.signal()
}
sem.wait()

guard pistaV != nil else {
    print("""
    ✗ El archivo no trae pista de video que AVFoundation pueda leer.
      Si es .mkv, remuxéalo a .mp4 desde OBS: Archivo → Remuxear grabaciones.
    """)
    exit(1)
}

let segundosTotales = CMTimeGetSeconds(duracion)
print("""

  NORTHPOINT · cortador
  ─────────────────────────────────────────────
  video    \(rutaVideo.lastPathComponent)  (\(Int(tamano.width))x\(Int(tamano.height)), \(fmt(segundosTotales)))
  marcas   \(M.marcas.count)
  salida   \(salida.path)

""")

func fmt(_ s: Double) -> String {
    let x = Int(max(0, s))
    return String(format: "%02d:%02d:%02d", x/3600, (x%3600)/60, x%60)
}
func limpio(_ s: String) -> String {
    let ok = CharacterSet.alphanumerics.union(CharacterSet(charactersIn: "-_"))
    return String(s.unicodeScalars.map { ok.contains($0) ? Character($0) : "-" })
        .lowercased().prefix(28).description
}

// ── LA MARCA, RASTERIZADA ── (diseño de la landing)
//  Los CATextLayer NO se dibujan en un script de línea de comandos (no hay
//  run loop que los rasterice: salen barras vacías). La forma que SÍ
//  funciona: pintar con CoreText a un CGImage y colgarlo como `contents`.
func textoImagen(ancho: CGFloat, alto: CGFloat, videoAlto: CGFloat,
                 titulo: String, etiqueta: String) -> CGImage? {
    let esp = CGColorSpaceCreateDeviceRGB()
    guard let cx = CGContext(data: nil, width: Int(ancho), height: Int(alto),
            bitsPerComponent: 8, bytesPerRow: 0, space: esp,
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return nil }
    cx.clear(CGRect(x: 0, y: 0, width: ancho, height: alto))

    let oro   = CGColor(red: 0.788, green: 0.659, blue: 0.298, alpha: 1)
    let claro = CGColor(gray: 0.95, alpha: 1)
    let tenue = CGColor(gray: 0.52, alpha: 1)
    let margen = (alto - videoAlto) / 2          // alto de cada barra
    let vTop = alto - margen                      // borde superior del video
    let vBot = margen                             // borde inferior del video

    func pinta(_ txt: String, _ fuente: String, _ tam: CGFloat,
               _ color: CGColor, _ y: CGFloat, _ track: CGFloat = 0) {
        let f = CTFontCreateWithName(fuente as CFString, tam, nil)
        var atts: [NSAttributedString.Key: Any] = [
            kCTFontAttributeName as NSAttributedString.Key: f,
            kCTForegroundColorAttributeName as NSAttributedString.Key: color
        ]
        if track != 0 { atts[kCTKernAttributeName as NSAttributedString.Key] = track }
        let linea = CTLineCreateWithAttributedString(
            NSAttributedString(string: txt, attributes: atts))
        // OJO: CTLineGetImageBounds da el origen RELATIVO al textPosition que
        // traiga el contexto (basura de la línea anterior). Para centrar va el
        // ancho TIPOGRÁFICO.
        let w = CGFloat(CTLineGetTypographicBounds(linea, nil, nil, nil))
        cx.textPosition = CGPoint(x: (ancho - w)/2, y: y)
        CTLineDraw(linea, cx)
    }

    // ── el fondo: negro con un halo dorado muy contenido, como la landing ──
    cx.setFillColor(CGColor(red: 0.031, green: 0.031, blue: 0.031, alpha: 1))
    cx.fill(CGRect(x: 0, y: 0, width: ancho, height: alto))
    if let g = CGGradient(colorsSpace: esp, colors: [
            CGColor(red: 0.788, green: 0.659, blue: 0.298, alpha: 0.13),
            CGColor(red: 0.788, green: 0.659, blue: 0.298, alpha: 0)] as CFArray,
            locations: [0, 1]) {
        cx.drawRadialGradient(g, startCenter: CGPoint(x: ancho*0.78, y: alto*0.9),
            startRadius: 0, endCenter: CGPoint(x: ancho*0.78, y: alto*0.9),
            endRadius: ancho*0.85, options: [])
    }
    // campo de estrellas determinista (el mismo gesto de todas las pantallas)
    for i in 0..<130 {
        let d = Double(i)
        cx.setFillColor(CGColor(gray: 1, alpha: 0.05 + Double(i % 5)*0.035))
        cx.fill(CGRect(x: (d*173.2).truncatingRemainder(dividingBy: Double(ancho)),
                       y: (d*97.3).truncatingRemainder(dividingBy: Double(alto)),
                       width: 2, height: 2))
    }

    // ── EL HUECO ── la marca va ENCIMA del video, así que hay que abrirle
    // la ventana o el fondo lo tapa (pasó: marco perfecto, video invisible).
    cx.clear(CGRect(x: 0, y: vBot - 8, width: ancho, height: videoAlto + 16))

    // ── el marco del video: borde fino + escuadras doradas en las esquinas ──
    let m: CGFloat = 26
    cx.setStrokeColor(CGColor(gray: 1, alpha: 0.16)); cx.setLineWidth(1)
    cx.stroke(CGRect(x: m, y: vBot - 10, width: ancho - m*2, height: videoAlto + 20))
    cx.setStrokeColor(oro); cx.setLineWidth(3)
    let e: CGFloat = 46
    for (px, py, sx, sy) in [(m, vBot-10, 1.0, 1.0), (ancho-m, vBot-10, -1.0, 1.0),
                             (m, vBot+videoAlto+10, 1.0, -1.0),
                             (ancho-m, vBot+videoAlto+10, -1.0, -1.0)] {
        cx.move(to: CGPoint(x: px + e*CGFloat(sx), y: py))
        cx.addLine(to: CGPoint(x: px, y: py))
        cx.addLine(to: CGPoint(x: px, y: py + e*CGFloat(sy)))
        cx.strokePath()
    }

    // ── ARRIBA: la marca, su bajada y la etiqueta de sesión ──
    pinta("NORTHPOINT", "HelveticaNeue-Bold", 58, claro, vTop + margen*0.56, 8)
    pinta("TRADER BACKING", "Menlo-Regular", 20, oro, vTop + margen*0.42, 9)
    // píldora de la sesión
    let f = CTFontCreateWithName("Menlo-Bold" as CFString, 21, nil)
    let l = CTLineCreateWithAttributedString(NSAttributedString(string: etiqueta,
        attributes: [kCTFontAttributeName as NSAttributedString.Key: f,
                     kCTKernAttributeName as NSAttributedString.Key: 5]))
    let wEt = CGFloat(CTLineGetTypographicBounds(l, nil, nil, nil))
    let py = vTop + margen*0.18
    cx.setStrokeColor(CGColor(gray: 1, alpha: 0.22)); cx.setLineWidth(1)
    let pill = CGRect(x: (ancho-wEt)/2 - 22, y: py - 12, width: wEt + 44, height: 44)
    cx.addPath(CGPath(roundedRect: pill, cornerWidth: 22, cornerHeight: 22, transform: nil))
    cx.strokePath()
    pinta(etiqueta, "Menlo-Bold", 21, CGColor(gray: 0.82, alpha: 1), py, 5)

    // ── ABAJO: raya dorada, el titular (hasta dos renglones) y el llamado ──
    cx.setFillColor(oro)
    cx.fill(CGRect(x: ancho/2 - 46, y: vBot - margen*0.30, width: 92, height: 4))

    let maxAncho = ancho - 130
    var l1 = titulo, l2 = ""
    let fTit = CTFontCreateWithName("HelveticaNeue-Bold" as CFString, 54, nil)
    func mide(_ t: String) -> CGFloat {
        CGFloat(CTLineGetTypographicBounds(CTLineCreateWithAttributedString(
            NSAttributedString(string: t, attributes:
                [kCTFontAttributeName as NSAttributedString.Key: fTit])), nil, nil, nil))
    }
    if mide(titulo) > maxAncho {
        var a: [String] = [], b: [String] = []
        for p in titulo.split(separator: " ") {
            if b.isEmpty && mide((a + [String(p)]).joined(separator: " ")) <= maxAncho {
                a.append(String(p))
            } else { b.append(String(p)) }
        }
        l1 = a.joined(separator: " "); l2 = b.joined(separator: " ")
    }
    if l2.isEmpty {
        pinta(l1, "HelveticaNeue-Bold", 54, claro, vBot - margen*0.55)
    } else {
        pinta(l1, "HelveticaNeue-Bold", 50, claro, vBot - margen*0.48)
        pinta(l2, "HelveticaNeue-Bold", 50, claro, vBot - margen*0.48 - 62)
    }
    pinta("discord.gg/TWeVqTTPS", "Menlo-Regular", 23, tenue, 62, 4)

    return cx.makeImage()
}

// ── exportar un rango ──
func exporta(desde: Double, hasta: Double, a destino: URL,
             vertical: Bool, titulo: String, etiqueta: String,
             zona: [Double]? = nil, musica: URL? = nil,
             listo: @escaping (Bool, String) -> Void) {

    let comp = AVMutableComposition()
    guard let cv = comp.addMutableTrack(withMediaType: .video,
                    preferredTrackID: kCMPersistentTrackID_Invalid) else {
        listo(false, "no pude crear pista"); return
    }
    // la pista de audio se crea SOLO si el original trae audio: una pista
    // vacía hace que el export muera con "Operation Stopped"
    let ca = (pistaA != nil) ? comp.addMutableTrack(withMediaType: .audio,
               preferredTrackID: kCMPersistentTrackID_Invalid) : nil

    let ini = CMTime(seconds: max(0, desde), preferredTimescale: 600)
    let dur = CMTime(seconds: max(0.5, hasta - max(0, desde)), preferredTimescale: 600)
    let rango = CMTimeRange(start: ini, duration: dur)

    do {
        try cv.insertTimeRange(rango, of: pistaV!, at: .zero)
        if let pa = pistaA, let ca = ca {
            try ca.insertTimeRange(rango, of: pa, at: .zero)
        }
    } catch {
        listo(false, "\(error.localizedDescription)"); return
    }

    // ── LA MÚSICA ── se mete como segunda pista y se agacha para que la
    // voz mande. Es un loop ORIGINAL (musica.py): nada con dueño, así no
    // hay strike en TikTok ni en YouTube.
    var mezclaAudio: AVMutableAudioMix? = nil
    if let mus = musica, FileManager.default.fileExists(atPath: mus.path),
       let cm = comp.addMutableTrack(withMediaType: .audio,
                  preferredTrackID: kCMPersistentTrackID_Invalid) {
        let am = AVURLAsset(url: mus)
        // el .wav es local y ligero: la carga síncrona aquí es honesta y
        // evita el lío de capturar vars mutables en una Task concurrente
        let pm = am.tracks(withMediaType: .audio).first
        let dm = am.duration
        if let pm = pm, dm.seconds > 0.5 {
            var puesto = CMTime.zero
            while puesto < dur {                       // en bucle hasta cubrir
                let queda = dur - puesto
                let cacho = CMTimeMinimum(dm, queda)
                try? cm.insertTimeRange(CMTimeRange(start: .zero, duration: cacho),
                                        of: pm, at: puesto)
                puesto = puesto + cacho
            }
            let par = AVMutableAudioMixInputParameters(track: cm)
            par.setVolume(0.11, at: .zero)             // bien atrás de la voz
            par.setVolumeRamp(fromStartVolume: 0, toEndVolume: 0.11,
                              timeRange: CMTimeRange(start: .zero,
                                duration: CMTime(seconds: 1.2, preferredTimescale: 600)))
            par.setVolumeRamp(fromStartVolume: 0.11, toEndVolume: 0,
                              timeRange: CMTimeRange(
                                start: dur - CMTime(seconds: 1.5, preferredTimescale: 600),
                                duration: CMTime(seconds: 1.5, preferredTimescale: 600)))
            let mx = AVMutableAudioMix()
            var pars: [AVAudioMixInputParameters] = [par]
            if let ca = ca {
                let po = AVMutableAudioMixInputParameters(track: ca)
                po.setVolume(1.0, at: .zero)
                pars.append(po)
            }
            mx.inputParameters = pars
            mezclaAudio = mx
        }
    }

    let vc = AVMutableVideoComposition()
    vc.frameDuration = CMTime(value: 1, timescale: 30)

    let inst = AVMutableVideoCompositionInstruction()
    inst.timeRange = CMTimeRange(start: .zero, duration: dur)
    let capa = AVMutableVideoCompositionLayerInstruction(assetTrack: cv)

    if vertical {
        // 1080x1920. Si la marca trae ZONA, se recorta ese pedazo y se
        // agranda a ancho completo — así el panel que importa se lee en un
        // celular. Sin zona, entra el frame completo.
        let W: CGFloat = 1080, H: CGFloat = 1920
        vc.renderSize = CGSize(width: W, height: H)
        var escala: CGFloat, altoV: CGFloat, dx: CGFloat = 0, dy: CGFloat
        if let z = zona, z.count == 4 {
            let zx = CGFloat(z[0]) * tamano.width
            let zy = CGFloat(z[1]) * tamano.height
            let zw = CGFloat(z[2]) * tamano.width
            let zh = CGFloat(z[3]) * tamano.height
            escala = W / zw
            altoV = zh * escala
            // el eje Y del video crece hacia arriba: la zona se mide desde
            // arriba, así que hay que voltearla
            dx = -zx * escala
            dy = -(tamano.height - zy - zh) * escala + (H - altoV)/2
        } else {
            escala = W / tamano.width
            altoV = tamano.height * escala
            dy = (H - altoV)/2
        }
        var t = CGAffineTransform(scaleX: escala, y: escala)
        t = t.concatenating(CGAffineTransform(translationX: dx, y: dy))
        capa.setTransform(t, at: .zero)

        let padre = CALayer()
        padre.frame = CGRect(x: 0, y: 0, width: W, height: H)
        padre.backgroundColor = CGColor(red: 0.031, green: 0.031, blue: 0.031, alpha: 1)
        let capaVideo = CALayer()
        capaVideo.frame = padre.frame
        padre.addSublayer(capaVideo)              // el video primero…
        let marca = CALayer()                      // …y la marca ENCIMA
        marca.frame = padre.frame
        marca.contents = textoImagen(ancho: W, alto: H,
                                     videoAlto: min(altoV, H * 0.72),
                                     titulo: titulo, etiqueta: etiqueta)
        padre.addSublayer(marca)
        vc.animationTool = AVVideoCompositionCoreAnimationTool(
            postProcessingAsVideoLayer: capaVideo, in: padre)
    } else {
        vc.renderSize = tamano
    }

    inst.layerInstructions = [capa]
    vc.instructions = [inst]

    try? FileManager.default.removeItem(at: destino)
    guard let ex = AVAssetExportSession(asset: comp,
            presetName: AVAssetExportPresetHighestQuality) else {
        listo(false, "no pude crear el exportador"); return
    }
    ex.outputURL = destino
    ex.outputFileType = .mp4
    ex.videoComposition = vc
    if let mx = mezclaAudio { ex.audioMix = mx }
    ex.shouldOptimizeForNetworkUse = true
    ex.exportAsynchronously {
        let e = ex.error as NSError?
        let msg = e.map { "\($0.localizedDescription) [\($0.domain) \($0.code)]" +
            (($0.userInfo[NSUnderlyingErrorKey] as? NSError).map { u in
                "  ← \(u.domain) \(u.code)" } ?? "") } ?? ""
        listo(ex.status == .completed, msg)
    }
}

// ── se compone el loop una vez y sirve para todos los clips ──
var pistaMusica: URL? = nil
if !soloResumen && !M.marcas.isEmpty {
    let wav = salida.appendingPathComponent("northpoint-loop.wav")
    let py = rutaVideo.deletingLastPathComponent()   // musica.py vive con el script
    let script = URL(fileURLWithPath: #filePath).deletingLastPathComponent()
        .appendingPathComponent("musica.py")
    if FileManager.default.fileExists(atPath: script.path) {
        let p = Process()
        p.executableURL = URL(fileURLWithPath: "/usr/bin/env")
        p.arguments = ["python3", script.path, String(Int(ANTES + DESPUES + 6)), wav.path]
        p.standardOutput = FileHandle.nullDevice
        p.standardError = FileHandle.nullDevice
        try? p.run(); p.waitUntilExit()
        if FileManager.default.fileExists(atPath: wav.path) {
            pistaMusica = wav
            print("  ♪ música original compuesta para los clips\n")
        }
    }
    _ = py
}

// ══ 1 · LOS CLIPS VERTICALES ══
if !soloResumen && !M.marcas.isEmpty {
    print("  CLIPS VERTICALES (TikTok · Reels · Shorts)")
    for (i, m) in M.marcas.enumerated() {
        let desde = max(0, m.t - ANTES)
        let hasta = min(segundosTotales, m.t + DESPUES)
        if hasta - desde < 3 { print("  · \(i+1) saltado (fuera del video)"); continue }

        let nota = (m.nota ?? "").isEmpty ? m.tipo : m.nota!
        let nombre = String(format: "clip-%02d-%@.mp4", i+1, limpio(nota))
        let destino = salida.appendingPathComponent(nombre)

        let s2 = DispatchSemaphore(value: 0)
        var ok = false, err = ""
        exporta(desde: desde, hasta: hasta, a: destino, vertical: true,
                titulo: nota.uppercased(),
                etiqueta: m.tipo + (m.auto == true ? " · JOURNAL" : ""),
                zona: m.zona, musica: pistaMusica) { o, e in
            ok = o; err = e; s2.signal()
        }
        s2.wait()
        print("  \(ok ? "✓" : "✗") \(nombre)   [\(fmt(desde)) → \(fmt(hasta))]\(ok ? "" : "  " + err)")
    }
    print("")
}

// ══ 2 · EL RESUMEN PARA YOUTUBE ══
if !soloClips && !M.marcas.isEmpty {
    print("  RESUMEN (YouTube)")
    let comp = AVMutableComposition()
    guard let cv = comp.addMutableTrack(withMediaType: .video,
                    preferredTrackID: kCMPersistentTrackID_Invalid) else {
        print("  ✗ no pude armar el resumen"); exit(1)
    }
    let ca = (pistaA != nil) ? comp.addMutableTrack(withMediaType: .audio,
                preferredTrackID: kCMPersistentTrackID_Invalid) : nil

    var cursor = CMTime.zero
    var puestos = 0
    // se juntan los momentos que se traslapan para que no salgan repetidos
    var rangos: [(Double, Double)] = []
    for m in M.marcas.sorted(by: { $0.t < $1.t }) {
        let a = max(0, m.t - ANTES), b = min(segundosTotales, m.t + DESPUES)
        if b - a < 3 { continue }
        if var ult = rangos.last, a <= ult.1 + 2 {
            ult.1 = max(ult.1, b); rangos[rangos.count-1] = ult
        } else {
            rangos.append((a, b))
        }
    }
    for (a, b) in rangos {
        let r = CMTimeRange(start: CMTime(seconds: a, preferredTimescale: 600),
                            duration: CMTime(seconds: b - a, preferredTimescale: 600))
        do {
            try cv.insertTimeRange(r, of: pistaV!, at: cursor)
            if let pa = pistaA, let ca = ca { try ca.insertTimeRange(r, of: pa, at: cursor) }
            cursor = cursor + r.duration
            puestos += 1
        } catch { print("  · tramo saltado: \(error.localizedDescription)") }
    }

    let destino = salida.appendingPathComponent("resumen-\(M.sesion).mp4")
    try? FileManager.default.removeItem(at: destino)
    if let ex = AVAssetExportSession(asset: comp,
            presetName: AVAssetExportPresetHighestQuality) {
        ex.outputURL = destino
        ex.outputFileType = .mp4
        ex.shouldOptimizeForNetworkUse = true
        let s3 = DispatchSemaphore(value: 0)
        ex.exportAsynchronously { s3.signal() }
        s3.wait()
        let ok = ex.status == .completed
        print("  \(ok ? "✓" : "✗") resumen-\(M.sesion).mp4   \(puestos) momentos · \(fmt(CMTimeGetSeconds(cursor)))")
        if !ok { print("     \(ex.error?.localizedDescription ?? "")") }
    }
    print("")
}

print("  Listo. Los archivos están en:\n  \(salida.path)\n")
