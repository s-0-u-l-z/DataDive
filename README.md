# 🚀 DataDive - Ultimate Reconnaissance Toolkit

## 🌟 Overview

Welcome to **DataDive**, the all-in-one reconnaissance tool for security researchers and penetration testers! 🗏️💻 This powerhouse integrates multiple security tools to streamline subdomain discovery, live host testing, SSL vulnerability checks, and much more. Designed for Linux systems using `deb` package management, DataDive automates your reconnaissance workflow like never before! ⚡

This project is built around **GoPath**, leveraging its capabilities for high-speed directory scanning, making enumeration faster and more efficient. Unlike other tools, **GoPath does not need to be downloaded separately**—it runs straight from the source code within this repository. **DataDive** is a personal project aimed at creating a streamlined, powerful reconnaissance workflow with seamless automation. 🚀

## 🔥 Features

✅ **Subdomain Enumeration** - Uses Subfinder to uncover hidden subdomains.\
✅ **Live Host Detection** - Uses Httpx to verify active domains.\
✅ **Favicon Hashing** - Extracts favicons & generates mmh3 hashes for Shodan & Zoomeye searches.\
✅ **Website Screenshots** - Uses Aquatone to capture visuals of live sites.\
✅ **Directory Enumeration** - Finds hidden files & directories with GoPath.\
✅ **SSL Security Scanning** - Identifies SSL/TLS weaknesses using SSLyze.\
✅ **Network Reconnaissance** - Uses Nmap for deep network scans.\
✅ **Web Security Auditing** - Detects vulnerabilities in web servers with Nikto.\
✅ **Exploit Detection** - Leverages Nuclei for known vulnerability scans.\
✅ **Spyhunt Integration** - Automates attack surface discovery techniques.

## ⚡ Prerequisites

Ensure your system runs a **Linux distribution** with `apt` package management. You’ll need the following tools installed:

- `subfinder`
- `httpx-toolkit`
- `aquatone`
- `GoPath` (for ultra-fast directory scanning!)
- `sslyze`
- `nmap`
- `nikto`
- `nuclei`
- `spyhunt`
- `python3`
- Python libraries: `requests`, `mmh3`, `favicon`, `base64`

## 🚀 Installation

1️⃣ **Clone the Repository:**

```sh
git clone <repository-url>
cd DataDive
```

2️⃣ **Install Required Dependencies:**

```sh
sudo apt install subfinder httpx-toolkit nmap nikto
wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip
unzip aquatone_linux_amd64_1.7.0.zip
```

3️⃣ **Install Python Libraries:**

```sh
pip install requests mmh3 favicon
```

4️⃣ **GoPath for Directory Enumeration:**

No separate installation needed! **GoPath runs directly from this repository**, using its built-in functionality to execute scans.

## 🎯 How to Use

🔹 **Run the script:**

```sh
python3 datadive.py
```

🔹 **Follow the prompts** to conduct reconnaissance effortlessly.\
🔹 **Outputs** are automatically saved for later analysis.

## ⚠️ Important Notes

⚡ **GoPath consumes a significant amount of system resources**, especially during large scans.\
⚡ Some scans launch in **new terminal (****`konsole`****) windows** and run multiple threads simultaneously for maximum performance.\
⚡ Ensure `konsole` is installed on your system before running the tool.\
⚡ Default output filenames are prompted during execution.

## ⚖️ Disclaimer

This tool is meant for **security research & educational purposes only**. Unauthorized use on systems without permission is **illegal & unethical**. Stay responsible! 🔒

---

✨ **Empower your recon game with DataDive – Because Knowledge is Power!** 

