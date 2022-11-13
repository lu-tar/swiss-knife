#!/usr/bin/env python
import cmd2, subprocess, re, requests, platform
from scapy.all import sr1, IP, ICMP
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table

# Globals chilling on top of the code
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
BANNER = False
#INTERNET_IP = str(requests.get("https://api.ipify.org?format=text").text)
INTERNET_IP = "Do not disturb API during tests"
OPERATING_SYSTEM = platform.system()

# Pre cmd-loop interface info interrogation using netsh windows command
# checks OPERATING_SYSTEM to skips netsh commands
# using api.ipify.org to pull the public ip address

if BANNER == True and OPERATING_SYSTEM == "Windows":
   # Netsh interrogation
   netsh_ethernet_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet"], stdout=subprocess.PIPE, shell=True)
   ethernet_output = netsh_ethernet_if.communicate()[0]
   ethernet_info = re.findall(IP_REGEX, str(ethernet_output))

   netsh_wifi_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Wi-Fi"], stdout=subprocess.PIPE, shell=True)
   wifi_output = netsh_wifi_if.communicate()[0]
   wifi_info = re.findall(IP_REGEX, str(wifi_output))

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
   intro_table.add_row("Ethernet",ethernet_info[0], ethernet_info[1], ethernet_info[2], ethernet_info[3], ethernet_info[4])
   intro_table.add_row("Wi-Fi", wifi_info[0], wifi_info[1], wifi_info[2], wifi_info[3], wifi_info[4])

   console = Console()
   console.print(intro_table)
else:
   pass

#
# CMD LOOP
#
class FirstApp(cmd2.Cmd):
   CURRENT_TIME = datetime.now()
   CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
   prompt = "# "
   intro = "Welcome! This is an intro " + CLOCK_TIME + "\n"

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
      if uname_output != "":
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

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())