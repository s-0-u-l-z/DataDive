import shutil
from termcolor import colored
import sys
import os
import time as tm
import requests
import subprocess

sys.stdout.reconfigure(line_buffering=True)

# Needed for checking if the version is up to date or not
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
    # To correctly determine the package manager, you might need to
    # prompt the user or detect it earlier in your script.
    pkg_manager = "apt" # Placeholder: Replace with actual package manager logic

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
    # This check `if pkg_manager not in install_cmds:` needs to refer to `install_aws` not `install_cmds`.
    if pkg_manager not in install_aws: # Corrected: checking against install_aws
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

def command(cmd, description=""):
    """
    Executes a shell command and prints its output.
    Args:
        cmd (str): The shell command to execute.
        description (str): A brief explanation of what the command does.
    """
    if description:
        print(f"[{INF}] Executing: {description}")
        print(f"    Command: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"{ERR}", result.stderr)

# Needed for checking requirements

def install_package(go_path):
    print(f"[{INF}] Installing {go_path}")
    command(f"go install {go_path}", f"Installing Go package {go_path}")

# Needed for wc -l

def get_line_count(file_path):
    """
    Gets the number of lines in a file using 'wc -l'.
    Args:
        file_path (str): The path to the file.
    Returns:
        int: The number of lines in the file, or 0 if an error occurs.
    """
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
    """
    Checks if a given binary is installed and installs it if not.
    Args:
        binary (str): The name of the binary to check/install.
    """
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
    # os.environ("") # This line is incomplete, assuming it's for GOPATH setup
    # If you intend to set GOPATH, please provide the correct path, e.g.:
    # os.environ["GOPATH"] = os.path.expanduser("~/go")
    command("mkdir -p ~/.gf", "Creating .gf directory for GF patterns if it doesn't exist.")
    command("cp GFPattern/* ~/.gf", "Copying GF patterns to the .gf directory.")

    # ========================================================================
    # Section: Subdomain Enumeration
    # Tags: #Subdomain_Enumeration #Reconnaissance
    # ========================================================================
    print(f'\n\n{"="*70}')
    print(f'[{INF}] Starting Subdomain Enumeration')
    print(f'{"="*70}\n')
    sleep(2.5)

    subenumweb = input("What is the website you want to scan for subdomains?: ")

    print(colored("Running Subfinder", "yellow"))
    print("")
    sleep(2.5)
    command(f'subfinder -d {subenumweb} -all >> subfinder.txt',
            f'Using Subfinder to discover subdomains for {subenumweb}. '
            'The `-d` flag specifies the domain, `-all` uses all available sources, '
            'and `>>` appends output to `subfinder.txt`.')
    print("")

    print(colored("Running Assetfinder", "yellow"))
    sleep(2.5)
    print("")
    command(f'assetfinder --subs-only {subenumweb} >> assetfinder.txt',
            f'Running Assetfinder to find related subdomains for {subenumweb}. '
            'The `--subs-only` flag restricts output to only subdomains.')
    print("")

    print(colored("Running Amass", "yellow"))
    sleep(2.5)
    print("")
    command(f'amass enum -timeout 30 -norecursive -d {subenumweb} >> amass.txt',
            f'Performing Amass enumeration for {subenumweb}. '
            'Amass is a powerful reconnaissance tool. '
            '`-timeout 30` sets a 30-second timeout, `-norecursive` prevents recursive subdomain search, '
            'and `-d` specifies the target domain.')
    print("")

    print(f"[{INF}] Combining results into subdomains.txt")
    print("")
    command("sort -u subfinder.txt assetfinder.txt amass.txt > subdomains.txt",
            'Merging and de-duplicating subdomains from `subfinder.txt`, `assetfinder.txt`, '
            'and `amass.txt` into `subdomains.txt`. `sort -u` sorts and removes duplicates.')
    line_count = get_line_count('subdomains.txt')
    print(f"[{INF}] Total found subdomains: {line_count}")
    print("")

    print(colored("Running httpx to find alive subdomains", "yellow"))
    print("")
    sleep(2)
    if line_count >= 500:
        command("httpx -l subdomains.txt -o alive.txt -t 50",
                'Probing subdomains from `subdomains.txt` with httpx to check for live hosts. '
                '`-l` specifies the input file, `-o` for output, and `-t 50` sets 50 concurrent threads '
                'for faster scanning (used for larger lists).')
    else:
        command("httpx -l subdomains.txt -o alive.txt",
                'Probing subdomains from `subdomains.txt` with httpx to check for live hosts. '
                '`-l` specifies the input file, `-o` for output. Default threads are used for smaller lists.')
    print("")

    print(f"[{INF}] Checking status codes with httpx")
    print("")
    command('httpx -l subdomains.txt -sc >> status_codes.txt',
            'Scanning all subdomains in `subdomains.txt` with httpx to retrieve HTTP status codes. '
            '`-sc` displays the status code, and `>>` appends to `status_codes.txt`.')
    print("")

    print(f"[{INF}] Filtering 200 OK responses")
    print("")
    command("cat status_codes.txt | grep '200' >> 200.txt",
            'Extracting only the lines with a "200 OK" status code from `status_codes.txt` '
            'and saving them to `200.txt`.')
    print("")

    print(f"[{INF}] Running Subjack and Nuclei for subdomain takeover checks")
    print("")
    command("subjack -w subdomains.txt -t 100 -ssl -v -o subjack.txt",
            'Running Subjack to check for potential subdomain takeovers. '
            '`-w` specifies the wordlist (subdomains), `-t 100` sets 100 threads, '
            '`-ssl` enables SSL/TLS checks, `-v` for verbose output, and `-o` for output file.')
    command("nuclei -l subdomains.txt -t ~/nuclei-templates/takeovers/detect-all-takeovers.yaml >> nuclei-subdomaintakeovers.txt",
            'Using Nuclei with a specific template to detect various subdomain takeover vulnerabilities '
            'on the discovered subdomains. `-l` for list, `-t` for template.')
    print("")

    print(f"[{INF}] Running Katana for JS and deep scan")
    print("")
    command("katana -u alive.txt -jc -o katana-JS.txt",
            'Running Katana, a web crawler, on `alive.txt` to discover JavaScript files. '
            '`-u` specifies the input URLs, `-jc` extracts JavaScript files, and `-o` saves the output.')
    command("katana -u alive.txt -d 5 -ef woff,css,png,svg,jpg,woff2,jpeg,gif -o Katana-DeepScan-allurls.txt",
            'Performing a deeper crawl with Katana on `alive.txt`. '
            '`-d 5` sets the recursion depth to 5, and `-ef` excludes common file extensions '
            'to focus on more interesting content.')
    print("")

    # ========================================================================
    # Section: Open Redirect Testing
    # Tags: #Open_Redirect #Vulnerability_Scanning
    # ========================================================================
    print(f'\n\n{"="*70}')
    print(f'[{INF}] Starting Open Redirect Testing')
    print(f'{"="*70}\n')
    sleep(2.5)

    print(f'[{INF}] We\'re going to run Gau + Nuclei to find OpenRedirects')
    print("")

    print(colored("Running Gau", "yellow"))
    command("cat subdomains.txt | gau --o Gau-OpenRedirect.txt",
            'Using Gau (Get All URLs) to fetch URLs from the Wayback Machine '
            'and other sources for each subdomain in `subdomains.txt`. '
            'Output is saved to `Gau-OpenRedirect.txt`.')
    command("cat Gau-OpenRedirect.txt | gf redirect | uro | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com'",
            'Piping URLs from `Gau-OpenRedirect.txt` to `gf redirect` (a GF pattern for redirect parameters). '
            'Then, `uro` normalizes URLs, `qsreplace` injects `https://evil.com` into query parameters, '
            'and `httpx` silently checks for responses containing `evil.com`, indicating a potential open redirect.')
    print("")

    print(colored("Running Nuclei (Open Redirect)", "yellow"))
    print("")
    command("cat alive.txt | nuclei -t ~/nuclei-templates/http/open-redirect/open-redirect.yaml -c 45",
            'Scanning all alive subdomains with Nuclei using a specific template '
            'designed to identify open redirect vulnerabilities. '
            '`-c 45` sets 45 concurrent requests.')
    print("")

    print(f"{INF} Time to use ffuf to replace a redirect query like: returnUrl=, continue=  with an open redirect payload")
    print("")
    print(colored("We will use Gau + Katana + Urlfinder + hakrawler to find as much redirect querys as possible", "yellow"))
    command("cat alive.txt | katana -d 2 -o katana-redirect.txt",
            'Crawling `alive.txt` with Katana (depth 2) to find more URLs, including those with potential redirect parameters.')
    command("cat alive.txt | urlfinder -o urlfinder-redirect.txt",
            'Using urlfinder to extract URLs from `alive.txt`, which may contain redirect parameters.')
    command("cat alive.txt | hakrawler > hakrawler-redirect.txt",
            'Crawling `alive.txt` with hakrawler to discover URLs, including those with redirect parameters.')
    command("cat katana-redirect.txt urlfinder-redirect.txt hakrawler-redirect.txt Gau-OpenRedirect.txt | uro | sort -u  | tee final-redirect.txt",
            'Combining URLs from Katana, Urlfinder, Hakrawler, and Gau, then normalizing, '
            'de-duplicating, and saving them to `final-redirect.txt`. `tee` also prints to console.')

    open_redirect_regex = "returnUrl=|continue=|dest=|destination=|forward=|go=|goto=|login\\?to=|login_url=|logout=|next=|next_page=|out=|g=|redir=|redirect=|redirect_to=|redirect_uri=|redirect_url=|return=|returnTo=|return_path=|return_to=|return_url=|rurl=|site=|target=|to=|uri=|url=|qurl=|rit_url=|jump=|jump_url=|originUrl=|origin=|Url=|desturl=|u=|Redirect=|location=|ReturnUrl=|redirect_url=|redirect_to=|forward_to=|forward_url=|destination_url=|jump_to=|go_to=|goto_url=|target_url=|redirect_link="
    command(f"cat final-redirect.txt | grep -Pi '{open_redirect_regex}' | tee redirect_params.txt",
            'Filtering `final-redirect.txt` to find URLs containing common open redirect parameter names '
            'using a case-insensitive regex. Results are saved to `redirect_params.txt` and printed.')
    command("cat redirect_params.txt | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com' >> openredirect-test-1.txt ",
            'Injecting `https://evil.com` into parameters of URLs from `redirect_params.txt` '
            'and using `httpx` to check if `evil.com` is reflected in the final redirected URL.')
    command(r'cat redirect_params.txt | qsreplace "https://evil.com" | xargs -I {} curl -s -o /dev/null -w "%{url_effective} -> %{redirect_url}\n" {} >> openredirect-test-2.txt',
            'Similar to the previous command, but uses `curl` to explicitly follow redirects and '
            'print the effective URL and redirect URL to `openredirect-test-2.txt`. '
            'This provides more detailed redirect information.')
    command(f'subfinder -d {subenumweb} | httpx -silent | gau | gf redirect | uro | qsreplace "https://evil.com" | httpx -silent -fr -mr "evil.com" >> openredirect-test-3.txt',
            'A combined pipeline: find subdomains, check if alive, fetch URLs with Gau, '
            'filter for redirects with GF, normalize with uro, inject payload, and check for redirection.')

    print(f'[{INF}] Using advanced payloads from payloads/openredirect.txt for open redirect testing.')
    print(f'[{WARN}] Ensure you have created a file named `openredirect.txt` in a `payloads` directory and populated it with your desired open redirect payloads.')
    command(f'cat Gau-OpenRedirect.txt | gf redirect | uro | while read url; do cat payloads/openredirect.txt | while read payload; do echo "$url" | qsreplace "$payload"; done; done | httpx -silent -fr -mr "google.com" >> openredirect-test-4.txt',
            'Iterating through URLs from `Gau-OpenRedirect.txt` (filtered by `gf redirect` and normalized by `uro`). '
            'For each URL, it tries every payload from `payloads/openredirect.txt`, '
            'injects it with `qsreplace`, and checks if the redirection leads to `google.com` (as an example of a controlled external site).')

    print(f'\n[{WARN}] For a tool with no false positives for open redirects, consider using **lox.sh**.')
    print(f'        First, prepare the input file by running: cat Gau-OpenRedirect.txt | sed \'s/=.*/=/\' | uro > final_lox.txt')
    print(f'        This command processes the Gau-OpenRedirect.txt file. `sed \'s/=.*/=/\'` removes everything after the first equals sign '
            '(to standardize parameter names for lox.sh), and `uro` normalizes the URLs. The output is saved to `final_lox.txt`.')
    print(f'        Then, run lox.sh manually with: ./lox.sh < final_lox.txt')
    print(f'        This command feeds the prepared list of URLs into the `lox.sh` tool for open redirect validation.')
    print("")

    # ========================================================================
    # Section: WAF Bypass Techniques (ProxyChains & SQLMap)
    # Tags: #WAF_Bypass #SQL_Injection #ProxyChains #Security_Testing
    # ========================================================================
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
    
    input("Are you ready?: ")

    print(f'\n[{INF}] Validating ProxyChains setup...')
    print(f'[{WARN}] Run the following commands to confirm ProxyChains is working:')
    sleep(2)
    print(colored("Executing: proxychains curl http://ipinfo.io", "yellow"))
    command("proxychains curl http://ipinfo.io",
            'Using `proxychains` to route `curl` through the configured proxies to `http://ipinfo.io`. '
            'This command helps verify if ProxyChains is active and changing your apparent IP address.')
    sleep(1)
    print(colored("Executing: proxychains curl http://ipinfo.io/ip", "yellow"))
    command("proxychains curl http://ipinfo.io/ip",
            'Similar to the previous command, this specifically fetches only the IP address '
            'to quickly confirm if the IP is being rotated by ProxyChains.')
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
        command(f'proxychains sqlmap -u \'{sqlmap_target_url}\' --dbs --batch -p id --random-agent --tamper=between,space2comment --dbms mysql --tech=B --no-cast --flush-session --threads 10',
                'Running SQLMap with ProxyChains for WAF bypass. '
                '`-u` specifies the target URL. `--dbs` enumerates databases. '
                '`--batch` runs in non-interactive mode. `-p id` targets the "id" parameter. '
                '`--random-agent` uses a random User-Agent. '
                '`--tamper=between,space2comment` uses tamper scripts to obfuscate payloads. '
                '`--dbms mysql` specifies the database management system. '
                '`--tech=B` uses boolean-based blind SQLi. `--no-cast` avoids casting. '
                '`--flush-session` clears the session. `--threads 10` sets 10 concurrent threads.')
        print(f'[{OK}] SQLMap execution completed. Review the output for bypassed WAFs and dumped databases.')
    else:
        print(f'[{WARN}] No URL provided for SQLMap testing. Skipping this step.')
    sleep(3)

    print(f'\n[{INF}] Mass Hunting for SQL Injection Vulnerabilities')
    print(f'[{WARN}] This section outlines steps to scale SQLi detection across multiple targets.')
    sleep(2)

    print(f'[{INF}] Step 1: Extracting unique domain names from `alive.txt` (or your initial URL list).')
    print(f"        Command: cat alive.txt | awk -F/ '{{print $3}}' | sort -u > unique_domains_for_sqli.txt")
    command("cat alive.txt | awk -F/ '{print $3}' | sort -u > unique_domains_for_sqli.txt",
            'Extracting only the domain (hostname) from each URL in `alive.txt`, '
            'then sorting and removing duplicates to create `unique_domains_for_sqli.txt`. '
            '`awk -F/ \'{print $3}\'` extracts the third field separated by `/` (the hostname).')
    line_count_domains = get_line_count('unique_domains_for_sqli.txt')
    print(f'[{OK}] Extracted {line_count_domains} unique domains to unique_domains_for_sqli.txt')
    sleep(2)

    print(f'[{INF}] Step 2: Using waybackurls, gf sqli, and uro to find SQLi parameter URLs from passive sources.')
    print(f'        Command: cat unique_domains_for_sqli.txt | waybackurls | gf sqli | uro > sqli_urls_raw.txt')
    command("cat unique_domains_for_sqli.txt | waybackurls | gf sqli | uro > sqli_urls_raw.txt",
            'Piping unique domains to `waybackurls` to fetch historical URLs, '
            'then `gf sqli` filters for URLs with common SQLi parameters, '
            'and `uro` normalizes them. Results are saved to `sqli_urls_raw.txt`.')
    line_count_sqli_raw = get_line_count('sqli_urls_raw.txt')
    print(f'[{OK}] Found {line_count_sqli_raw} potential SQLi URLs to sqli_urls_raw.txt')
    sleep(2)

    print(f'[{INF}] Step 3: Reducing noise by getting only one SQL parameter URL per domain.')
    print(f'        Command: cat sqli_urls_raw.txt | gawk -F/ \'{{host=$3; sub(/:80$/, "", host); if (!(host in seen)) {{ print $0; seen[host] }} }}\' > sqli_urls_filtered.txt')
    command('cat sqli_urls_raw.txt | gawk -F/ \'{host=$3; sub(/:80$/, "", host); if (!(host in seen)) { print $0; seen[host] } }\' > sqli_urls_filtered.txt',
            'Filtering `sqli_urls_raw.txt` to select only one URL per unique domain. '
            'This prevents redundant scanning of multiple URLs on the same domain with Nuclei. '
            '`gawk` is used for more advanced text processing, keeping track of seen hosts.')
    line_count_sqli_filtered = get_line_count('sqli_urls_filtered.txt')
    print(f'[{OK}] Filtered down to {line_count_sqli_filtered} unique SQLi URLs in sqli_urls_filtered.txt')
    sleep(2)

    print(f'[{INF}] Step 4: Scanning with Nuclei using the DAST SQLi template.')
    print(f'        Command: nuclei -l sqli_urls_filtered.txt -t ~/nuclei-templates/dast/sql-injection.yaml -c 45')
    print(f'[{WARN}] Ensure you have the nuclei-templates repository cloned (e.g., `git clone https://github.com/projectdiscovery/nuclei-templates ~/nuclei-templates`)')
    command("nuclei -l sqli_urls_filtered.txt -t ~/nuclei-templates/dast/sql-injection.yaml -c 45 >> nuclei-sqli-results.txt",
            'Running Nuclei to actively scan the filtered SQLi URLs for SQL Injection vulnerabilities '
            'using the `dast/sql-injection.yaml` template. `-c 45` sets 45 concurrent requests. '
            'Results are appended to `nuclei-sqli-results.txt`.')
    print(f'[{OK}] Nuclei SQLi scan completed. Results saved to nuclei-sqli-results.txt.')
    sleep(3)

    print(f'\n{"="*70}')
    print(f'[{OK}] WAF Bypass Techniques Section Completed.')
    print(f'{"="*70}\n')
    sleep(2)

    # ========================================================================
    # Section: S3 Bucket Scanning
    # Tags: #S3_Bucket #Cloud_Security #Information_Disclosure
    # ========================================================================
    print(f'\n\n{"="*70}')
    print(f'[{INF}] Starting S3 Bucket Scanning')
    print(f'{"="*70}\n')
    sleep(2.5)

    print(f'[{INF}] We will use subfinder, nuclei, katana, and other methods. I also recommend **Github dorking** separately.')
    print("")

    # Initial S3 detection
    print(f'[{INF}] Running Subfinder + Httpx for finding Amazon S3 Sites')
    command(f'subfinder -d {subenumweb} -all -silent | httpx -sc -title -td | grep "Amazon S3" >> subfinder-s3-scanning.txt',
            f'Discovering subdomains for {subenumweb} with Subfinder, then piping them to httpx '
            'to check for live hosts and extract status codes, titles, and technology detections. '
            'Finally, `grep "Amazon S3"` filters for responses indicating Amazon S3 services, '
            'saving them to `subfinder-s3-scanning.txt`.')
    print("")

    print(f'[{INF}] Using Nuclei to find S3 sites')
    command(f'subfinder -d {subenumweb} -all -silent | nuclei -t ~/nuclei-templates/s3/s3-detect.yaml',
            f'Using Subfinder to get subdomains, then piping them to Nuclei to scan for '
            'known S3 bucket misconfigurations and common S3 bucket patterns '
            'using the `s3-detect.yaml` template.')
    print("")

    # JS file analysis for S3 URLs
    print(f'[{INF}] Time to use Katana to download all of the JS files, then search for AWS S3 URLs in those files')
    print("")
    command(f"katana -u {subenumweb} -d 5 -jc | grep '\.js$' | tee alljs.txt",
            f'Crawling {subenumweb} with Katana (depth 5) to find JavaScript files (`-jc`), '
            'filtering for `.js` extensions, and saving them to `alljs.txt` and printing to console.')
    command(f'echo {subenumweb} | gau | grep "\.js$" | anew alljs.txt',
            f'Fetching URLs for {subenumweb} using Gau, filtering for `.js` files, '
            'and adding new unique JS URLs to `alljs.txt` using `anew`.')
    command(f'cat alljs.txt | uro | sort -u | httpx -mc -o {subenumweb}.txt',
            'Normalizing, de-duplicating, and then checking the status of JavaScript URLs '
            'from `alljs.txt` with `httpx`. `-mc` shows status codes. The output is saved to a file named after the target.')
    command(f'cat {subenumweb}.txt | jsleak -s -l -k',
            f'Running `jsleak` on the previously collected JavaScript files (from {subenumweb}.txt) '
            'to find sensitive information like AWS keys, secrets, and other credentials. '
            '`-s` for secret, `-l` for link, `-k` for key.')
    command(f'cat {subenumweb} | nuclei -t templates/credentials-disclosure-all.yaml -c 30 -o credentials-disclosure-nuclei.txt',
            f'Scanning the target website with Nuclei using a broad `credentials-disclosure-all.yaml` template '
            'to find any exposed credentials. `-c 30` sets 30 concurrent requests. Output to `credentials-disclosure-nuclei.txt`.')

    print(f"[{INF}] Extracting S3 URLs from JS files")
    command(r'cat alljs.txt | xargs -I {} curl -s {} | grep -oE "http[s]?://[^"]*.s3.amazonaws.com"',
            'Downloading the content of each JavaScript file listed in `alljs.txt` using `curl`. '
            'Then, `grep -oE` extracts (only matches) specific patterns '
            'that indicate Amazon S3 URLs (e.g., `http://bucketname.s3.amazonaws.com`).')
    print("")

    # S3 bucket dorking with Google (manual part, for user reference)
    print(f'\n{"="*70}')
    print(f'[{INF}] Manual Google Dorking for AWS S3 Buckets')
    print(f'{"="*70}\n')
    print(f'[{WARN}] Remember to perform **Google dorking** for AWS S3 buckets manually using:')
    print(f'        site:s3.amazonaws.com "{subenumweb}"')
    print(f'        This Google Dork searches for pages indexed by Google that are hosted on `s3.amazonaws.com` '
            f'and contain the target domain name (`{subenumweb}`). This helps find publicly exposed S3 buckets.')
    print(f'        And for a more extensive dork:')
    print(f'        (site:*.s3.amazonaws.com OR site:*.s3-external-1.amazonaws.com OR site:*.s3.duelstack.us-east-1.amazonaws.com OR site:*.s3.ap-south-1.amazonaws.com) "{subenumweb}"')
    print(f'        This extended dork includes common S3 endpoint variations to cover more regions and types of S3 buckets.')
    print(f'        Open each result; "Access Denied" means private, otherwise you\'ve accessed its contents.')
    print("")

    # Automation with Dork Eye (if you integrate it) and S3BucketMisconf
    print(f'[{INF}] For automated Google Dorking for S3 buckets, consider using **Dork Eye**.')
    print(f'        If you use Dork Eye, you can then feed its results into **S3BucketMisconf**:')
    print(f'        (Note: S3BucketMisconf would need to be installed and accessible)')
    print(f'        s3bucketmisconf -dorkeye_results your_dorkeye_results.txt')
    print(f'        This outlines a potential workflow where `Dork Eye` automates the Google Dorking, '
            f'and its output (`your_dorkeye_results.txt`) is then used as input for `S3BucketMisconf` '
            f'to check for common S3 bucket misconfigurations (e.g., public write access).')
    print("")

    # Alternative S3 bucket discovery from subdomains
    print(f'[{INF}] Filtering protocols from subdomains.txt and preparing for Java2S3.py')
    command(f'cat subdomains.txt | grep -oP \'(?<=https?://).*\' > final.txt',
            'Removing `http://` or `https://` prefixes from URLs in `subdomains.txt` '
            'to prepare them for `java2s3.py`, which often expects just the hostname or path.')
    print(f'[{INF}] Running java2s3.py (assuming it is available in your PATH)')
    # You need to ensure java2s3.py is in your execution path or provide its full path.
    # Replace 'target.com' with 'subenumweb' for dynamic target.
    command(f'python java2s3.py final.txt {subenumweb} output.txt',
            f'Executing `java2s3.py` with the filtered subdomains (`final.txt`) and the target domain (`{subenumweb}`). '
            'This script is designed to enumerate S3 buckets related to a given domain. '
            'Results are saved to `output.txt`.')
    print("")

    print(f'[{INF}] Extracting S3 Buckets lines from output.txt')
    command('cat output.txt | grep -E "S3 Buckets: \\[.*?\\]" >> extracted_s3_buckets.txt',
            'Filtering `output.txt` to extract lines specifically containing "S3 Buckets: [...]", '
            'which typically list discovered S3 bucket names. Appended to `extracted_s3_buckets.txt`.')
    print(f'[{INF}] Extracting full S3 bucket URLs (with object paths)')
    command('cat output.txt | grep -oP \'https://[a-zA-Z0-9.-]*s3(\\.dualstack)?\\.[a-z0-9-]+\\.amazonaws\\.com/[^"\\s<>]+\' | sort -u >> full_s3_urls.txt',
            'Extracting complete S3 bucket URLs (including paths to objects) from `output.txt` '
            'using a regex that matches common S3 URL patterns. Unique URLs are saved to `full_s3_urls.txt`.')
    print(f'[{INF}] Extracting S3 bucket hostnames (only domain part)')
    command('cat output.txt | grep -oP \'([a-zA-Z0-9.-]*\\.s3(\\.dualstack)?\\.[a-z0-9-]+\\.amazonaws\\.com)\' | sort -u >> s3_hostnames.txt',
            'Extracting just the hostnames of S3 buckets (e.g., `bucketname.s3.amazonaws.com`) '
            'from `output.txt`. Unique hostnames are saved to `s3_hostnames.txt`.')
    print("")

    # S3Scanner integration (assuming it's installed and in PATH)
    print(f'[{INF}] Running s3scanner to enumerate bucket permissions (requires a list of buckets)')
    command(f's3scanner -bucket-file s3_hostnames.txt -enumerate -threads 10 | grep -oE \'AllUsers: \\[.*(READ|WRITE|FULL).\' >> s3scanner_results.txt',
            'Using `s3scanner` to enumerate permissions of S3 buckets listed in `s3_hostnames.txt`. '
            '`-enumerate` checks common permissions, `-threads 10` sets concurrency. '
            '`grep -oE` then extracts lines indicating `AllUsers` have `READ`, `WRITE`, or `FULL` access, '
            'which signifies critical misconfigurations. Results are appended to `s3scanner_results.txt`.')
    print("")

    # ========================================================================
    # Section: GitHub Dorking and Secret Scanning
    # Tags: #GitHub_Dorking #Secret_Scanning #Information_Disclosure
    # ========================================================================
    print(f'\n\n{"="*70}')
    print(f'[{INF}] Starting GitHub Dorking for Sensitive Information')
    print(f'{"="*70}\n')
    sleep(2) # Pause for readability

    github_dorks_content = f"""
    --- GitHub Dorking Queries for {subenumweb} ---

    Method 1: Searching for keywords in an organization\'s repositories
    ------------------------------------------------------------------
    * To find passwords: "{subenumweb}" password
      Explanation: This dork searches GitHub for files containing both your target domain and the keyword "password".
    * To find JSON-structured data for potential credentials: "{subenumweb}" password extension:json
      Explanation: This narrows the search to JSON files containing your target domain and "password",
                   often revealing API keys, database credentials, or other secrets.

    Method 2: Using OR operators to find secret keys and API keys
    ------------------------------------------------------------
    * Generic key dork: org:{subenumweb} "aws_access_key_id" OR "aws_secret_access_key" OR "api_key" OR "secret_key" OR "client_secret"
      Explanation: This dork specifically targets the GitHub organization associated with your target
                   and searches for common patterns of cloud credentials (AWS) and generic API/secret keys.
    * Environment files: org:{subenumweb} path:.env
      Explanation: Searches for `.env` (environment) files within the organization's repositories.
                   These files often contain sensitive configuration details, including API keys and database connections.
    * Git configuration files: org:{subenumweb} path:.git
      Explanation: Looks for `.git` configuration files, which can sometimes contain credentials or internal repository information.

    --- End of GitHub Dorking Queries ---
    """
    with open("github_dorks.txt", "w") as f:
        f.write(github_dorks_content)

    print(f'[{INF}] GitHub dorking queries have been saved to github_dorks.txt')
    print(f'[{WARN}] Remember to manually perform these GitHub dorks (e.g., by pasting them into the GitHub search bar on GitHub.com).')
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
        command(f'trufflehog github --org={org_input} --json | jq . >> trufflehog_results.json',
                f'Running `trufflehog` against the specified GitHub organization (`{org_input}`). '
                '`trufflehog` scans repositories for hardcoded secrets, '
                'and `--json` outputs results in JSON format. '
                'The output is then piped to `jq` for pretty-printing and saved to `trufflehog_results.json`.')
        print(f'[{OK}] Trufflehog scan completed. Results saved to trufflehog_results.json.')
    else:
        print(f'[{WARN}] No GitHub organization provided for Trufflehog scan. Skipping.')
    print("")


if __name__ == "__main__":
    welcome()
