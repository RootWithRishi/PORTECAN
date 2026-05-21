# 🔍 Advanced Port Scanner GUI

A beginner-friendly **Python + Tkinter + Nmap** based advanced port scanner with multiple scanning modes and a graphical interface.

Designed for learning:

* Networking
* Ethical Hacking
* Cybersecurity
* Port Enumeration
* Python GUI Development

---

## 📸 Features

✔ Basic TCP Port Scan
✔ Common Ports Scan
✔ Full TCP Port Scan
✔ Service Version Detection
✔ OS Detection
✔ Aggressive Scan
✔ Fast Scan
✔ TCP SYN Scan
✔ UDP Scan
✔ Custom Nmap Command Execution
✔ Automatic Default Scan (1–1024)
✔ Separate Popup Result Window
✔ GUI-Based Interface
✔ Beginner Friendly

---

## 🛠 Requirements

Install dependencies:

```bash
sudo apt update
sudo apt install python3 python3-tk nmap -y
```

Install Python packages:

```bash
pip install tkinter
```

---

## 🚀 Run Project

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/advanced-port-scanner.git
```

Move into project:

```bash
cd advanced-port-scanner
```

Run:

```bash
python3 port_scanner_gui.py
```

---

## 🖥 Scan Modes

| Scan Type         | Description              |
| ----------------- | ------------------------ |
| Basic TCP Scan    | Scan selected port range |
| Common Ports Scan | Scan popular ports       |
| Full TCP Scan     | Scan all TCP ports       |
| Service Version   | Detect running services  |
| OS Detection      | Detect operating system  |
| Aggressive Scan   | Advanced discovery       |
| Fast Scan         | Quick scan               |
| TCP SYN Scan      | TCP SYN discovery        |
| UDP Scan          | UDP enumeration          |
| Custom Nmap       | User-defined command     |

---

## 📚 Example Commands

Service Scan:

```bash
nmap -sV 192.168.1.1
```

OS Detection:

```bash
nmap -O 192.168.1.1
```

Aggressive Scan:

```bash
nmap -A 192.168.1.1
```

Custom Port Range:

```bash
nmap -p 1-5000 192.168.1.1
```

---

## 📁 Project Structure

```plaintext
advanced-port-scanner/
│
├── port_scanner_gui.py
├── README.md
└── requirements.txt
```

---

## 🎯 Why This Project

This project helps beginners understand:

* How port scanning works
* Network service discovery
* Enumeration concepts
* Nmap integration
* Python socket programming
* GUI application development

Instead of memorizing commands, users can learn visually.

---

## ⚠ Disclaimer

This project is intended for:

✔ Personal Labs
✔ Local Networks
✔ CTF Practice
✔ Authorized Testing

Do not scan systems without permission.

---



Built with Python + Tkinter + Nmap


## 👨‍💻 Author 
        Rishikesh Borah
Linkedin - www.linkedin.com/in/rishikeshborah


portfolio - rishidev.online


tryhackme - https://tryhackme.com/p/Rishi007r
