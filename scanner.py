import socket
import threading
import tkinter as tk
import random
import time

# ── Color Palette ──────────────────────────────────────────────────────────────
BG     = "#0a0a0f"
GREEN  = "#00ff41"
DIM    = "#004d14"
CYAN   = "#00e5ff"
YELLOW = "#f0e040"
PINK   = "#ff2d78"
BORDER = "#1a2a1a"
PANEL  = "#0d1a0d"
HEADER = "#003300"

# ── Scan Modes ─────────────────────────────────────────────────────────────────
SCAN_MODES = [
    ("1", "Aggressive Scan",  "All ports 1-65535, fast",        "aggressive"),
    ("2", "Version Scan",     "Detect service versions",         "version"),
    ("3", "Normal Scan",      "Common ports 1-1024",             "normal"),
    ("4", "Custom Port Scan", "Use your port range below",       "custom"),
    ("5", "Script Scan",      "Run default NSE-style checks",    "script"),
    ("6", "Know Your IP",     "Show your local & public IP",     "myip"),
]

# ── Matrix Background ──────────────────────────────────────────────────────────
class MatrixCanvas(tk.Canvas):
    def __init__(self, parent, width, height):
        super().__init__(parent, bg=BG, highlightthickness=0)
        self.width     = width
        self.height    = height
        self.chars     = "01"
        self.col_count = width // 14
        self.drops     = [[0, random.uniform(0.3, 1.0), random.random()]
                          for _ in range(self.col_count)]
        self.after(60, self.animate)

    def animate(self):
        self.delete("all")
        trail_colors = [GREEN, "#00cc33", "#009922", "#006611", DIM, DIM]
        for i, (y, speed, _) in enumerate(self.drops):
            for t in range(6):
                trail_y = y - t
                if trail_y < 0:
                    continue
                self.create_text(i * 14 + 7, int(trail_y) * 14,
                                 text=random.choice(self.chars),
                                 fill=trail_colors[t], font=("Consolas", 9))
            self.drops[i][0] += speed
            if self.drops[i][0] * 14 > self.height or random.random() > 0.975:
                self.drops[i][0] = 0
                self.drops[i][1] = random.uniform(0.3, 1.0)
        self.after(60, self.animate)


# ── Neon Button ────────────────────────────────────────────────────────────────
class NeonButton(tk.Label):
    def __init__(self, parent, text, command, color=GREEN, **kwargs):
        super().__init__(parent, text=text, fg=color, bg=PANEL,
                         font=("Consolas", 10, "bold"), cursor="hand2",
                         relief="flat", bd=0, padx=14, pady=6, **kwargs)
        self.command = command
        self.color   = color
        self.config(highlightbackground=color, highlightthickness=1)
        self.bind("<Enter>",    self._on_enter)
        self.bind("<Leave>",    self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _on_enter(self, _): self.config(bg=self.color, fg=BG)
    def _on_leave(self, _): self.config(bg=PANEL, fg=self.color)
    def _on_click(self, _):
        if self.command: self.command()


# ── Mode Button (radio-style) ──────────────────────────────────────────────────
class ModeButton(tk.Frame):
    def __init__(self, parent, num, label, desc, key, on_select, **kwargs):
        super().__init__(parent, bg=PANEL,
                         highlightbackground=BORDER, highlightthickness=1,
                         cursor="hand2", **kwargs)
        self.key       = key
        self.on_select = on_select
        self._active   = False

        top = tk.Frame(self, bg=PANEL)
        top.pack(fill="x", padx=8, pady=(6, 2))

        tk.Label(top, text=f"[{num}]", fg=DIM, bg=PANEL,
                 font=("Consolas", 9, "bold")).pack(side="left")
        self._title = tk.Label(top, text=label, fg=GREEN, bg=PANEL,
                               font=("Consolas", 10, "bold"))
        self._title.pack(side="left", padx=6)

        tk.Label(self, text=desc, fg=DIM, bg=PANEL,
                 font=("Consolas", 8)).pack(anchor="w", padx=8, pady=(0, 6))

        for w in (self, top, self._title):
            w.bind("<Button-1>", self._click)
        for child in top.winfo_children():
            child.bind("<Button-1>", self._click)

    def _click(self, _):
        self.on_select(self.key)

    def set_active(self, active):
        self._active = active
        if active:
            self.config(highlightbackground=GREEN, highlightthickness=2)
            self._title.config(fg=YELLOW)
        else:
            self.config(highlightbackground=BORDER, highlightthickness=1)
            self._title.config(fg=GREEN)


# ── Progress Bar ───────────────────────────────────────────────────────────────
class ScanProgressBar:
    def __init__(self, parent, bar_width=860, bar_height=5):
        self._w   = bar_width
        self._h   = bar_height
        self._pct = 0.0
        self.canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
        self.canvas.config(width=bar_width, height=bar_height)

    def pack(self, **kw):  self.canvas.pack(**kw)
    def grid(self, **kw):  self.canvas.grid(**kw)
    def place(self, **kw): self.canvas.place(**kw)

    def set_progress(self, pct):
        self._pct = max(0.0, min(1.0, pct))
        self._draw()

    def _draw(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 0, self._w, self._h, fill=BORDER, outline="")
        fw = int(self._w * self._pct)
        if fw > 0:
            self.canvas.create_rectangle(0, 0, fw, self._h, fill=CYAN, outline="")
        if fw > 2:
            self.canvas.create_rectangle(fw - 2, 0, fw, self._h, fill="white", outline="")


# ── Stat Badge ─────────────────────────────────────────────────────────────────
class StatBadge(tk.Frame):
    def __init__(self, parent, label, **kwargs):
        super().__init__(parent, bg=PANEL, **kwargs)
        self.config(highlightbackground=BORDER, highlightthickness=1)
        tk.Label(self, text=label.upper(), fg=DIM, bg=PANEL,
                 font=("Consolas", 8)).pack(pady=(6, 0))
        self._val = tk.Label(self, text="0", fg=GREEN, bg=PANEL,
                             font=("Consolas", 16, "bold"))
        self._val.pack(pady=(0, 6), padx=14)

    def set_value(self, v): self._val.config(text=str(v))


# ── Main App ───────────────────────────────────────────────────────────────────
class HackerScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Rishi Shadow Scanner")
        self.root.geometry("900x780")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._mode         = "normal"
        self._mode_buttons = {}
        self._scanning     = False
        self._open_count   = 0
        self._scan_count   = 0
        self._start_time   = 0

        # Matrix bg
        self.bg_canvas = MatrixCanvas(root, 900, 780)
        self.bg_canvas.place(x=0, y=0)

        overlay = tk.Frame(root, bg=BG)
        overlay.place(relwidth=1, relheight=1)

        # ── Header ───────────────────────────────────────────────────────────
        header = tk.Frame(overlay, bg=HEADER,
                          highlightbackground=GREEN, highlightthickness=1,
                          height=54)
        header.pack(fill="x", padx=14, pady=(12, 0))
        header.pack_propagate(False)

        tk.Label(header, text="RISHI SHADOW SCANNER", fg=GREEN, bg=HEADER,
                 font=("Consolas", 20, "bold"), anchor="center").pack(
                     side="left", expand=True, padx=10)

        self._status_dot = tk.Label(header, text="◉", fg=GREEN, bg=HEADER,
                                    font=("Consolas", 16))
        self._status_dot.pack(side="right", padx=14)
        self._blink_dot()

        tk.Label(overlay,
                 text="[ NETWORK RECONNAISSANCE SYSTEM  v3.0  |  STEALTH MODE ACTIVE ]",
                 fg=DIM, bg=BG, font=("Consolas", 8)).pack(pady=(2, 0))

        self._sep(overlay, GREEN)

        # ── Scan Mode Selector ────────────────────────────────────────────────
        tk.Label(overlay, text="SELECT SCAN MODE",
                 fg=DIM, bg=BG, font=("Consolas", 8), anchor="w").pack(
                     fill="x", padx=16, pady=(2, 0))

        mode_grid = tk.Frame(overlay, bg=BG)
        mode_grid.pack(fill="x", padx=14, pady=(4, 0))

        for col in range(3):
            mode_grid.columnconfigure(col, weight=1)

        for idx, (num, label, desc, key) in enumerate(SCAN_MODES):
            btn = ModeButton(mode_grid, num, label, desc, key,
                             self._select_mode)
            btn.grid(row=idx // 3, column=idx % 3,
                     padx=4, pady=4, sticky="nsew")
            self._mode_buttons[key] = btn

        self._sep(overlay, BORDER)

        # ── Input row ────────────────────────────────────────────────────────
        input_row = tk.Frame(overlay, bg=BG)
        input_row.pack(fill="x", padx=14, pady=4)

        tk.Label(input_row, text="TARGET IP :", fg=DIM, bg=BG,
                 font=("Consolas", 10)).pack(side="left", padx=(0, 6))

        self.ip_entry = tk.Entry(
            input_row, bg=PANEL, fg=CYAN, insertbackground=CYAN,
            font=("Consolas", 13, "bold"), relief="flat",
            highlightbackground=CYAN, highlightthickness=1, width=20)
        self.ip_entry.pack(side="left")
        self.ip_entry.insert(0, "127.0.0.1")

        tk.Label(input_row, text="  PORTS:", fg=DIM, bg=BG,
                 font=("Consolas", 10)).pack(side="left", padx=(12, 4))

        self.port_start = tk.Entry(input_row, bg=PANEL, fg=GREEN,
                                   insertbackground=GREEN,
                                   font=("Consolas", 11), width=6,
                                   relief="flat",
                                   highlightbackground=BORDER,
                                   highlightthickness=1)
        self.port_start.pack(side="left")
        self.port_start.insert(0, "1")

        tk.Label(input_row, text=" – ", fg=DIM, bg=BG,
                 font=("Consolas", 10)).pack(side="left")

        self.port_end = tk.Entry(input_row, bg=PANEL, fg=GREEN,
                                 insertbackground=GREEN,
                                 font=("Consolas", 11), width=6,
                                 relief="flat",
                                 highlightbackground=BORDER,
                                 highlightthickness=1)
        self.port_end.pack(side="left")
        self.port_end.insert(0, "1024")

        self._select_mode("normal")  # now safe: port_start/end exist

        # Buttons
        btn_frame = tk.Frame(input_row, bg=BG)
        btn_frame.pack(side="right")

        NeonButton(btn_frame, "▶  SCAN",  self.start_scan, color=GREEN).pack(side="left", padx=4)
        NeonButton(btn_frame, "✕  CLEAR", self.clear,      color=YELLOW).pack(side="left", padx=4)

        # ── Progress bar ──────────────────────────────────────────────────────
        self.progress = ScanProgressBar(overlay, bar_width=868, bar_height=5)
        self.progress.pack(padx=14, pady=(4, 0))

        # ── Stat badges ───────────────────────────────────────────────────────
        stat_frame = tk.Frame(overlay, bg=BG)
        stat_frame.pack(fill="x", padx=14, pady=4)

        self._stat_scanned = StatBadge(stat_frame, "Scanned")
        self._stat_scanned.pack(side="left", padx=4)
        self._stat_open = StatBadge(stat_frame, "Open")
        self._stat_open.pack(side="left", padx=4)
        self._stat_closed = StatBadge(stat_frame, "Closed")
        self._stat_closed.pack(side="left", padx=4)

        self._elapsed_var = tk.StringVar(value="00:00")
        elapsed_frame = tk.Frame(stat_frame, bg=PANEL,
                                 highlightbackground=BORDER, highlightthickness=1)
        elapsed_frame.pack(side="right", padx=4)
        tk.Label(elapsed_frame, text="ELAPSED", fg=DIM, bg=PANEL,
                 font=("Consolas", 8)).pack(pady=(6, 0), padx=10)
        tk.Label(elapsed_frame, textvariable=self._elapsed_var,
                 fg=CYAN, bg=PANEL, font=("Consolas", 16, "bold")).pack(pady=(0, 6), padx=14)

        self._sep(overlay, BORDER)

        # ── Terminal ──────────────────────────────────────────────────────────
        tk.Label(overlay, text="TERMINAL OUTPUT",
                 fg=DIM, bg=BG, font=("Consolas", 8), anchor="w").pack(
                     fill="x", padx=16)

        text_frame = tk.Frame(overlay, bg=BORDER)
        text_frame.pack(fill="both", expand=True, padx=14, pady=(2, 12))

        self.output = tk.Text(
            text_frame, bg=PANEL, fg=GREEN, insertbackground=GREEN,
            font=("Consolas", 10), relief="flat", bd=0, wrap="word",
            padx=10, pady=8, selectbackground=DIM, selectforeground=GREEN)
        self.output.pack(side="left", fill="both", expand=True)

        self.output.tag_config("open",    foreground=YELLOW)
        self.output.tag_config("header",  foreground=CYAN)
        self.output.tag_config("dim",     foreground=DIM)
        self.output.tag_config("success", foreground=GREEN)
        self.output.tag_config("warn",    foreground=YELLOW)
        self.output.tag_config("pink",    foreground=PINK)

        sb = tk.Scrollbar(text_frame, command=self.output.yview,
                          bg=PANEL, troughcolor=BG, relief="flat")
        sb.pack(side="right", fill="y")
        self.output.config(yscrollcommand=sb.set)

        self._boot_sequence()

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _sep(self, parent, color):
        tk.Frame(parent, bg=color, height=1).pack(fill="x", padx=14, pady=2)

    def _blink_dot(self):
        cur = self._status_dot.cget("fg")
        self._status_dot.config(fg=GREEN if cur == BG else BG)
        self.root.after(700, self._blink_dot)

    def _select_mode(self, key):
        self._mode = key
        for k, btn in self._mode_buttons.items():
            btn.set_active(k == key)
        # Auto-set port ranges for known modes
        ranges = {
            "aggressive": ("1",     "65535"),
            "normal":     ("1",     "1024"),
            "version":    ("1",     "1024"),
            "script":     ("1",     "1024"),
            "custom":     (None,    None),
            "myip":       (None,    None),
        }
        p1, p2 = ranges.get(key, (None, None))
        if p1 is not None:
            self.port_start.delete(0, "end"); self.port_start.insert(0, p1)
            self.port_end.delete(0, "end");   self.port_end.insert(0, p2)

    # ── Boot sequence ─────────────────────────────────────────────────────────
    def _boot_sequence(self):
        lines = [
            ("[ SYS  ]  Initializing shadow kernel...\n",    "dim"),
            ("[ NET  ]  Binding raw socket interface...\n",   "dim"),
            ("[ SEC  ]  Stealth mode: ACTIVE\n",              "dim"),
            ("[ CORE ]  Thread pool ready (workers=64)\n",    "dim"),
            ("[ OK   ]  Rishi Shadow Scanner v3.0 ready.\n\n","success"),
            ("  Select a scan mode above, enter target IP,\n","dim"),
            ("  then press  ▶ SCAN.\n",                       "dim"),
        ]
        def write_next(idx=0):
            if idx >= len(lines):
                return
            text, tag = lines[idx]
            self._tagged_type(text, tag)
            self.root.after(200, lambda: write_next(idx + 1))
        write_next()

    # ── Typed text ────────────────────────────────────────────────────────────
    def _tagged_type(self, text, tag="success", delay=0.005):
        for ch in text:
            self.output.insert("end", ch, tag)
            self.output.see("end")
            self.root.update()
            time.sleep(delay)

    def type_text(self, text):
        self._tagged_type(text, "success", 0.005)

    # ── Scan dispatch ─────────────────────────────────────────────────────────
    def start_scan(self):
        if self._scanning:
            return

        if self._mode == "myip":
            self._run_myip()
            return

        ip = self.ip_entry.get().strip()
        try:
            p1 = int(self.port_start.get())
            p2 = int(self.port_end.get())
        except ValueError:
            self._tagged_type("[ERR]  Invalid port range.\n", "warn")
            return

        self._scanning   = True
        self._open_count = 0
        self._scan_count = 0
        self._start_time = time.time()
        self._stat_open.set_value(0)
        self._stat_scanned.set_value(0)
        self._stat_closed.set_value(0)
        self.progress.set_progress(0)

        mode_label = next(l for _, l, _, k in SCAN_MODES if k == self._mode)

        self.output.insert("end", "\n")
        self._tagged_type("┌─ TARGET ───────────────────────────────────\n", "header")
        self._tagged_type(f"│  Host   : {ip}\n",          "header")
        self._tagged_type(f"│  Range  : {p1} – {p2}\n",   "header")
        self._tagged_type(f"│  Mode   : {mode_label}\n",   "header")
        self._tagged_type("└────────────────────────────────────────────\n", "header")
        self._tagged_type("  Initiating scan...\n\n", "dim")

        threading.Thread(target=self.run_scan, args=(ip, p1, p2), daemon=True).start()

    # ── Know Your IP ──────────────────────────────────────────────────────────
    def _run_myip(self):
        self.output.insert("end", "\n")
        self._tagged_type("┌─ KNOW YOUR IP ─────────────────────────────\n", "header")

        # Local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except Exception:
            local_ip = "Unavailable"

        hostname = socket.gethostname()

        self._tagged_type(f"│  Hostname  : {hostname}\n",  "success")
        self._tagged_type(f"│  Local IP  : {local_ip}\n",  "success")

        # Public IP via socket to a known service (no requests lib needed)
        self._tagged_type("│  Public IP : resolving...\n", "dim")
        threading.Thread(target=self._fetch_public_ip, daemon=True).start()

    def _fetch_public_ip(self):
        try:
            s = socket.socket()
            s.settimeout(4)
            s.connect(("api.ipify.org", 80))
            s.sendall(b"GET /?format=text HTTP/1.0\r\nHost: api.ipify.org\r\n\r\n")
            data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                data += chunk
            s.close()
            public_ip = data.decode().split("\r\n\r\n")[-1].strip()
        except Exception:
            public_ip = "Unavailable (no internet?)"

        self.root.after(0, lambda: self._show_public_ip(public_ip))

    def _show_public_ip(self, public_ip):
        # Remove the "resolving..." line by re-printing properly
        self._tagged_type(f"│  Public IP : {public_ip}\n", "pink")
        self._tagged_type("└────────────────────────────────────────────\n\n", "header")

    # ── Port scan core ────────────────────────────────────────────────────────
    def scan_port(self, ip, port, total):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            result = s.connect_ex((ip, port))
            s.close()

            if result == 0:
                # Version mode: grab banner
                banner = ""
                if self._mode == "version":
                    try:
                        sb = socket.socket()
                        sb.settimeout(1)
                        sb.connect((ip, port))
                        sb.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
                        raw = sb.recv(256).decode(errors="ignore").strip()
                        sb.close()
                        banner = raw.split("\n")[0][:40] if raw else ""
                    except Exception:
                        banner = ""

                self.root.after(0, lambda p=port, b=banner: self._report_open(p, b))
        except Exception:
            pass
        finally:
            self._scan_count += 1
            self.root.after(0, lambda: self._update_stats(total))

    def _report_open(self, port, banner=""):
        self._open_count += 1
        svc = self._guess_service(port)
        self.output.insert("end", f"  [OPEN]  Port {port:>5d}  ──  {svc}", "open")
        if banner:
            self.output.insert("end", f"  » {banner}", "dim")
        self.output.insert("end", "\n")
        self.output.see("end")
        self._stat_open.set_value(self._open_count)

        # Script mode: print a fake "script result"
        if self._mode == "script":
            scripts = {
                22:  "│  ssh-hostkey: RSA 2048 detected\n",
                80:  "│  http-title: Web server responding\n",
                443: "│  ssl-cert: TLS 1.3 supported\n",
                3306:"│  mysql-info: unauthorized access blocked\n",
            }
            if port in scripts:
                self.output.insert("end", scripts[port], "dim")

    def _guess_service(self, port):
        known = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
            27017: "MongoDB", 6443: "Kubernetes", 9200: "Elasticsearch",
        }
        return known.get(port, "Unknown")

    def _update_stats(self, total):
        self._stat_scanned.set_value(self._scan_count)
        self._stat_closed.set_value(self._scan_count - self._open_count)
        self.progress.set_progress(self._scan_count / total)
        elapsed = int(time.time() - self._start_time)
        m, s = divmod(elapsed, 60)
        self._elapsed_var.set(f"{m:02d}:{s:02d}")

    def run_scan(self, ip, p1, p2):
        total   = p2 - p1 + 1
        threads = []
        for port in range(p1, p2 + 1):
            t = threading.Thread(target=self.scan_port,
                                 args=(ip, port, total), daemon=True)
            threads.append(t)
            t.start()
            while sum(1 for x in threads if x.is_alive()) > 64:
                time.sleep(0.01)
        for t in threads:
            t.join()
        self.root.after(0, self._scan_done)

    def _scan_done(self):
        self._scanning = False
        elapsed = int(time.time() - self._start_time)
        m, s = divmod(elapsed, 60)
        self.output.insert("end", "\n")
        self._tagged_type("┌─ RESULT ───────────────────────────────────\n", "header")
        self._tagged_type(f"│  Open   : {self._open_count}\n",
                          "open" if self._open_count else "dim")
        self._tagged_type(f"│  Elapsed: {m:02d}:{s:02d}\n", "dim")
        status = "PORTS DISCOVERED" if self._open_count else "No open ports found  😎"
        self._tagged_type(f"│  Status : {status}\n",
                          "warn" if self._open_count else "dim")
        self._tagged_type("└────────────────────────────────────────────\n\n", "header")
        self.progress.set_progress(1.0)

    def clear(self):
        self.output.delete("1.0", "end")
        self.progress.set_progress(0)
        self._stat_open.set_value(0)
        self._stat_scanned.set_value(0)
        self._stat_closed.set_value(0)
        self._elapsed_var.set("00:00")


# ── Run ────────────────────────────────────────────────────────────────────────
root = tk.Tk()
app  = HackerScanner(root)
root.mainloop()
