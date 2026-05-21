import socket
import subprocess
import shlex
import tkinter as tk
from tkinter import messagebox, ttk


COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3306, 3389, 5000, 8080]


def basic_tcp_scan(ip, start_port=1, end_port=1024):
    open_ports = []

    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
        except socket.error:
            pass

    return open_ports


def common_ports_scan(ip):
    open_ports = []

    for port in COMMON_PORTS:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.5)
                if sock.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
        except socket.error:
            pass

    return open_ports


def run_command(command):
    try:
        args = shlex.split(command)

        if not args:
            return "No command entered."

        if args[0] != "nmap":
            return "For safety, only nmap commands are allowed."

        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=180
        )

        output = result.stdout

        if result.stderr:
            output += "\n\nErrors:\n" + result.stderr

        return output

    except FileNotFoundError:
        return "Nmap is not installed. Install it using: sudo apt install nmap -y"

    except subprocess.TimeoutExpired:
        return "Command timed out."

    except Exception as e:
        return f"Error: {e}"


class PortScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Port Scanner")
        self.root.geometry("560x530")
        self.root.resizable(False, False)

        tk.Label(
            root,
            text="Advanced Port Scanner",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(root, text="Target IP / Hostname:").pack(pady=5)
        self.ip_entry = tk.Entry(root, width=50)
        self.ip_entry.pack(pady=5)

        tk.Label(root, text="Starting Port (default: 1):").pack(pady=5)
        self.start_port_entry = tk.Entry(root, width=50)
        self.start_port_entry.pack(pady=5)

        tk.Label(root, text="Ending Port (default: 1024):").pack(pady=5)
        self.end_port_entry = tk.Entry(root, width=50)
        self.end_port_entry.pack(pady=5)

        tk.Label(root, text="Select Scan Type:").pack(pady=5)

        self.scan_type = ttk.Combobox(
            root,
            width=47,
            state="readonly",
            values=[
                "Basic TCP Scan",
                "Common Ports Scan",
                "Full TCP Scan",
                "Service Version Scan",
                "OS Detection Scan",
                "Aggressive Scan",
                "Fast Scan",
                "TCP SYN Scan",
                "UDP Scan",
                "Custom Nmap Command"
            ]
        )
        self.scan_type.current(0)
        self.scan_type.pack(pady=5)
        self.scan_type.bind("<<ComboboxSelected>>", self.toggle_custom_command)

        tk.Label(root, text="Custom Nmap Command:").pack(pady=5)
        self.custom_command_entry = tk.Entry(root, width=55)
        self.custom_command_entry.pack(pady=5)
        self.custom_command_entry.insert(0, "nmap -sV 127.0.0.1")
        self.custom_command_entry.config(state="disabled")

        tk.Button(
            root,
            text="Start Scan",
            width=25,
            command=self.start_scan
        ).pack(pady=15)

        tk.Label(
            root,
            text="Use only on your own system, lab, or authorized target.",
            fg="red"
        ).pack(pady=10)

    def toggle_custom_command(self, event=None):
        if self.scan_type.get() == "Custom Nmap Command":
            self.custom_command_entry.config(state="normal")
        else:
            self.custom_command_entry.config(state="disabled")

    def get_target(self):
        ip = self.ip_entry.get().strip()

        if not ip:
            messagebox.showerror("Invalid Input", "Please enter target IP or hostname.")
            return None

        return ip

    def get_ports(self):
        start_text = self.start_port_entry.get().strip()
        end_text = self.end_port_entry.get().strip()

        if not start_text and not end_text:
            return 1, 1024

        try:
            start_port = int(start_text) if start_text else 1
            end_port = int(end_text) if end_text else 1024

            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError

            return start_port, end_port

        except ValueError:
            messagebox.showerror(
                "Invalid Ports",
                "Enter valid ports between 1 and 65535."
            )
            return None

    def show_result_popup(self, title, result_text):
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("800x550")

        tk.Label(
            result_window,
            text=title,
            font=("Arial", 15, "bold")
        ).pack(pady=10)

        frame = tk.Frame(result_window)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        output = tk.Text(
            frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=output.yview)

        output.insert(tk.END, result_text)
        output.config(state="disabled")

        tk.Button(
            result_window,
            text="Close",
            command=result_window.destroy
        ).pack(pady=10)

    def start_scan(self):
        selected_scan = self.scan_type.get()

        if selected_scan == "Custom Nmap Command":
            command = self.custom_command_entry.get().strip()

            if not command:
                messagebox.showerror("Invalid Command", "Please enter an Nmap command.")
                return

            messagebox.showinfo("Scanning", "Custom Nmap command started. Please wait...")
            result = run_command(command)
            self.show_result_popup("Custom Nmap Command Result", result)
            return

        ip = self.get_target()

        if not ip:
            return

        messagebox.showinfo("Scanning", f"{selected_scan} started. Please wait...")

        if selected_scan == "Basic TCP Scan":
            ports = self.get_ports()
            if not ports:
                return

            start_port, end_port = ports
            open_ports = basic_tcp_scan(ip, start_port, end_port)

            result = f"Target: {ip}\nScan Type: Basic TCP Scan\nPorts: {start_port}-{end_port}\n\n"

            if open_ports:
                result += "Open Ports Found:\n\n"
                for port in open_ports:
                    result += f"Port {port} is OPEN\n"
            else:
                result += "No open ports found."

            self.show_result_popup("Basic TCP Scan Result", result)

        elif selected_scan == "Common Ports Scan":
            open_ports = common_ports_scan(ip)

            result = f"Target: {ip}\nScan Type: Common Ports Scan\n\n"

            if open_ports:
                result += "Open Common Ports Found:\n\n"
                for port in open_ports:
                    result += f"Port {port} is OPEN\n"
            else:
                result += "No common open ports found."

            self.show_result_popup("Common Ports Scan Result", result)

        elif selected_scan == "Full TCP Scan":
            open_ports = basic_tcp_scan(ip, 1, 65535)

            result = f"Target: {ip}\nScan Type: Full TCP Scan\nPorts: 1-65535\n\n"

            if open_ports:
                result += "Open Ports Found:\n\n"
                for port in open_ports:
                    result += f"Port {port} is OPEN\n"
            else:
                result += "No open ports found."

            self.show_result_popup("Full TCP Scan Result", result)

        else:
            nmap_commands = {
                "Service Version Scan": f"nmap -sV {ip}",
                "OS Detection Scan": f"nmap -O {ip}",
                "Aggressive Scan": f"nmap -A {ip}",
                "Fast Scan": f"nmap -F {ip}",
                "TCP SYN Scan": f"nmap -sS {ip}",
                "UDP Scan": f"nmap -sU {ip}",
            }

            command = nmap_commands.get(selected_scan)

            result = run_command(command)
            self.show_result_popup(f"{selected_scan} Result", result)


if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerApp(root)
    root.mainloop()
