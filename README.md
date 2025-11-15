# DataDive - Ultimate Reconnaissance Toolkit

## Overview

Welcome to **DataDive**, the all-in-one reconnaissance tool for security researchers and penetration testers! This toolkit integrates multiple security tools to streamline subdomain discovery, live host testing, SSL vulnerability checks, and more. Designed for Linux systems using `deb` package management, DataDive automates your reconnaissance workflow efficiently.

This project is built around **GoPath**, leveraging its capabilities for high-speed directory scanning. Unlike other tools, **GoPath does not need to be downloaded separately** - it runs directly from the source code included in this repository. **DataDive** focuses on creating a fast, automated, and powerful reconnaissance workflow.

## Features

* **Subdomain Enumeration** - Uses Subfinder to uncover subdomains.
* **Live Host Detection** - Uses Httpx to verify active domains.
* **Favicon Hashing** - Extracts favicons and generates mmh3 hashes for Shodan and Zoomeye searches.
* **Website Screenshots** - Uses Aquatone to capture visuals of live sites.
* **Directory Enumeration** - Finds hidden files and directories with GoPath.
* **SSL Security Scanning** - Identifies SSL/TLS weaknesses using SSLyze.
* **Network Reconnaissance** - Uses Nmap for detailed scanning.
* **Web Security Auditing** - Detects vulnerabilities in web servers with Nikto.
* **Exploit Detection** - Uses Nuclei for vulnerability detection.
* **Spyhunt Integration** - Automates attack surface discovery.

## Prerequisites

Ensure your system runs a **Linux distribution** with `apt` package management. You will need the following tools installed:

* `subfinder`
* `httpx-toolkit`
* `aquatone`
* `GoPath`
* `sslyze`
* `nmap`
* `nikto`
* `nuclei`
* `spyhunt`
* `python3`
* Python libraries: `requests`, `mmh3`, `favicon`, `base64`

## Installation

1. **Clone the Repository:**

```sh
git clone <repository-url>
cd DataDive
```

2. **Install Required Dependencies:**

```sh
sudo apt install subfinder httpx-toolkit nmap nikto
wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip
unzip aquatone_linux_amd64_1.7.0.zip
```

3. **Install Python Libraries:**

```sh
pip install requests mmh3 favicon
```

4. **GoPath for Directory Enumeration:**

No separate installation needed - **GoPath runs directly from this repository**.

## How to Use

* **Run the script:**

```sh
python3 datadive.py
```

* Follow the prompts.
* Outputs are saved for later analysis.

## Important Notes

* **GoPath uses significant system resources**, especially on large scans.
* Some scans launch in **new terminal (`konsole`) windows** and run multi-threaded.
* Ensure `konsole` is installed before running the tool.
* Default output filenames are requested during execution.

## Disclaimer

This tool is for **security research and educational purposes only**. Using it on systems without permission is **illegal and unethical**. Use responsibly.
