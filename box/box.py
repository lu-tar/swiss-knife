import platform, socket, time
import datetime
import hashlib
from pathlib import *
from session import *
from ipadd import *
from hashing import *
from scan2 import *
from macfinder import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#
# to do list: inserire delle checklist di troubleshooting
#
#

def banner():
    print("""
     ______     ___   ____  ____
    |_   _ \  .'   `.|_  _||_  _|
      | |_) |/  .-.  \ \ \  / /
      |  __'.| |   | |  > `' <
     _| |__) \  `-'  /_/ /'`\ \_
    |_______/ `.___.'|____||____|

    Lookup
    - https://scapy.readthedocs.io/en/latest/installation.html
    - https://nmap.org/book/man-examples.html
    - subprocess.Popen("start cmd /K ping 8.8.8.8 -t", shell=True)
    """)
    print("Build 1.0")
    print(datetime.datetime.now())
    print(platform.platform()+" "+socket.gethostname()+"\n")

def helper():
    print("""Comandi
    |__[e] esci dallo script
    |__[h][help] helper
    |__[e] banner
    L4
    |__[t] telnet
    |__[s] ssh
    |__[nmap] nmap -v
    L3
    |__[net] network check
    |__[ip] ip address check
    |__[subnets] show subnets
    |__[ippub] GET http://ifconfig.co/
    |__[ipapi] GET http://ip-api.com/
    |__[ping] ping -t
    L2
    |__[mac] mac address -> vendor
    File
    |__[md5] MD5 a file
    Miscellanea
    |__Firmware CISCO
    """)

def webIos():
    driver = webdriver.Firefox()
    driver.get("https://software.cisco.com/download/navigator.html")

#def flush():
    #elimina il contenuto di log.txt

banner()

with open("log.txt", "a") as log:
    log.write(str(datetime.datetime.now()) + " START\n")
while True:
    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")
    console = input(timestamp+">> ")

    # banner e helper
    if console == "b":      banner()
    if console == "help" or console == "h": helper()

    # comandi box
    if console == "t":      telnet()
    if console == "s":      secureshell()
    if console == "nmap":   nmap()
    if console == "net":    netCheck()
    if console == "ip":     ipCheck()
    if console == "ippub":  pubCheck()
    if console == "ipapi":  ipapi()
    if console == "subnets":subnets()
    if console == "ping":   pinger()
    if console == "md5":    md5()
    if console == "mac":    macFinder()
    # controllare metodi portscan
    if console == "scan":   main()
    if console == "ios":    webIos()

    # uscire dallo script
    if console == "e":
        with open("log.txt", "a") as log:
            log.write(str(datetime.datetime.now()) + " EXIT\n")
        exit()
    else:
        pass
