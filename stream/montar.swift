import AVFoundation
import CoreGraphics
import CoreText
import Foundation

/*  NORTHPOINT · MONTA LA PRESENTACIÓN
    Toma las tomas de voz de André (ya cortadas por cortar-voz.py), dibuja la
    lámina de cada una y las empalma. La duración la manda LA VOZ.

    Las láminas se dibujan AQUÍ, con CoreGraphics. El primer intento las sacaba
    de capturas de Chrome: un perfil nuevo por lámina tardaba minutos y de 18
    salieron 2. Dibujarlas es instantáneo y además deja el centrado exacto.

        swift montar.swift                    # usa la voz real
        swift montar.swift --prueba           # usa la voz de máquina, para ver  */

let HOME = FileManager.default.homeDirectoryForCurrentUser.path
let NP = HOME + "/claude/northpoint"
let INTRO = NP + "/.respaldos/intro"
let PRUEBA = CommandLine.arguments.contains("--prueba")
let VOZ = INTRO + (PRUEBA ? "/voz2-maquina" : "/voz-real")
let W = 1920, H = 1080
let FONDO = CGColor(red: 8/255, green: 8/255, blue: 8/255, alpha: 1)
let ORO = CGColor(red: 200/255, green: 162/255, blue: 74/255, alpha: 1)
let HUESO = CGColor(red: 244/255, green: 244/255, blue: 244/255, alpha: 1)
let TENUE = CGColor(gray: 0.62, alpha: 1)
let DEBIL = CGColor(gray: 0.44, alpha: 1)

struct Lamina {
    var kicker = "", num = "", titulo: [String] = [], sub = "", pie = ""
    var esVideo = false
}

/* Cada bloque: el archivo de voz y lo que se ve mientras se oye. El orden es
   el del guion — y el mismo de plan.json, que es lo que corta la grabación. */
let bloques: [(String, Lamina)] = [
  ("01-marca", Lamina(kicker: "SESIÓN EN VIVO · NUEVA YORK", titulo: ["NORTHPOINT"],
                      sub: "La mesa, en vivo.", pie: "DISCORD.GG/TWEVQTTPS")),
  ("02-no-señales", Lamina(kicker: "SI ES TU PRIMERA VEZ",
                      titulo: ["Esto no es", "un canal de señales"],
                      sub: "Es una mesa de trading en vivo. Vas a ver cómo se opera de verdad,\ný los días en los que no pasa absolutamente nada.")),
  ("03-sin-trade", Lamina(titulo: ["Hoy puede que", "no haya trade."],
                      sub: "Y si no lo hay, el stream fue un éxito.")),
  ("04-quien", Lamina(kicker: "QUIÉN HABLA", titulo: ["André"],
                      sub: "Futuros del Nasdaq — el micro, MNQ.\nCuentas de fondeo, retiros cobrados, todo registrado trade por trade.")),
  ("05-firma", Lamina(kicker: "LA FIRMA", titulo: ["Respaldamos traders", "que ya son rentables"],
                      sub: "Si ya sacas payouts, nosotros pagamos tus evaluaciones.\nTú pones el talento, nosotros el capital.")),
  ("06-primero", Lamina(titulo: ["Primero demuestras,", "después entras."],
                      sub: "No es un curso de «hazte rico». No le vendo el sueño a nadie.")),
  ("07-reglas", Lamina(kicker: "EL CORAZÓN DEL CANAL", titulo: ["Las cinco reglas"],
                      sub: "No se negocian. Están en pantalla todo el tiempo.")),
  ("08-r1", Lamina(num: "01", titulo: ["Un solo trade", "al día"],
                      sub: "Uno. Gane o pierda, se acabó. No hay revancha.")),
  ("09-r2", Lamina(num: "02", titulo: ["Sin alerta,", "no hay trade"],
                      sub: "Si el indicador no suena, el trade no existe.\nAunque yo tenga ganas. Aunque el mercado se vea obvio.")),
  ("10-r3", Lamina(num: "03", titulo: ["El stop", "se respeta"],
                      sub: "Nunca lo muevo. Cuando el mercado me dice que estoy\nequivocado, le creo.")),
  ("11-r4", Lamina(num: "04", titulo: ["Cada trade", "se escribe"],
                      sub: "Todos. Con captura. Los buenos y los feos.")),
  ("12-r5", Lamina(num: "05", titulo: ["La paciencia", "es la ventaja"],
                      sub: "La que manda sobre todas las demás.")),
  ("13-aburrirse", Lamina(titulo: ["Así no se pierde", "una cuenta."],
                      sub: "No se pierde por equivocarse en un trade.\nSe pierde por aburrirse y meter cinco.")),
  ("14-plan", Lamina(kicker: "EL PLAN DE HOY", titulo: ["Dos pantallas"],
                      sub: "5 minutos para el contexto. 1 minuto para ejecutar.")),
  ("__video__", Lamina(esVideo: true)),
  ("15-nadie", Lamina(titulo: ["Todo mundo enseña", "la entrada."],
                      sub: "Nadie te enseña las tres horas de no hacer nada\nque vienen antes.")),
  ("16-discord", Lamina(kicker: "DÓNDE VIVE LA MESA", titulo: ["El Discord"],
                      sub: "El journal, el bootcamp y la gente que está haciendo lo mismo.\nEs gratis entrar.", pie: "DISCORD.GG/TWEVQTTPS")),
  ("17-aviso", Lamina(kicker: "Y VA EN SERIO", titulo: ["No soy tu", "asesor financiero"],
                      sub: "Nada de lo que veas aquí es una recomendación. Los futuros tienen\napalancamiento y se puede perder dinero rápido.")),
  ("18-vamonos", Lamina(titulo: ["Vámonos."],
                      sub: "A partir de aquí es la sesión. Pregunta lo que quieras en el chat.",
                      pie: "NORTHPOINT · TRADER BACKING")),
]

// ─────────────────────────── dibujo ───────────────────────────

func fuente(_ nombre: String, _ tam: CGFloat) -> CTFont {
    CTFontCreateWithName(nombre as CFString, tam, nil)
}

/* una línea de texto, centrada en x */
func linea(_ cx: CGContext, _ txt: String, _ f: CTFont, _ col: CGColor,
           y: CGFloat, tracking: CGFloat = 0) {
    guard !txt.isEmpty else { return }
    /* las claves de NSAttributedString.Key no existen sin AppKit; las de
       CoreText sí y son las que de verdad lee CTLine */
    let attrs: [CFString: Any] = [
        kCTFontAttributeName: f,
        kCTForegroundColorAttributeName: col,
        kCTKernAttributeName: tracking]
    let linea = CTLineCreateWithAttributedString(
        CFAttributedStringCreate(nil, txt as CFString, attrs as CFDictionary)!)
    let ancho = CTLineGetTypographicBounds(linea, nil, nil, nil)
    cx.textPosition = CGPoint(x: (CGFloat(W) - CGFloat(ancho))/2, y: y)
    CTLineDraw(linea, cx)
}

/* el mismo cielo en todas las láminas: semilla fija, si no parpadea entre corte
   y corte y parece un error de codificación */
func estrellas(_ cx: CGContext) {
    var s: UInt64 = 7
    func r() -> CGFloat { s = (s &* 6364136223846793005 &+ 1442695040888963407); return CGFloat((s >> 33) % 100000) / 100000 }
    for _ in 0..<420 {
        let x = r()*CGFloat(W), y = r()*CGFloat(H), a = r()*0.5 + 0.05, t = r()*1.4 + 0.35
        cx.setFillColor(CGColor(gray: 1, alpha: a))
        cx.fillEllipse(in: CGRect(x: x, y: y, width: t, height: t))
    }
}

func dibuja(_ l: Lamina) -> CGImage {
    let cs = CGColorSpaceCreateDeviceRGB()
    let cx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8,
                       bytesPerRow: 0, space: cs,
                       bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    cx.setFillColor(FONDO); cx.fill(CGRect(x: 0, y: 0, width: W, height: H))
    estrellas(cx)

    /* halo cálido al centro: le quita lo plano al negro */
    if let g = CGGradient(colorsSpace: cs,
        colors: [CGColor(red: 200/255, green: 162/255, blue: 74/255, alpha: 0.10),
                 CGColor(red: 200/255, green: 162/255, blue: 74/255, alpha: 0)] as CFArray,
        locations: [0, 1]) {
        cx.drawRadialGradient(g, startCenter: CGPoint(x: W/2, y: H/2), startRadius: 0,
                              endCenter: CGPoint(x: W/2, y: H/2), endRadius: 760,
                              options: [])
    }
    /* marco */
    cx.setStrokeColor(CGColor(gray: 1, alpha: 0.07)); cx.setLineWidth(1)
    cx.stroke(CGRect(x: 46, y: 46, width: CGFloat(W)-92, height: CGFloat(H)-92))

    let mono = "Menlo", sans = "HelveticaNeue-Medium", sansL = "HelveticaNeue-Light"

    /* marca, arriba */
    linea(cx, "NORTHPOINT", fuente(sans, 26), HUESO, y: CGFloat(H) - 116, tracking: 9)
    linea(cx, "TRADER BACKING", fuente(mono, 13), DEBIL, y: CGFloat(H) - 148, tracking: 5.5)

    /* el bloque central se arma de abajo hacia arriba para quedar centrado de
       verdad: medir primero, colocar después */
    let hKicker: CGFloat = l.kicker.isEmpty ? 0 : 62
    let hNum: CGFloat = l.num.isEmpty ? 0 : 172
    let hTit: CGFloat = CGFloat(l.titulo.count) * (l.titulo.count > 1 ? 108 : 124)
    let subLineas = l.sub.isEmpty ? [] : l.sub.components(separatedBy: "\n")
    let hSub: CGFloat = subLineas.isEmpty ? 0 : CGFloat(subLineas.count) * 52 + 30
    var y = CGFloat(H)/2 + (hKicker + hNum + hTit + hSub)/2 - 40

    if !l.kicker.isEmpty {
        y -= 20; linea(cx, l.kicker, fuente(mono, 19), TENUE, y: y, tracking: 8); y -= 42
    }
    if !l.num.isEmpty {
        y -= 118; linea(cx, l.num, fuente("HelveticaNeue-Thin", 150), ORO, y: y, tracking: -4); y -= 54
    }
    let tamTit: CGFloat = l.titulo.count > 1 ? 84 : 118
    for t in l.titulo {
        y -= tamTit * 0.86
        linea(cx, t, fuente(sans, tamTit), HUESO, y: y, tracking: -tamTit*0.026)
        y -= tamTit * 0.14
    }
    if !subLineas.isEmpty {
        y -= 46
        for t in subLineas { linea(cx, t, fuente(sansL, 38), TENUE, y: y); y -= 52 }
    }
    if !l.pie.isEmpty { linea(cx, l.pie, fuente(mono, 20), DEBIL, y: 96, tracking: 6) }

    return cx.makeImage()!
}

// ─────────────────────────── montaje ───────────────────────────

/* una lámina → clip de N segundos. El mismo pixel buffer se re-usa en cada
   frame: escribir 40 segundos cuesta lo mismo que escribir uno. */
func clip(_ img: CGImage, seg: Double) -> AVAsset? {
    let tmp = URL(fileURLWithPath: NSTemporaryDirectory())
        .appendingPathComponent("np-\(UUID().uuidString).mp4")
    guard let wr = try? AVAssetWriter(outputURL: tmp, fileType: .mp4) else { return nil }
    let inp = AVAssetWriterInput(mediaType: .video, outputSettings: [
        AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: W, AVVideoHeightKey: H])
    let ad = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: inp,
        sourcePixelBufferAttributes: [kCVPixelBufferPixelFormatTypeKey as String:
            Int(kCVPixelFormatType_32BGRA)])
    wr.add(inp); wr.startWriting(); wr.startSession(atSourceTime: .zero)

    var pb: CVPixelBuffer?
    CVPixelBufferCreate(nil, W, H, kCVPixelFormatType_32BGRA, nil, &pb)
    guard let buf = pb else { return nil }
    CVPixelBufferLockBaseAddress(buf, [])
    let cx = CGContext(data: CVPixelBufferGetBaseAddress(buf), width: W, height: H,
        bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(buf),
        space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
                  | CGBitmapInfo.byteOrder32Little.rawValue)!
    cx.draw(img, in: CGRect(x: 0, y: 0, width: W, height: H))
    CVPixelBufferUnlockBaseAddress(buf, [])

    let fps: Int32 = 30, total = max(1, Int(seg * Double(fps)))
    var i = 0
    let s = DispatchSemaphore(value: 0)
    inp.requestMediaDataWhenReady(on: DispatchQueue(label: "np.lamina")) {
        while inp.isReadyForMoreMediaData {
            if i >= total { inp.markAsFinished(); wr.finishWriting { s.signal() }; return }
            ad.append(buf, withPresentationTime: CMTime(value: CMTimeValue(i), timescale: fps))
            i += 1
        }
    }
    s.wait()
    return AVURLAsset(url: tmp)
}

let comp = AVMutableComposition()
let pv = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
let pa = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
var cursor = CMTime.zero
var instrucciones: [AVMutableVideoCompositionInstruction] = []
var faltan: [String] = []

for (nombre, lam) in bloques {
    /* la voz manda: si falta una toma, se avisa y se sigue — más vale un video
       incompleto y señalado que uno que se cuelga */
    var voz: AVURLAsset? = nil
    for ext in ["wav", "aiff", "m4a"] {
        let u = URL(fileURLWithPath: "\(VOZ)/\(nombre).\(ext)")
        if FileManager.default.fileExists(atPath: u.path) { voz = AVURLAsset(url: u); break }
    }
    guard let v = voz, let ta = v.tracks(withMediaType: .audio).first else {
        faltan.append(nombre); continue
    }
    let dur = v.duration
    try? pa.insertTimeRange(CMTimeRange(start: .zero, duration: dur), of: ta, at: cursor)

    var fuente: AVAsset?
    var rango = CMTimeRange(start: .zero, duration: dur)
    var escala: CGFloat = 0            // 0 = se calcula del tamaño real

    if lam.esVideo {
        /* la mesa de verdad: el corte del stream */
        let mesa = URL(fileURLWithPath: HOME + "/Movies/northpoint-2026-08-14-desde-37.mp4")
        if FileManager.default.fileExists(atPath: mesa.path) {
            fuente = AVURLAsset(url: mesa)
            rango = CMTimeRange(start: CMTime(seconds: 60, preferredTimescale: 600), duration: dur)
        } else {
            fuente = clip(dibuja(Lamina(kicker: "LA MESA", titulo: ["En vivo"])), seg: CMTimeGetSeconds(dur))
        }
    } else {
        fuente = clip(dibuja(lam), seg: CMTimeGetSeconds(dur))
    }
    guard let f = fuente, let tv = f.tracks(withMediaType: .video).first else { continue }
    try? pv.insertTimeRange(rango, of: tv, at: cursor)

    let nat = tv.naturalSize
    if escala == 0 { escala = min(CGFloat(W)/nat.width, CGFloat(H)/nat.height) }
    let ins = AVMutableVideoCompositionInstruction()
    ins.timeRange = CMTimeRange(start: cursor, duration: dur)
    ins.backgroundColor = FONDO
    let li = AVMutableVideoCompositionLayerInstruction(assetTrack: pv)
    li.setTransform(CGAffineTransform(scaleX: escala, y: escala)
        .concatenating(CGAffineTransform(translationX: (CGFloat(W) - nat.width*escala)/2,
                                         y: (CGFloat(H) - nat.height*escala)/2)), at: .zero)
    ins.layerInstructions = [li]
    instrucciones.append(ins)
    cursor = cursor + dur
    print(String(format: "  ✓ %-14s %5.1fs", (nombre as NSString).utf8String!, CMTimeGetSeconds(dur)))
}

if !faltan.isEmpty {
    print("  ⚠ sin voz (\(faltan.count)): " + faltan.joined(separator: ", "))
}
if instrucciones.isEmpty {
    print("  ✗ no hay ninguna toma de voz en \(VOZ)")
    print("    Graba siguiendo stream/GRABAR-VOZ.md y corre:")
    print("    python3 stream/cortar-voz.py ~/Movies/voz-andre.m4a")
    exit(1)
}

let vc = AVMutableVideoComposition()
vc.frameDuration = CMTime(value: 1, timescale: 30)
vc.renderSize = CGSize(width: W, height: H)
vc.instructions = instrucciones

let dst = URL(fileURLWithPath: HOME + "/Movies/NORTHPOINT-presentacion.mp4")
try? FileManager.default.removeItem(at: dst)
guard let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPreset1920x1080) else { exit(1) }
ex.outputURL = dst; ex.outputFileType = .mp4; ex.videoComposition = vc
ex.shouldOptimizeForNetworkUse = true
let s = DispatchSemaphore(value: 0)
ex.exportAsynchronously { s.signal() }
while ex.status == .exporting || ex.status == .waiting {
    print(String(format: "  montando… %.0f%%", ex.progress*100)); Thread.sleep(forTimeInterval: 15)
}
s.wait()
print(ex.status == .completed
  ? "✓ \(dst.path) · \(String(format: "%.1f", CMTimeGetSeconds(comp.duration)/60)) min"
  : "✗ \(ex.error?.localizedDescription ?? "")")
