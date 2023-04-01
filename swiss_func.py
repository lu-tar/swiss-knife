# Custom configuration
from swiss_conf import *
import subprocess
import platform
import re
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
import requests
import ifaddr

OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
INTERNET_IP = str(requests.get("https://api.ipify.org?format=text").text)

# Pre cmd-loop interface info interrogation using scapy
# checks BANNER variable and ingnores interfaces 
# in array IP_INTERFACES_IGNORE
# using api.ipify.org to pull the public ip address
# [ ] rendere modulare il comando netsh
# [ ] aggiungere sistema operativo linux


def interfaces_table():
    if BANNER == True:

        # Intro table
        intro_table = Table(title="My deafault ip configuration")

        # Set columns
        intro_table.add_column("🐢", justify="center", style="white")
        intro_table.add_column("IP", justify="center", style="cyan")
        intro_table.add_column("Gate", justify="center", style="green")
        intro_table.add_column("DNS", justify="center", style="magenta")

    adapters = ifaddr.get_adapters()
    print(adapters)
    for adapter in adapters:
        print(adapter.nice_name)
        for ip in adapter.ips:
            print("   %s/%s" % (ip.ip, ip.network_prefix))

        # Rows
        intro_table.add_row("Internet", INTERNET_IP)
        # If the interface is disabled I have one or zero regex match so I check 5 items

        RICH_CONSOLE.print(intro_table)
    else:
        pass
    return
interfaces_table()