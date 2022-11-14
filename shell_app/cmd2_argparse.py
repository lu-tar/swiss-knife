#!/usr/bin/env python
import cmd2, subprocess, re, requests, platform
from scapy.all import sr1, IP, ICMP
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
from tcp_latency import measure_latency

# Globals chilling on top of the code
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
BANNER = True
#INTERNET_IP = str(requests.get("https://api.ipify.org?format=text").text)
INTERNET_IP = "Do not disturb API"
OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")

# Pre cmd-loop interface info interrogation using netsh windows command
# checks OPERATING_SYSTEM to skips netsh commands
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

interfaces_table()

#
# CMD LOOP APP
#
class FirstApp(cmd2.Cmd):
   prompt = "# "
   intro = "Welcome! This is an intro " + CLOCK_TIME + "\n"

   # Show interfaces: 
   # default is eth
   # verbose and wifi with args
   ip_parser = cmd2.Cmd2ArgumentParser()
   ip_parser.add_argument('-w', '--wifi', default=False, action='store_true', help='show wireless interface ip')
   ip_parser.add_argument('-v', '--verbose', default=False, action='store_true', help='show interfaces table')
   ip_parser.add_argument('-usb', '--usb', default=False, action='store_true', help='show usb-c interface ip')
   @cmd2.with_argparser(ip_parser)
   def do_ip(self, args):
      if args.verbose:
         interfaces_table()
      elif args.wifi:
         netsh_wifi_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Wi-Fi"], stdout=subprocess.PIPE, shell=True)
         wifi_output = netsh_wifi_if.communicate()[0]
         wifi_info = re.findall(IP_REGEX, str(wifi_output)) # Array of IP
         if len(wifi_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
            for i in ethernet_info: print(i, end=" ")
            print("\n")
      elif args.usb:
         netsh_eth_usb_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet 7"], stdout=subprocess.PIPE, shell=True)
         eth_usb_output = netsh_eth_usb_if.communicate()[0]
         eth_usb_info = re.findall(IP_REGEX, str(eth_usb_output)) # Array of IP
         if len(eth_usb_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
            for i in eth_usb_info: print(i, end=" ")
            print("\n")
      else:
         netsh_ethernet_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet"], stdout=subprocess.PIPE, shell=True)
         ethernet_output = netsh_ethernet_if.communicate()[0]
         ethernet_info = re.findall(IP_REGEX, str(ethernet_output)) # Array of IP
         if len(ethernet_info) == 5: # If the interface is disabled I have one or zero regex match so I check 5 items
            for i in ethernet_info: print(i, end=" ")
            print("\n")


   # Show wifi statistics from netsh
   def do_wifistat(self):
      CURRENT_TIME = datetime.now()
      CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
      netsh_wifi_stats = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
      outStr = netsh_wifi_stats.stdout.decode('utf-8', 'ignore')
      if "disconnessa" in outStr:
         print("No Wi-fi connection")
      else:
         for e in outStr.splitlines():
            if "BSSID" in e: 
               bssid = e[29:]
            elif "Canale" in e: 
               channel = e[27:]
            elif "ricezione" in e: 
               downRate = e[32:]
            elif "trasmissione" in e: 
               upRate = e[34:]
            elif "frequenza" in e: 
               fq = e[29:]
            elif "Segnale" in e: 
               signal = e[26:]

         #print ("%s, %s, %s, %s, %s, %s" % (bssid, channel, downRate, upRate, fq, signal))
         # Wifi statistics table from netsh
         wifi_table = Table(title="Wi-Fi statistics")
         # Columns
         wifi_table.add_column("⏱️", justify="center", style="white")
         wifi_table.add_column("BSSID", justify="center", style="white")
         wifi_table.add_column("Download rate", justify="center", style="yellow")
         wifi_table.add_column("Upload rate", justify="center", style="yellow")
         wifi_table.add_column("Frequency", justify="center", style="green")
         wifi_table.add_column("Channel", justify="center", style="green")
         wifi_table.add_column("Signal", justify="center", style="green")
         # Rows
         wifi_table.add_row(CLOCK_TIME, bssid, downRate, upRate, fq, channel, signal)
         RICH_CONSOLE.print(wifi_table)

   # Show my public IP address
   pubip_parser = cmd2.Cmd2ArgumentParser()
   pubip_parser.add_argument('-v', '--verbose', default=False, action='store_true', help='show ip public info from ifconfing.co API')
   @cmd2.with_argparser(pubip_parser)
   def do_pub(self, args):
      if args.verbose:
         print("Verbose API call")
         ifconfig_api = requests.get("http://ifconfig.co/json").json()
         print(ifconfig_api)
      else:
         print(INTERNET_IP)

   # Ping using scapy lib
   sping_parser = cmd2.Cmd2ArgumentParser()
   sping_parser.add_argument(dest='sping_ip',type=str, help='IP Address')
   sping_parser.add_argument('-r', '--repeat', type=int, default=3, nargs='?', help='output [n] times')
   @cmd2.with_argparser(sping_parser)
   def do_sping(self, args):
      for i in range(0,args.repeat):
         icmp = IP(dst=args.sping_ip)/ICMP()
         resp = sr1(icmp,timeout=2,verbose=False)
         if resp == None:
            print("Unreachable")
         else:
            print("OK!")
   
   # Ping using pythonping + if spw argument is specified the script try to open a shell pinging
   # Using uname_output we can check if we are in a Linux o Win machine
   ping_parser = cmd2.Cmd2ArgumentParser()
   ping_parser.add_argument(dest='address',type=str, help='IP Address')
   ping_parser.add_argument('-r', '--repeat', type=int, default=3, nargs='?', help='output [n] times')
   ping_parser.add_argument('-spw', '--spawn', default=False, action="store_true")
   @cmd2.with_argparser(ping_parser)
   def do_ping(self, args):
      if OPERATING_SYSTEM == "Windows":
         if args.spawn:
            for i in range(0,args.repeat):
               CURRENT_TIME = datetime.now()
               CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
               print(CLOCK_TIME, end =" ")
               ping(args.address, verbose=True, count=1, interval=1)
      else:
         if args.spawn:
            #with open ("ping_conf", "w") as file:
            #   file.write(args.address + "\n" + args.repeat)
            subprocess.Popen('x-terminal-emulator -e "bash -c \\"ping 1.1.1.1; exec bash\\""', shell=True)
   
   # Latency checks
   # latency_parser = cmd2.Cmd2ArgumentParser()
   # latency_parser

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())