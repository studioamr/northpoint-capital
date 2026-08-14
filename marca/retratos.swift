import AppKit
import CoreImage
import Vision
import Foundation

/*  NORTHPOINT · RETRATOS
    Convierte las fotos de André en retratos con el mismo lenguaje que el resto
    de la marca: fondo apagado, luz dura de un lado, blanco y negro con negros
    profundos. La referencia es el perfil de Goyo.

    Las de Goyo son GENERADAS por IA. Éstas son las fotos reales de André,
    tratadas — y para un negocio cuyo activo es la credibilidad, eso es mejor:
    nadie puede señalar la foto y decir «ése no eres tú».

    La cara se encuentra con Vision, no a ojo: encuadrar por el centro de la
    imagen deja la cabeza cortada en cuanto la selfie viene ladeada, que es
    justo como vienen todas.

        swift retratos.swift                    # procesa lo que haya en marca/fotos
        swift retratos.swift --color            # deja el color en vez de B/N   */

let HOME = FileManager.default.homeDirectoryForCurrentUser.path
let DIR = HOME + "/claude/northpoint/marca/fotos"
let SALIDA = HOME + "/claude/northpoint/marca/retratos"
let COLOR = CommandLine.arguments.contains("--color")
let ctx = CIContext()

struct Formato { let nombre: String; let w: Int; let h: Int; let holgura: CGFloat }
/* holgura = cuánto espacio dejar alrededor de la cara, en anchos de cara */
let FORMATOS = [
    Formato(nombre: "retrato",  w: 1200, h: 1600, holgura: 1.65),  // la página de perfil
    Formato(nombre: "avatar",   w: 1000, h: 1000, holgura: 1.15),  // IG · TikTok · YouTube
    Formato(nombre: "portada",  w: 2560, h: 1440, holgura: 3.20),  // banner de YouTube
]

/// Carga la foto YA ENDEREZADA. Las del iPhone vienen con la orientación en
/// los metadatos, no en los píxeles: sin esto, Vision busca la cara en una
/// imagen acostada y el encuadre sale por cualquier lado.
func carga(_ ruta: String) -> CIImage? {
    guard let img = CIImage(contentsOf: URL(fileURLWithPath: ruta),
                            options: [.applyOrientationProperty: true]) else { return nil }
    return img
}

/// El brillo medio de una zona. Sirve para exponer por la CARA y no por el
/// cuarto: casi todas las selfies de André son de noche y en interior, así que
/// medir la imagen completa da un número que no dice nada de su cara.
func brilloMedio(_ img: CIImage, en zona: CGRect) -> CGFloat {
    let f = CIFilter(name: "CIAreaAverage")!
    f.setValue(img.cropped(to: zona), forKey: kCIInputImageKey)
    f.setValue(CIVector(cgRect: zona), forKey: kCIInputExtentKey)
    guard let out = f.outputImage else { return 0.5 }
    var px = [UInt8](repeating: 0, count: 4)
    ctx.render(out, toBitmap: &px, rowBytes: 4, bounds: CGRect(x: 0, y: 0, width: 1, height: 1),
               format: .RGBA8, colorSpace: CGColorSpaceCreateDeviceRGB())
    return (CGFloat(px[0]) * 0.30 + CGFloat(px[1]) * 0.59 + CGFloat(px[2]) * 0.11) / 255
}

/// Dónde está la cara, en coordenadas de imagen (origen abajo-izquierda).
func caraEn(_ img: CIImage) -> CGRect? {
    let pet = VNDetectFaceRectanglesRequest()
    let man = VNImageRequestHandler(ciImage: img, options: [:])
    try? man.perform([pet])
    guard let obs = (pet.results as? [VNFaceObservation])?
        .max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { return nil }
    let e = img.extent
    return CGRect(x: e.origin.x + obs.boundingBox.origin.x * e.width,
                  y: e.origin.y + obs.boundingBox.origin.y * e.height,
                  width:  obs.boundingBox.width  * e.width,
                  height: obs.boundingBox.height * e.height)
}

/// El tratamiento: negros profundos, piel con textura, fondo que se va.
func trata(_ base: CIImage, cara: CGRect?) -> CIImage {
    var img = base

    /* ── EXPONER POR LA CARA ──
       El primer intento aplicaba contraste y viñeta a la foto tal cual, y con
       una selfie de noche el resultado era una mancha negra: no había luz que
       contrastar. Aquí se mide la cara y se sube la exposición hasta dejarla
       donde debe estar, ANTES de tocar nada más. */
    if let c = cara {
        let medio = brilloMedio(img, en: c)
        if medio > 0.02 {
            let objetivo: CGFloat = 0.60
            let ev = max(-1.0, min(3.8, log2(objetivo / medio)))
            let e = CIFilter(name: "CIExposureAdjust")!
            e.setValue(img, forKey: kCIInputImageKey)
            e.setValue(ev, forKey: kCIInputEVKey)
            img = e.outputImage ?? img
        }
    }

    /* Recuperar luces y abrir sombras. Subir la exposición de una foto a
       contraluz revienta lo blanco —la camisa se convierte en un papel— y deja
       la cara todavía en sombra. Esto trata cada extremo por separado. */
    if let hs = CIFilter(name: "CIHighlightShadowAdjust") {
        hs.setValue(img, forKey: kCIInputImageKey)
        hs.setValue(0.74, forKey: "inputHighlightAmount")   // <1 baja las luces
        hs.setValue(0.38, forKey: "inputShadowAmount")      // >0 abre las sombras
        img = hs.outputImage ?? img
    }

    /* el ruido sube junto con la exposición: se limpia antes de afilar */
    if let r = CIFilter(name: "CINoiseReduction") {
        r.setValue(img, forKey: kCIInputImageKey)
        r.setValue(0.035, forKey: "inputNoiseLevel")
        r.setValue(0.75, forKey: "inputSharpness")
        img = r.outputImage ?? img
    }

    if !COLOR {
        /* B/N por mezcla de canales, no por desaturar: subir el rojo hace que
           la piel se abra y la barba se separe del fondo. Desaturar a secas
           deja una papilla gris. */
        let f = CIFilter(name: "CIColorMatrix")!
        f.setValue(img, forKey: kCIInputImageKey)
        let r: CGFloat = 0.46, g: CGFloat = 0.40, b: CGFloat = 0.14
        f.setValue(CIVector(x: r, y: g, z: b, w: 0), forKey: "inputRVector")
        f.setValue(CIVector(x: r, y: g, z: b, w: 0), forKey: "inputGVector")
        f.setValue(CIVector(x: r, y: g, z: b, w: 0), forKey: "inputBVector")
        img = f.outputImage ?? img
    }

    /* contraste y un punto de negro real: las selfies de interior vienen
       lavadas y sin negro, y eso es lo que las delata como selfie */
    let c = CIFilter(name: "CIColorControls")!
    c.setValue(img, forKey: kCIInputImageKey)
    c.setValue(1.09, forKey: kCIInputContrastKey)
    c.setValue(0.012, forKey: kCIInputBrightnessKey)
    c.setValue(COLOR ? 0.82 : 1.0, forKey: kCIInputSaturationKey)
    img = c.outputImage ?? img

    /* curva en S suave: aplasta las sombras y deja respirar las luces */
    let t = CIFilter(name: "CIToneCurve")!
    t.setValue(img, forKey: kCIInputImageKey)
    t.setValue(CIVector(x: 0.00, y: 0.00), forKey: "inputPoint0")
    t.setValue(CIVector(x: 0.24, y: 0.21), forKey: "inputPoint1")
    t.setValue(CIVector(x: 0.50, y: 0.50), forKey: "inputPoint2")
    t.setValue(CIVector(x: 0.76, y: 0.83), forKey: "inputPoint3")
    t.setValue(CIVector(x: 1.00, y: 1.00), forKey: "inputPoint4")
    img = t.outputImage ?? img

    /* nitidez fina: la cámara frontal es blanda y el retrato pide filo en ojos
       y barba, no en toda la imagen */
    let s = CIFilter(name: "CIUnsharpMask")!
    s.setValue(img, forKey: kCIInputImageKey)
    s.setValue(1.9, forKey: kCIInputRadiusKey)
    s.setValue(0.24, forKey: kCIInputIntensityKey)
    img = s.outputImage ?? img

    return img
}

/// Viñeta fuerte: es lo que apaga la sala de la casa y deja sólo la cara.
func vineta(_ img: CIImage, cara: CGRect?) -> CIImage {
    let e = img.extent
    let f = CIFilter(name: "CIVignetteEffect")!
    f.setValue(img, forKey: kCIInputImageKey)
    let c = cara.map { CIVector(x: $0.midX, y: $0.midY) }
        ?? CIVector(x: e.midX, y: e.midY)
    f.setValue(c, forKey: kCIInputCenterKey)
    f.setValue(max(e.width, e.height) * 0.90, forKey: kCIInputRadiusKey)
    f.setValue(0.85, forKey: kCIInputIntensityKey)
    f.setValue(1.10, forKey: "inputFalloff")
    return f.outputImage ?? img
}

/// Grano: sin él, el B/N con mucho contraste se ve digital y plano.
func grano(_ img: CIImage) -> CIImage {
    guard let r = CIFilter(name: "CIRandomGenerator")?.outputImage else { return img }
    let g = r.cropped(to: img.extent)
    let gris = CIFilter(name: "CIColorMatrix")!
    gris.setValue(g, forKey: kCIInputImageKey)
    let k: CGFloat = 0.016
    gris.setValue(CIVector(x: k, y: 0, z: 0, w: 0), forKey: "inputRVector")
    gris.setValue(CIVector(x: k, y: 0, z: 0, w: 0), forKey: "inputGVector")
    gris.setValue(CIVector(x: k, y: 0, z: 0, w: 0), forKey: "inputBVector")
    gris.setValue(CIVector(x: 0, y: 0, z: 0, w: 0), forKey: "inputAVector")
    gris.setValue(CIVector(x: 0, y: 0, z: 0, w: 1), forKey: "inputBiasVector")
    guard let ruido = gris.outputImage else { return img }
    let mez = CIFilter(name: "CIOverlayBlendMode")!
    mez.setValue(ruido, forKey: kCIInputImageKey)
    mez.setValue(img, forKey: kCIInputBackgroundImageKey)
    return mez.outputImage ?? img
}

/// Recorta al formato pedido, encuadrando la cara donde va en un retrato:
/// los ojos cerca del tercio superior, no en el centro.
func encuadra(_ img: CIImage, cara: CGRect?, _ f: Formato) -> CIImage {
    let e = img.extent
    let objetivo = CGFloat(f.w) / CGFloat(f.h)
    var caja: CGRect

    if let c = cara {
        let ancho = min(e.width, c.width * f.holgura * (objetivo > 1 ? objetivo : 1))
        let alto = min(e.height, ancho / objetivo)
        /* la cara arriba del centro: en un retrato los ojos van al tercio */
        let cy = c.midY - alto * 0.10
        var x = c.midX - ancho / 2
        var y = cy - alto / 2
        x = max(e.minX, min(x, e.maxX - ancho))
        y = max(e.minY, min(y, e.maxY - alto))
        caja = CGRect(x: x, y: y, width: ancho, height: alto)
    } else {
        let ancho = min(e.width, e.height * objetivo)
        let alto = ancho / objetivo
        caja = CGRect(x: e.midX - ancho/2, y: e.midY - alto/2, width: ancho, height: alto)
    }
    let cortada = img.cropped(to: caja)
    let escala = CGFloat(f.w) / caja.width
    return cortada
        .transformed(by: CGAffineTransform(translationX: -caja.minX, y: -caja.minY))
        .transformed(by: CGAffineTransform(scaleX: escala, y: escala))
}

func guarda(_ img: CIImage, _ ruta: String) {
    guard let cg = ctx.createCGImage(img, from: img.extent) else { return }
    let rep = NSBitmapImageRep(cgImage: cg)
    guard let d = rep.representation(using: .jpeg,
        properties: [.compressionFactor: 0.93]) else { return }
    try? d.write(to: URL(fileURLWithPath: ruta))
}

// ───────────────────────────────────────────────

let fm = FileManager.default
try? fm.createDirectory(atPath: SALIDA, withIntermediateDirectories: true)
let fotos = ((try? fm.contentsOfDirectory(atPath: DIR)) ?? [])
    .filter { $0.lowercased().hasSuffix(".jpg") || $0.lowercased().hasSuffix(".jpeg")
           || $0.lowercased().hasSuffix(".png") }
    .sorted()

if fotos.isEmpty {
    print("  ✗ no hay fotos en \(DIR)")
    print("    Arrastra ahí 4–6 fotos tuyas y vuelve a correrlo.")
    exit(1)
}

print("  \(fotos.count) fotos · \(COLOR ? "color" : "blanco y negro")")
var hechos = 0, sinCara = 0

for nombre in fotos {
    let ruta = DIR + "/" + nombre
    guard let base = carga(ruta) else { continue }
    let cara = caraEn(base)
    if cara == nil { sinCara += 1 }
    let tratada = grano(vineta(trata(base, cara: cara), cara: cara))
    let raiz = (nombre as NSString).deletingPathExtension

    for f in FORMATOS {
        let out = "\(SALIDA)/\(raiz)-\(f.nombre).jpg"
        guarda(encuadra(tratada, cara: cara, f), out)
        hechos += 1
    }
    print(String(format: "  ✓ %-18s %@", (raiz as NSString).utf8String!,
                 cara == nil ? "(sin cara detectada — encuadre al centro)" : ""))
}

print("  ── \(hechos) imágenes en marca/retratos/")
if sinCara > 0 { print("  ⚠ \(sinCara) sin cara detectada: revisa que salga completa y con luz") }
