import shutil
from termcolor import colored
import sys
import os
import time as tm
import requests
import subprocess

sys.stdout.reconfigure(line_buffering=True)

latestversion = requests.get('https://raw.githubusercontent.com/s-0-u-l-z/DataDive/refs/heads/DataDive-Main/version.txt')
currentversion = 2.01

INF = colored("INF", "blue")
OK = colored("[OK]", "green")
ERR = colored("[ERR]", "red")
WARN = colored("[!]", "yellow")



def check_and_install_go():
    global pkg_manager
    global install_cmds
    global all_pkg_managers

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

    install_aws = {
        "apt": "sudo apt install awscli",
        "pacman": "sudo pacman -S aws-cli",
        "dnf": "sudo dnf install awscli",
        "zypper": "sudo zypper install aws-cli-v2",
        "eopkg": "sudo eopkg install aws-cli",
        "xbps": "sudo xbps-install -S aws-cli",
        "apk": "sudo apk add aws-cli",
        "emerge": "emerge -av net-misc/awscli",
        "nix": "-iA nixpkgs.awscli2",
        "brew": "brew install awscli"
    }

    if shutil.which("aws") is not None:
        return 
    print(f"{ERR} AWS is not installed on your system")
    if pkg_manager not in install_cmds:
        print(f"{ERR} Unsupported or unknown package manager: {pkg_manager}")
        sys.exit(1)
    print(f"[{INF}] Installing AWS using {pkg_manager}")
    os.system(install_aws[pkg_manager])
    print(f"{OK} AWS installation complete.")



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
        ██████╔╝██║░░██║░░░██║░░░██║░░██║██████╔╝██║░░╚██╔╝░░███████╗
        ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚══════╝

                                By s0ulz

    [{INF}] Current DataDive version v{currentversion} {status} 
"""

if currentversion > float(latestversion.text.strip()):
    input(f"{WARN} How tf can the version number of this be higher than the latest version on the official github page?: ")
    print(colored("YOU EDITED THIS FILE BRUH", "magenta"))

for line in banner.split('\n'):
    print(line)

check_and_install_go()

def command(cmd):
    os.system(cmd)

def install_package(go_path):
    print(f"[{INF}] Installing {go_path}")
    command(f"go install {go_path}")

def get_line_count(file_path):
    result = subprocess.run(['wc', '-l', file_path], capture_output=True, text=True)
    return int(result.stdout.strip().split()[0]) if result.returncode == 0 else 0

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
    "gf": "github.com/tomnomnom/gf@latest"
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
    os.system("export GOPATH=$HOME/go")
    os.system("mkdir ~/.gf")
    os.system("cp GFPattern/* ~/.gf")
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
        return
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
    command("nuclei -l subdomains.txt -t templates/detect-all-takeovers.yaml >> nuclei-subdomaintakeovers.txt")
    print("")
    print(f"[{INF}] Running Katana for JS and deep scan")
    print("")
    command("katana -u alive.txt -jc -o js.txt")
    command("katana -u alive.txt -d 5 -ef woff,css,png,svg,jpg,woff2,jpeg,gif -o allurls.txt")
    print("")
    print(f'[{INF}] Were going to run Gau + Nuclei to find OpenRedirects')
    print("")
    print(colored("Running Gau", "yellow"))
    command("cat subdomains.txt | gau --o Gau-OpenRedirect.txt")
    command("cat Gau-OpenRedirect.txt | gf redirect | uro | qsreplace 'https://evil.com' | httpx -silent -fr -mr 'evil.com'")
    print("")
    print("Running Nuclei (Subdomaintakeover)")
    command("cat alive.txt | nuclei -t templates/openRedirect.yaml -c 30")


welcome()
