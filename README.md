🟢 RISHI SHADOW PORT SCANNER

A Python-based advanced port scanner with a hacker-style terminal interface.
Designed for learning cybersecurity, networking, and ethical hacking.

🚀 Features
⚡ Aggressive Port Scan (1–1000)
🔍 Version Detection Scan
📊 Normal Scan (basic ports)
🎯 Custom Port Scan (user-defined)
🧩 Script Scan (run your own scripts)
🌐 Know Your IP (public + local)
💻 Hacker-style green terminal UI
⛔ Ctrl + C safe exit
⚙️ Multi-threaded fast scanning
🧠 Use Cases
Learning port scanning concepts
Practicing ethical hacking
Network troubleshooting
Cybersecurity projects
⚠️ Disclaimer

This tool is made for educational purposes only.
Do NOT scan any system without proper authorization.

📦 Requirements
Python 3.x
Internet connection (for IP detection)
Built-in Libraries Used:
socket
threading
os
time
sys
urllib

(No external libraries required ✅)

🛠️ Installation
1. Clone the repository
git clone https://github.com/your-username/port-scanner.git
cd port-scanner
2. Run the tool
python portscanner.py
📋 Usage

After running the script, you will see:

1. Aggressive Scan
2. Version Scan
3. Normal Scan
4. Custom Port Scan
5. Script Scan
6. Know Your IP
Example:
Select option → 1
Enter target IP → 192.168.1.1
🔥 Scan Modes Explained
1. Aggressive Scan

Scans ports from 1 to 1000 quickly.

2. Version Scan

Attempts to detect service banners.

3. Normal Scan

Basic scan for common ports (1–200).

4. Custom Port Scan

User defines ports:

80,443,21
5. Script Scan

Run your own Python script:

python your_script.py <target_ip>
6. Know Your IP

Displays:

Public IP 🌐
Local IP 🖥️
⛔ Exit Tool

Press:

CTRL + C

✔ Safely stops scanning
✔ No crash

🖥️ Example Output
[+] Aggressive Scan Running...

[OPEN] Port 22
[OPEN] Port 80
[OPEN] Port 443

[✓] Scan completed in 3.45 sec
🔮 Future Improvements
Save results (JSON / CSV)
OS detection
Advanced service detection
GUI version (Tkinter dashboard)
Stealth scan (SYN scan using Scapy)
Kali Linux installer
👨‍💻 Author

Rishikesh Borah
Aspiring Cybersecurity Professional 🔐
BCA Student | Python & Networking Enthusiast

⭐ Support

If you like this project:

⭐ Star the repo
🍴 Fork it
🧠 Improve it
