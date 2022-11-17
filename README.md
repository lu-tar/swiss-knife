# swiss-knife
A copilot for networking tasks written in Python cmd2.

## Features:
## *Self* network
1. show local ip address ✅
2. show public ip address ✅
3. netsh ✅
4. change ip address from static to dynamic

## Network
1. Ping
	1. Normal ✅
		1. https://pypi.org/project/ping3/ ⚠️
	2. Spawn ping 
2. SSH [[Putty command line]] ✅
	1. [SSH Automation](https://medium.com/@simon.hawe/save-time-by-automating-ssh-and-scp-tasks-with-python-e149de606c7b)
3. Bandwidth check
4. [Domaintools API](https://github.com/DomainTools/python_api)
	1. [nslookup](https://www.ionos.it/digitalguide/server/tools-o-strumenti/nslookup/)
5. [Port scanner](https://www.geeksforgeeks.org/port-scanner-using-python-nmap/)
6. Subnet calculator
7. Private and public ranges, address is private?
8. Byte calculator
9. Binary conversion ✅
10. Geolocalization
11. [Crack password 7](https://github.com/theevilbit/ciscot7)
12. [MAC Vendor](https://macvendors.com/api)
13. [Scapy dev roadmap](https://thepacketgeek.com/scapy/building-network-tools/)
14. List ports ✅
15. Latency test ✅

### Wireless
1. netsh script for RSSI and datarates ✅
2. 

## Log & tech-support pattern search
1. Search a file for a list of keyword
	1. [[Python project 🐍 - Box#Obsidian]]
	2. `cat WLC_IMPRIMA_086ac5200e9f_2.txt | grep "RSSI"`
	3. `cat WLC_IMPRIMA_086ac5200e9f_2.txt | grep "Reassociation received from mobile on BSSID"`

## Explorer & files
1. Big listing files in directory
	1. [Tree listing](https://betterprogramming.pub/designing-beautiful-command-line-applications-with-python-72bd2f972ea)
2. [Grep a file](https://linuxhint.com/run-grep-python/)
3. Big notepad - al posto di aprire una nota in Notepad++ la si crea direttamente da CLI / opzione di criptare il file
4. Search a file for a list of keyword
5. Sharepoint scanner
6. Folder scanner
7. Big regex cheatsheet for "important strings" like IPs

## VPS & Remote Execution
1. [Fabric](https://docs.fabfile.org/en/1.10/index.html)
2. Link reducer
3. File sharing like WeTransfer or FTP automation

## Open a...
1. Open a browser tab
2. Open a win app
3. Open Anyconnect / Global Protect
4. Open Bitwarden with PyAutogui or copy the [regex](https://bitwarden.com/help/searching-vault/) to clipboard
5. HTTP server
6. FTP server
7. SFTP server
8. TFTP server

## Obsidian
1. Open a markdown with a template

## Fun CLI enviroment
1. A big `while True:`
	1. [CMD library](https://stackoverflow.com/questions/9340391/python-interactive-shell-type-application)
	2. https://code-maven.com/interactive-shell-with-cmd-in-python
	3. `pythonx-terminal-emulator -e "bash -c \"ping 1.1.1.1; exec bash\""`
2. [Weather API](https://www.weatherapi.com/)
3. [Colors](https://pypi.org/project/colored/) + Colorama
4. [String animation](https://www.geeksforgeeks.org/python-create-simple-animation-for-console-based-application/)
5. Clock and date hh:mm:ss d/m/y
6. How to lock a line or more lines in terminal?
7. [Terminaltables](https://pypi.org/project/terminaltables/)
8. [Prettify CLI](https://betterprogramming.pub/designing-beautiful-command-line-applications-with-python-72bd2f972ea)
9. [Copy text to clipboard](https://pypi.org/project/pyperclip/)
10. Se serve formattare meglio l'ouput di un comando creare un xml / html file da aprire al volo sul browser (inline CSS cdn)
11. Windows version
12. [Logging in Python](https://realpython.com/python-logging/)
13. Task and script configuration file
14. Themes
15. Textualize
16. https://pypi.org/project/plotext/

## Task
1. Unire più azioni / automatizzare sequenze di comandi / Ansible playbooks