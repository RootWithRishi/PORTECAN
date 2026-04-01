import socket
import threading
import os
import time
import sys
import urllib.request

# Colors
GREEN = "\033[92m"
RESET = "\033[0m"

# Clear Screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Banner
def banner():
    clear()
    print(GREEN)
    print(r"""
██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
██████╔╝██║   ██║██████╔╝   ██║   █████╗  ██║     ███████║██╔██╗ ██║
██╔═══╝ ██║   ██║██╔══██╗   ██║   ██╔══╝  ██║     ██╔══██║██║╚██╗██║
██║     ╚██████╔╝██║  ██║   ██║   ███████╗╚██████╗██║  ██║██║ ╚████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
    """)
    print("        RISHI SHADOW PORT SCANNER\n")
    print(RESET)

# Port Scan
def scan_port(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        s.connect((ip, port))
        print(GREEN + f"[OPEN] Port {port}" + RESET)
        s.close()
    except:
        pass

# Version Scan
def version_scan(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode(errors="ignore").strip()
        print(GREEN + f"[OPEN] Port {port} | {banner}" + RESET)
        s.close()
    except:
        pass

# Threading
def run_scan(ip, ports, mode):
    threads = []

    for port in ports:
        if mode == "version":
            t = threading.Thread(target=version_scan, args=(ip, port))
        else:
            t = threading.Thread(target=scan_port, args=(ip, port))

        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Get IP Info
def get_my_ip():
    try:
        # Public IP
        public_ip = urllib.request.urlopen("https://api.ipify.org").read().decode()

        # Local IP
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        print(GREEN + "\n[+] Your IP Information\n" + RESET)
        print(GREEN + f"Public IP : {public_ip}")
        print(f"Local IP  : {local_ip}\n" + RESET)

    except:
        print(GREEN + "[-] Unable to fetch IP!" + RESET)

# Ctrl+C Exit
def exit_gracefully():
    print("\n" + GREEN + "[!] Scan interrupted (Ctrl+C)" + RESET)
    sys.exit()

# Main
def main():
    try:
        banner()

        print(GREEN + "Select Option:\n")
        print("1. Aggressive Scan")
        print("2. Version Scan")
        print("3. Normal Scan")
        print("4. Custom Port Scan")
        print("5. Script Scan")
        print("6. Know Your IP\n" + RESET)

        choice = input(GREEN + "Enter option: " + RESET)

        if choice == "6":
            get_my_ip()
            return

        ip = input(GREEN + "Enter Target IP: " + RESET)

        start_time = time.time()

        if choice == "1":
            print(GREEN + "\n[+] Aggressive Scan Running...\n" + RESET)
            run_scan(ip, range(1, 1000), "normal")

        elif choice == "2":
            print(GREEN + "\n[+] Version Scan Running...\n" + RESET)
            run_scan(ip, range(1, 500), "version")

        elif choice == "3":
            print(GREEN + "\n[+] Normal Scan Running...\n" + RESET)
            run_scan(ip, range(1, 200), "normal")

        elif choice == "4":
            ports_input = input(GREEN + "Enter ports (80,443,21): " + RESET)
            ports = [int(p.strip()) for p in ports_input.split(",")]
            print(GREEN + "\n[+] Custom Scan Running...\n" + RESET)
            run_scan(ip, ports, "normal")

        elif choice == "5":
            script = input(GREEN + "Enter script path: " + RESET)

            if os.path.exists(script):
                print(GREEN + "\n[+] Running Script...\n" + RESET)
                os.system(f"python {script} {ip}")
            else:
                print(GREEN + "[-] Script not found!" + RESET)

        else:
            print(GREEN + "Invalid option!" + RESET)

        end_time = time.time()
        print(GREEN + f"\n[✓] Scan completed in {round(end_time - start_time, 2)} sec" + RESET)

    except KeyboardInterrupt:
        exit_gracefully()

if __name__ == "__main__":
    main()