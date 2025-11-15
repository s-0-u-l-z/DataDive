#!/usr/bin/env python3
import shutil
from termcolor import colored
import sys
import os
import time as tm
import requests
import subprocess
import json
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

LVU = 'https://raw.githubusercontent.com/s-0-u-l-z/DataDive/refs/heads/DataDive-Main/version.txt'
CV = 2.01

INF = colored("INF", "blue")
OK = colored("[OK]", "green")
ERR = colored("[ERR]", "red")
WARN = colored("[!]", "yellow")
PROG = colored("[→]", "cyan")

OUTD = Path("datadive_output")
SUBD = OUTD / "subdomains"
REDD = OUTD / "open_redirects"
SQLD = OUTD / "sql_injection"
S3D = OUTD / "s3_buckets"
GITHD = OUTD / "github_secrets"

def slp(sec):
    tm.sleep(sec)

def mkdirs():
    dirs = [OUTD, SUBD, REDD, SQLD, S3D, GITHD]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    print(f"{OK} Output directories created in: {OUTD.absolute()}")

def printhdr(title):
    print(f'\n\n{"="*70}')
    print(f'[{INF}] {title}')
    print(f'{"="*70}\n')
    slp(1)

def cmd(c, desc="", silent=False):
    if desc and not silent:
        print(f"[{INF}] {desc}")
        print(f"{PROG} Command: {c}")
    
    try:
        res = subprocess.run(
            c, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=300
        )
        
        if res.stdout and not silent:
            print(res.stdout)
        
        if res.stderr and res.returncode != 0:
            print(f"{ERR} Error executing command:")
            print(res.stderr)
        
        return res
        
    except subprocess.TimeoutExpired:
        print(f"{ERR} Command timed out after 5 minutes: {c}")
        return None
    except Exception as e:
        print(f"{ERR} Unexpected error: {str(e)}")
        return None

def lc(fp):
    try:
        res = subprocess.run(['wc', '-l', fp], capture_output=True, text=True)
        if res.returncode == 0:
            return int(res.stdout.strip().split()[0])
    except (ValueError, IndexError):
        pass
    return 0

def fex(fp):
    p = Path(fp)
    return p.exists() and p.stat().st_size > 0

def detpm():
    mgrs = {
        "apt": ["apt", "apt-get"],
        "dnf": ["dnf"],
        "pacman": ["pacman"],
        "zypper": ["zypper"],
        "xbps": ["xbps-install"],
        "eopkg": ["eopkg"],
        "apk": ["apk"],
        "emerge": ["emerge"],
        "brew": ["brew"],
        "nix": ["nix-env"]
    }
    
    for mgr, cmds in mgrs.items():
        for c in cmds:
            if shutil.which(c):
                return mgr
    return None

def instgo():
    if shutil.which("go") is not None:
        print(f"{OK} Go is already installed")
        return True
    
    print(f"{ERR} Go is not installed on your system.")
    print(f"{WARN} Go is required for installing reconnaissance tools.")
    
    pm = detpm()
    if not pm:
        allpm = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
        print(f"{WARN} Could not auto-detect package manager.")
        print(f"{WARN} Please enter your package manager ({'/'.join(allpm)}):")
        pm = input("Package manager: ").strip().lower()
    
    icmd = {
        "apt": "sudo apt update && sudo apt install golang -y",
        "dnf": "sudo dnf install golang -y",
        "pacman": "sudo pacman -Sy --noconfirm go",
        "zypper": "sudo zypper install golang",
        "xbps": "sudo xbps-install -S golang",
        "eopkg": "sudo eopkg install golang",
        "apk": "sudo apk add go",
        "emerge": "sudo emerge dev-lang/go",
        "brew": "brew install go",
        "nix": "nix-env -iA nixpkgs.go"
    }
    
    if pm not in icmd:
        print(f"{ERR} Unsupported or unknown package manager: {pm}")
        return False
    
    print(f"[{INF}] Installing Go using {pm}...")
    os.system(icmd[pm])
    
    if shutil.which("go"):
        print(f"{OK} Go installation complete.")
        return True
    else:
        print(f"{ERR} Go installation failed. Please install manually.")
        return False

def instaws():
    if shutil.which("aws") is not None:
        print(f"{OK} AWS CLI is already installed")
        return True
    
    print(f"{WARN} AWS CLI is not installed. This is needed for S3 bucket analysis.")
    
    pm = detpm()
    if not pm:
        pm = "apt"
    
    icmd = {
        "apt": "sudo apt install awscli -y",
        "pacman": "sudo pacman -S aws-cli --noconfirm",
        "dnf": "sudo dnf install awscli -y",
        "zypper": "sudo zypper install aws-cli-v2",
        "eopkg": "sudo eopkg install aws-cli",
        "xbps": "sudo xbps-install -S aws-cli",
        "apk": "sudo apk add aws-cli",
        "emerge": "emerge -av net-misc/awscli",
        "nix": "nix-env -iA nixpkgs.awscli2",
        "brew": "brew install awscli"
    }
    
    if pm not in icmd:
        print(f"{WARN} Cannot auto-install AWS CLI. Please install manually:")
        print(f"        https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
        return False
    
    print(f"[{INF}] Installing AWS CLI using {pm}")
    os.system(icmd[pm])
    
    if shutil.which("aws"):
        print(f"{OK} AWS CLI installation complete.")
        return True
    else:
        print(f"{WARN} AWS CLI installation failed. Some S3 features may not work.")
        return False

def chkuro():
    if shutil.which("uro") is not None:
        print(f"{OK} uro is installed")
        return True
    
    print(f'{WARN} uro is not installed. This tool helps deduplicate URLs.')
    print(f'{WARN} Install it from: https://github.com/s0md3v/uro')
    print(f'{WARN} Or run: pip3 install uro')
    
    inst = input(f"[{INF}] Try to install via pip3? (y/n): ").lower()
    if inst == 'y':
        os.system("pip3 install uro")
        return shutil.which("uro") is not None
    return False

def instjq():
    if shutil.which("jq") is not None:
        print(f"{OK} jq is already installed")
        return True
    
    print(f'{ERR} jq is not installed. This tool is essential for processing JSON output.')
    
    pm = detpm()
    if not pm:
        allpm = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
        print(f"{WARN} Please enter your package manager ({'/'.join(allpm)}):")
        pm = input("Package manager: ").strip().lower()
    
    icmd = {
        "apt": "sudo apt update && sudo apt install jq -y",
        "dnf": "sudo dnf install jq -y",
        "pacman": "sudo pacman -Sy --noconfirm jq",
        "zypper": "sudo zypper install jq",
        "xbps": "sudo xbps-install -S jq",
        "eopkg": "sudo eopkg install jq",
        "apk": "sudo apk add jq",
        "emerge": "sudo emerge app-misc/jq",
        "brew": "brew install jq",
        "nix": "nix-env -iA nixpkgs.jq"
    }
    
    if pm not in icmd:
        print(f"{ERR} Unsupported package manager: {pm}")
        return False
    
    print(f"[{INF}] Installing jq using {pm}...")
    os.system(icmd[pm])
    
    if shutil.which("jq"):
        print(f"{OK} jq installation complete.")
        return True
    else:
        print(f"{ERR} jq installation failed.")
        return False

def instgopkg(gp):
    print(f"[{INF}] Installing {gp}")
    cmd(f"go install {gp}", f"Installing Go package {gp}")

def chktools():
    gt = {
        "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
        "katana": "github.com/projectdiscovery/katana/cmd/katana@latest",
        "amass": "github.com/owasp-amass/amass/v3/...@master",
        "subjack": "github.com/haccer/subjack@latest",
        "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
        "assetfinder": "github.com/tomnomnom/assetfinder@latest",
        "naabu": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
        "gau": "github.com/lc/gau/v2/cmd/gau@latest",
        "ffuf": "github.com/ffuf/ffuf@latest",
        "nuclei": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        "waybackurls": "github.com/tomnomnom/waybackurls@latest",
        "gf": "github.com/tomnomnom/gf@latest",
        "qsreplace": "github.com/tomnomnom/qsreplace@latest",
        "hakrawler": "github.com/hakluke/hakrawler@latest"
    }
    
    tst = {}
    
    print(f"\n[{INF}] Checking required reconnaissance tools...")
    print(f"{PROG} This may take a few minutes for first-time setup.\n")
    
    for bin, gp in gt.items():
        pth = shutil.which(bin)
        if pth:
            print(f"{OK} {bin:20s} → Installed at {pth}")
            tst[bin] = True
        else:
            print(f"{WARN} {bin:20s} → Not found, installing...")
            instgopkg(gp)
            
            if shutil.which(bin):
                print(f"{OK} {bin:20s} → Successfully installed")
                tst[bin] = True
            else:
                print(f"{ERR} {bin:20s} → Installation failed")
                tst[bin] = False
    
    return tst

def chkver():
    try:
        r = requests.get(LVU, timeout=5)
        lv = float(r.text.strip())
        
        if CV < lv:
            st = f"({colored('outdated', 'red')})"
            msg = f"{WARN} A newer version (v{lv}) is available!"
        elif CV > lv:
            st = f"({colored('dev build', 'yellow')})"
            msg = f"{WARN} You're running a development build"
        else:
            st = f"({colored('latest', 'green')})"
            msg = f"{OK} You're running the latest version"
        
        return CV, lv, st, msg
    except Exception as e:
        st = f"({colored('unknown', 'yellow')})"
        msg = f"{WARN} Could not check for updates: {str(e)}"
        return CV, None, st, msg

def banner():
    cv, lv, st, msg = chkver()
    
    bnr = f"""
        ██████╗░░█████╗░████████╗░█████╗░██████╗░██╗██╗░░░██╗███████╗
        ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
        ██║░░██║███████║░░░██║░░░███████║██║░░██║██║╚██╗░██╔╝█████╗░░
        ██║░░██║██╔══██║░░░██║░░░██╔══██║██║░░██║██║░╚████╔╝░██╔══╝░░
        ██████╔╝██║░░██║░░░╚═══╝░░██║░░██║██████╔╝██║░░╚██╔╝░░███████╗
        ╚═════╝░╚═╝░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚══════╝

                            By s0ulz
                Advanced Security Reconnaissance Framework

    [{INF}] Current version: v{cv} {st}
    {msg}
    """
    
    for line in bnr.split('\n'):
        print(line)
    
    slp(1)

def subenum(tgt):
    printhdr("Subdomain Enumeration & Discovery")
    
    print(f"[{INF}] Target domain: {colored(tgt, 'cyan')}")
    print(f"[{INF}] This process discovers all subdomains associated with the target")
    print(f"{PROG} Using multiple data sources for comprehensive coverage\n")
    slp(2)
    
    sfo = SUBD / "subfinder.txt"
    afo = SUBD / "assetfinder.txt"
    amo = SUBD / "amass.txt"
    co = SUBD / "all_subdomains.txt"
    ao = SUBD / "alive.txt"
    sco = SUBD / "status_codes.txt"
    
    print(colored("→ Running Subfinder", "yellow"))
    print(f"{PROG} Subfinder queries multiple sources (crt.sh, VirusTotal, etc.)")
    cmd(
        f'subfinder -d {tgt} -all -silent >> {sfo}',
        f'Discovering subdomains for {tgt} using all available sources'
    )
    sfc = lc(str(sfo))
    print(f"{OK} Subfinder found {sfc} subdomains\n")
    slp(1)
    
    print(colored("→ Running Assetfinder", "yellow"))
    print(f"{PROG} Assetfinder finds related assets and subdomains")
    cmd(
        f'assetfinder --subs-only {tgt} >> {afo}',
        f'Finding related subdomains using Assetfinder'
    )
    afc = lc(str(afo))
    print(f"{OK} Assetfinder found {afc} subdomains\n")
    slp(1)
    
    print(colored("→ Running Amass (30s timeout)", "yellow"))
    print(f"{PROG} Amass performs deep DNS enumeration")
    print(f"{WARN} Timeout set to prevent excessive runtime")
    cmd(
        f'amass enum -timeout 30 -norecursive -d {tgt} >> {amo}',
        f'Running Amass enumeration with controlled timeout'
    )
    amc = lc(str(amo))
    print(f"{OK} Amass found {amc} subdomains\n")
    slp(1)
    
    print(f"[{INF}] Merging results from all tools...")
    cmd(
        f"sort -u {sfo} {afo} {amo} > {co}",
        'Combining and deduplicating subdomains from all sources'
    )
    tc = lc(str(co))
    print(f"{OK} Total unique subdomains discovered: {colored(str(tc), 'green', attrs=['bold'])}\n")
    
    print(colored("→ Probing for live subdomains with httpx", "yellow"))
    print(f"{PROG} This checks which subdomains are actually responding")
    
    if tc >= 500:
        print(f"{WARN} Large subdomain list detected, using 50 threads for faster scanning")
        cmd(
            f"httpx -l {co} -o {ao} -t 50 -silent",
            'Checking subdomain availability with increased concurrency'
        )
    else:
        cmd(
            f"httpx -l {co} -o {ao} -silent",
            'Checking which subdomains are live and responding'
        )
    
    ac = lc(str(ao))
    print(f"{OK} Live subdomains: {colored(str(ac), 'green', attrs=['bold'])} out of {tc}")
    print(f"{OK} Results saved to: {ao}\n")
    
    print(f"[{INF}] Collecting HTTP status codes...")
    cmd(
        f'httpx -l {co} -sc -silent >> {sco}',
        'Retrieving HTTP status codes for all subdomains'
    )
    
    oko = SUBD / "200_ok.txt"
    cmd(
        f"cat {sco} | grep '\\[200\\]' >> {oko}",
        'Filtering for successful (200 OK) responses'
    )
    okc = lc(str(oko))
    print(f"{OK} Subdomains with 200 OK status: {okc}\n")
    
    printhdr("Subdomain Takeover Detection")
    print(f"{PROG} Checking for vulnerable subdomain configurations...")
    
    sjo = SUBD / "subjack_results.txt"
    cmd(
        f"subjack -w {co} -t 100 -ssl -v -o {sjo}",
        'Running Subjack to detect potential subdomain takeovers'
    )
    
    nto = SUBD / "nuclei_takeover.txt"
    cmd(
        f"nuclei -l {co} -t ~/nuclei-templates/takeovers/ -silent >> {nto}",
        'Using Nuclei templates to detect takeover vulnerabilities'
    )
    print(f"{OK} Takeover check results saved to: {SUBD}\n")
    
    printhdr("Deep Web Crawling")
    print(f"{PROG} Crawling live subdomains to discover hidden content...")
    
    kjo = SUBD / "katana_js.txt"
    kdo = SUBD / "katana_deep.txt"
    
    cmd(
        f"katana -list {ao} -jc -silent -o {kjo}",
        'Extracting JavaScript files from live subdomains'
    )
    
    cmd(
        f"katana -list {ao} -d 5 -ef woff,css,png,svg,jpg,woff2,jpeg,gif,ico -silent -o {kdo}",
        'Performing deep crawl (depth=5) to discover all URLs'
    )
    
    jsc = lc(str(kjo))
    dc = lc(str(kdo))
    print(f"{OK} JavaScript files discovered: {jsc}")
    print(f"{OK} Total URLs discovered: {dc}\n")
    
    return str(co)

def redtest(tgt, sf):
    printhdr("Open Redirect Vulnerability Detection")
    
    print(f"[{INF}] Open redirects allow attackers to redirect users to malicious sites")
    print(f"{PROG} Testing {colored(tgt, 'cyan')} for redirect vulnerabilities\n")
    slp(2)
    
    print(colored("→ Phase 1: URL Collection", "yellow"))
    print(f"{PROG} Gathering URLs from Wayback Machine and crawlers...\n")
    
    go = REDD / "gau_urls.txt"
    ko = REDD / "katana_urls.txt"
    uo = REDD / "urlfinder_urls.txt"
    ho = REDD / "hakrawler_urls.txt"
    
    cmd(
        f"cat {sf} | gau --o {go}",
        'Fetching historical URLs from Wayback Machine and CommonCrawl'
    )
    
    cmd(
        f"cat {SUBD / 'alive.txt'} | katana -d 2 -silent -o {ko}",
        'Crawling live sites for URLs with redirect parameters'
    )
    
    cmd(
        f"cat {SUBD / 'alive.txt'} | hakrawler -d 2 -silent > {ho}",
        'Using Hakrawler for additional URL discovery'
    )
    
    cu = REDD / "all_redirect_urls.txt"
    cmd(
        f"cat {go} {ko} {ho} | uro | sort -u > {cu}",
        'Normalizing and deduplicating all discovered URLs'
    )
    
    uc = lc(str(cu))
    print(f"{OK} Total URLs collected: {uc}\n")
    
    print(colored("→ Phase 2: Redirect Parameter Detection", "yellow"))
    print(f"{PROG} Filtering URLs with common redirect parameter names...\n")
    
    rpo = REDD / "redirect_params.txt"
    rrx = "returnUrl=|continue=|dest=|destination=|forward=|go=|goto=|login\\?to=|next=|next_page=|out=|redir=|redirect=|redirect_to=|redirect_uri=|return=|returnTo=|return_url=|url=|qurl=|jump=|originUrl=|Url=|location=|ReturnUrl="
    
    cmd(
        f"cat {cu} | grep -Pi '{rrx}' > {rpo}",
        'Extracting URLs with potential redirect parameters'
    )
    
    rc = lc(str(rpo))
    print(f"{OK} URLs with redirect parameters: {rc}\n")
    
    if rc == 0:
        print(f"{WARN} No redirect parameters found. Skipping payload injection.")
        return
    
    print(colored("→ Phase 3: Payload Injection & Testing", "yellow"))
    print(f"{PROG} Injecting test payloads to detect open redirects...\n")
    
    t1o = REDD / "test_method1.txt"
    cmd(
        f"cat {rpo} | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com' >> {t1o}",
        'Testing Method 1: Direct payload injection with httpx validation'
    )
    
    t2o = REDD / "test_method2.txt"
    cmd(
        r'cat ' + str(rpo) + r' | qsreplace "https://evil.com" | xargs -I {} curl -s -o /dev/null -w "%{url_effective} -> %{redirect_url}\n" {} >> ' + str(t2o),
        'Testing Method 2: Using curl to track redirect chains'
    )
    
    t3o = REDD / "nuclei_openredirect.txt"
    cmd(
        f"nuclei -l {SUBD / 'alive.txt'} -t ~/nuclei-templates/http/vulnerabilities/open-redirect/ -silent -c 45 >> {t3o}",
        'Testing Method 3: Nuclei template-based detection'
    )
    
    print(f"\n[{INF}] Advanced Payload Testing")
    print(f"{PROG} Using comprehensive payload list...\n")
    
    pd = Path("payloads")
    pd.mkdir(exist_ok=True)
    pf = pd / "openredirect.txt"
    
    if not pf.exists():
        pl = [
            "https://google.com",
            "//google.com",
            "https://evil.com",
            "//evil.com/%2f..",
            "javascript:alert(1)",
            "/\\google.com",
            "https:google.com",
            "//google%E3%80%82com",
            "/〱google.com",
            "////google.com",
        ]
        with open(pf, 'w') as f:
            f.write('\n'.join(pl))
        print(f"{OK} Created sample payload file at {pf}")
    
    t4o = REDD / "test_advanced.txt"
    if pf.exists():
        cmd(
            f'cat {rpo} | head -50 | while read url; do cat {pf} | while read payload; do echo "$url" | qsreplace "$payload"; done; done | httpx -silent -fr -mc 301,302 >> {t4o}',
            'Testing with advanced payload list (limited to first 50 URLs to prevent timeout)'
        )
    
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} Open Redirect Testing Complete!")
    print(f"{colored('='*70, 'green')}\n")
    
    print(f"[{INF}] Results Summary:")
    print(f"    • Method 1 (httpx): {lc(str(t1o))} potential findings")
    print(f"    • Method 2 (curl): {lc(str(t2o))} redirect chains")
    print(f"    • Method 3 (Nuclei): {lc(str(t3o))} validated vulnerabilities")
    print(f"    • Method 4 (Advanced): {lc(str(t4o))} additional findings")
    print(f"\n{PROG} All results saved to: {REDD}\n")
    
    print(f"{WARN} Manual verification recommended for all findings")
    print(f"{WARN} False positives are common - verify in browser\n")

def wafbyp(tgt, sf):
    printhdr("WAF Bypass & SQL Injection Testing")
    
    print(f"[{INF}] Web Application Firewalls (WAFs) block malicious requests")
    print(f"{PROG} We'll use IP rotation and payload obfuscation to bypass them\n")
    slp(2)
    
    print(colored("→ ProxyChains Configuration", "yellow"))
    print(f"\n{WARN} IMPORTANT: ProxyChains Setup Required\n")
    print("ProxyChains routes your traffic through proxy servers to:")
    print("  • Evade IP-based rate limiting")
    print("  • Bypass geographic restrictions")
    print("  • Avoid IP blacklisting")
    print("\nSetup Instructions:")
    print(f"{PROG} 1. Edit configuration: sudo nano /etc/proxychains.conf")
    print(f"{PROG} 2. Comment out: #socks4 127.0.0.1 9050")
    print(f"{PROG} 3. Enable: random_chain (uncomment)")
    print(f"{PROG} 4. Add proxies (get free ones from https://www.sslproxies.org/):")
    print("       http <ip> <port> <username> <password>")
    print("       Example: http 192.168.1.1 8080")
    print(f"{PROG} 5. Optional: Enable quiet_mode to reduce logs\n")
    
    rdy = input(f"[{INF}] Have you configured ProxyChains? (y/n): ").lower()
    
    if rdy == 'y':
        print(f"\n[{INF}] Testing ProxyChains configuration...")
        print(colored("Testing IP rotation...", "yellow"))
        
        print(f"\n{PROG} Test 1: Check current IP")
        cmd("proxychains curl -s http://ipinfo.io/ip", "Fetching IP through ProxyChains")
        
        print(f"\n{PROG} Test 2: Verify IP rotation")
        cmd("proxychains curl -s http://ipinfo.io/ip", "Fetching IP again to verify rotation")
        
        print(f"\n{OK} If you see different IPs above, ProxyChains is working!\n")
        slp(2)
    else:
        print(f"{WARN} ProxyChains not configured. Continuing without IP rotation...")
        print(f"{WARN} WAF bypass effectiveness will be limited\n")
        slp(2)
    
    print(colored("→ SQLMap with WAF Bypass", "yellow"))
    print(f"\n[{INF}] SQLMap is an automated SQL injection tool")
    print(f"{PROG} We'll combine it with ProxyChains and tamper scripts\n")
    
    sqlt = input(f"[{INF}] Enter URL for SQLMap testing (or press Enter to skip): ").strip()
    
    if sqlt:
        print(f"\n[{INF}] Launching SQLMap with bypass techniques...")
        print(f"{WARN} This may take 10-30 minutes depending on the target\n")
        
        sqlo = SQLD / "sqlmap_results.txt"
        sqlc = f"sqlmap -u '{sqlt}' --dbs --batch --random-agent --tamper=between,space2comment --level=5 --risk=3 --threads=10 2>&1 | tee {sqlo}"
        
        if rdy == 'y':
            sqlc = "proxychains " + sqlc
            print(f"{PROG} Using ProxyChains for IP rotation")
        
        print(f"\n{PROG} Command breakdown:")
        print("  --dbs: Enumerate databases")
        print("  --batch: Non-interactive mode")
        print("  --random-agent: Rotate User-Agent headers")
        print("  --tamper=between,space2comment: Obfuscate payloads")
        print("  --level=5 --risk=3: Maximum testing depth")
        print("  --threads=10: Concurrent requests\n")
        
        cmd(sqlc, "Running SQLMap with WAF bypass techniques")
        print(f"\n{OK} SQLMap results saved to: {sqlo}\n")
    
    printhdr("Mass SQL Injection Discovery")
    print(f"{PROG} Scaling SQLi detection across all discovered subdomains...\n")
    
print(f"[{INF}] Step 1: Extracting unique domains...")
    ud = SQLD / "unique_domains.txt"
    cmd(
        f"cat {SUBD / 'alive.txt'} | awk -F/ '{{print $3}}' | sort -u > {ud}",
        "Extracting hostnames from live URLs"
    )
    dc = lc(str(ud))
    print(f"{OK} Extracted {dc} unique domains\n")
    
    print(f"[{INF}] Step 2: Collecting URLs with SQL parameters...")
    sur = SQLD / "sqli_urls_raw.txt"
    cmd(
        f"cat {ud} | waybackurls | gf sqli | uro > {sur}",
        "Using waybackurls + GF patterns to find potential SQLi points"
    )
    rawc = lc(str(sur))
    print(f"{OK} Found {rawc} URLs with SQL-like parameters\n")
    
    if rawc == 0:
        print(f"{WARN} No SQL parameter URLs found. Skipping SQLi testing.")
        return
    
    print(f"[{INF}] Step 3: Deduplicating URLs (one per domain)...")
    suf = SQLD / "sqli_urls_filtered.txt"
    cmd(
        f"cat {sur} | awk -F/ '{{if (!seen[$3]++) print}}' > {suf}",
        "Keeping only one URL per unique domain to prevent redundant scanning"
    )
    fc = lc(str(suf))
    print(f"{OK} Reduced to {fc} unique targets\n")
    
    print(f"[{INF}] Step 4: Scanning with Nuclei DAST templates...")
    print(f"{PROG} This actively tests for SQL injection vulnerabilities\n")
    
    nso = SQLD / "nuclei_sqli_findings.txt"
    cmd(
        f"nuclei -l {suf} -t ~/nuclei-templates/http/vulnerabilities/sqli/ -c 30 -silent >> {nso}",
        "Running Nuclei SQL injection detection templates"
    )
    
    finds = lc(str(nso))
    
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} SQL Injection Testing Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Findings Summary:")
    print(f"    • URLs tested: {fc}")
    print(f"    • Vulnerabilities found: {colored(str(finds), 'red' if finds > 0 else 'green')}")
    print(f"    • Results saved to: {SQLD}\n")
    
    if finds > 0:
        print(f"{WARN} CRITICAL: SQL injection vulnerabilities detected!")
        print(f"{WARN} Review {nso} immediately\n")

def s3scan(tgt, sf):
    printhdr("AWS S3 Bucket Discovery & Analysis")
    
    print(f"[{INF}] Searching for exposed Amazon S3 buckets associated with {colored(tgt, 'cyan')}")
    print(f"{PROG} S3 misconfigurations are a common source of data breaches\n")
    slp(2)
    
    print(colored("→ Method 1: Direct S3 Detection", "yellow"))
    sdo = S3D / "s3_direct_findings.txt"
    
    cmd(
        f"subfinder -d {tgt} -all -silent | httpx -silent -sc -title -td | grep -i 's3\\|amazon' >> {sdo}",
        "Scanning subdomains for direct S3 service indicators"
    )
    
    cmd(
        f"nuclei -l {sf} -t ~/nuclei-templates/http/technologies/s3-detect.yaml -silent >> {sdo}",
        "Using Nuclei to detect S3 bucket patterns"
    )
    
    dfc = lc(str(sdo))
    print(f"{OK} Direct S3 detections: {dfc}\n")
    
    print(colored("→ Method 2: JavaScript File Analysis", "yellow"))
    print(f"{PROG} Extracting S3 URLs from JavaScript files...\n")
    
    ajf = S3D / "all_javascript.txt"
    
    cmd(
        f"katana -u {tgt} -d 5 -jc -silent | grep '\\.js' > {ajf}",
        "Crawling for JavaScript files (depth=5)"
    )
    
    cmd(
        f"echo {tgt} | gau | grep '\\.js' | anew {ajf}",
        "Adding historical JS files from Wayback Machine"
    )
    
    jsa = S3D / "js_alive.txt"
    cmd(
        f"cat {ajf} | uro | sort -u | httpx -silent -mc 200 -o {jsa}",
        "Verifying which JS files are accessible"
    )
    
    jsc = lc(str(jsa))
    print(f"{OK} Live JavaScript files: {jsc}\n")
    
    sfj = S3D / "s3_urls_from_js.txt"
    jsc3 = 0
    if jsc > 0:
        cmd(
            f'cat {jsa} | xargs -I {{}} curl -s {{}} | grep -oE "(https?://[^/]*\\.s3[^/]*\\.amazonaws\\.com[^\\s\\"\\'<>]*)" | sort -u >> {sfj}',
            "Extracting S3 bucket URLs from JavaScript content"
        )
        
        jsc3 = lc(str(sfj))
        print(f"{OK} S3 URLs found in JavaScript: {jsc3}\n")
    
    print(colored("→ Method 3: Manual Google Dorking", "yellow"))
    print(f"\n{WARN} Perform these Google searches manually:\n")
    
    gd = [
        f'site:s3.amazonaws.com "{tgt}"',
        f'site:*.s3.amazonaws.com "{tgt}"',
        f'(site:*.s3.amazonaws.com OR site:*.s3-external-1.amazonaws.com) "{tgt}"',
        f'inurl:s3.amazonaws.com intitle:index.of.bucket "{tgt}"'
    ]
    
    dkf = S3D / "google_dorks.txt"
    with open(dkf, 'w') as f:
        f.write("Google Dorking Queries for S3 Bucket Discovery\n")
        f.write("="*70 + "\n\n")
        f.write("How to use these dorks:\n")
        f.write("1. Copy each query below\n")
        f.write("2. Paste into Google search bar\n")
        f.write("3. Review results for exposed buckets\n")
        f.write("4. Check for public vs private access\n\n")
        f.write("="*70 + "\n\n")
        
        for i, d in enumerate(gd, 1):
            print(f"  {i}. {colored(d, 'cyan')}")
            f.write(f"{i}. {d}\n")
    
    print(f"\n{OK} Dorks saved to: {dkf}")
    print(f"{PROG} Look for 'Access Denied' (private) vs. file listings (exposed)\n")
    
    print(colored("→ Method 4: Bucket Name Extraction", "yellow"))
    print(f"{PROG} Compiling list of discovered S3 buckets...\n")
    
    shn = S3D / "s3_bucket_names.txt"
    sfu = S3D / "s3_full_urls.txt"
    
    asrc = [sdo, sfj]
    cs3 = S3D / "all_s3_references.txt"
    
    cmd(
        f"cat {' '.join(str(f) for f in asrc if Path(f).exists())} | sort -u > {cs3}",
        "Combining all S3 references from different sources"
    )
    
    cmd(
        f"cat {cs3} | grep -oP '([a-zA-Z0-9.-]*\\.s3[^/]*\\.amazonaws\\.com)' | sort -u > {shn}",
        "Extracting S3 bucket hostnames"
    )
    
    cmd(
        f"cat {cs3} | grep -oP 'https?://[^\\s\"<>]*s3[^\\s\"<>]*amazonaws\\.com[^\\s\"<>]*' | sort -u > {sfu}",
        "Extracting complete S3 URLs with paths"
    )
    
    bc = lc(str(shn))
    uc = lc(str(sfu))
    
    print(f"{OK} Unique S3 buckets discovered: {bc}")
    print(f"{OK} Total S3 URLs (with paths): {uc}\n")
    
    if bc > 0:
        print(colored("→ Method 5: Permission Analysis", "yellow"))
        print(f"{PROG} Checking bucket permissions (requires AWS CLI)...\n")
        
        spm = S3D / "s3_permissions.txt"
        
        if shutil.which("aws"):
            print(f"[{INF}] Testing bucket access permissions...")
            cmd(
                f"cat {shn} | while read bucket; do echo \"Testing: $bucket\"; aws s3 ls s3://$bucket --no-sign-request 2>&1; done >> {spm}",
                "Attempting anonymous access to discovered buckets"
            )
            print(f"{OK} Permission check complete. Review {spm}\n")
        else:
            print(f"{WARN} AWS CLI not installed. Skipping permission checks.")
            print(f"{WARN} Install with: pip install awscli\n")
    
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} S3 Bucket Scanning Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Discovery Summary:")
    print(f"    • Direct detections: {dfc}")
    print(f"    • Buckets from JS files: {jsc3}")
    print(f"    • Total unique buckets: {bc}")
    print(f"    • All results saved to: {S3D}\n")
    
    if bc > 0:
        print(f"{WARN} Next Steps:")
        print(f"    1. Review {shn} for bucket names")
        print(f"    2. Check {spm} for access levels")
        print(f"    3. Test buckets manually: aws s3 ls s3://bucket-name")
        print(f"    4. Look for sensitive files: backups, configs, credentials\n")

def githscan(tgt):
    printhdr("GitHub Secret & Credential Discovery")
    
    print(f"[{INF}] Searching for exposed secrets related to {colored(tgt, 'cyan')}")
    print(f"{PROG} Public GitHub repositories are a goldmine for credentials\n")
    slp(2)
    
    print(colored("→ GitHub Dorking Queries", "yellow"))
    print(f"\n{WARN} Perform these searches on GitHub.com manually:\n")
    
    gdk = {
        "Passwords": f'"{tgt}" password',
        "API Keys (JSON)": f'"{tgt}" password extension:json',
        "Environment Files": f'org:{tgt} path:.env',
        "AWS Credentials": f'org:{tgt} "aws_access_key_id" OR "aws_secret_access_key"',
        "Generic Secrets": f'org:{tgt} "api_key" OR "secret_key" OR "client_secret"',
        "Database Credentials": f'"{tgt}" "database" "password" extension:yml',
        "Private Keys": f'org:{tgt} "BEGIN RSA PRIVATE KEY" OR "BEGIN PRIVATE KEY"',
        "Tokens": f'"{tgt}" "token" extension:txt',
        "Configuration Files": f'org:{tgt} filename:config.json OR filename:settings.json'
    }
    
    dkf = GITHD / "github_dorks.txt"
    with open(dkf, 'w') as f:
        f.write(f"GitHub Dorking Queries for {tgt}\n")
        f.write("="*70 + "\n\n")
        f.write("How to use these dorks:\n")
        f.write("1. Copy each query below\n")
        f.write("2. Paste into GitHub search bar (github.com/search)\n")
        f.write("3. Review code results for exposed credentials\n")
        f.write("4. Check commit history for removed secrets\n\n")
        f.write("="*70 + "\n\n")
        
        for cat, dk in gdk.items():
            print(f"  • {colored(cat, 'yellow')}: {colored(dk, 'cyan')}")
            f.write(f"{cat}:\n{dk}\n\n")
    
    print(f"\n{OK} All GitHub dorks saved to: {dkf}\n")
    
    print(colored("→ Automated Secret Scanning with Trufflehog", "yellow"))
    print(f"\n[{INF}] Trufflehog scans git repositories for high-entropy strings and secrets")
    print(f"{PROG} This can find credentials that were committed and later removed\n")
    
    if not shutil.which("trufflehog"):
        print(f"{WARN} Trufflehog is not installed")
        print(f"{PROG} Install with: pip install trufflehog OR use Docker")
        print(f"{PROG} Docker: docker run -it trufflesecurity/trufflehog:latest --help\n")
        
        itf = input(f"[{INF}] Try to install trufflehog via pip? (y/n): ").lower()
        if itf == 'y':
            cmd("pip3 install trufflehog", "Installing Trufflehog")
    
    if shutil.which("trufflehog"):
        orgn = input(f"[{INF}] Enter GitHub organization name (or press Enter to skip): ").strip()
        
        if orgn:
            print(f"\n{WARN} This scan may take 10-60 minutes depending on repository size")
            print(f"{PROG} Scanning all repositories in organization: {orgn}\n")
            
            tfo = GITHD / f"trufflehog_{orgn}.json"
            tfs = GITHD / f"trufflehog_{orgn}_summary.txt"
            
            cmd(
                f"trufflehog github --org={orgn} --json > {tfo} 2>&1",
                f"Scanning {orgn} organization for secrets"
            )
            
            if fex(str(tfo)):
                print(f"\n[{INF}] Parsing Trufflehog results...")
                
                try:
                    with open(tfo, 'r') as f:
                        finds = [json.loads(line) for line in f if line.strip()]
                    
                    stypes = {}
                    for find in finds:
                        det = find.get('DetectorName', 'Unknown')
                        stypes[det] = stypes.get(det, 0) + 1
                    
                    with open(tfs, 'w') as f:
                        f.write(f"Trufflehog Scan Summary for {orgn}\n")
                        f.write("="*70 + "\n\n")
                        f.write(f"Total Secrets Found: {len(finds)}\n\n")
                        f.write("Breakdown by Type:\n")
                        for st, cnt in sorted(stypes.items(), key=lambda x: x[1], reverse=True):
                            f.write(f"  • {st}: {cnt}\n")
                    
                    print(f"{OK} Found {colored(str(len(finds)), 'red' if len(finds) > 0 else 'green')} potential secrets")
                    print(f"{OK} Summary saved to: {tfs}\n")
                    
                    if len(finds) > 0:
                        print(f"{WARN} CRITICAL: Secrets detected in GitHub repositories!")
                        print(f"{WARN} These credentials should be rotated immediately\n")
                
                except Exception as e:
                    print(f"{WARN} Could not parse Trufflehog output: {str(e)}\n")
    
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} GitHub Secret Scanning Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Additional Recommendations:\n")
    print(f"  1. Check commit history for deleted secrets")
    print(f"  2. Search for organization members' personal repos")
    print(f"  3. Look for forked repositories with secrets")
    print(f"  4. Monitor GitHub for new commits with credentials")
    print(f"  5. Use GitHub's secret scanning alerts (if you own the org)\n")
    print(f"{PROG} All results saved to: {GITHD}\n")

def setupgf():
    gfd = Path.home() / ".gf"
    gfd.mkdir(exist_ok=True)
    
    if Path("GFPattern").exists():
        cmd(
            f"cp GFPattern/* {gfd}/",
            "Copying GF patterns for URL parameter filtering"
        )
        print(f"{OK} GF patterns configured\n")
    else:
        print(f"{WARN} GFPattern directory not found. You may need to clone:")
        print(f"        git clone https://github.com/1ndianl33t/Gf-Patterns GFPattern\n")

def genrep(tgt):
    repf = OUTD / f"REPORT_{tgt.replace('.', '_')}.txt"
    
    with open(repf, 'w') as f:
        f.write(f"DataDive Security Assessment Report\n")
        f.write(f"="*70 + "\n\n")
        f.write(f"Target: {tgt}\n")
        f.write(f"Scan Date: {tm.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"DataDive Version: {CV}\n\n")
        f.write(f"="*70 + "\n\n")
        
        f.write("1. SUBDOMAIN ENUMERATION\n")
        f.write("-" * 70 + "\n")
        if (SUBD / "all_subdomains.txt").exists():
            tots = lc(str(SUBD / "all_subdomains.txt"))
            als = lc(str(SUBD / "alive.txt"))
            f.write(f"Total Subdomains: {tots}\n")
            f.write(f"Live Subdomains: {als}\n")
            f.write(f"Coverage: {(als/tots*100 if tots > 0 else 0):.1f}%\n\n")
        
        f.write("2. OPEN REDIRECT VULNERABILITIES\n")
        f.write("-" * 70 + "\n")
        redf = 0
        for tf in REDD.glob("test_*.txt"):
            redf += lc(str(tf))
        f.write(f"Potential Findings: {redf}\n")
        f.write(f"Status: {'CRITICAL' if redf > 0 else 'CLEAR'}\n\n")
        
        f.write("3. SQL INJECTION TESTING\n")
        f.write("-" * 70 + "\n")
        if (SQLD / "nuclei_sqli_findings.txt").exists():
            sqlf = lc(str(SQLD / "nuclei_sqli_findings.txt"))
            f.write(f"Vulnerabilities Found: {sqlf}\n")
            f.write(f"Status: {'CRITICAL' if sqlf > 0 else 'CLEAR'}\n\n")
        
        f.write("4. S3 BUCKET EXPOSURE\n")
        f.write("-" * 70 + "\n")
        if (S3D / "s3_bucket_names.txt").exists():
            s3b = lc(str(S3D / "s3_bucket_names.txt"))
            f.write(f"Buckets Discovered: {s3b}\n")
            f.write(f"Status: {'REVIEW REQUIRED' if s3b > 0 else 'NONE FOUND'}\n\n")
        
        f.write("="*70 + "\n")
        f.write(f"Full results available in: {OUTD.absolute()}\n")
    
    print(f"{OK} Comprehensive report generated: {repf}\n")

def main():
    banner()
    mkdirs()
    
    printhdr("Dependency Verification")
    print(f"[{INF}] Checking required tools and dependencies...")
    print(f"{PROG} This ensures all reconnaissance tools are available\n")
    
    dpsok = True
    dpsok = instgo() and dpsok
    dpsok = instaws() and dpsok
    dpsok = chkuro() and dpsok
    dpsok = instjq() and dpsok
    
    if not dpsok:
        print(f"\n{WARN} Some dependencies failed to install")
        print(f"{WARN} Continuing anyway - some features may not work\n")
        input(f"Press Enter to continue...")
    
    tst = chktools()
    mtls = [t for t, inst in tst.items() if not inst]
    
    if mtls:
        print(f"\n{WARN} The following tools failed to install: {', '.join(mtls)}")
        print(f"{WARN} Some modules may not function correctly\n")
        cont = input(f"Continue anyway? (y/n): ").lower()
        if cont != 'y':
            print(f"{ERR} Exiting. Please install missing tools manually.")
            sys.exit(1)
    
    setupgf()
    
    print(f"\n{OK} All systems ready!")
    slp(2)
    
    printhdr("Target Configuration")
    tgt = input(f"[{INF}] Enter the target domain (e.g., example.com): ").strip()
    
    if not tgt:
        print(f"{ERR} No target specified. Exiting.")
        sys.exit(1)
    
    if tgt.startswith("http://") or tgt.startswith("https://"):
        tgt = tgt.split("://")[1].split("/")[0]
        print(f"{WARN} Cleaned target domain: {tgt}")
    
    print(f"\n{OK} Target set to: {colored(tgt, 'cyan', attrs=['bold'])}")
    print(f"{PROG} All results will be saved to: {OUTD.absolute()}\n")
    
    print(f"[{INF}] Select modules to run:\n")
    print(f"  1. Full Scan (All modules)")
    print(f"  2. Subdomain Enumeration Only")
    print(f"  3. Open Redirect Testing Only")
    print(f"  4. SQL Injection Testing Only")
    print(f"  5. S3 Bucket Discovery Only")
    print(f"  6. GitHub Secret Scanning Only")
    print(f"  7. Custom Selection\n")
    
    choice = input(f"[{INF}] Enter your choice (1-7): ").strip()
    
    mods = {
        'subdomain': False,
        'openredirect': False,
        'sqli': False,
        's3': False,
        'github': False
    }
    
    if choice == '1':
        mods = {k: True for k in mods}
        print(f"{OK} Running full scan on {tgt}\n")
    elif choice == '2':
        mods['subdomain'] = True
    elif choice == '3':
        mods['subdomain'] = True
        mods['openredirect'] = True
    elif choice == '4':
        mods['subdomain'] = True
        mods['sqli'] = True
    elif choice == '5':
        mods['subdomain'] = True
        mods['s3'] = True
    elif choice == '6':
        mods['github'] = True
    elif choice == '7':
        print(f"\n[{INF}] Select modules to run (y/n for each):\n")
        mods['subdomain'] = input("  Run Subdomain Enumeration? (y/n): ").lower() == 'y'
        mods['openredirect'] = input("  Run Open Redirect Testing? (y/n): ").lower() == 'y'
        mods['sqli'] = input("  Run SQL Injection Testing? (y/n): ").lower() == 'y'
        mods['s3'] = input("  Run S3 Bucket Discovery? (y/n): ").lower() == 'y'
        mods['github'] = input("  Run GitHub Secret Scanning? (y/n): ").lower() == 'y'
    else:
        print(f"{WARN} Invalid choice. Running full scan.")
        mods = {k: True for k in mods}
    
    if mods['openredirect'] or mods['sqli'] or mods['s3']:
        if not mods['subdomain']:
            print(f"\n{WARN} Selected modules require subdomain enumeration")
            mods['subdomain'] = True
    
    print(f"\n{OK} Scan configuration confirmed. Starting...\n")
    slp(2)
    
    startt = tm.time()
    sf = None
    
    try:
        if mods['subdomain']:
            sf = subenum(tgt)
        
        if mods['openredirect']:
            if sf:
                redtest(tgt, sf)
            else:
                print(f"{ERR} Skipping Open Redirect - no subdomains file")
        
        if mods['sqli']:
            if sf:
                wafbyp(tgt, sf)
            else:
                print(f"{ERR} Skipping SQLi Testing - no subdomains file")
        
        if mods['s3']:
            if sf:
                s3scan(tgt, sf)
            else:
                print(f"{ERR} Skipping S3 Scanning - no subdomains file")
        
        if mods['github']:
            githscan(tgt)
        
        genrep(tgt)
        
    except KeyboardInterrupt:
        print(f"\n\n{WARN} Scan interrupted by user")
        print(f"{PROG} Partial results saved to: {OUTD}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ERR} Unexpected error occurred: {str(e)}")
        print(f"{PROG} Partial results may be available in: {OUTD}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    elap = tm.time() - startt
    hrs, rem = divmod(elap, 3600)
    mins, secs = divmod(rem, 60)
    
    print(f"\n\n{'='*70}")
    print(f"{colored('SCAN COMPLETE!', 'green', attrs=['bold'])}")
    print(f"{'='*70}\n")
    print(f"[{INF}] Scan Statistics:")
    print(f"    • Target: {tgt}")
    print(f"    • Duration: {int(hrs)}h {int(mins)}m {int(secs)}s")
    print(f"    • Results: {OUTD.absolute()}")
    print(f"\n{OK} Review the generated report and individual module outputs")
    print(f"{PROG} Next steps:")
    print(f"    1. Verify all findings manually")
    print(f"    2. Prioritize critical vulnerabilities")
    print(f"    3. Document and report responsibly")
    print(f"    4. Follow coordinated disclosure practices\n")
    print(f"{WARN} Remember: This tool is for authorized testing only!")
    print(f"{WARN} Unauthorized access to systems is illegal.\n")

def welcome():
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{WARN} Operation cancelled by user")
        sys.exit(0)

if __name__ == "__main__":
    welcome()
