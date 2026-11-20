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
                    "Python 3.8+ was not found on this system.\nPlease install Python from https://www.python.org/ or enable it in PATH.",
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
            SetupTrayIcon();

            // 5. Poll server readiness asynchronously, then launch browser window
            ThreadPool.QueueUserWorkItem((state) =>
            {
                bool ready = WaitForServerReady(30, 250); // wait up to 7.5 seconds
                if (ready)
                {
                    LaunchAppWindow();
                }
                else
                {
                    MessageBox.Show(
                        "The backend server did not respond in time.\nYou can try opening " + _appUrl + " manually.",
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
            // Check specific working environments
            string localAppData = Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData);
            string programFiles = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles);
            string programFilesX86 = Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86);

            string[] knownPaths = new string[]
            {
                Path.Combine(localAppData, @"Programs\DeepSeek Harness\resources\runtime\primary-runtime\dependencies\python\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python312\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python311\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python310\python.exe"),
                Path.Combine(localAppData, @"Programs\Python\Python39\python.exe"),
                Path.Combine(programFiles, @"Python312\python.exe"),
                Path.Combine(programFiles, @"Python311\python.exe"),
                Path.Combine(programFiles, @"Python310\python.exe"),
                Path.Combine(programFiles, @"Python39\python.exe"),
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

        public static void LaunchAppWindow()
        {
            // Prefer Microsoft Edge in app mode (installed on all modern Windows versions)
            string edgePath = FindEdgePath();
            if (!string.IsNullOrEmpty(edgePath))
            {
                try
                {
                    ProcessStartInfo psi = new ProcessStartInfo
                    {
                        FileName = edgePath,
                        Arguments = string.Format("--app=\"{0}\" --window-size=1400,900", _appUrl),
                        UseShellExecute = false
                    };
                    Process.Start(psi);
                    return;
                }
                catch {}
            }

            // Fallback: Google Chrome in app mode
            string chromePath = FindChromePath();
            if (!string.IsNullOrEmpty(chromePath))
            {
                try
                {
                    ProcessStartInfo psi = new ProcessStartInfo
                    {
                        FileName = chromePath,
                        Arguments = string.Format("--app=\"{0}\" --window-size=1400,900", _appUrl),
                        UseShellExecute = false
                    };
                    Process.Start(psi);
                    return;
                }
                catch {}
            }

            // Universal fallback: default browser
            try
            {
                Process.Start(new ProcessStartInfo(_appUrl) { UseShellExecute = true });
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

        private static void SetupTrayIcon()
        {
            ContextMenu menu = new ContextMenu();
            menu.MenuItems.Add("Open Brain Circuit Atlas", (s, e) => LaunchAppWindow());
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

            _trayIcon = new NotifyIcon
            {
                Icon = SystemIcons.Application,
                ContextMenu = menu,
                Text = "Brain Circuit Atlas v0.3",
                Visible = true
            };

            _trayIcon.DoubleClick += (s, e) => LaunchAppWindow();
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
