import Cocoa

func renderIcon(size: Int) -> NSImage {
    let s = CGFloat(size)
    let img = NSImage(size: NSSize(width: s, height: s))
    img.lockFocus()

    let ctx = NSGraphicsContext.current!.cgContext

    // Background macOS squircle / rounded rect
    let rect = CGRect(x: s * 0.05, y: s * 0.05, width: s * 0.9, height: s * 0.9)
    let path = CGPath(roundedRect: rect, cornerWidth: s * 0.22, cornerHeight: s * 0.22, transform: nil)
    ctx.addPath(path)
    ctx.setFillColor(NSColor(red: 0.08, green: 0.11, blue: 0.16, alpha: 1.0).cgColor)
    ctx.fillPath()

    // Subtle border glow
    ctx.addPath(path)
    ctx.setStrokeColor(NSColor(red: 0.35, green: 0.65, blue: 1.0, alpha: 0.4).cgColor)
    ctx.setLineWidth(s * 0.02)
    ctx.strokePath()

    // Brain logo outline (normalized to 32x32 coordinate space)
    ctx.saveGState()
    ctx.scaleBy(x: s / 32.0, y: s / 32.0)

    // Outer brain curve: M3 17c0-7 6-12 13-12s13 5 13 12c0 5-5 9-13 9S3 22 3 17z
    let brainPath = CGMutablePath()
    brainPath.move(to: CGPoint(x: 3, y: 15))
    brainPath.addCurve(to: CGPoint(x: 16, y: 27), control1: CGPoint(x: 3, y: 22), control2: CGPoint(x: 9, y: 27))
    brainPath.addCurve(to: CGPoint(x: 29, y: 15), control1: CGPoint(x: 23, y: 27), control2: CGPoint(x: 29, y: 22))
    brainPath.addCurve(to: CGPoint(x: 16, y: 6), control1: CGPoint(x: 29, y: 10), control2: CGPoint(x: 24, y: 6))
    brainPath.addCurve(to: CGPoint(x: 3, y: 15), control1: CGPoint(x: 8, y: 6), control2: CGPoint(x: 3, y: 10))
    brainPath.closeSubpath()

    ctx.addPath(brainPath)
    ctx.setStrokeColor(NSColor(red: 0.35, green: 0.65, blue: 1.0, alpha: 1.0).cgColor)
    ctx.setLineWidth(1.8)
    ctx.strokePath()

    // Inner folds:
    // M7 17c2-4 5-6 9-6s7 2 9 6
    let folds1 = CGMutablePath()
    folds1.move(to: CGPoint(x: 7, y: 15))
    folds1.addCurve(to: CGPoint(x: 25, y: 15), control1: CGPoint(x: 12, y: 19), control2: CGPoint(x: 20, y: 19))
    ctx.addPath(folds1)
    ctx.setStrokeColor(NSColor(red: 0.47, green: 0.75, blue: 1.0, alpha: 1.0).cgColor)
    ctx.setLineWidth(1.4)
    ctx.setLineCap(.round)
    ctx.strokePath()

    // M9.5 21c2-2.6 4-3.6 6.5-3.6s4.5 1 6.5 3.6
    let folds2 = CGMutablePath()
    folds2.move(to: CGPoint(x: 9.5, y: 11))
    folds2.addCurve(to: CGPoint(x: 22.5, y: 11), control1: CGPoint(x: 13.5, y: 14.6), control2: CGPoint(x: 18.5, y: 14.6))
    ctx.addPath(folds2)
    ctx.strokePath()

    // Central sulcus / crest: M16 5.2v4
    let crest = CGMutablePath()
    crest.move(to: CGPoint(x: 16, y: 22.8))
    crest.addLine(to: CGPoint(x: 16, y: 26.8))
    ctx.addPath(crest)
    ctx.strokePath()

    ctx.restoreGState()
    img.unlockFocus()
    return img
}

func savePNG(image: NSImage, path: String) {
    guard let tiff = image.tiffRepresentation,
          let rep = NSBitmapImageRep(data: tiff),
          let png = rep.representation(using: .png, properties: [:]) else { return }
    try? png.write(to: URL(fileURLWithPath: path))
}

let iconsetDir = "/tmp/AppIcon.iconset"
try? FileManager.default.createDirectory(atPath: iconsetDir, withIntermediateDirectories: true)

let sizes: [(Int, String)] = [
    (16, "icon_16x16.png"),
    (32, "icon_16x16@2x.png"),
    (32, "icon_32x32.png"),
    (64, "icon_32x32@2x.png"),
    (128, "icon_128x128.png"),
    (256, "icon_128x128@2x.png"),
    (256, "icon_256x256.png"),
    (512, "icon_256x256@2x.png"),
    (512, "icon_512x512.png"),
    (1024, "icon_512x512@2x.png")
]

for (s, filename) in sizes {
    let img = renderIcon(size: s)
    savePNG(image: img, path: "\(iconsetDir)/\(filename)")
}
print("Iconset created at \(iconsetDir)")
