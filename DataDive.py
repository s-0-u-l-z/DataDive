import time
import os
import subprocess
from termcolor import colored
import base64
import favicon
import mmh3
import re
import requests
import threading


def run_command_in_konsole(command):
    """Helper function to run a command in a new konsole window."""
    subprocess.Popen(["konsole", "-e", "bash", "-c", command])


def sleep(seconds):
    time.sleep(seconds)


def install_package(package_name):
    subprocess.run(f'sudo apt install {package_name}', shell=True)


banner = """
██████╗░░█████╗░████████╗░█████╗░██████╗░██╗██╗░░░██╗███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██║██║░░░██║██╔════╝
██║░░██║███████║░░░██║░░░███████║██║░░██║██║╚██╗░██╔╝█████╗░░
██║░░██║██╔══██║░░░██║░░░██╔══██║██║░░██║██║░╚████╔╝░██╔══╝░░
██████╔╝██║░░██║░░░██║░░░██║░░██║██████╔╝██║░░╚██╔╝░░███████╗
╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═════╝░╚═╝░░░╚═╝░░░╚══════╝
V 4.1
By s0ulz
"""

# Display the banner
for line in banner.split('\n'):
    for char in line:
        print(char, end='', flush=True)
        sleep(0.005)
    print()

sleep(0.5)

warning = colored('Warning this program only works in Linux distros that use deb!', 'red', attrs=['reverse', 'blink'])
print(warning)

sleep(2.2)
print("")
sleep(1)

def run_command(command):
    """Helper function to run a command and print the output."""
    print(f"Running: {command}")
    os.system(command)

def subfinder():
    subfinderinstalled = input("Do you have Subfinder installed (y/n)?: ").lower()
    if subfinderinstalled == "no":
        install_package('subfinder')

    global subfinderoutput
    global subfinderurl
    subfinderurl = input("Enter the Subfinder URL: ")
    subfinderoutput = input("Enter the filename for Subfinder output: ")

    os.system(f'subfinder -d {subfinderurl} -o {subfinderoutput}')


def httpx():
    httpxinstalled = input("Do you have httpx installed (y/n)?: ")
    if httpxinstalled == "no":
        install_package('httpx-toolkit')

    global httpxoutputname
    httpxoutputname = input("What is the output file name for httpx?: ")
    
    

    os.system(f'httpx-toolkit -l {subfinderoutput} -o {httpxoutputname}')
    os.system(f'wc -l {httpxoutputname}')

def install_aquatone():
    run_command("wget https://github.com/michenriksen/aquatone/releases/download/v1.7.0/aquatone_linux_amd64_1.7.0.zip")
    run_command("unzip aquatone_linux_amd64_1.7.0.zip")

def aquatone():
    run_command_in_konsole(f'cat {httpxoutputname} | ./aquatone')


def dirsearch():
    run_command_in_konsole(f'go run main.go -l {httpxoutputname} -o gopath_output.txt ')


def sslyze():
    run_command_in_konsole(f'while read -r url; do sslyze "$url"; done < cleaned_urls.txt > sslyze_scan.txt')


def get_favicon_hash():
    """Fetches a website's favicon, calculates its mmh3 hash, and prints it for Shodan/Zoomeye searches."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
    }

    while True:
        url = input("Enter a URL (must include http:// or https://): ").strip()
        if url.lower().startswith(("http://", "https://")):
            break
        print("Invalid URL. Please include 'http://' or 'https://'.")

    try:
        if url.lower().endswith((".ico", ".jpg", ".png", ".gif")):
            favicon_url = url  # Direct favicon URL
        else:
            icons = favicon.get(url, headers=headers)
            if not icons:
                print(f"No favicon found. Try using {url}/favicon.ico directly.")
                return
            favicon_url = icons[0].url

        response = requests.get(favicon_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for HTTP failures

        if response.status_code == 403:
            print(f"Access to {favicon_url} is forbidden (403). Skipping...")
            return

        icon_hash = mmh3.hash(base64.b64encode(response.content))

        print(f"\nFavicon Hash: {icon_hash}")
        print(f"Shodan Query: http.favicon.hash:{icon_hash}")
        print(f"Zoomeye Query: iconhash:\"{icon_hash}\"")

    except requests.exceptions.RequestException as req_err:
        print(f"Network error: {req_err}")
    except Exception as err:
        print(f"Unexpected error: {err}")


def nmap():
    run_command_in_konsole(f'nmap -iL cleaned_urls.txt -sS -sV -sC -O --script vulners -T4 -oN detailed_scan.txt')


def nikto():
    run_command_in_konsole(f'nikto -h {httpxoutputname} -o nikto_results.txt')


def spyhunt():
    spyhuntinstalled = input("Do you have spyhunt installed (y/n)?: ")
    if spyhuntinstalled.lower() == 'n':
        run_command('git clone https://github.com/gotr00t0day/spyhunt')
    os.system(f'cp {httpxoutputname} spyhunt')
    os.chdir("spyhunt")
    run_command(f"python3 spyhunt.py -hh {httpxoutputname} -sv host_header_injection_output.txt")
    url = input("Enter an IP for Spyhunt's network analyzer: ")
    run_command(f"python3 spyhunt.py -na {url} -sv networkanalyzer.txt")
    run_command(f'python3 spyhunt.py -co {httpxoutputname} -sv CoRsSpyhunt.txt')
    openredirecturl = input('What URL do you want to scan for open redirect?: ')
    autorecon = input("What domain do you want to scan with auto recon?: ")
    run_command(f'python3 spyhunt.py -ar {autorecon}')


def nuclei():
    run_command_in_konsole(
        f'nuclei -l {httpxoutputname} -severity unknown,low,medium,high,critical -etags "intrusive" >> nuclei_output.txt')


# Run Subfinder & Httpx first in same terminal and get favicon
subfinder()
httpx()
get_favicon_hash()




# Run everything else at the same time in new Konsole windows
aquatoneinstalled = input("Is aquatone installed in this directory?: ")
if aquatoneinstalled.lower() == 'no':
    install_aquatone()
else:
    pass

aquatone()
dirsearch()
sslyze()
nmap()
nikto()
nuclei()
spyhunt()

banner = """
                                    ..,,,.,..
                           ....,,.,,,,,,,,..,,,,,,,..
                       ,..,,.,,,,,,,,,,,,,,,,,,,,,,.,,.,..
                   ..,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,,
                 .,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,..
               ,.,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,..,
             .,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
            .,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
           ,.,,,,,,,,,,,,,,.,,,,.,..,,,,,,,,,.,,,,,,,,,,,,,,,,,,,,,,,,
          ,,,,,,,,,,,,,.,.#%&&&&&&(,,.,,,,,,..&&&&&&&&,,.,,,,,,,,,,,,,.
         ,,,,,,,,,,,,,,,.%&&&#,%&&&&.,.,,,..#&&&%*,&&&&%..,,,,,,,,,,,,,
         ,,,,,,,,,,,,,,,,*/..,,,,,%(.,,,,,,../*,,,,,,/%,,,,,,,,,,,,,,,,,
         .,,,,,.///////,..,,,,,,,,,,,,,,,,,,,,,,,,,,,,,..,//////,,..,,,,
         .,,,,./////////,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,////////*.,,,,,
         ,,,,,,,///////,,.,.,,.,.,,,,,,,,,,,,,,,,.,.,....*///////..,,,,,
         .,,,..,.,..,,.,.%&&%,,..,,,,,,,,,,,,,,,,,,%&&&,,,,...,,,,.,,,,
          ,,,,,,,,,,,,,.,,,&%&&&&&&&&&&&&&&&&&&&&&&&%.,,,,,,,,,,,,,,,.,
           ..,,,,,,,,,,,,,,,,./&&&&&&&&&&&&&&&&&&&.,..,,,,,,,,,,,,,,,.
            .,,,,,,,,,,,,,,,,,,,,,.,,..*(*.,,..,,,,,,,,,,,,,,,,,,,,.,
             ,.,,,,,,,,,,,,,,,,,,,,,,,,,,,.,,,,,,,,,,,,,,,,,,,,,,.,,
               ..,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
                 .,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.
                   ,,.,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,.,..
                      ..,,,,.,,,,,,,,,,,,,,,,,,,,,,,,,,...
                          ..,,,,,,,,,,,,,,,,,,,,,,,.,,
                                  .,,,,,,,..,,.

                Thanks for using DataDive!
"""
print(banner)
