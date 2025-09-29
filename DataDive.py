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

# Enable line buffering for real-time output
sys.stdout.reconfigure(line_buffering=True)

# ========================================================================
# Configuration and Constants
# ========================================================================
LATEST_VERSION_URL = 'https://raw.githubusercontent.com/s-0-u-l-z/DataDive/refs/heads/DataDive-Main/version.txt'
CURRENT_VERSION = 2.01

# Color-coded status indicators
INF = colored("INF", "blue")
OK = colored("[OK]", "green")
ERR = colored("[ERR]", "red")
WARN = colored("[!]", "yellow")
PROGRESS = colored("[→]", "cyan")

# Output directories
OUTPUT_DIR = Path("datadive_output")
SUBDOMAINS_DIR = OUTPUT_DIR / "subdomains"
REDIRECT_DIR = OUTPUT_DIR / "open_redirects"
SQLI_DIR = OUTPUT_DIR / "sql_injection"
S3_DIR = OUTPUT_DIR / "s3_buckets"
GITHUB_DIR = OUTPUT_DIR / "github_secrets"

# ========================================================================
# Utility Functions
# ========================================================================

def sleep(seconds):
    """Wrapper for time.sleep for consistent usage"""
    tm.sleep(seconds)

def create_output_directories():
    """Create organized output directory structure"""
    directories = [OUTPUT_DIR, SUBDOMAINS_DIR, REDIRECT_DIR, SQLI_DIR, S3_DIR, GITHUB_DIR]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    print(f"{OK} Output directories created in: {OUTPUT_DIR.absolute()}")

def print_section_header(title):
    """Print a formatted section header"""
    print(f'\n\n{"="*70}')
    print(f'[{INF}] {title}')
    print(f'{"="*70}\n')
    sleep(1)

def command(cmd, description="", silent=False):
    """
    Execute shell commands with enhanced error handling and logging.
    
    Args:
        cmd (str): The shell command to execute
        description (str): Human-readable explanation of what the command does
        silent (bool): If True, suppress stdout (but still show errors)
    
    Returns:
        subprocess.CompletedProcess: The result of the command execution
    """
    if description and not silent:
        print(f"[{INF}] {description}")
        print(f"{PROGRESS} Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=300  # 5 minute timeout for long-running commands
        )
        
        if result.stdout and not silent:
            print(result.stdout)
        
        if result.stderr and result.returncode != 0:
            print(f"{ERR} Error executing command:")
            print(result.stderr)
        
        return result
        
    except subprocess.TimeoutExpired:
        print(f"{ERR} Command timed out after 5 minutes: {cmd}")
        return None
    except Exception as e:
        print(f"{ERR} Unexpected error: {str(e)}")
        return None

def get_line_count(file_path):
    """
    Count lines in a file efficiently.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        int: Number of lines in the file, or 0 if error
    """
    try:
        result = subprocess.run(['wc', '-l', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return int(result.stdout.strip().split()[0])
    except (ValueError, IndexError):
        pass
    return 0

def file_exists_and_not_empty(filepath):
    """Check if file exists and has content"""
    path = Path(filepath)
    return path.exists() and path.stat().st_size > 0

# ========================================================================
# Dependency Management
# ========================================================================

def detect_package_manager():
    """
    Auto-detect the system's package manager.
    
    Returns:
        str: Name of detected package manager or None
    """
    managers = {
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
    
    for manager, commands in managers.items():
        for cmd in commands:
            if shutil.which(cmd):
                return manager
    return None

def check_and_install_go():
    """Install Go programming language if not present"""
    if shutil.which("go") is not None:
        print(f"{OK} Go is already installed")
        return True
    
    print(f"{ERR} Go is not installed on your system.")
    print(f"{WARN} Go is required for installing reconnaissance tools.")
    
    pkg_manager = detect_package_manager()
    if not pkg_manager:
        all_pkg_managers = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
        print(f"{WARN} Could not auto-detect package manager.")
        print(f"{WARN} Please enter your package manager ({'/'.join(all_pkg_managers)}):")
        pkg_manager = input("Package manager: ").strip().lower()
    
    install_cmds = {
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
    
    if pkg_manager not in install_cmds:
        print(f"{ERR} Unsupported or unknown package manager: {pkg_manager}")
        return False
    
    print(f"[{INF}] Installing Go using {pkg_manager}...")
    os.system(install_cmds[pkg_manager])
    
    if shutil.which("go"):
        print(f"{OK} Go installation complete.")
        return True
    else:
        print(f"{ERR} Go installation failed. Please install manually.")
        return False

def check_and_install_aws():
    """Install AWS CLI if not present"""
    if shutil.which("aws") is not None:
        print(f"{OK} AWS CLI is already installed")
        return True
    
    print(f"{WARN} AWS CLI is not installed. This is needed for S3 bucket analysis.")
    
    pkg_manager = detect_package_manager()
    if not pkg_manager:
        pkg_manager = "apt"  # Default fallback
    
    install_aws = {
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
    
    if pkg_manager not in install_aws:
        print(f"{WARN} Cannot auto-install AWS CLI. Please install manually:")
        print(f"        https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html")
        return False
    
    print(f"[{INF}] Installing AWS CLI using {pkg_manager}")
    os.system(install_aws[pkg_manager])
    
    if shutil.which("aws"):
        print(f"{OK} AWS CLI installation complete.")
        return True
    else:
        print(f"{WARN} AWS CLI installation failed. Some S3 features may not work.")
        return False

def check_uro():
    """Check for uro (URL deduplication tool)"""
    if shutil.which("uro") is not None:
        print(f"{OK} uro is installed")
        return True
    
    print(f'{WARN} uro is not installed. This tool helps deduplicate URLs.')
    print(f'{WARN} Install it from: https://github.com/s0md3v/uro')
    print(f'{WARN} Or run: pip3 install uro')
    
    install = input(f"[{INF}] Try to install via pip3? (y/n): ").lower()
    if install == 'y':
        os.system("pip3 install uro")
        return shutil.which("uro") is not None
    return False

def check_jq():
    """Install jq (JSON processor) if not present"""
    if shutil.which("jq") is not None:
        print(f"{OK} jq is already installed")
        return True
    
    print(f'{ERR} jq is not installed. This tool is essential for processing JSON output.')
    
    pkg_manager = detect_package_manager()
    if not pkg_manager:
        all_pkg_managers = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
        print(f"{WARN} Please enter your package manager ({'/'.join(all_pkg_managers)}):")
        pkg_manager = input("Package manager: ").strip().lower()
    
    install_cmds = {
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
    
    if pkg_manager not in install_cmds:
        print(f"{ERR} Unsupported package manager: {pkg_manager}")
        return False
    
    print(f"[{INF}] Installing jq using {pkg_manager}...")
    os.system(install_cmds[pkg_manager])
    
    if shutil.which("jq"):
        print(f"{OK} jq installation complete.")
        return True
    else:
        print(f"{ERR} jq installation failed.")
        return False

def install_go_package(go_path):
    """
    Install a Go-based security tool.
    
    Args:
        go_path (str): The Go module path (e.g., github.com/user/tool@latest)
    """
    print(f"[{INF}] Installing {go_path}")
    command(f"go install {go_path}", f"Installing Go package {go_path}")

def check_go_tools():
    """
    Check and install all required Go-based reconnaissance tools.
    
    Returns:
        dict: Status of each tool (installed: bool)
    """
    go_tools = {
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
    
    tool_status = {}
    
    print(f"\n[{INF}] Checking required reconnaissance tools...")
    print(f"{PROGRESS} This may take a few minutes for first-time setup.\n")
    
    for binary, go_path in go_tools.items():
        path = shutil.which(binary)
        if path:
            print(f"{OK} {binary:20s} → Installed at {path}")
            tool_status[binary] = True
        else:
            print(f"{WARN} {binary:20s} → Not found, installing...")
            install_go_package(go_path)
            
            if shutil.which(binary):
                print(f"{OK} {binary:20s} → Successfully installed")
                tool_status[binary] = True
            else:
                print(f"{ERR} {binary:20s} → Installation failed")
                tool_status[binary] = False
    
    return tool_status

# ========================================================================
# Version Management
# ========================================================================

def check_version():
    """
    Check if DataDive is up to date.
    
    Returns:
        tuple: (current_version, latest_version, status_message)
    """
    try:
        response = requests.get(LATEST_VERSION_URL, timeout=5)
        latest_version = float(response.text.strip())
        
        if CURRENT_VERSION < latest_version:
            status = f"({colored('outdated', 'red')})"
            message = f"{WARN} A newer version (v{latest_version}) is available!"
        elif CURRENT_VERSION > latest_version:
            status = f"({colored('dev build', 'yellow')})"
            message = f"{WARN} You're running a development build"
        else:
            status = f"({colored('latest', 'green')})"
            message = f"{OK} You're running the latest version"
        
        return CURRENT_VERSION, latest_version, status, message
    except Exception as e:
        status = f"({colored('unknown', 'yellow')})"
        message = f"{WARN} Could not check for updates: {str(e)}"
        return CURRENT_VERSION, None, status, message

def print_banner():
    """Display the DataDive banner with version information"""
    current, latest, status, message = check_version()
    
    banner = f"""
        ██████╗░░█████╗░████████╗░█████╗░██████╗░██╗██╗░░░██╗███████╗
        ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
        ██║░░██║███████║░░░██║░░░███████║██║░░██║██║╚██╗░██╔╝█████╗░░
        ██║░░██║██╔══██║░░░██║░░░██╔══██║██║░░██║██║░╚████╔╝░██╔══╝░░
        ██████╔╝██║░░██║░░░╚═══╝░░██║░░██║██████╔╝██║░░╚██╔╝░░███████╗
        ╚═════╝░╚═╝░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚══════╝

                            By s0ulz
                Advanced Security Reconnaissance Framework

    [{INF}] Current version: v{current} {status}
    {message}
    """
    
    for line in banner.split('\n'):
        print(line)
    
    sleep(1)

# ========================================================================
# Subdomain Enumeration Module
# ========================================================================

def subdomain_enumeration(target):
    """
    Comprehensive subdomain discovery using multiple tools.
    
    This module combines results from:
    - Subfinder: Fast passive subdomain discovery
    - Assetfinder: Additional subdomain sources
    - Amass: In-depth reconnaissance (rate-limited)
    
    Args:
        target (str): The target domain to scan
    
    Returns:
        str: Path to the combined subdomains file
    """
    print_section_header("Subdomain Enumeration & Discovery")
    
    print(f"[{INF}] Target domain: {colored(target, 'cyan')}")
    print(f"[{INF}] This process discovers all subdomains associated with the target")
    print(f"{PROGRESS} Using multiple data sources for comprehensive coverage\n")
    sleep(2)
    
    # Create subdomain-specific output files
    subfinder_out = SUBDOMAINS_DIR / "subfinder.txt"
    assetfinder_out = SUBDOMAINS_DIR / "assetfinder.txt"
    amass_out = SUBDOMAINS_DIR / "amass.txt"
    combined_out = SUBDOMAINS_DIR / "all_subdomains.txt"
    alive_out = SUBDOMAINS_DIR / "alive.txt"
    status_codes_out = SUBDOMAINS_DIR / "status_codes.txt"
    
    # Subfinder - Fast and reliable
    print(colored("→ Running Subfinder", "yellow"))
    print(f"{PROGRESS} Subfinder queries multiple sources (crt.sh, VirusTotal, etc.)")
    command(
        f'subfinder -d {target} -all -silent >> {subfinder_out}',
        f'Discovering subdomains for {target} using all available sources'
    )
    subfinder_count = get_line_count(str(subfinder_out))
    print(f"{OK} Subfinder found {subfinder_count} subdomains\n")
    sleep(1)
    
    # Assetfinder - Additional coverage
    print(colored("→ Running Assetfinder", "yellow"))
    print(f"{PROGRESS} Assetfinder finds related assets and subdomains")
    command(
        f'assetfinder --subs-only {target} >> {assetfinder_out}',
        f'Finding related subdomains using Assetfinder'
    )
    assetfinder_count = get_line_count(str(assetfinder_out))
    print(f"{OK} Assetfinder found {assetfinder_count} subdomains\n")
    sleep(1)
    
    # Amass - Thorough but slower
    print(colored("→ Running Amass (30s timeout)", "yellow"))
    print(f"{PROGRESS} Amass performs deep DNS enumeration")
    print(f"{WARN} Timeout set to prevent excessive runtime")
    command(
        f'amass enum -timeout 30 -norecursive -d {target} >> {amass_out}',
        f'Running Amass enumeration with controlled timeout'
    )
    amass_count = get_line_count(str(amass_out))
    print(f"{OK} Amass found {amass_count} subdomains\n")
    sleep(1)
    
    # Combine and deduplicate results
    print(f"[{INF}] Merging results from all tools...")
    command(
        f"sort -u {subfinder_out} {assetfinder_out} {amass_out} > {combined_out}",
        'Combining and deduplicating subdomains from all sources'
    )
    total_count = get_line_count(str(combined_out))
    print(f"{OK} Total unique subdomains discovered: {colored(str(total_count), 'green', attrs=['bold'])}\n")
    
    # Probe for live hosts
    print(colored("→ Probing for live subdomains with httpx", "yellow"))
    print(f"{PROGRESS} This checks which subdomains are actually responding")
    
    if total_count >= 500:
        print(f"{WARN} Large subdomain list detected, using 50 threads for faster scanning")
        command(
            f"httpx -l {combined_out} -o {alive_out} -t 50 -silent",
            'Checking subdomain availability with increased concurrency'
        )
    else:
        command(
            f"httpx -l {combined_out} -o {alive_out} -silent",
            'Checking which subdomains are live and responding'
        )
    
    alive_count = get_line_count(str(alive_out))
    print(f"{OK} Live subdomains: {colored(str(alive_count), 'green', attrs=['bold'])} out of {total_count}")
    print(f"{OK} Results saved to: {alive_out}\n")
    
    # Get status codes for analysis
    print(f"[{INF}] Collecting HTTP status codes...")
    command(
        f'httpx -l {combined_out} -sc -silent >> {status_codes_out}',
        'Retrieving HTTP status codes for all subdomains'
    )
    
    # Extract 200 OK responses
    ok_responses_out = SUBDOMAINS_DIR / "200_ok.txt"
    command(
        f"cat {status_codes_out} | grep '\\[200\\]' >> {ok_responses_out}",
        'Filtering for successful (200 OK) responses'
    )
    ok_count = get_line_count(str(ok_responses_out))
    print(f"{OK} Subdomains with 200 OK status: {ok_count}\n")
    
    # Subdomain takeover checks
    print_section_header("Subdomain Takeover Detection")
    print(f"{PROGRESS} Checking for vulnerable subdomain configurations...")
    
    subjack_out = SUBDOMAINS_DIR / "subjack_results.txt"
    command(
        f"subjack -w {combined_out} -t 100 -ssl -v -o {subjack_out}",
        'Running Subjack to detect potential subdomain takeovers'
    )
    
    nuclei_takeover_out = SUBDOMAINS_DIR / "nuclei_takeover.txt"
    command(
        f"nuclei -l {combined_out} -t ~/nuclei-templates/takeovers/ -silent >> {nuclei_takeover_out}",
        'Using Nuclei templates to detect takeover vulnerabilities'
    )
    print(f"{OK} Takeover check results saved to: {SUBDOMAINS_DIR}\n")
    
    # Deep crawling with Katana
    print_section_header("Deep Web Crawling")
    print(f"{PROGRESS} Crawling live subdomains to discover hidden content...")
    
    katana_js_out = SUBDOMAINS_DIR / "katana_js.txt"
    katana_deep_out = SUBDOMAINS_DIR / "katana_deep.txt"
    
    command(
        f"katana -list {alive_out} -jc -silent -o {katana_js_out}",
        'Extracting JavaScript files from live subdomains'
    )
    
    command(
        f"katana -list {alive_out} -d 5 -ef woff,css,png,svg,jpg,woff2,jpeg,gif,ico -silent -o {katana_deep_out}",
        'Performing deep crawl (depth=5) to discover all URLs'
    )
    
    js_count = get_line_count(str(katana_js_out))
    deep_count = get_line_count(str(katana_deep_out))
    print(f"{OK} JavaScript files discovered: {js_count}")
    print(f"{OK} Total URLs discovered: {deep_count}\n")
    
    return str(combined_out)

# ========================================================================
# Open Redirect Module
# ========================================================================

def open_redirect_testing(target, subdomains_file):
    """
    Test for open redirect vulnerabilities using multiple methods.
    
    Open redirects can be used for phishing and bypassing security controls.
    This module tests for them using:
    - URL parameter fuzzing
    - Historical URL analysis
    - Pattern matching for redirect parameters
    
    Args:
        target (str): The target domain
        subdomains_file (str): Path to discovered subdomains
    """
    print_section_header("Open Redirect Vulnerability Detection")
    
    print(f"[{INF}] Open redirects allow attackers to redirect users to malicious sites")
    print(f"{PROGRESS} Testing {colored(target, 'cyan')} for redirect vulnerabilities\n")
    sleep(2)
    
    # URL collection from multiple sources
    print(colored("→ Phase 1: URL Collection", "yellow"))
    print(f"{PROGRESS} Gathering URLs from Wayback Machine and crawlers...\n")
    
    gau_out = REDIRECT_DIR / "gau_urls.txt"
    katana_out = REDIRECT_DIR / "katana_urls.txt"
    urlfinder_out = REDIRECT_DIR / "urlfinder_urls.txt"
    hakrawler_out = REDIRECT_DIR / "hakrawler_urls.txt"
    
    command(
        f"cat {subdomains_file} | gau --o {gau_out}",
        'Fetching historical URLs from Wayback Machine and CommonCrawl'
    )
    
    command(
        f"cat {SUBDOMAINS_DIR / 'alive.txt'} | katana -d 2 -silent -o {katana_out}",
        'Crawling live sites for URLs with redirect parameters'
    )
    
    command(
        f"cat {SUBDOMAINS_DIR / 'alive.txt'} | hakrawler -d 2 -silent > {hakrawler_out}",
        'Using Hakrawler for additional URL discovery'
    )
    
    # Combine all URLs
    combined_urls = REDIRECT_DIR / "all_redirect_urls.txt"
    command(
        f"cat {gau_out} {katana_out} {hakrawler_out} | uro | sort -u > {combined_urls}",
        'Normalizing and deduplicating all discovered URLs'
    )
    
    url_count = get_line_count(str(combined_urls))
    print(f"{OK} Total URLs collected: {url_count}\n")
    
    # Filter for redirect parameters
    print(colored("→ Phase 2: Redirect Parameter Detection", "yellow"))
    print(f"{PROGRESS} Filtering URLs with common redirect parameter names...\n")
    
    redirect_params_out = REDIRECT_DIR / "redirect_params.txt"
    redirect_regex = "returnUrl=|continue=|dest=|destination=|forward=|go=|goto=|login\\?to=|next=|next_page=|out=|redir=|redirect=|redirect_to=|redirect_uri=|return=|returnTo=|return_url=|url=|qurl=|jump=|originUrl=|Url=|location=|ReturnUrl="
    
    command(
        f"cat {combined_urls} | grep -Pi '{redirect_regex}' > {redirect_params_out}",
        'Extracting URLs with potential redirect parameters'
    )
    
    redirect_count = get_line_count(str(redirect_params_out))
    print(f"{OK} URLs with redirect parameters: {redirect_count}\n")
    
    if redirect_count == 0:
        print(f"{WARN} No redirect parameters found. Skipping payload injection.")
        return
    
    # Test redirect parameters
    print(colored("→ Phase 3: Payload Injection & Testing", "yellow"))
    print(f"{PROGRESS} Injecting test payloads to detect open redirects...\n")
    
    # Method 1: Simple evil.com injection
    test1_out = REDIRECT_DIR / "test_method1.txt"
    command(
        f"cat {redirect_params_out} | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com' >> {test1_out}",
        'Testing Method 1: Direct payload injection with httpx validation'
    )
    
    # Method 2: Curl with redirect tracking
    test2_out = REDIRECT_DIR / "test_method2.txt"
    command(
        r'cat ' + str(redirect_params_out) + r' | qsreplace "https://evil.com" | xargs -I {} curl -s -o /dev/null -w "%{url_effective} -> %{redirect_url}\n" {} >> ' + str(test2_out),
        'Testing Method 2: Using curl to track redirect chains'
    )
    
    # Method 3: Nuclei scanning
    test3_out = REDIRECT_DIR / "nuclei_openredirect.txt"
    command(
        f"nuclei -l {SUBDOMAINS_DIR / 'alive.txt'} -t ~/nuclei-templates/http/vulnerabilities/open-redirect/ -silent -c 45 >> {test3_out}",
        'Testing Method 3: Nuclei template-based detection'
    )
    
    # Advanced testing with custom payloads
    print(f"\n[{INF}] Advanced Payload Testing")
    print(f"{PROGRESS} Using comprehensive payload list...\n")
    
    # Create sample payload file if it doesn't exist
    payload_dir = Path("payloads")
    payload_dir.mkdir(exist_ok=True)
    payload_file = payload_dir / "openredirect.txt"
    
    if not payload_file.exists():
        sample_payloads = [
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
        with open(payload_file, 'w') as f:
            f.write('\n'.join(sample_payloads))
        print(f"{OK} Created sample payload file at {payload_file}")
    
    test4_out = REDIRECT_DIR / "test_advanced.txt"
    if payload_file.exists():
        command(
            f'cat {redirect_params_out} | head -50 | while read url; do cat {payload_file} | while read payload; do echo "$url" | qsreplace "$payload"; done; done | httpx -silent -fr -mc 301,302 >> {test4_out}',
            'Testing with advanced payload list (limited to first 50 URLs to prevent timeout)'
        )
    
    # Results summary
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} Open Redirect Testing Complete!")
    print(f"{colored('='*70, 'green')}\n")
    
    print(f"[{INF}] Results Summary:")
    print(f"    • Method 1 (httpx): {get_line_count(str(test1_out))} potential findings")
    print(f"    • Method 2 (curl): {get_line_count(str(test2_out))} redirect chains")
    print(f"    • Method 3 (Nuclei): {get_line_count(str(test3_out))} validated vulnerabilities")
    print(f"    • Method 4 (Advanced): {get_line_count(str(test4_out))} additional findings")
    print(f"\n{PROGRESS} All results saved to: {REDIRECT_DIR}\n")
    
    print(f"{WARN} Manual verification recommended for all findings")
    print(f"{WARN} False positives are common - verify in browser\n")

# ========================================================================
# WAF Bypass & SQL Injection Module
# ========================================================================

def waf_bypass_and_sqli(target, subdomains_file):
    """
    Advanced WAF bypass techniques and SQL injection testing.
    
    This module demonstrates:
    - ProxyChains setup for IP rotation
    - SQLMap with tamper scripts
    - Mass SQL injection hunting
    
    Args:
        target (str): The target domain
        subdomains_file (str): Path to discovered subdomains
    """
    print_section_header("WAF Bypass & SQL Injection Testing")
    
    print(f"[{INF}] Web Application Firewalls (WAFs) block malicious requests")
    print(f"{PROGRESS} We'll use IP rotation and payload obfuscation to bypass them\n")
    sleep(2)
    
    # ProxyChains setup guide
    print(colored("→ ProxyChains Configuration", "yellow"))
    print(f"\n{WARN} IMPORTANT: ProxyChains Setup Required\n")
    print("ProxyChains routes your traffic through proxy servers to:")
    print("  • Evade IP-based rate limiting")
    print("  • Bypass geographic restrictions")
    print("  • Avoid IP blacklisting")
    print("\nSetup Instructions:")
    print(f"{PROGRESS} 1. Edit configuration: sudo nano /etc/proxychains.conf")
    print(f"{PROGRESS} 2. Comment out: #socks4 127.0.0.1 9050")
    print(f"{PROGRESS} 3. Enable: random_chain (uncomment)")
    print(f"{PROGRESS} 4. Add proxies (get free ones from https://www.sslproxies.org/):")
    print("       http <ip> <port> <username> <password>")
    print("       Example: http 192.168.1.1 8080")
    print(f"{PROGRESS} 5. Optional: Enable quiet_mode to reduce logs\n")
    
    ready = input(f"[{INF}] Have you configured ProxyChains? (y/n): ").lower()
    
    if ready == 'y':
        print(f"\n[{INF}] Testing ProxyChains configuration...")
        print(colored("Testing IP rotation...", "yellow"))
        
        # Test ProxyChains
        print(f"\n{PROGRESS} Test 1: Check current IP")
        command("proxychains curl -s http://ipinfo.io/ip", "Fetching IP through ProxyChains")
        
        print(f"\n{PROGRESS} Test 2: Verify IP rotation")
        command("proxychains curl -s http://ipinfo.io/ip", "Fetching IP again to verify rotation")
        
        print(f"\n{OK} If you see different IPs above, ProxyChains is working!\n")
        sleep(2)
    else:
        print(f"{WARN} ProxyChains not configured. Continuing without IP rotation...")
        print(f"{WARN} WAF bypass effectiveness will be limited\n")
        sleep(2)
    
    # SQLMap testing
    print(colored("→ SQLMap with WAF Bypass", "yellow"))
    print(f"\n[{INF}] SQLMap is an automated SQL injection tool")
    print(f"{PROGRESS} We'll combine it with ProxyChains and tamper scripts\n")
    
    sqlmap_target = input(f"[{INF}] Enter URL for SQLMap testing (or press Enter to skip): ").strip()
    
    if sqlmap_target:
        print(f"\n[{INF}] Launching SQLMap with bypass techniques...")
        print(f"{WARN} This may take 10-30 minutes depending on the target\n")
        
        sqlmap_out = SQLI_DIR / "sqlmap_results.txt"
        sqlmap_cmd = f"sqlmap -u '{sqlmap_target}' --dbs --batch --random-agent --tamper=between,space2comment --level=5 --risk=3 --threads=10 2>&1 | tee {sqlmap_out}"
        
        if ready == 'y':
            sqlmap_cmd = "proxychains " + sqlmap_cmd
            print(f"{PROGRESS} Using ProxyChains for IP rotation")
        
        print(f"\n{PROGRESS} Command breakdown:")
        print("  --dbs: Enumerate databases")
        print("  --batch: Non-interactive mode")
        print("  --random-agent: Rotate User-Agent headers")
        print("  --tamper=between,space2comment: Obfuscate payloads")
        print("  --level=5 --risk=3: Maximum testing depth")
        print("  --threads=10: Concurrent requests\n")
        
        command(sqlmap_cmd, "Running SQLMap with WAF bypass techniques")
        print(f"\n{OK} SQLMap results saved to: {sqlmap_out}\n")
    
    # Mass SQL injection hunting
    print_section_header("Mass SQL Injection Discovery")
    print(f"{PROGRESS} Scaling SQLi detection across all discovered subdomains...\n")
    
    # Extract unique domains
    print(f"[{INF}] Step 1: Extracting unique domains...")
    unique_domains = SQLI_DIR / "unique_domains.txt"
    command(
        f"cat {SUBDOMAINS_DIR / 'alive.txt'} | awk -F/ '{{print $3}}' | sort -u > {unique_domains}",
        "Extracting hostnames from live URLs"
    )
    domain_count = get_line_count(str(unique_domains))
    print(f"{OK} Extracted {domain_count} unique domains\n")
    
    # Gather SQLi parameter URLs
    print(f"[{INF}] Step 2: Collecting URLs with SQL parameters...")
    sqli_urls_raw = SQLI_DIR / "sqli_urls_raw.txt"
    command(
        f"cat {unique_domains} | waybackurls | gf sqli | uro > {sqli_urls_raw}",
        "Using waybackurls + GF patterns to find potential SQLi points"
    )
    raw_count = get_line_count(str(sqli_urls_raw))
    print(f"{OK} Found {raw_count} URLs with SQL-like parameters\n")
    
    if raw_count == 0:
        print(f"{WARN} No SQL parameter URLs found. Skipping SQLi testing.")
        return
    
    # Deduplicate by domain
    print(f"[{INF}] Step 3: Deduplicating URLs (one per domain)...")
    sqli_urls_filtered = SQLI_DIR / "sqli_urls_filtered.txt"
    command(
        f"cat {sqli_urls_raw} | awk -F/ '{{if (!seen[$3]++) print}}' > {sqli_urls_filtered}",
        "Keeping only one URL per unique domain to prevent redundant scanning"
    )
    filtered_count = get_line_count(str(sqli_urls_filtered))
    print(f"{OK} Reduced to {filtered_count} unique targets\n")
    
    # Scan with Nuclei
    print(f"[{INF}] Step 4: Scanning with Nuclei DAST templates...")
    print(f"{PROGRESS} This actively tests for SQL injection vulnerabilities\n")
    
    nuclei_sqli_out = SQLI_DIR / "nuclei_sqli_findings.txt"
    command(
        f"nuclei -l {sqli_urls_filtered} -t ~/nuclei-templates/http/vulnerabilities/sqli/ -c 30 -silent >> {nuclei_sqli_out}",
        "Running Nuclei SQL injection detection templates"
    )
    
    findings = get_line_count(str(nuclei_sqli_out))
    
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} SQL Injection Testing Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Findings Summary:")
    print(f"    • URLs tested: {filtered_count}")
    print(f"    • Vulnerabilities found: {colored(str(findings), 'red' if findings > 0 else 'green')}")
    print(f"    • Results saved to: {SQLI_DIR}\n")
    
    if findings > 0:
        print(f"{WARN} CRITICAL: SQL injection vulnerabilities detected!")
        print(f"{WARN} Review {nuclei_sqli_out} immediately\n")

# ========================================================================
# S3 Bucket Discovery Module
# ========================================================================

def s3_bucket_scanning(target, subdomains_file):
    """
    Discover and analyze AWS S3 bucket misconfigurations.
    
    Misconfigured S3 buckets can expose:
    - Sensitive files and backups
    - API keys and credentials
    - Customer data
    - Internal documentation
    
    Args:
        target (str): The target domain
        subdomains_file (str): Path to discovered subdomains
    """
    print_section_header("AWS S3 Bucket Discovery & Analysis")
    
    print(f"[{INF}] Searching for exposed Amazon S3 buckets associated with {colored(target, 'cyan')}")
    print(f"{PROGRESS} S3 misconfigurations are a common source of data breaches\n")
    sleep(2)
    
    # Direct S3 detection
    print(colored("→ Method 1: Direct S3 Detection", "yellow"))
    s3_direct_out = S3_DIR / "s3_direct_findings.txt"
    
    command(
        f"subfinder -d {target} -all -silent | httpx -silent -sc -title -td | grep -i 's3\\|amazon' >> {s3_direct_out}",
        "Scanning subdomains for direct S3 service indicators"
    )
    
    command(
        f"nuclei -l {subdomains_file} -t ~/nuclei-templates/http/technologies/s3-detect.yaml -silent >> {s3_direct_out}",
        "Using Nuclei to detect S3 bucket patterns"
    )
    
    direct_findings = get_line_count(str(s3_direct_out))
    print(f"{OK} Direct S3 detections: {direct_findings}\n")
    
    # JavaScript file analysis
    print(colored("→ Method 2: JavaScript File Analysis", "yellow"))
    print(f"{PROGRESS} Extracting S3 URLs from JavaScript files...\n")
    
    alljs_file = S3_DIR / "all_javascript.txt"
    
    # Collect JS files
    command(
        f"katana -u {target} -d 5 -jc -silent | grep '\\.js > {alljs_file}",
        "Crawling for JavaScript files (depth=5)"
    )
    
    command(
        f"echo {target} | gau | grep '\\.js | anew {alljs_file}",
        "Adding historical JS files from Wayback Machine"
    )
    
    # Check JS files are alive
    js_alive = S3_DIR / "js_alive.txt"
    command(
        f"cat {alljs_file} | uro | sort -u | httpx -silent -mc 200 -o {js_alive}",
        "Verifying which JS files are accessible"
    )
    
    js_count = get_line_count(str(js_alive))
    print(f"{OK} Live JavaScript files: {js_count}\n")
    
    # Extract S3 URLs from JS
    s3_from_js = S3_DIR / "s3_urls_from_js.txt"
    if js_count > 0:
        command(
            f'cat {js_alive} | xargs -I {{}} curl -s {{}} | grep -oE "(https?://[^/]*\\.s3[^/]*\\.amazonaws\\.com[^\\s\\"\\'<>]*)" | sort -u >> {s3_from_js}',
            "Extracting S3 bucket URLs from JavaScript content"
        )
        
        js_s3_count = get_line_count(str(s3_from_js))
        print(f"{OK} S3 URLs found in JavaScript: {js_s3_count}\n")
    
    # Google dorking guide
    print(colored("→ Method 3: Manual Google Dorking", "yellow"))
    print(f"\n{WARN} Perform these Google searches manually:\n")
    
    google_dorks = [
        f'site:s3.amazonaws.com "{target}"',
        f'site:*.s3.amazonaws.com "{target}"',
        f'(site:*.s3.amazonaws.com OR site:*.s3-external-1.amazonaws.com) "{target}"',
        f'inurl:s3.amazonaws.com intitle:index.of.bucket "{target}"'
    ]
    
    dorks_file = S3_DIR / "google_dorks.txt"
    with open(dorks_file, 'w') as f:
        f.write("Google Dorking Queries for S3 Bucket Discovery\n")
        f.write("="*70 + "\n\n")
        for i, dork in enumerate(google_dorks, 1):
            print(f"  {i}. {colored(dork, 'cyan')}")
            f.write(f"{i}. {dork}\n")
    
    print(f"\n{OK} Dorks saved to: {dorks_file}")
    print(f"{PROGRESS} Look for 'Access Denied' (private) vs. file listings (exposed)\n")
    
    # Extract S3 bucket names
    print(colored("→ Method 4: Bucket Name Extraction", "yellow"))
    print(f"{PROGRESS} Compiling list of discovered S3 buckets...\n")
    
    s3_hostnames = S3_DIR / "s3_bucket_names.txt"
    s3_full_urls = S3_DIR / "s3_full_urls.txt"
    
    # Combine all S3 findings
    all_s3_sources = [s3_direct_out, s3_from_js]
    combined_s3 = S3_DIR / "all_s3_references.txt"
    
    command(
        f"cat {' '.join(str(f) for f in all_s3_sources if Path(f).exists())} | sort -u > {combined_s3}",
        "Combining all S3 references from different sources"
    )
    
    # Extract bucket hostnames
    command(
        f"cat {combined_s3} | grep -oP '([a-zA-Z0-9.-]*\\.s3[^/]*\\.amazonaws\\.com)' | sort -u > {s3_hostnames}",
        "Extracting S3 bucket hostnames"
    )
    
    # Extract full URLs
    command(
        f"cat {combined_s3} | grep -oP 'https?://[^\\s\"<>]*s3[^\\s\"<>]*amazonaws\\.com[^\\s\"<>]*' | sort -u > {s3_full_urls}",
        "Extracting complete S3 URLs with paths"
    )
    
    bucket_count = get_line_count(str(s3_hostnames))
    url_count = get_line_count(str(s3_full_urls))
    
    print(f"{OK} Unique S3 buckets discovered: {bucket_count}")
    print(f"{OK} Total S3 URLs (with paths): {url_count}\n")
    
    # Permission checking
    if bucket_count > 0:
        print(colored("→ Method 5: Permission Analysis", "yellow"))
        print(f"{PROGRESS} Checking bucket permissions (requires AWS CLI)...\n")
        
        s3_permissions = S3_DIR / "s3_permissions.txt"
        
        # Check if AWS CLI is available
        if shutil.which("aws"):
            print(f"[{INF}] Testing bucket access permissions...")
            command(
                f"cat {s3_hostnames} | while read bucket; do echo \"Testing: $bucket\"; aws s3 ls s3://$bucket --no-sign-request 2>&1; done >> {s3_permissions}",
                "Attempting anonymous access to discovered buckets"
            )
            print(f"{OK} Permission check complete. Review {s3_permissions}\n")
        else:
            print(f"{WARN} AWS CLI not installed. Skipping permission checks.")
            print(f"{WARN} Install with: pip install awscli\n")
    
    # Results summary
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} S3 Bucket Scanning Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Discovery Summary:")
    print(f"    • Direct detections: {direct_findings}")
    print(f"    • Buckets from JS files: {js_s3_count if js_count > 0 else 0}")
    print(f"    • Total unique buckets: {bucket_count}")
    print(f"    • All results saved to: {S3_DIR}\n")
    
    if bucket_count > 0:
        print(f"{WARN} Next Steps:")
        print(f"    1. Review {s3_hostnames} for bucket names")
        print(f"    2. Check {s3_permissions} for access levels")
        print(f"    3. Test buckets manually: aws s3 ls s3://bucket-name")
        print(f"    4. Look for sensitive files: backups, configs, credentials\n")

# ========================================================================
# GitHub Secrets Module
# ========================================================================

def github_secret_scanning(target):
    """
    Discover leaked credentials and secrets in GitHub repositories.
    
    Developers often accidentally commit:
    - API keys and tokens
    - Database credentials
    - AWS access keys
    - Private keys and certificates
    
    Args:
        target (str): The target domain or organization
    """
    print_section_header("GitHub Secret & Credential Discovery")
    
    print(f"[{INF}] Searching for exposed secrets related to {colored(target, 'cyan')}")
    print(f"{PROGRESS} Public GitHub repositories are a goldmine for credentials\n")
    sleep(2)
    
    # Generate GitHub dorks
    print(colored("→ GitHub Dorking Queries", "yellow"))
    print(f"\n{WARN} Perform these searches on GitHub.com manually:\n")
    
    github_dorks = {
        "Passwords": f'"{target}" password',
        "API Keys (JSON)": f'"{target}" password extension:json',
        "Environment Files": f'org:{target} path:.env',
        "AWS Credentials": f'org:{target} "aws_access_key_id" OR "aws_secret_access_key"',
        "Generic Secrets": f'org:{target} "api_key" OR "secret_key" OR "client_secret"',
        "Database Credentials": f'"{target}" "database" "password" extension:yml',
        "Private Keys": f'org:{target} "BEGIN RSA PRIVATE KEY" OR "BEGIN PRIVATE KEY"',
        "Tokens": f'"{target}" "token" extension:txt',
        "Configuration Files": f'org:{target} filename:config.json OR filename:settings.json'
    }
    
    dorks_file = GITHUB_DIR / "github_dorks.txt"
    with open(dorks_file, 'w') as f:
        f.write(f"GitHub Dorking Queries for {target}\n")
        f.write("="*70 + "\n\n")
        f.write("How to use these dorks:\n")
        f.write("1. Copy each query below\n")
        f.write("2. Paste into GitHub search bar (github.com/search)\n")
        f.write("3. Review code results for exposed credentials\n")
        f.write("4. Check commit history for removed secrets\n\n")
        f.write("="*70 + "\n\n")
        
        for category, dork in github_dorks.items():
            print(f"  • {colored(category, 'yellow')}: {colored(dork, 'cyan')}")
            f.write(f"{category}:\n{dork}\n\n")
    
    print(f"\n{OK} All GitHub dorks saved to: {dorks_file}\n")
    
    # Trufflehog integration
    print(colored("→ Automated Secret Scanning with Trufflehog", "yellow"))
    print(f"\n[{INF}] Trufflehog scans git repositories for high-entropy strings and secrets")
    print(f"{PROGRESS} This can find credentials that were committed and later removed\n")
    
    if not shutil.which("trufflehog"):
        print(f"{WARN} Trufflehog is not installed")
        print(f"{PROGRESS} Install with: pip install trufflehog OR use Docker")
        print(f"{PROGRESS} Docker: docker run -it trufflesecurity/trufflehog:latest --help\n")
        
        install_tf = input(f"[{INF}] Try to install trufflehog via pip? (y/n): ").lower()
        if install_tf == 'y':
            command("pip3 install trufflehog", "Installing Trufflehog")
    
    if shutil.which("trufflehog"):
        org_name = input(f"[{INF}] Enter GitHub organization name (or press Enter to skip): ").strip()
        
        if org_name:
            print(f"\n{WARN} This scan may take 10-60 minutes depending on repository size")
            print(f"{PROGRESS} Scanning all repositories in organization: {org_name}\n")
            
            trufflehog_out = GITHUB_DIR / f"trufflehog_{org_name}.json"
            trufflehog_summary = GITHUB_DIR / f"trufflehog_{org_name}_summary.txt"
            
            command(
                f"trufflehog github --org={org_name} --json > {trufflehog_out} 2>&1",
                f"Scanning {org_name} organization for secrets"
            )
            
            # Parse results
            if file_exists_and_not_empty(str(trufflehog_out)):
                print(f"\n[{INF}] Parsing Trufflehog results...")
                
                try:
                    with open(trufflehog_out, 'r') as f:
                        findings = [json.loads(line) for line in f if line.strip()]
                    
                    # Summarize findings
                    secret_types = {}
                    for finding in findings:
                        detector = finding.get('DetectorName', 'Unknown')
                        secret_types[detector] = secret_types.get(detector, 0) + 1
                    
                    with open(trufflehog_summary, 'w') as f:
                        f.write(f"Trufflehog Scan Summary for {org_name}\n")
                        f.write("="*70 + "\n\n")
                        f.write(f"Total Secrets Found: {len(findings)}\n\n")
                        f.write("Breakdown by Type:\n")
                        for secret_type, count in sorted(secret_types.items(), key=lambda x: x[1], reverse=True):
                            f.write(f"  • {secret_type}: {count}\n")
                    
                    print(f"{OK} Found {colored(str(len(findings)), 'red' if len(findings) > 0 else 'green')} potential secrets")
                    print(f"{OK} Summary saved to: {trufflehog_summary}\n")
                    
                    if len(findings) > 0:
                        print(f"{WARN} CRITICAL: Secrets detected in GitHub repositories!")
                        print(f"{WARN} These credentials should be rotated immediately\n")
                
                except Exception as e:
                    print(f"{WARN} Could not parse Trufflehog output: {str(e)}\n")
    
    # Additional recommendations
    print(f"\n{colored('='*70, 'green')}")
    print(f"{OK} GitHub Secret Scanning Complete!")
    print(f"{colored('='*70, 'green')}\n")
    print(f"[{INF}] Additional Recommendations:\n")
    print(f"  1. Check commit history for deleted secrets")
    print(f"  2. Search for organization members' personal repos")
    print(f"  3. Look for forked repositories with secrets")
    print(f"  4. Monitor GitHub for new commits with credentials")
    print(f"  5. Use GitHub's secret scanning alerts (if you own the org)\n")
    print(f"{PROGRESS} All results saved to: {GITHUB_DIR}\n")

# ========================================================================
# Main Execution Flow
# ========================================================================

def setup_gf_patterns():
    """Setup GF (grep patterns) for parameter discovery"""
    gf_dir = Path.home() / ".gf"
    gf_dir.mkdir(exist_ok=True)
    
    # Check if GF patterns exist locally
    if Path("GFPattern").exists():
        command(
            f"cp GFPattern/* {gf_dir}/",
            "Copying GF patterns for URL parameter filtering"
        )
        print(f"{OK} GF patterns configured\n")
    else:
        print(f"{WARN} GFPattern directory not found. You may need to clone:")
        print(f"        git clone https://github.com/1ndianl33t/Gf-Patterns GFPattern\n")

def generate_final_report(target):
    """Generate a comprehensive summary report"""
    report_file = OUTPUT_DIR / f"REPORT_{target.replace('.', '_')}.txt"
    
    with open(report_file, 'w') as f:
        f.write(f"DataDive Security Assessment Report\n")
        f.write(f"="*70 + "\n\n")
        f.write(f"Target: {target}\n")
        f.write(f"Scan Date: {tm.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"DataDive Version: {CURRENT_VERSION}\n\n")
        f.write(f"="*70 + "\n\n")
        
        # Subdomain Summary
        f.write("1. SUBDOMAIN ENUMERATION\n")
        f.write("-" * 70 + "\n")
        if (SUBDOMAINS_DIR / "all_subdomains.txt").exists():
            total_subs = get_line_count(str(SUBDOMAINS_DIR / "all_subdomains.txt"))
            alive_subs = get_line_count(str(SUBDOMAINS_DIR / "alive.txt"))
            f.write(f"Total Subdomains: {total_subs}\n")
            f.write(f"Live Subdomains: {alive_subs}\n")
            f.write(f"Coverage: {(alive_subs/total_subs*100 if total_subs > 0 else 0):.1f}%\n\n")
        
        # Open Redirect Summary
        f.write("2. OPEN REDIRECT VULNERABILITIES\n")
        f.write("-" * 70 + "\n")
        redirect_findings = 0
        for test_file in REDIRECT_DIR.glob("test_*.txt"):
            redirect_findings += get_line_count(str(test_file))
        f.write(f"Potential Findings: {redirect_findings}\n")
        f.write(f"Status: {'CRITICAL' if redirect_findings > 0 else 'CLEAR'}\n\n")
        
        # SQLi Summary
        f.write("3. SQL INJECTION TESTING\n")
        f.write("-" * 70 + "\n")
        if (SQLI_DIR / "nuclei_sqli_findings.txt").exists():
            sqli_findings = get_line_count(str(SQLI_DIR / "nuclei_sqli_findings.txt"))
            f.write(f"Vulnerabilities Found: {sqli_findings}\n")
            f.write(f"Status: {'CRITICAL' if sqli_findings > 0 else 'CLEAR'}\n\n")
        
        # S3 Summary
        f.write("4. S3 BUCKET EXPOSURE\n")
        f.write("-" * 70 + "\n")
        if (S3_DIR / "s3_bucket_names.txt").exists():
            s3_buckets = get_line_count(str(S3_DIR / "s3_bucket_names.txt"))
            f.write(f"Buckets Discovered: {s3_buckets}\n")
            f.write(f"Status: {'REVIEW REQUIRED' if s3_buckets > 0 else 'NONE FOUND'}\n\n")
        
        f.write("="*70 + "\n")
        f.write(f"Full results available in: {OUTPUT_DIR.absolute()}\n")
    
    print(f"{OK} Comprehensive report generated: {report_file}\n")

def main():
    """Main execution workflow"""
    # Setup
    print_banner()
    create_output_directories()
    
    # Dependency checks
    print_section_header("Dependency Verification")
    print(f"[{INF}] Checking required tools and dependencies...")
    print(f"{PROGRESS} This ensures all reconnaissance tools are available\n")
    
    deps_ok = True
    deps_ok = check_and_install_go() and deps_ok
    deps_ok = check_and_install_aws() and deps_ok
    deps_ok = check_uro() and deps_ok
    deps_ok = check_jq() and deps_ok
    
    if not deps_ok:
        print(f"\n{WARN} Some dependencies failed to install")
        print(f"{WARN} Continuing anyway - some features may not work\n")
        input(f"Press Enter to continue...")
    
    # Check Go tools
    tool_status = check_go_tools()
    missing_tools = [tool for tool, installed in tool_status.items() if not installed]
    
    if missing_tools:
        print(f"\n{WARN} The following tools failed to install: {', '.join(missing_tools)}")
        print(f"{WARN} Some modules may not function correctly\n")
        cont = input(f"Continue anyway? (y/n): ").lower()
        if cont != 'y':
            print(f"{ERR} Exiting. Please install missing tools manually.")
            sys.exit(1)
    
    # Setup GF patterns
    setup_gf_patterns()
    
    print(f"\n{OK} All systems ready!")
    sleep(2)
    
    # Get target from user
    print_section_header("Target Configuration")
    target = input(f"[{INF}] Enter the target domain (e.g., example.com): ").strip()
    
    if not target:
        print(f"{ERR} No target specified. Exiting.")
        sys.exit(1)
    
    # Validate domain format
    if target.startswith("http://") or target.startswith("https://"):
        target = target.split("://")[1].split("/")[0]
        print(f"{WARN} Cleaned target domain: {target}")
    
    print(f"\n{OK} Target set to: {colored(target, 'cyan', attrs=['bold'])}")
    print(f"{PROGRESS} All results will be saved to: {OUTPUT_DIR.absolute()}\n")
    
    # Module selection
    print(f"[{INF}] Select modules to run:\n")
    print(f"  1. Full Scan (All modules)")
    print(f"  2. Subdomain Enumeration Only")
    print(f"  3. Open Redirect Testing Only")
    print(f"  4. SQL Injection Testing Only")
    print(f"  5. S3 Bucket Discovery Only")
    print(f"  6. GitHub Secret Scanning Only")
    print(f"  7. Custom Selection\n")
    
    choice = input(f"[{INF}] Enter your choice (1-7): ").strip()
    
    modules = {
        'subdomain': False,
        'openredirect': False,
        'sqli': False,
        's3': False,
        'github': False
    }
    
    if choice == '1':
        modules = {k: True for k in modules}
        print(f"{OK} Running full scan on {target}\n")
    elif choice == '2':
        modules['subdomain'] = True
    elif choice == '3':
        modules['subdomain'] = True  # Required for open redirect
        modules['openredirect'] = True
    elif choice == '4':
        modules['subdomain'] = True  # Required for SQLi
        modules['sqli'] = True
    elif choice == '5':
        modules['subdomain'] = True  # Required for S3
        modules['s3'] = True
    elif choice == '6':
        modules['github'] = True
    elif choice == '7':
        print(f"\n[{INF}] Select modules to run (y/n for each):\n")
        modules['subdomain'] = input("  Run Subdomain Enumeration? (y/n): ").lower() == 'y'
        modules['openredirect'] = input("  Run Open Redirect Testing? (y/n): ").lower() == 'y'
        modules['sqli'] = input("  Run SQL Injection Testing? (y/n): ").lower() == 'y'
        modules['s3'] = input("  Run S3 Bucket Discovery? (y/n): ").lower() == 'y'
        modules['github'] = input("  Run GitHub Secret Scanning? (y/n): ").lower() == 'y'
    else:
        print(f"{WARN} Invalid choice. Running full scan.")
        modules = {k: True for k in modules}
    
    # Ensure dependencies
    if modules['openredirect'] or modules['sqli'] or modules['s3']:
        if not modules['subdomain']:
            print(f"\n{WARN} Selected modules require subdomain enumeration")
            modules['subdomain'] = True
    
    print(f"\n{OK} Scan configuration confirmed. Starting...\n")
    sleep(2)
    
    # Execute modules
    start_time = tm.time()
    subdomains_file = None
    
    try:
        # Module 1: Subdomain Enumeration
        if modules['subdomain']:
            subdomains_file = subdomain_enumeration(target)
        
        # Module 2: Open Redirect Testing
        if modules['openredirect']:
            if subdomains_file:
                open_redirect_testing(target, subdomains_file)
            else:
                print(f"{ERR} Skipping Open Redirect - no subdomains file")
        
        # Module 3: SQL Injection Testing
        if modules['sqli']:
            if subdomains_file:
                waf_bypass_and_sqli(target, subdomains_file)
            else:
                print(f"{ERR} Skipping SQLi Testing - no subdomains file")
        
        # Module 4: S3 Bucket Discovery
        if modules['s3']:
            if subdomains_file:
                s3_bucket_scanning(target, subdomains_file)
            else:
                print(f"{ERR} Skipping S3 Scanning - no subdomains file")
        
        # Module 5: GitHub Secret Scanning
        if modules['github']:
            github_secret_scanning(target)
        
        # Generate final report
        generate_final_report(target)
        
    except KeyboardInterrupt:
        print(f"\n\n{WARN} Scan interrupted by user")
        print(f"{PROGRESS} Partial results saved to: {OUTPUT_DIR}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{ERR} Unexpected error occurred: {str(e)}")
        print(f"{PROGRESS} Partial results may be available in: {OUTPUT_DIR}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Completion
    elapsed_time = tm.time() - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\n\n{'='*70}")
    print(f"{colored('SCAN COMPLETE!', 'green', attrs=['bold'])}")
    print(f"{'='*70}\n")
    print(f"[{INF}] Scan Statistics:")
    print(f"    • Target: {target}")
    print(f"    • Duration: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    print(f"    • Results: {OUTPUT_DIR.absolute()}")
    print(f"\n{OK} Review the generated report and individual module outputs")
    print(f"{PROGRESS} Next steps:")
    print(f"    1. Verify all findings manually")
    print(f"    2. Prioritize critical vulnerabilities")
    print(f"    3. Document and report responsibly")
    print(f"    4. Follow coordinated disclosure practices\n")
    print(f"{WARN} Remember: This tool is for authorized testing only!")
    print(f"{WARN} Unauthorized access to systems is illegal.\n")

def welcome():
    """Entry point with initial checks"""
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{WARN} Operation cancelled by user")
        sys.exit(0)

# ========================================================================
# Script Entry Point
# ========================================================================

if __name__ == "__main__":
    welcome()
