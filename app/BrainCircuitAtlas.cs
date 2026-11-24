// Brain Circuit Atlas - Windows Desktop Host (v0.3)
// Compiles with standard Microsoft csc.exe into a standalone native Windows executable.
// Runs the local Python backend server and opens the app in a sleek borderless window.

using System;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net;
using System.Threading;
using System.Windows.Forms;

namespace BrainCircuitAtlas
{
    static class Program
    {
        private static Process _pythonProcess;
        private static NotifyIcon _trayIcon;
        private static int _port = 8765;
        private static string _appUrl;

        [STAThread]
        static void Main(string[] args)
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            int customPort;
            if (args.Length > 0 && int.TryParse(args[0], out customPort))
            {
                _port = customPort;
            }

            _appUrl = string.Format("http://127.0.0.1:{0}/index.html", _port);

            // 1. Locate repository root & backend/server.py
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string scriptPath = FindServerScript(baseDir);

            if (string.IsNullOrEmpty(scriptPath))
            {
                MessageBox.Show(
                    "Could not locate backend/server.py.\nPlease run BrainCircuitAtlas.exe from the repository root or app folder.",
                    "Brain Circuit Atlas Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            string projectRoot = Path.GetFullPath(Path.Combine(Path.GetDirectoryName(scriptPath), ".."));

            // 2. Locate Python executable
            string pythonExe = FindPythonExecutable();
            if (string.IsNullOrEmpty(pythonExe))
            {
                MessageBox.Show(
                    "Python 3.8+ was not found on this system.\nPlease install Python from https://www.python.org/ or the Microsoft Store and ensure it is in PATH.",
                    "Brain Circuit Atlas - Python Required",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning
                );
                return;
            }

            // 3. Launch Python backend server in the background
            try
            {
                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = pythonExe,
                    Arguments = string.Format("\"{0}\" {1}", scriptPath, _port),
                    WorkingDirectory = projectRoot,
                    CreateNoWindow = true,
                    UseShellExecute = false,
                    WindowStyle = ProcessWindowStyle.Hidden
                };

                _pythonProcess = Process.Start(psi);
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Failed to start Python backend server:\n" + ex.Message,
                    "Brain Circuit Atlas Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            // Ensure clean shutdown on process exit
            AppDomain.CurrentDomain.ProcessExit += (s, e) => StopBackend();

            // 4. Setup System Tray Icon & Menu
            SetupTrayIcon(baseDir, projectRoot);

            // 5. Poll server readiness asynchronously, then launch browser window
            ThreadPool.QueueUserWorkItem((state) =>
            {
                bool ready = WaitForServerReady(35, 250); // wait up to ~9 seconds
                if (ready)
                {
                    LaunchAppWindow();
                }
                else
                {
                    MessageBox.Show(
                        "The backend server is starting up or taking longer than expected.\nYou can open " + _appUrl + " from the system tray menu.",
                        "Brain Circuit Atlas - Connecting...",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information
                    );
                }
            });

            Application.Run();
        }

        private static string FindServerScript(string baseDir)
        {
            string[] candidates = new string[]
            {
                Path.Combine(baseDir, "backend", "server.py"),
                Path.Combine(baseDir, "..", "backend", "server.py"),
                Path.Combine(baseDir, "..", "..", "backend", "server.py"),
                Path.Combine(Environment.CurrentDirectory, "backend", "server.py")
            };

            foreach (string p in candidates)
            {
                if (File.Exists(p))
                {
                    return Path.GetFullPath(p);
                }
            }

            return null;
        }

        private static string FindPythonExecutable()
        {
            string localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            string programFiles = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);
            string programFilesX86 = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);

            string[] knownPaths = new string[]
            {
                Path.Combine(localAppData, @"Programs\Python\Python313\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python312\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python311\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python310\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python39\python.exe"),
                Path.Combine(programFiles, @"Python313\python.exe"),
                Path.Combine(programFiles, @"Python312\python.exe"),
                Path.Combine(programFiles, @"Python311\python.exe"),
                Path.Combine(programFiles, @"Python310\python.exe"),
                Path.Combine(programFiles, @"Python39\python.exe"),
                Path.Combine(programFilesX86, @"Python312\python.exe"),
                Path.Combine(programFilesX86, @"Python311\python.exe"),
                Path.Combine(localAppData, @"Microsoft\WindowsApps\python.exe"),
                Path.Combine(localAppData, @"Microsoft\WindowsApps\python3.exe"),
                "python.exe",
                "py.exe"
            };

            foreach (string path in knownPaths)
            {
                if (path.Contains("\\") && File.Exists(path))
                {
                    return path;
                }
            }

            // Test if python is in PATH
            try
            {
                Process p = new Process();
                p.StartInfo.FileName = "python.exe";
                p.StartInfo.Arguments = "--version";
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.UseShellExecute = false;
                if (p.Start())
                {
                    p.WaitForExit(1000);
                    if (p.ExitCode == 0) return "python.exe";
                }
            }
            catch {}

            try
            {
                Process p = new Process();
                p.StartInfo.FileName = "py.exe";
                p.StartInfo.Arguments = "-3 --version";
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.UseShellExecute = false;
                if (p.Start())
                {
                    p.WaitForExit(1000);
                    if (p.ExitCode == 0) return "py.exe";
                }
            }
            catch {}

            return null;
        }

        private static bool WaitForServerReady(int maxAttempts, int intervalMs)
        {
            string statusUrl = string.Format("http://127.0.0.1:{0}/api/status", _port);
            for (int i = 0; i < maxAttempts; i++)
            {
                try
                {
                    HttpWebRequest request = (HttpWebRequest)WebRequest.Create(statusUrl);
                    request.Timeout = 800;
                    request.Method = "GET";
                    using (HttpWebResponse response = (HttpWebResponse)request.GetResponse())
                    {
                        if (response.StatusCode == HttpStatusCode.OK)
                        {
                            return true;
                        }
                    }
                }
                catch
                {
                    // Server not ready yet
                }

                Thread.Sleep(intervalMs);
            }

            return false;
        }

        public static void LaunchAppWindow(string hash = "")
        {
            string targetUrl = string.IsNullOrEmpty(hash) ? _appUrl : (_appUrl + hash);

            // 1. Prefer Microsoft Edge in app mode (installed on all Windows 10 & 11)
            string edgePath = FindEdgePath();
            if (!string.IsNullOrEmpty(edgePath))
            {
                try
                {
                    ProcessStartInfo psi = new ProcessStartInfo
                    {
                        FileName = edgePath,
                        Arguments = string.Format("--app=\"{0}\" --window-size=1400,900", targetUrl),
                        UseShellExecute = false
                    };
                    Process.Start(psi);
                    return;
                }
                catch {}
            }

            // 2. Fallback: Google Chrome in app mode
            string chromePath = FindChromePath();
            if (!string.IsNullOrEmpty(chromePath))
            {
                try
                {
                    ProcessStartInfo psi = new ProcessStartInfo
                    {
                        FileName = chromePath,
                        Arguments = string.Format("--app=\"{0}\" --window-size=1400,900", targetUrl),
                        UseShellExecute = false
                    };
                    Process.Start(psi);
                    return;
                }
                catch {}
            }

            // 3. Universal fallback: default browser
            try
            {
                Process.Start(new ProcessStartInfo(targetUrl) { UseShellExecute = true });
            }
            catch (Exception ex)
            {
                MessageBox.Show("Could not open browser: " + ex.Message);
            }
        }

        private static string FindEdgePath()
        {
            string[] candidates = new string[]
            {
                @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Microsoft\Edge\Application\msedge.exe")
            };

            foreach (string p in candidates)
            {
                if (File.Exists(p)) return p;
            }

            return null;
        }

        private static string FindChromePath()
        {
            string[] candidates = new string[]
            {
                @"C:\Program Files\Google\Chrome\Application\chrome.exe",
                @"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), @"Google\Chrome\Application\chrome.exe")
            };

            foreach (string p in candidates)
            {
                if (File.Exists(p)) return p;
            }

            return null;
        }

        private static void SetupTrayIcon(string baseDir, string projectRoot)
        {
            ContextMenu menu = new ContextMenu();
            menu.MenuItems.Add("Open Brain Circuit Atlas", (s, e) => LaunchAppWindow());

            // Views submenu
            MenuItem viewsMenu = new MenuItem("Go to View");
            viewsMenu.MenuItems.Add("3D Atlas (Ctrl+1)", (s, e) => LaunchAppWindow("#/atlas"));
            viewsMenu.MenuItems.Add("Functional Map (Ctrl+2)", (s, e) => LaunchAppWindow("#/map"));
            viewsMenu.MenuItems.Add("Microcircuit (Ctrl+3)", (s, e) => LaunchAppWindow("#/circuit"));
            viewsMenu.MenuItems.Add("Cells & Molecules (Ctrl+4)", (s, e) => LaunchAppWindow("#/molecules"));
            viewsMenu.MenuItems.Add("Across Scales (Ctrl+5)", (s, e) => LaunchAppWindow("#/scales"));
            viewsMenu.MenuItems.Add("Evidence & Gaps (Ctrl+6)", (s, e) => LaunchAppWindow("#/gaps"));
            viewsMenu.MenuItems.Add("Hypothesis Lab (Ctrl+7)", (s, e) => LaunchAppWindow("#/lab"));
            viewsMenu.MenuItems.Add("Literature Library (Ctrl+8)", (s, e) => LaunchAppWindow("#/library"));
            menu.MenuItems.Add(viewsMenu);

            menu.MenuItems.Add("-");
            menu.MenuItems.Add("Keyboard Shortcuts...", (s, e) => ShowShortcutsDialog());
            menu.MenuItems.Add("Open in Default Browser", (s, e) => Process.Start(new ProcessStartInfo(_appUrl) { UseShellExecute = true }));
            menu.MenuItems.Add("-");
            menu.MenuItems.Add("Exit", (s, e) =>
            {
                StopBackend();
                if (_trayIcon != null)
                {
                    _trayIcon.Visible = false;
                    _trayIcon.Dispose();
                }
                Application.Exit();
            });

            Icon appIcon = SystemIcons.Application;
            string[] iconPaths = new string[]
            {
                Path.Combine(baseDir, "app", "AppIcon.ico"),
                Path.Combine(baseDir, "AppIcon.ico"),
                Path.Combine(projectRoot, "app", "AppIcon.ico")
            };

            foreach (string ip in iconPaths)
            {
                if (File.Exists(ip))
                {
                    try { appIcon = new Icon(ip); break; } catch {}
                }
            }

            _trayIcon = new NotifyIcon
            {
                Icon = appIcon,
                ContextMenu = menu,
                Text = "Brain Circuit Atlas v0.3",
                Visible = true
            };

            _trayIcon.DoubleClick += (s, e) => LaunchAppWindow();
        }

        private static void ShowShortcutsDialog()
        {
            MessageBox.Show(
                "Brain Circuit Atlas - Windows Display & Navigation Shortcuts\n\n" +
                "Display & Zoom Controls:\n" +
                "• Zoom In:  Ctrl + +  or  Ctrl + =\n" +
                "• Zoom Out:  Ctrl + -\n" +
                "• Actual Size (100%):  Ctrl + 0\n" +
                "• Full Screen:  F11  or  Ctrl + Shift + F\n" +
                "• Toggle Dark / Light Mode:  Ctrl + Shift + D\n" +
                "• Toggle 3D Labels:  Ctrl + Shift + L\n" +
                "• Toggle Brain Surface (3D):  Ctrl + Shift + B\n" +
                "• Toggle Signal Flow (3D):  Ctrl + Shift + A\n" +
                "• Reset 3D Camera / Overview:  Ctrl + Alt + 0\n\n" +
                "Atlas Views & Navigation:\n" +
                "• 3D Atlas:  Ctrl + 1\n" +
                "• Functional Map:  Ctrl + 2\n" +
                "• Microcircuit:  Ctrl + 3\n" +
                "• Cells & Molecules:  Ctrl + 4\n" +
                "• Across Scales:  Ctrl + 5\n" +
                "• Evidence & Gaps:  Ctrl + 6\n" +
                "• Hypothesis Lab:  Ctrl + 7\n" +
                "• Literature Library:  Ctrl + 8\n" +
                "• History Back / Forward:  Alt + Left / Alt + Right\n\n" +
                "Search & Windows:\n" +
                "• Find in Atlas:  Ctrl + F  or  /\n" +
                "• Minimize Window:  Win + Down\n" +
                "• Close Window:  Ctrl + W  or  Alt + F4\n" +
                "• Close Details Panel / Esc:  Esc\n" +
                "• Reload Page:  Ctrl + R  or  F5\n" +
                "• Force Reload:  Ctrl + Shift + R  or  Ctrl + F5",
                "Brain Circuit Atlas - Keyboard Shortcuts",
                MessageBoxButtons.OK,
                MessageBoxIcon.Information
            );
        }

        private static void StopBackend()
        {
            try
            {
                if (_pythonProcess != null && !_pythonProcess.HasExited)
                {
                    _pythonProcess.Kill();
                    _pythonProcess.Dispose();
                    _pythonProcess = null;
                }
            }
            catch {}
        }
    }
}
