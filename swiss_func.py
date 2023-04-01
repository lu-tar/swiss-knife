import subprocess
from swiss_conf import *
from rich.console import Console
import platform
import re
from datetime import datetime
from rich.table import Table

OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")

# Pre cmd-loop interface info interrogation using netsh windows command
# checks OPERATING_SYSTEM to skips netsh commands and BANNER variable <-- implementare load di configurazione alla "linux"
# using api.ipify.org to pull the public ip address
def interfaces_table():
   if BANNER == True and OPERATING_SYSTEM == "Windows":
      # Netsh interrogation
      netsh_ethernet_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet"], stdout=subprocess.PIPE, shell=True)
      ethernet_output = netsh_ethernet_if.communicate()[0]
      ethernet_info = re.findall(IP_REGEX, str(ethernet_output)) # Array of IP

      netsh_wifi_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Wi-Fi"], stdout=subprocess.PIPE, shell=True)
      wifi_output = netsh_wifi_if.communicate()[0]
      wifi_info = re.findall(IP_REGEX, str(wifi_output)) # Array of IP

      netsh_eth_usb_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet 7"], stdout=subprocess.PIPE, shell=True)
      eth_usb_output = netsh_eth_usb_if.communicate()[0]
      eth_usb_info = re.findall(IP_REGEX, str(eth_usb_output)) # Array of IP

      # Intro table
      intro_table = Table(title="My ip configuration")
      # Columns
      intro_table.add_column("🐢", justify="center", style="white")
      intro_table.add_column("IP", justify="center", style="cyan")
      intro_table.add_column("Network", justify="center", style="green")
      intro_table.add_column("Mask", justify="center", style="green")
      intro_table.add_column("Gate", justify="center", style="green")
      intro_table.add_column("DNS", justify="center", style="magenta")
      # Rows
      intro_table.add_row("Internet", INTERNET_IP)
      if len(ethernet_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
         intro_table.add_row("Ethernet",ethernet_info[0], ethernet_info[1], ethernet_info[2], ethernet_info[3], ethernet_info[4])
      else:
         pass
      if len(wifi_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
         intro_table.add_row("Wi-Fi", wifi_info[0], wifi_info[1], wifi_info[2], wifi_info[3], wifi_info[4])
      else:
         pass
      if len(eth_usb_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
         intro_table.add_row("Ethernet USB-C",eth_usb_info[0], eth_usb_info[1], eth_usb_info[2], eth_usb_info[3], eth_usb_info[4])
      else:
         pass

      RICH_CONSOLE.print(intro_table)
   else:
      pass
   return