import Cocoa
import WebKit

class AppDelegate: NSObject, NSApplicationDelegate, NSWindowDelegate {
    var window: NSWindow!
    var webView: WKWebView!
    var pythonProcess: Process?
    var serverPort: Int = 8765

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupMenu()
        startPythonBackend()

        // Create main application window
        let screenSize = NSScreen.main?.visibleFrame.size ?? CGSize(width: 1400, height: 900)
        let windowWidth = min(1400, screenSize.width * 0.9)
        let windowHeight = min(900, screenSize.height * 0.9)
        let rect = NSRect(x: (screenSize.width - windowWidth) / 2,
                          y: (screenSize.height - windowHeight) / 2,
                          width: windowWidth,
                          height: windowHeight)

        let styleMask: NSWindow.StyleMask = [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView]
        window = NSWindow(contentRect: rect, styleMask: styleMask, backing: .buffered, defer: false)
        window.title = "Brain Circuit Atlas"
        window.titlebarAppearsTransparent = true
        window.titleVisibility = .hidden
        window.isReleasedWhenClosed = false
        window.delegate = self
        window.center()

        // Configure WKWebView for high performance WebGL 3D
        let config = WKWebViewConfiguration()
        config.preferences.setValue(true, forKey: "developerExtrasEnabled")
        let prefs = WKWebpagePreferences()
        prefs.allowsContentJavaScript = true
        config.defaultWebpagePreferences = prefs

        webView = WKWebView(frame: window.contentView!.bounds, configuration: config)
        webView.autoresizingMask = [.width, .height]
        window.contentView?.addSubview(webView)

        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)

        // Load app from local Python server
        loadAtlasUrl()
    }

    func loadAtlasUrl(attempts: Int = 0) {
        guard let url = URL(string: "http://127.0.0.1:\(serverPort)/index.html") else { return }
        
        let request = URLRequest(url: url, cachePolicy: .reloadIgnoringLocalCacheData, timeoutInterval: 2.0)
        let task = URLSession.shared.dataTask(with: request) { [weak self] (_, response, error) in
            DispatchQueue.main.async {
                guard let self = self else { return }
                if let httpResp = response as? HTTPURLResponse, httpResp.statusCode == 200 {
                    self.webView.load(URLRequest(url: url))
                } else if attempts < 15 {
                    DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) {
                        self.loadAtlasUrl(attempts: attempts + 1)
                    }
                } else {
                    self.webView.loadHTMLString("""
                        <html><body style="font-family:sans-serif;background:#0d1117;color:#c9d1d9;display:flex;align-items:center;justify-content:center;height:100vh;">
                        <div style="text-align:center;">
                            <h2>Connecting to Brain Circuit Atlas backend...</h2>
                            <p>Port: \(self.serverPort)</p>
                        </div>
                        </body></html>
                    """, baseURL: nil)
                }
            }
        }
        task.resume()
    }

    func startPythonBackend() {
        // Locate python script in app bundle or source dir
        let bundlePath = Bundle.main.bundlePath
        let possibleDirs = [
            Bundle.main.resourcePath.map { "\($0)/backend/server.py" },
            "\(bundlePath)/Contents/Resources/backend/server.py",
            "\(bundlePath)/../../backend/server.py",
            "./backend/server.py"
        ].compactMap { $0 }

        var scriptPath = "./backend/server.py"
        for p in possibleDirs {
            if FileManager.default.fileExists(atPath: p) {
                scriptPath = p
                break
            }
        }

        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        process.arguments = [scriptPath, String(serverPort)]
        
        // Working directory
        let workingDir = (scriptPath as NSString).deletingLastPathComponent.replacingOccurrences(of: "/backend", with: "")
        process.currentDirectoryURL = URL(fileURLWithPath: workingDir)

        do {
            try process.run()
            self.pythonProcess = process
        } catch {
            print("Failed to launch python backend: \(error)")
        }
    }

    func windowShouldClose(_ sender: NSWindow) -> Bool {
        NSApp.terminate(nil)
        return true
    }

    func applicationWillTerminate(_ notification: Notification) {
        if let proc = pythonProcess, proc.isRunning {
            proc.terminate()
        }
    }

    func setupMenu() {
        let mainMenu = NSMenu()
        
        // App Menu
        let appMenuItem = NSMenuItem()
        let appMenu = NSMenu()
        appMenu.addItem(withTitle: "About Brain Circuit Atlas", action: #selector(NSApplication.orderFrontStandardAboutPanel(_:)), keyEquivalent: "")
        appMenu.addItem(NSMenuItem.separator())
        appMenu.addItem(withTitle: "Hide Brain Circuit Atlas", action: #selector(NSApplication.hide(_:)), keyEquivalent: "h")
        let hideOthers = NSMenuItem(title: "Hide Others", action: #selector(NSApplication.hideOtherApplications(_:)), keyEquivalent: "h")
        hideOthers.keyEquivalentModifierMask = [.command, .option]
        appMenu.addItem(hideOthers)
        appMenu.addItem(withTitle: "Show All", action: #selector(NSApplication.unhideAllApplications(_:)), keyEquivalent: "")
        appMenu.addItem(NSMenuItem.separator())
        appMenu.addItem(withTitle: "Quit Brain Circuit Atlas", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q")
        appMenuItem.submenu = appMenu
        mainMenu.addItem(appMenuItem)

        // Edit Menu (Enables Cmd+C, Cmd+V, Cmd+X, Cmd+A, Cmd+Z in WKWebView)
        let editMenuItem = NSMenuItem()
        let editMenu = NSMenu(title: "Edit")
        editMenu.addItem(withTitle: "Undo", action: #selector(UndoManager.undo), keyEquivalent: "z")
        editMenu.addItem(withTitle: "Redo", action: #selector(UndoManager.redo), keyEquivalent: "Z")
        editMenu.addItem(NSMenuItem.separator())
        editMenu.addItem(withTitle: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
        editMenu.addItem(withTitle: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
        editMenu.addItem(withTitle: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")
        editMenu.addItem(withTitle: "Select All", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a")
        editMenuItem.submenu = editMenu
        mainMenu.addItem(editMenuItem)

        // View Menu
        let viewMenuItem = NSMenuItem()
        let viewMenu = NSMenu(title: "View")
        viewMenu.addItem(withTitle: "Reload", action: #selector(reloadWebView), keyEquivalent: "r")
        viewMenu.addItem(withTitle: "Toggle Full Screen", action: #selector(toggleFullScreen), keyEquivalent: "f")
        viewMenuItem.submenu = viewMenu
        mainMenu.addItem(viewMenuItem)

        NSApp.mainMenu = mainMenu
    }

    @objc func reloadWebView() {
        webView?.reload()
    }

    @objc func toggleFullScreen() {
        window?.toggleFullScreen(nil)
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
