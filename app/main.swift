import Cocoa
import WebKit

class AppDelegate: NSObject, NSApplicationDelegate, NSWindowDelegate {
    var window: NSWindow!
    var webView: WKWebView!
    var pythonProcess: Process?
    var serverPort: Int = 8765

    func applicationDidFinishLaunching(_ notification: Notification) {
        setupMenu()
        setupEventMonitors()
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

    func setupEventMonitors() {
        // Intercept standard display and zoom hotkeys at the app level
        NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            guard let self = self else { return event }
            let flags = event.modifierFlags.intersection(.deviceIndependentFlagsMask)
            let chars = event.charactersIgnoringModifiers ?? ""

            // Cmd + = or Cmd + + -> Zoom In
            if flags == [.command] && (chars == "=" || chars == "+") {
                self.zoomIn()
                return nil
            }
            // Cmd + - -> Zoom Out
            if flags == [.command] && chars == "-" {
                self.zoomOut()
                return nil
            }
            // Cmd + 0 -> Reset Zoom to 100%
            if flags == [.command] && chars == "0" {
                self.actualSize()
                return nil
            }
            // Cmd + [ -> History Back
            if flags == [.command] && chars == "[" {
                self.goBack()
                return nil
            }
            // Cmd + ] -> History Forward
            if flags == [.command] && chars == "]" {
                self.goForward()
                return nil
            }

            return event
        }
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

    // =========================================================================
    // Native macOS Menus and Display Hotkeys
    // =========================================================================
    func setupMenu() {
        let mainMenu = NSMenu()
        
        // --------------------------------------------------
        // 1. App Menu
        // --------------------------------------------------
        let appMenuItem = NSMenuItem()
        let appMenu = NSMenu()
        let aboutItem = NSMenuItem(title: "About Brain Circuit Atlas", action: #selector(openAbout), keyEquivalent: "")
        aboutItem.target = self
        appMenu.addItem(aboutItem)
        appMenu.addItem(NSMenuItem.separator())

        let settingsItem = NSMenuItem(title: "Settings...", action: #selector(openSettings), keyEquivalent: ",")
        settingsItem.keyEquivalentModifierMask = [.command]
        settingsItem.target = self
        appMenu.addItem(settingsItem)
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

        // --------------------------------------------------
        // 2. File Menu
        // --------------------------------------------------
        let fileMenuItem = NSMenuItem()
        let fileMenu = NSMenu(title: "File")

        let closeItem = NSMenuItem(title: "Close Window", action: #selector(closeWindow), keyEquivalent: "w")
        closeItem.keyEquivalentModifierMask = [.command]
        closeItem.target = self
        fileMenu.addItem(closeItem)
        fileMenu.addItem(NSMenuItem.separator())

        let printItem = NSMenuItem(title: "Print...", action: #selector(printPage), keyEquivalent: "p")
        printItem.keyEquivalentModifierMask = [.command]
        printItem.target = self
        fileMenu.addItem(printItem)

        fileMenuItem.submenu = fileMenu
        mainMenu.addItem(fileMenuItem)

        // --------------------------------------------------
        // 3. Edit Menu
        // --------------------------------------------------
        let editMenuItem = NSMenuItem()
        let editMenu = NSMenu(title: "Edit")
        editMenu.addItem(withTitle: "Undo", action: #selector(UndoManager.undo), keyEquivalent: "z")
        let redoItem = NSMenuItem(title: "Redo", action: #selector(UndoManager.redo), keyEquivalent: "z")
        redoItem.keyEquivalentModifierMask = [.command, .shift]
        editMenu.addItem(redoItem)
        editMenu.addItem(NSMenuItem.separator())
        editMenu.addItem(withTitle: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x")
        editMenu.addItem(withTitle: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c")
        editMenu.addItem(withTitle: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v")
        editMenu.addItem(withTitle: "Select All", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a")
        editMenu.addItem(NSMenuItem.separator())

        let findItem = NSMenuItem(title: "Find in Atlas...", action: #selector(focusSearch), keyEquivalent: "f")
        findItem.keyEquivalentModifierMask = [.command]
        findItem.target = self
        editMenu.addItem(findItem)

        editMenuItem.submenu = editMenu
        mainMenu.addItem(editMenuItem)

        // --------------------------------------------------
        // 4. View Menu (Display, Zoom, Appearance, 3D Controls)
        // --------------------------------------------------
        let viewMenuItem = NSMenuItem()
        let viewMenu = NSMenu(title: "View")

        let reloadItem = NSMenuItem(title: "Reload Page", action: #selector(reloadWebView), keyEquivalent: "r")
        reloadItem.keyEquivalentModifierMask = [.command]
        reloadItem.target = self
        viewMenu.addItem(reloadItem)

        let forceReloadItem = NSMenuItem(title: "Force Reload from Origin", action: #selector(forceReloadWebView), keyEquivalent: "r")
        forceReloadItem.keyEquivalentModifierMask = [.command, .shift]
        forceReloadItem.target = self
        viewMenu.addItem(forceReloadItem)

        viewMenu.addItem(NSMenuItem.separator())

        // Zoom Controls
        let zoomInItem = NSMenuItem(title: "Zoom In", action: #selector(zoomIn), keyEquivalent: "+")
        zoomInItem.keyEquivalentModifierMask = [.command]
        zoomInItem.target = self
        viewMenu.addItem(zoomInItem)

        let zoomInAlt = NSMenuItem(title: "Zoom In", action: #selector(zoomIn), keyEquivalent: "=")
        zoomInAlt.keyEquivalentModifierMask = [.command]
        zoomInAlt.isAlternate = true
        zoomInAlt.target = self
        viewMenu.addItem(zoomInAlt)

        let zoomOutItem = NSMenuItem(title: "Zoom Out", action: #selector(zoomOut), keyEquivalent: "-")
        zoomOutItem.keyEquivalentModifierMask = [.command]
        zoomOutItem.target = self
        viewMenu.addItem(zoomOutItem)

        let actualSizeItem = NSMenuItem(title: "Actual Size (100%)", action: #selector(actualSize), keyEquivalent: "0")
        actualSizeItem.keyEquivalentModifierMask = [.command]
        actualSizeItem.target = self
        viewMenu.addItem(actualSizeItem)

        viewMenu.addItem(NSMenuItem.separator())

        // Display Modes & Theme
        let themeItem = NSMenuItem(title: "Toggle Dark / Light Mode", action: #selector(toggleTheme), keyEquivalent: "d")
        themeItem.keyEquivalentModifierMask = [.command, .shift]
        themeItem.target = self
        viewMenu.addItem(themeItem)

        let labelsItem = NSMenuItem(title: "Toggle 3D Labels", action: #selector(toggleLabels), keyEquivalent: "l")
        labelsItem.keyEquivalentModifierMask = [.command, .shift]
        labelsItem.target = self
        viewMenu.addItem(labelsItem)

        let shellItem = NSMenuItem(title: "Toggle Brain Surface", action: #selector(toggleBrainSurface), keyEquivalent: "b")
        shellItem.keyEquivalentModifierMask = [.command, .shift]
        shellItem.target = self
        viewMenu.addItem(shellItem)

        let flowItem = NSMenuItem(title: "Toggle Signal Flow Animation", action: #selector(toggleSignalFlow), keyEquivalent: "a")
        flowItem.keyEquivalentModifierMask = [.command, .shift]
        flowItem.target = self
        viewMenu.addItem(flowItem)

        viewMenu.addItem(NSMenuItem.separator())

        // 3D Camera Controls
        let resetCamItem = NSMenuItem(title: "Reset 3D Camera / Overview", action: #selector(resetCamera), keyEquivalent: "0")
        resetCamItem.keyEquivalentModifierMask = [.command, .option]
        resetCamItem.target = self
        viewMenu.addItem(resetCamItem)

        let cameraSubMenuItem = NSMenuItem(title: "3D Camera Presets", action: nil, keyEquivalent: "")
        let cameraSubMenu = NSMenu(title: "3D Camera Presets")

        let camTop = NSMenuItem(title: "Top View", action: #selector(cameraTop), keyEquivalent: "1")
        camTop.keyEquivalentModifierMask = [.command, .option]
        camTop.target = self
        cameraSubMenu.addItem(camTop)

        let camLeft = NSMenuItem(title: "Left View", action: #selector(cameraLeft), keyEquivalent: "2")
        camLeft.keyEquivalentModifierMask = [.command, .option]
        camLeft.target = self
        cameraSubMenu.addItem(camLeft)

        let camBack = NSMenuItem(title: "Back View", action: #selector(cameraBack), keyEquivalent: "3")
        camBack.keyEquivalentModifierMask = [.command, .option]
        camBack.target = self
        cameraSubMenu.addItem(camBack)

        let camBelow = NSMenuItem(title: "Below View", action: #selector(cameraBelow), keyEquivalent: "4")
        camBelow.keyEquivalentModifierMask = [.command, .option]
        camBelow.target = self
        cameraSubMenu.addItem(camBelow)

        cameraSubMenuItem.submenu = cameraSubMenu
        viewMenu.addItem(cameraSubMenuItem)

        viewMenu.addItem(NSMenuItem.separator())

        let closePanelItem = NSMenuItem(title: "Close Details Panel", action: #selector(closePanelOrModal), keyEquivalent: "p")
        closePanelItem.keyEquivalentModifierMask = [.command, .option]
        closePanelItem.target = self
        viewMenu.addItem(closePanelItem)

        viewMenu.addItem(NSMenuItem.separator())

        let fsItem = NSMenuItem(title: "Toggle Full Screen", action: #selector(toggleFullScreen), keyEquivalent: "f")
        fsItem.keyEquivalentModifierMask = [.control, .command]
        fsItem.target = self
        viewMenu.addItem(fsItem)

        viewMenuItem.submenu = viewMenu
        mainMenu.addItem(viewMenuItem)

        // --------------------------------------------------
        // 5. Go Menu (Atlas Navigation & Views)
        // --------------------------------------------------
        let goMenuItem = NSMenuItem()
        let goMenu = NSMenu(title: "Go")

        let backItem = NSMenuItem(title: "Back", action: #selector(goBack), keyEquivalent: "[")
        backItem.keyEquivalentModifierMask = [.command]
        backItem.target = self
        goMenu.addItem(backItem)

        let fwdItem = NSMenuItem(title: "Forward", action: #selector(goForward), keyEquivalent: "]")
        fwdItem.keyEquivalentModifierMask = [.command]
        fwdItem.target = self
        goMenu.addItem(fwdItem)

        goMenu.addItem(NSMenuItem.separator())

        let viewsList: [(String, String, String)] = [
            ("3D Atlas", "atlas", "1"),
            ("Functional Map", "map", "2"),
            ("Microcircuit", "circuit", "3"),
            ("Cells & Molecules", "molecules", "4"),
            ("Across Scales", "scales", "5"),
            ("Evidence & Gaps", "gaps", "6"),
            ("Hypothesis Lab", "lab", "7"),
            ("Literature Library", "library", "8")
        ]

        for (title, viewId, key) in viewsList {
            let item = NSMenuItem(title: title, action: #selector(navigateToView(_:)), keyEquivalent: key)
            item.keyEquivalentModifierMask = [.command]
            item.representedObject = viewId
            item.target = self
            goMenu.addItem(item)
        }

        goMenuItem.submenu = goMenu
        mainMenu.addItem(goMenuItem)

        // --------------------------------------------------
        // 6. Window Menu
        // --------------------------------------------------
        let windowMenuItem = NSMenuItem()
        let windowMenu = NSMenu(title: "Window")
        let miniItem = NSMenuItem(title: "Minimize", action: #selector(NSWindow.performMiniaturize(_:)), keyEquivalent: "m")
        windowMenu.addItem(miniItem)
        let zoomWinItem = NSMenuItem(title: "Zoom", action: #selector(NSWindow.performZoom(_:)), keyEquivalent: "")
        windowMenu.addItem(zoomWinItem)
        windowMenu.addItem(NSMenuItem.separator())
        let frontItem = NSMenuItem(title: "Bring All to Front", action: #selector(NSApplication.arrangeInFront(_:)), keyEquivalent: "")
        windowMenu.addItem(frontItem)
        windowMenuItem.submenu = windowMenu
        mainMenu.addItem(windowMenuItem)

        // --------------------------------------------------
        // 7. Help Menu
        // --------------------------------------------------
        let helpMenuItem = NSMenuItem()
        let helpMenu = NSMenu(title: "Help")

        let aboutHelpItem = NSMenuItem(title: "Brain Circuit Atlas Documentation", action: #selector(openAbout), keyEquivalent: "")
        aboutHelpItem.target = self
        helpMenu.addItem(aboutHelpItem)

        let shortcutsItem = NSMenuItem(title: "Keyboard Shortcuts...", action: #selector(showShortcuts), keyEquivalent: "/")
        shortcutsItem.keyEquivalentModifierMask = [.command, .shift]
        shortcutsItem.target = self
        helpMenu.addItem(shortcutsItem)

        helpMenuItem.submenu = helpMenu
        mainMenu.addItem(helpMenuItem)

        NSApp.mainMenu = mainMenu
        NSApp.windowsMenu = windowMenu
        NSApp.helpMenu = helpMenu
    }

    // =========================================================================
    // Action Implementations
    // =========================================================================

    // MARK: - Zoom Actions
    @objc func zoomIn() {
        guard let wv = webView else { return }
        wv.pageZoom = min(3.0, wv.pageZoom + 0.15)
    }

    @objc func zoomOut() {
        guard let wv = webView else { return }
        wv.pageZoom = max(0.5, wv.pageZoom - 0.15)
    }

    @objc func actualSize() {
        webView?.pageZoom = 1.0
    }

    // MARK: - Navigation Actions
    @objc func goBack() {
        if webView?.canGoBack == true {
            webView?.goBack()
        } else {
            webView?.evaluateJavaScript("window.history.back()", completionHandler: nil)
        }
    }

    @objc func goForward() {
        if webView?.canGoForward == true {
            webView?.goForward()
        } else {
            webView?.evaluateJavaScript("window.history.forward()", completionHandler: nil)
        }
    }

    @objc func navigateToView(_ sender: NSMenuItem) {
        guard let viewId = sender.representedObject as? String else { return }
        webView?.evaluateJavaScript("window.location.hash = '#/\(viewId)'", completionHandler: nil)
    }

    // MARK: - Display & Appearance Actions
    @objc func toggleTheme() {
        webView?.evaluateJavaScript("if (window.CA?.setTheme) { window.CA.setTheme(window.CA.theme === 'light' ? 'dark' : 'light'); } else { document.getElementById('theme-btn')?.click(); }", completionHandler: nil)
    }

    @objc func toggleLabels() {
        webView?.evaluateJavaScript("if (window.CA?.setLabelMode) { window.CA.setLabelMode(window.CA.labelMode === 'model' ? 'legend' : 'model'); } else { document.querySelector('#labels-seg button:not(.on)')?.click(); }", completionHandler: nil)
    }

    @objc func toggleBrainSurface() {
        webView?.evaluateJavaScript("if (window.CA?.atlas3d?.toggleShell) { window.CA.atlas3d.toggleShell(); } else { const cb = Array.from(document.querySelectorAll('.atlas-controls label.check')).find(l => l.textContent.includes('Brain surface'))?.querySelector('input'); if (cb) cb.click(); }", completionHandler: nil)
    }

    @objc func toggleSignalFlow() {
        webView?.evaluateJavaScript("if (window.CA?.atlas3d?.toggleFlow) { window.CA.atlas3d.toggleFlow(); } else { const cb = Array.from(document.querySelectorAll('.atlas-controls label.check')).find(l => l.textContent.includes('Animate signal flow'))?.querySelector('input'); if (cb) cb.click(); }", completionHandler: nil)
    }

    @objc func resetCamera() {
        webView?.evaluateJavaScript("if (window.CA?.atlas3d?.flyTo) { window.CA.atlas3d.flyTo('overview'); } else { window.location.hash = '#/atlas'; }", completionHandler: nil)
    }

    @objc func cameraTop() {
        webView?.evaluateJavaScript("window.CA?.atlas3d?.flyTo?.('top')", completionHandler: nil)
    }

    @objc func cameraLeft() {
        webView?.evaluateJavaScript("window.CA?.atlas3d?.flyTo?.('left')", completionHandler: nil)
    }

    @objc func cameraBack() {
        webView?.evaluateJavaScript("window.CA?.atlas3d?.flyTo?.('back')", completionHandler: nil)
    }

    @objc func cameraBelow() {
        webView?.evaluateJavaScript("window.CA?.atlas3d?.flyTo?.('below')", completionHandler: nil)
    }

    // MARK: - Search & Panel Actions
    @objc func focusSearch() {
        webView?.evaluateJavaScript("const el = document.getElementById('search'); if (el) { el.focus(); el.select(); }", completionHandler: nil)
    }

    @objc func closePanelOrModal() {
        webView?.evaluateJavaScript("""
            const m = document.getElementById('modal');
            if (m && !m.classList.contains('hidden')) {
                m.click();
            } else if (window.CA?.closePanel) {
                window.CA.closePanel();
            }
        """, completionHandler: nil)
    }

    // MARK: - Window & System Actions
    @objc func reloadWebView() {
        webView?.reload()
    }

    @objc func forceReloadWebView() {
        webView?.reloadFromOrigin()
    }

    @objc func toggleFullScreen() {
        window?.toggleFullScreen(nil)
    }

    @objc func closeWindow() {
        window?.performClose(nil)
    }

    @objc func printPage() {
        webView?.evaluateJavaScript("window.print()", completionHandler: nil)
    }

    @objc func openAbout() {
        webView?.evaluateJavaScript("document.getElementById('about-btn')?.click()", completionHandler: nil)
    }

    @objc func openSettings() {
        webView?.evaluateJavaScript("""
            if (window.CA && window.CA.openCloudModal) {
                window.CA.openCloudModal();
            } else {
                document.getElementById('about-btn')?.click();
            }
        """, completionHandler: nil)
    }

    @objc func showShortcuts() {
        let alert = NSAlert()
        alert.messageText = "Brain Circuit Atlas Display & Navigation Shortcuts"
        alert.informativeText = """
        Display & Zoom:
        • Zoom In:  ⌘+  or  ⌘=
        • Zoom Out:  ⌘-
        • Actual Size (100%):  ⌘0
        • Toggle Full Screen:  ⌃⌘F
        • Toggle Dark/Light Mode:  ⇧⌘D
        • Toggle 3D Labels:  ⇧⌘L
        • Toggle Brain Surface:  ⇧⌘B
        • Toggle Signal Flow:  ⇧⌘A
        • Reset 3D Camera:  ⌥⌘0
        • 3D Camera Top / Left / Back / Below:  ⌥⌘1 / ⌥⌘2 / ⌥⌘3 / ⌥⌘4

        Views & Navigation:
        • 3D Atlas:  ⌘1
        • Functional Map:  ⌘2
        • Microcircuit:  ⌘3
        • Cells & Molecules:  ⌘4
        • Across Scales:  ⌘5
        • Evidence & Gaps:  ⌘6
        • Hypothesis Lab:  ⌘7
        • Literature Library:  ⌘8
        • History Back / Forward:  ⌘[  /  ⌘]

        Search & Windows:
        • Find in Atlas:  ⌘F  (or /)
        • Close Details Panel:  ⌥⌘P  (or Esc)
        • Reload Page:  ⌘R
        • Force Reload:  ⇧⌘R
        • Settings:  ⌘,
        • Minimize:  ⌘M
        • Close Window:  ⌘W
        • Quit:  ⌘Q
        """
        alert.alertStyle = .informational
        alert.addButton(withTitle: "OK")
        alert.runModal()
    }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
