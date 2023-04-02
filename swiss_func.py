# Custom configuration
from swiss_conf import *
import platform
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
import requests
import netifaces

OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
INTERNET_IP = str(requests.get("https://api.ipify.org?format=text").text)

def interfaces_table():
    if BANNER == True:

        # Intro table
        intro_table = Table(title="My IP configuration")

        # Set columns
        intro_table.add_column("🐢", justify="center", style="white")
        intro_table.add_column("IP", justify="center", style="cyan")
        intro_table.add_column("Subnet", justify="center", style="cyan")
        intro_table.add_column("Gate", justify="center", style="green")
        intro_table.add_column("DNS", justify="center", style="magenta")

        # Using a list comprehension to find the difference 
        # between etifaces.interfaces() and IP_INTERFACES_IGNORE
        interfaces_list = [x for x in netifaces.interfaces() if x not in IP_INTERFACES_IGNORE]

        # Rows
        intro_table.add_row("Internet", INTERNET_IP)
        default_gateway = netifaces.gateways()
        for if_name in interfaces_list:
            if_specs = netifaces.ifaddresses(if_name)
            try:
                intro_table.add_row(if_name, 
                                    if_specs[netifaces.AF_INET][0]['addr'],
                                    if_specs[netifaces.AF_INET][0]['netmask'],
                                    default_gateway['default'][netifaces.AF_INET][0])
            except:
                print("An error occurred reading network interfaces")
        RICH_CONSOLE.print(intro_table)
    else:
        pass
    return