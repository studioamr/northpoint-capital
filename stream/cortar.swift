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

// ── LA MARCA, RASTERIZADA ──
//  Los CATextLayer NO se dibujan en un script de línea de comandos (no hay
//  run loop de AppKit que los rasterice: salen barras vacías — pasó dos
//  veces). La forma que SÍ funciona siempre: pintar el texto con CoreText
//  a un CGImage y colgarlo como `contents` de una capa normal.
func textoImagen(ancho: CGFloat, alto: CGFloat, videoAlto: CGFloat,
                 titulo: String, etiqueta: String) -> CGImage? {
    let esp = CGColorSpaceCreateDeviceRGB()
    guard let cx = CGContext(data: nil, width: Int(ancho), height: Int(alto),
            bitsPerComponent: 8, bytesPerRow: 0, space: esp,
            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { return nil }
    cx.clear(CGRect(x: 0, y: 0, width: ancho, height: alto))

    func pinta(_ txt: String, _ fuente: String, _ tam: CGFloat,
               _ color: CGColor, _ y: CGFloat, _ track: CGFloat = 0) {
        let f = CTFontCreateWithName(fuente as CFString, tam, nil)
        // claves de CoreText (sin AppKit: esto corre en línea de comandos)
        var atts: [NSAttributedString.Key: Any] = [
            kCTFontAttributeName as NSAttributedString.Key: f,
            kCTForegroundColorAttributeName as NSAttributedString.Key: color
        ]
        if track != 0 { atts[kCTKernAttributeName as NSAttributedString.Key] = track }
        let linea = CTLineCreateWithAttributedString(
            NSAttributedString(string: txt, attributes: atts))
        // OJO: CTLineGetImageBounds devuelve el origen RELATIVO al
        // textPosition que traiga el contexto — o sea, basura de la línea
        // anterior, y el texto se va fuera de pantalla. El ancho honesto
        // para centrar es el tipográfico.
        let w = CGFloat(CTLineGetTypographicBounds(linea, nil, nil, nil))
        cx.textPosition = CGPoint(x: (ancho - w)/2, y: y)
        CTLineDraw(linea, cx)
    }

    let margen = (alto - videoAlto) / 2      // alto de cada barra
    let oro   = CGColor(red: 0.788, green: 0.659, blue: 0.298, alpha: 1)
    let claro = CGColor(gray: 0.95, alpha: 1)
    let tenue = CGColor(gray: 0.55, alpha: 1)

    // ── barra de ARRIBA: marca + etiqueta de sesión ──
    let topBase = alto - margen
    pinta("NORTHPOINT", "HelveticaNeue-Bold", 60, claro, topBase + margen*0.52, 7)
    pinta(etiqueta, "Menlo-Bold", 26, oro, topBase + margen*0.30, 5)

    // ── barra de ABAJO: el titular del clip + el llamado ──
    // el titular se parte en dos renglones si no cabe
    let maxAncho = ancho - 120
    var l1 = titulo, l2 = ""
    let fTit = CTFontCreateWithName("HelveticaNeue-Bold" as CFString, 52, nil)
    func mide(_ t: String) -> CGFloat {
        CTLineGetTypographicBounds(CTLineCreateWithAttributedString(
            NSAttributedString(string: t, attributes:
                [kCTFontAttributeName as NSAttributedString.Key: fTit])), nil, nil, nil)
    }
    if mide(titulo) > maxAncho {
        let palabras = titulo.split(separator: " ")
        var a: [String] = [], b: [String] = []
        for p in palabras {
            if mide((a + [String(p)]).joined(separator: " ")) <= maxAncho && b.isEmpty {
                a.append(String(p))
            } else { b.append(String(p)) }
        }
        l1 = a.joined(separator: " "); l2 = b.joined(separator: " ")
    }
    if l2.isEmpty {
        pinta(l1, "HelveticaNeue-Bold", 52, claro, margen*0.52)
    } else {
        pinta(l1, "HelveticaNeue-Bold", 48, claro, margen*0.62)
        pinta(l2, "HelveticaNeue-Bold", 48, claro, margen*0.62 - 60)
    }
    pinta("discord.gg/TWeVqTTPS", "Menlo-Regular", 24, tenue, 58, 3)

    return cx.makeImage()
}

// ── exportar un rango ──
func exporta(desde: Double, hasta: Double, a destino: URL,
             vertical: Bool, titulo: String, etiqueta: String,
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

    let vc = AVMutableVideoComposition()
    vc.frameDuration = CMTime(value: 1, timescale: 30)

    let inst = AVMutableVideoCompositionInstruction()
    inst.timeRange = CMTimeRange(start: .zero, duration: dur)
    let capa = AVMutableVideoCompositionLayerInstruction(assetTrack: cv)

    if vertical {
        // 1080x1920 con el chart centrado a ancho completo y barras de marca
        let W: CGFloat = 1080, H: CGFloat = 1920
        vc.renderSize = CGSize(width: W, height: H)
        let escala = W / tamano.width
        let altoV = tamano.height * escala
        var t = CGAffineTransform(scaleX: escala, y: escala)
        t = t.concatenating(CGAffineTransform(translationX: 0, y: (H - altoV)/2))
        capa.setTransform(t, at: .zero)

        let padre = CALayer()
        padre.frame = CGRect(x: 0, y: 0, width: W, height: H)
        padre.backgroundColor = CGColor(red: 0.031, green: 0.031, blue: 0.031, alpha: 1)
        let capaVideo = CALayer()
        capaVideo.frame = padre.frame
        padre.addSublayer(capaVideo)              // el video primero…
        let marca = CALayer()                      // …y la marca ENCIMA
        marca.frame = padre.frame
        marca.contents = textoImagen(ancho: W, alto: H, videoAlto: altoV,
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
    ex.shouldOptimizeForNetworkUse = true
    ex.exportAsynchronously {
        let e = ex.error as NSError?
        let msg = e.map { "\($0.localizedDescription) [\($0.domain) \($0.code)]" +
            (($0.userInfo[NSUnderlyingErrorKey] as? NSError).map { u in
                "  ← \(u.domain) \(u.code)" } ?? "") } ?? ""
        listo(ex.status == .completed, msg)
    }
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
                etiqueta: m.tipo + (m.auto == true ? " · JOURNAL" : "")) { o, e in
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
