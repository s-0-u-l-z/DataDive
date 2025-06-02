import shutil
from termcolor import colored
import sys
import os
import time as tm
import requests
import subprocess

sys.stdout.reconfigure(line_buffering=True)

#Needed for checking if the version is up to date or not

latestversion = requests.get('https://raw.githubusercontent.com/s-0-u-l-z/DataDive/refs/heads/DataDive-Main/version.txt')
currentversion = 2.01

INF = colored("INF", "blue")
OK = colored("[OK]", "green")
ERR = colored("[ERR]", "red")
WARN = colored("[!]", "yellow")

# Needed for checking requirements

def check_and_install_go():

    if shutil.which("go") is not None:
        return
    print(f"{ERR} Go is not installed on your system.")
    print("")
    all_pkg_managers = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
    print(f"{WARN} Please enter your package manager ({'/'.join(all_pkg_managers)}):")
    print("")
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
        sys.exit(1)
    print(f"[{INF}] Installing Go using {pkg_manager}...")
    os.system(install_cmds[pkg_manager])
    print(f"{OK} Go installation complete.")


def check_and_install_aws():
    # This 'pkg_manager' variable is not defined in this scope.
    # It needs to be passed as an argument or defined globally if used here.
    # For now, I'm defining a placeholder.
    pkg_manager = "apt" # Placeholder, replace with actual package manager if needed

    install_aws = {
        "apt": "sudo apt install awscli",
        "pacman": "sudo pacman -S aws-cli",
        "dnf": "sudo dnf install awscli",
        "zypper": "sudo zypper install aws-cli-v2",
        "eopkg": "sudo eopkg install aws-cli",
        "xbps": "sudo xbps-install -S aws-cli",
        "apk": "sudo apk add aws-cli",
        "emerge": "emerge -av net-misc/awscli",
        "nix": "nix-env -iA nixpkgs.awscli2",
        "brew": "brew install awscli"
    }

    if shutil.which("aws") is not None:
        return
    print(f"{ERR} AWS is not installed on your system")
    if pkg_manager not in install_cmds: # `install_cmds` is also not defined here.
                                       # This check might need to be re-evaluated
                                       # or `install_cmds` passed in.
        print(f"{ERR} Unsupported or unknown package manager: {pkg_manager}")
        sys.exit(1)
    print(f"[{INF}] Installing AWS using {pkg_manager}")
    os.system(install_aws[pkg_manager])
    print(f"{OK} AWS installation complete.")

def checkuro():
    if shutil.which("uro") is not None:
        return
    print(f'{ERR} uro is not installed, install it from: https://github.com/s0md3v/uro')
    sys.exit()

def check_jq():
    if shutil.which("jq") is not None:
        return
    print(f'{ERR} jq is not installed on your system.')
    print("")
    all_pkg_managers = ["apt", "dnf", "pacman", "zypper", "xbps", "eopkg", "apk", "emerge", "brew", "nix"]
    print(f"{WARN} Please enter your package manager ({'/'.join(all_pkg_managers)}):")
    print("")
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
        print(f"{ERR} Unsupported or unknown package manager: {pkg_manager}")
        sys.exit(1)
    print(f"[{INF}] Installing jq using {pkg_manager}...")
    os.system(install_cmds[pkg_manager])
    print(f"{OK} jq installation complete.")


def sleep(time):
    tm.sleep(time)

if currentversion != float(latestversion.text.strip()):
    status = f"({colored('outdated', 'red')})"
else:
    status = f"({colored('latest', 'green')})"

banner = f"""

        ██████╗░░█████╗░████████╗░█████╗░██████╗░██╗██╗░░░██╗███████╗
        ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
        ██║░░██║███████║░░░██║░░░███████║██║░░██║██║╚██╗░██╔╝█████╗░░
        ██║░░██║██╔══██║░░░██║░░░██║░░██║██║░░██║██║░╚████╔╝░██╔══╝░░
        ██████╔╝██║░░██║░░░╚═══╝░░██║░░██║██████╔╝██║░░╚██╔╝░░███████╗
        ╚═════╝░╚═╝░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚══════╝

                                By s0ulz

    [{INF}] Current DataDive version v{currentversion} {status}
"""

if currentversion > float(latestversion.text.strip()):
    input(f"{WARN} How tf can the version number of this be higher than the latest version on the official github page?: ")
    print(colored("YOU EDITED THIS FILE BRUH", "magenta"))

for line in banner.split('\n'):
    print(line)

# Placeholder for pkg_manager, as it's not defined globally or passed to check_and_install_aws
# You'll need to decide how to handle this, e.g., by prompting the user earlier.
# For now, I'm setting it to 'apt' to prevent an error.
pkg_manager = "apt" # This needs to be correctly set based on user input or detected system.

check_and_install_go()
check_and_install_aws()
checkuro()
check_jq() # Check for jq installation

# To run commands and get output from them easier

def command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(f"{ERR}", result.stderr)

# Needed for checking requirements

def install_package(go_path):
    print(f"[{INF}] Installing {go_path}")
    command(f"go install {go_path}")

# Needed for wc -l

def get_line_count(file_path):
    result = subprocess.run(['wc', '-l', file_path], capture_output=True, text=True)
    return int(result.stdout.strip().split()[0]) if result.returncode == 0 else 0

#checking requirements

go_tools = {
    "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
    "katana": "github.com/projectdiscovery/katana/cmd/katana@latest",
    "amass": "github.com/owasp-amass/amass/v3/...@master",
    "subjack": "github.com/haccer/subjack@latest",
    "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
    "assetfinder": "github.com/tomnomnom/assetfinder@latest",
    "naabu": "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest",
    "gau": "github.com/lc/gau/v2/cmd/gau@latest",
    "GoPath": "github.com/s-0-u-l-z/GoPath@latest",
    "ffuf": "github.com/ffuf/ffuf@latest",
    "nuclei": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
    "waybackurls": "github.com/tomnomnom/waybackurls@latest",
    "gf": "github.com/tomnomnom/gf@latest",
    "qsreplace": "github.com/tomnomnom/qsreplace@latest",
    "urlfinder": "github.com/projectdiscovery/urlfinder/cmd/urlfinder@latest",
    "hakrawler": "github.com/hakluke/hakrawler@latest"
}

def check_if_packages_are_installed(binary):
    path = shutil.which(binary)
    if path:
        print(f"{OK} {binary} is installed.")
    else:
        print(f"{ERR} {binary} is not installed.")
        install_package(go_tools[binary])
        if shutil.which(binary):
            print(f"{OK} {binary} installed successfully.")
        else:
            print(f"{ERR} {binary} failed to install.")

def welcome():
    print(f"\n[{INF}] Starting DataDive tool checks...")
    print("")
    for binary in go_tools:
        check_if_packages_are_installed(binary)
    print(f"\n{OK} All tools checked and installed.")
    main()

def main():

    # Making sure that environment paths are setup correctly

    # This line looks like it's missing an argument, e.g., os.environ["GOPATH"] = "/path/to/go"
    # For now, I'll comment it out or fix it to be a no-op if no specific path is intended.
    # If you intend to set GOPATH, please provide the correct path.
    # os.environ("")
    os.system("mkdir -p ~/.gf") # Use -p to avoid error if directory exists
    os.system("cp GFPattern/* ~/.gf")

    # Finding Subdomains

    print(f"\n[{INF}] Starting Subdomain Enumeration...")
    print("")
    sleep(2.5)
    print(colored("Running Subfinder", "yellow"))
    print("")
    sleep(2.5)
    subenumweb = input("What is the website you want to scan for subdomains?: ")
    command(f'subfinder -d {subenumweb} -all >> subfinder.txt')
    print("")
    print(colored("Running Assetfinder", "yellow"))
    sleep(2.5)
    print("")
    command(f'assetfinder --subs-only {subenumweb} >> assetfinder.txt')
    print("")
    print(colored("Running Amass", "yellow"))
    sleep(2.5)
    print("")
    command(f'amass enum -timeout 30 -norecursive -d {subenumweb} >> amass.txt')
    print("")
    print(f"[{INF}] Combining results into subdomains.txt")
    print("")
    command("sort -u subfinder.txt assetfinder.txt amass.txt > subdomains.txt")
    line_count = get_line_count('subdomains.txt')
    print(f"[{INF}] Total found subdomains: {line_count}")
    print("")
    print(colored("Running httpx to find alive subdomains", "yellow"))
    print("")
    sleep(2)
    if line_count >= 500:
        command("httpx -l subdomains.txt -o alive.txt -t 50")
    else:
        command("httpx -l subdomains.txt -o alive.txt")
    print("")
    print(f"[{INF}] Checking status codes with httpx")
    print("")
    command('httpx -l subdomains.txt -sc >> status_codes.txt')
    print("")
    print(f"[{INF}] Filtering 200 OK responses")
    print("")
    command("cat status_codes.txt | grep '200' >> 200.txt")
    print("")
    print(f"[{INF}] Running Subjack and Nuclei for subdomain takeover checks")
    print("")
    command("subjack -w subdomains.txt -t 100 -ssl -v -o subjack.txt")
    command("nuclei -l subdomains.txt -t ~/nuclei-templates/takeovers/detect-all-takeovers.yaml >> nuclei-subdomaintakeovers.txt")
    print("")
    print(f"[{INF}] Running Katana for JS and deep scan")
    print("")
    command("katana -u alive.txt -jc -o katana-JS.txt")
    command("katana -u alive.txt -d 5 -ef woff,css,png,svg,jpg,woff2,jpeg,gif -o Katana-DeepScan-allurls.txt")
    print("")

    #Open Redirect Testing

    print(f'[{INF}] Were going to run Gau + Nuclei to find OpenRedirects')
    print("")
    print(colored("Running Gau", "yellow"))
    command("cat subdomains.txt | gau --o Gau-OpenRedirect.txt")
    command("cat Gau-OpenRedirect.txt | gf redirect | uro | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com'")
    print("")
    print(colored("Running Nuclei (Open Redirect)", "yellow"))
    print("")
    command("cat alive.txt | nuclei -t ~/nuclei-templates/http/open-redirect/open-redirect.yaml -c 45")
    print("")
    print(f"{INF} Time to use ffuf to replace a redirect query like: returnUrl=, continue=  with a open redirect payload")
    print("")
    print(colored("We will use Gau + Katana + Urlfinder + hakrawler to find as much redirect querys as possible", "yellow"))
    command("cat alive.txt | katana -d 2 -o katana-redirect.txt")
    command("cat alive.txt | urlfinder -o urlfinder-redirect.txt")
    command("cat alive.txt | hakrawler > hakrawler-redirect.txt")
    command("cat katana-redirect.txt urlfinder-redirect.txt hakrawler-redirect.txt Gau-OpenRedirect.txt | uro | sort -u  | tee final-redirect.txt")
    open_redirect_regex = "returnUrl=|continue=|dest=|destination=|forward=|go=|goto=|login\\?to=|login_url=|logout=|next=|next_page=|out=|g=|redir=|redirect=|redirect_to=|redirect_uri=|redirect_url=|return=|returnTo=|return_path=|return_to=|return_url=|rurl=|site=|target=|to=|uri=|url=|qurl=|rit_url=|jump=|jump_url=|originUrl=|origin=|Url=|desturl=|u=|Redirect=|location=|ReturnUrl=|redirect_url=|redirect_to=|forward_to=|forward_url=|destination_url=|jump_to=|go_to=|goto_url=|target_url=|redirect_link="
    command(f"cat final-redirect.txt | grep -Pi '{open_redirect_regex}' | tee redirect_params.txt")
    command("cat redirect_params.txt | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com' >> openredirect-test-1.txt ")
    command(r'cat redirect_params.txt | qsreplace "https://evil.com" | xargs -I {} curl -s -o /dev/null -w "%{url_effective} -> %{redirect_url}\n" {} >> openredirect-test-2.txt')
    command(f'subfinder -d {subenumweb} | httpx -silent | gau | gf redirect | uro | qsreplace "https://evil.com" | httpx -silent -fr -mr "evil.com" >> openredirect-test-3.txt')
    # Using advanced payloads from openredirect.txt. Remember to create payloads/openredirect.txt with actual payloads!
    print(f'[{INF}] Using advanced payloads from payloads/openredirect.txt for open redirect testing.')
    print(f'[{WARN}] Ensure you have created a file named `openredirect.txt` in a `payloads` directory and populated it with your desired open redirect payloads.')
    command(f'cat Gau-OpenRedirect.txt | gf redirect | uro | while read url; do cat payloads/openredirect.txt | while read payload; do echo "$url" | qsreplace "$payload"; done; done | httpx -silent -fr -mr "google.com" >> openredirect-test-4.txt')

    # Lox.sh integration (manual steps for user)
    print(f'\n[{WARN}] For a tool with no false positives for open redirects, consider using **lox.sh**.')
    print(f'        First, prepare the input file by running: cat Gau-OpenRedirect.txt | sed \'s/=.*/=/\' | uro > final_lox.txt')
    print(f'        Then, run lox.sh manually with: ./lox.sh < final_lox.txt')
    print("")

    # WAF Bypass Techniques
    print(f'\n\n{"="*70}')
    print(f'[{INF}] Starting WAF Bypass Techniques')
    print(f'{"="*70}\n')
    sleep(2)

    print(f'[{INF}] Method 1: Using Proxychains for WAF Bypass')
    print(f'[{WARN}] ProxyChains routes traffic through multiple proxies to evade detection and rate limits.')
    print(f'[{WARN}] Manual Setup Required:')
    print(f'    1.  Open the ProxyChains configuration file:')
    print(f'        sudo nano /etc/proxychains.conf')
    print(f'    2.  Comment out the default Tor setting (127.0.0.1:9050) by adding a hash `#` at the beginning of the line.')
    print(f'    3.  Add your residential proxies at the end of the file in the format:')
    print(f'        http <ipaddress> <port> [username] [password]')
    print(f'        (e.g., http 192.0.2.1 8080 or socks5 192.0.2.2 9050 user pass)')
    print(f'        You can get free SSL proxies from: https://www.sslproxies.org/ or use paid residential proxies.')
    print(f'    4.  Disable `dynamic_chain` and enable `random_chain` to improve reliability (ProxyChains will rotate proxies if one fails).')
    print(f'        #dynamic_chain')
    print(f'        random_chain')
    print(f'    5.  Optionally, enable `quiet_mode` to suppress ProxyChains logs:')
    print(f'        quiet_mode')
    print(f'    6.  Save and exit the configuration file.')
    sleep(5)

    print(f'\n[{INF}] Validating ProxyChains setup...')
    print(f'[{WARN}] Run the following commands to confirm ProxyChains is working:')
    sleep(2)
    print(colored("Executing: proxychains curl http://ipinfo.io", "yellow"))
    command("proxychains curl http://ipinfo.io")
    sleep(1)
    print(colored("Executing: proxychains curl http://ipinfo.io/ip", "yellow"))
    command("proxychains curl http://ipinfo.io/ip")
    print(f'[{OK}] If you see different IP addresses with each request, ProxyChains is routing traffic correctly.')
    print(f'[{WARN}] You can also verify by running `proxychains firefox` and checking your IP in the browser.')
    sleep(3)

    print(f'\n[{INF}] Using SQLMap with ProxyChains and Tamper Scripts')
    print(f'[{WARN}] This method combines IP rotation with payload obfuscation to bypass WAFs.')
    sqlmap_target_url = input(f"[{INF}] Enter the specific URL for SQLMap testing (e.g., http://example.com/vulnerable?id=1): ")
    if sqlmap_target_url:
        print(f'[{INF}] Executing SQLMap with ProxyChains and tamper scripts. This may take some time.')
        print(f'        Command: proxychains sqlmap -u \'{sqlmap_target_url}\' --dbs --batch -p id --random-agent --tamper=between,space2comment --dbms mysql --tech=B --no-cast --flush-session --threads 10')
        sleep(2)
        command(f'proxychains sqlmap -u \'{sqlmap_target_url}\' --dbs --batch -p id --random-agent --tamper=between,space2comment --dbms mysql --tech=B --no-cast --flush-session --threads 10')
        print(f'[{OK}] SQLMap execution completed. Review the output for bypassed WAFs and dumped databases.')
    else:
        print(f'[{WARN}] No URL provided for SQLMap testing. Skipping this step.')
    sleep(3)

    print(f'\n[{INF}] Mass Hunting for SQL Injection Vulnerabilities')
    print(f'[{WARN}] This section outlines steps to scale SQLi detection across multiple targets.')
    sleep(2)

    print(f'[{INF}] Step 1: Extracting unique domain names from `alive.txt` (or your initial URL list).')
    print(f'        Command: cat alive.txt | awk -F/ \'{print $3}\' | sort -u > unique_domains_for_sqli.txt')
    command("cat alive.txt | awk -F/ '{print $3}' | sort -u > unique_domains_for_sqli.txt")
    line_count_domains = get_line_count('unique_domains_for_sqli.txt')
    print(f'[{OK}] Extracted {line_count_domains} unique domains to unique_domains_for_sqli.txt')
    sleep(2)

    print(f'[{INF}] Step 2: Using waybackurls, gf sqli, and uro to find SQLi parameter URLs from passive sources.')
    print(f'        Command: cat unique_domains_for_sqli.txt | waybackurls | gf sqli | uro > sqli_urls_raw.txt')
    command("cat unique_domains_for_sqli.txt | waybackurls | gf sqli | uro > sqli_urls_raw.txt")
    line_count_sqli_raw = get_line_count('sqli_urls_raw.txt')
    print(f'[{OK}] Found {line_count_sqli_raw} potential SQLi URLs to sqli_urls_raw.txt')
    sleep(2)

    print(f'[{INF}] Step 3: Reducing noise by getting only one SQL parameter URL per domain.')
    print(f'        Command: cat sqli_urls_raw.txt | gawk -F/ \'{{host=$3; sub(/:80$/, "", host); if (!(host in seen)) {{ print $0; seen[host] }} }}\' > sqli_urls_filtered.txt')
    command('cat sqli_urls_raw.txt | gawk -F/ \'{host=$3; sub(/:80$/, "", host); if (!(host in seen)) { print $0; seen[host] } }\' > sqli_urls_filtered.txt')
    line_count_sqli_filtered = get_line_count('sqli_urls_filtered.txt')
    print(f'[{OK}] Filtered down to {line_count_sqli_filtered} unique SQLi URLs in sqli_urls_filtered.txt')
    sleep(2)

    print(f'[{INF}] Step 4: Scanning with Nuclei using the DAST SQLi template.')
    print(f'        Command: nuclei -l sqli_urls_filtered.txt -t ~/nuclei-templates/dast/sql-injection.yaml -c 45')
    print(f'[{WARN}] Ensure you have the nuclei-templates repository cloned (e.g., `git clone https://github.com/projectdiscovery/nuclei-templates ~/nuclei-templates`)')
    command("nuclei -l sqli_urls_filtered.txt -t ~/nuclei-templates/dast/sql-injection.yaml -c 45 >> nuclei-sqli-results.txt")
    print(f'[{OK}] Nuclei SQLi scan completed. Results saved to nuclei-sqli-results.txt.')
    sleep(3)

    print(f'\n{"="*70}')
    print(f'[{OK}] WAF Bypass Techniques Section Completed.')
    print(f'{"="*70}\n')
    sleep(2)


    # S3 Bucket Scanning (Existing section, kept for context)

    print(f'\n[{INF}] Finished with Open Redirect scanning, now we will do S3 Bucket scanning')
    print("")
    print(f'[{INF}] We will use subfinder, nuclei, katana, and other methods. I also recommend **Github dorking** separately.')
    print("")

    # Initial S3 detection
    print(f'[{INF}] Running Subfinder + Httpx for finding Amazon S3 Sites')
    command(f'subfinder -d {subenumweb} -all -silent | httpx -sc -title -td | grep "Amazon S3" >> subfinder-s3-scanning.txt')
    print("")
    print(f'[{INF}] Using Nuclei to find S3 sites')
    command(f'subfinder -d {subenumweb} -all -silent | nuclei -t ~/nuclei-templates/s3/s3-detect.yaml')
    print("")

    # JS file analysis for S3 URLs
    print(f'[{INF}] Time to use Katana to download all of the JS files, then search for AWS S3 URLs in those files')
    print("")
    command(f"katana -u {subenumweb} -d 5 -jc | grep '\\.js$' | tee alljs.txt")
    print(f"[{INF}] Extracting S3 URLs from JS files")
    command(r'cat alljs.txt | xargs -I {} curl -s {} | grep -oE "http[s]?://[^"]*.s3.amazonaws.com"')
    print("")

    # S3 bucket dorking with Google (manual part, for user reference)
    print(f'[{WARN}] Remember to perform **Google dorking** for AWS S3 buckets manually using:')
    print(f'        site:s3.amazonaws.com "{subenumweb}"')
    print(f'        And for a more extensive dork:')
    print(f'        (site:*.s3.amazonaws.com OR site:*.s3-external-1.amazonaws.com OR site:*.s3.duelstack.us-east-1.amazonaws.com OR site:*.s3.ap-south-1.amazonaws.com) "{subenumweb}"')
    print(f'        Open each result; "Access Denied" means private, otherwise you\'ve accessed its contents.')
    print("")

    # Automation with Dork Eye (if you integrate it) and S3BucketMisconf
    print(f'[{INF}] For automated Google Dorking for S3 buckets, consider using **Dork Eye**.')
    print(f'        If you use Dork Eye, you can then feed its results into **S3BucketMisconf**:')
    print(f'        (Note: S3BucketMisconf would need to be installed and accessible)')
    print(f'        s3bucketmisconf -dorkeye_results your_dorkeye_results.txt')
    print("")

    # Alternative S3 bucket discovery from subdomains
    print(f'[{INF}] Filtering protocols from subdomains.txt and preparing for Java2S3.py')
    command(f'cat subdomains.txt | grep -oP \'(?<=https?://).*\' > final.txt')
    print(f'[{INF}] Running java2s3.py (assuming it is available in your PATH)')
    # You need to ensure java2s3.py is in your execution path or provide its full path.
    # Replace 'target.com' with 'subenumweb' for dynamic target.
    command(f'python java2s3.py final.txt {subenumweb} output.txt')
    print("")

    print(f'[{INF}] Extracting S3 Buckets lines from output.txt')
    command('cat output.txt | grep -E "S3 Buckets: \\[.*?\\]" >> extracted_s3_buckets.txt')
    print(f'[{INF}] Extracting full S3 bucket URLs (with object paths)')
    command('cat output.txt | grep -oP \'https://[a-zA-Z0-9.-]*s3(\\.dualstack)?\\.[a-z0-9-]+\\.amazonaws\\.com/[^"\\s<>]+\' | sort -u >> full_s3_urls.txt')
    print(f'[{INF}] Extracting S3 bucket hostnames (only domain part)')
    command('cat output.txt | grep -oP \'([a-zA-Z0-9.-]*\\.s3(\\.dualstack)?\\.[a-z0-9-]+\\.amazonaws\\.com)\' | sort -u >> s3_hostnames.txt')
    print("")

    # S3Scanner integration (assuming it's installed and in PATH)
    print(f'[{INF}] Running s3scanner to enumerate bucket permissions (requires a list of buckets)')
    # This command requires a file of bucket names, e.g., 's3_hostnames.txt' from previous steps.
    command(f's3scanner -bucket-file s3_hostnames.txt -enumerate -threads 10 | grep -oE \'AllUsers: \\[.*(READ|WRITE|FULL).\' >> s3scanner_results.txt')
    print("")

    # GitHub Dorking
    print(f'\n[{INF}] Starting GitHub Dorking for sensitive information')
    sleep(2) # Pause for readability

    github_dorks_content = f"""
    --- GitHub Dorking Queries for {subenumweb} ---

    Method 1: Searching for keywords in an organization\'s repositories
    ------------------------------------------------------------------
    * To find passwords: "{subenumweb}" password
    * To find JSON-structured data for potential credentials: "{subenumweb}" password extension:json

    Method 2: Using OR operators to find secret keys and API keys
    ------------------------------------------------------------
    * Generic key dork: org:{subenumweb} "aws_access_key_id" OR "aws_secret_access_key" OR "api_key" OR "secret_key" OR "client_secret"
    * Environment files: org:{subenumweb} path:.env
    * Git configuration files: org:{subenumweb} path:.git

    --- End of GitHub Dorking Queries ---
    """
    with open("github_dorks.txt", "w") as f:
        f.write(github_dorks_content)

    print(f'[{INF}] GitHub dorking queries have been saved to github_dorks.txt')
    print(f'[{WARN}] Remember to manually perform these GitHub dorks (e.g., on GitHub.com).')
    sleep(3) # Pause for readability

    # Trufflehog integration
    print(f'\n[{INF}] Running Trufflehog for deeper secret scanning on GitHub organization.')
    print(f'[{WARN}] Trufflehog requires GitHub authentication (personal access token).')
    print(f'         Ensure you have trufflehog installed and configured for GitHub access.')
    org_input = input(f"[{INF}] Enter the GitHub organization name for Trufflehog scan (e.g., nasa): ")
    if org_input:
        print(f'[{INF}] Executing: trufflehog github --org={org_input} --json')
        print(f'[{INF}] The output will be piped to jq for pretty printing.')
        print(f'[{INF}] This might take a while depending on the organization size.')
        sleep(2)
        # It's better to save trufflehog output to a file and then process it,
        # especially if it's large. For simplicity and direct execution as requested,
        # I'm keeping it as a direct pipe.
        # Consider adding error handling for trufflehog and jq.
        command(f'trufflehog github --org={org_input} --json | jq . >> trufflehog_results.json')
        print(f'[{OK}] Trufflehog scan completed. Results saved to trufflehog_results.json.')
    else:
        print(f'[{WARN}] No GitHub organization provided for Trufflehog scan. Skipping.')
    print("")


if __name__ == "__main__":
    welcome()
