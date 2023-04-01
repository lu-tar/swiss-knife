#!/usr/bin/env python
'''
-------------------A multipurpose shell for networking / sysadmin tasks written in Python cmd2-------------------
GitHub: https://github.com/lu-tar/swiss-knife
Spring to-do list:
[ ] Change local ip address from static to dynamic
[ ] Feature to spawn a cmd.exe process + a specific ping to leaving the swiss knife shell free
[ ] Bandwidth check
[ ] Port scanner
[ ] Byte calculator
[ ] IP Geolocalization
[ ] Crack password 7 with https://github.com/theevilbit/ciscot7 + other decryption tools
[ ] Find a mac address vendor with https://macvendors.com/api
[ ] Search a file for a list of keyword like an automated grep
[ ] Tree listing files in directory + test on remote like Sharepoint
[ ] Generate gncrypted notes on the fly
[ ] Obsidian markdown integration + cheatsheet
[ ] File sharing with VPS / FTP automation
[ ] SSH automation + template
[ ] HTTP / FTP / SFTP / TFTP portable server
[ ] General Windows app automation maybe with PyAutogui or Selenium
[ ] Add templates to swiss knife
[ ] MD5 / SHA256 calculator
----------------------------------------------------------------------------------------------------------------
'''
import cmd2, subprocess, re, requests, platform, csv, ipaddress, calendar
from scapy.all import sr1, IP, ICMP
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
from tcp_latency import measure_latency
from ipaddress import ip_network

# Globals chilling on top of the code
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
BANNER = False
#INTERNET_IP = str(requests.get("https://api.ipify.org?format=text").text)
INTERNET_IP = "Do not disturb API"
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

interfaces_table()

#
# CMD LOOP APP
#
class FirstApp(cmd2.Cmd):
   prompt = "# "
   intro = "Welcome! This is an intro " + CLOCK_TIME + "\n"
   #
   # Pulling mac vendor from https://api.macvendors.com/FC:FB:FB:01:FA:21
   def do_mac(selg,args):
      print(requests.get("https://api.macvendors.com/" + args).text)

   # time
   def do_time(self,args):
      CURRENT_TIME = datetime.now()
      CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
      year = CURRENT_TIME.strftime("%Y")
      month = CURRENT_TIME.strftime("%m")
      print(CLOCK_TIME)
      print(calendar.month(int(year), int(month)))

   # nslookup
   def do_nslookup(self,args):
      nslookup_cmd = subprocess.run(["nslookup",str(args)], stdout=subprocess.PIPE)
      print(nslookup_cmd.stdout.decode('utf-8', 'ignore'))

   # subnet printer from decimal value
   def do_sub(self,args):
      mask = int(args)
      if mask > 32 or mask < 0:
         pass
      else:
         bin_train = "00000000000000000000000000000000"
         bin_train = bin_train.replace("0","1",mask)
         first_oct = int(bin_train[0:8],2)
         second_oct = int(bin_train[8:16],2)
         third_oct = int(bin_train[16:24],2)
         fourth_oct = int(bin_train[24:32],2)

         print ("%s.%s.%s.%s" % (first_oct, second_oct, third_oct, fourth_oct))


   # ipaddress — IPv4/IPv6 manipulation library
   ipadd_parser = cmd2.Cmd2ArgumentParser()
   ipadd_parser.add_argument('-c', '--check', dest='ipadd', type=str, nargs='?', help='Apply is_multicast, is_private ecc')
   @cmd2.with_argparser(ipadd_parser)
   def do_ipadd(ipadd, args):
      only_ip = re.findall(IP_REGEX, args.ipadd)
      print(only_ip[0])
      print("is_private: %s\nis_multicast: %s\nis_reserved: %s" % 
      (ipaddress.ip_address(only_ip[0]).is_private,
      ipaddress.ip_address(only_ip[0]).is_multicast,
      ipaddress.ip_address(only_ip[0]).is_reserved
      ))
      print(list(ip_network(args.ipadd).hosts()))

   
   # Putty automation: the command putty will open by default a ssh connection with admin and port 22, telnet is optional
   putty_parser = cmd2.Cmd2ArgumentParser()
   putty_parser.add_argument(dest='host', type=str)
   putty_parser.add_argument('-p', '--port', type=str, default="22", nargs='?', help='Destination port')
   putty_parser.add_argument('-l', '--username', type=str, default="admin", nargs='?', help='Username')
   putty_parser.add_argument('-pw', '--password', type=str, nargs='?', help='Measure_putty timeout')
   putty_parser.add_argument('-t', '--telnet', default=False, action='store_true', help='telnet session')
   @cmd2.with_argparser(putty_parser)
   def do_putty(self, args):
      if args.telnet == True:
         subprocess.Popen(["C:\Program Files\PuTTY\putty.exe", "-telnet", args.host], stdout=subprocess.PIPE)
      elif args.password == None:
         subprocess.Popen(["C:\Program Files\PuTTY\putty.exe", "-ssh", args.host, "-l", args.username, "-P", args.port], stdout=subprocess.PIPE)
      else:
         subprocess.Popen(["C:\Program Files\PuTTY\putty.exe", "-ssh", args.host, "-l", args.username, "-pw", args.password, "-P", args.port], stdout=subprocess.PIPE)
   
   
   # Binary to decimal conversion
   decimal_parser = cmd2.Cmd2ArgumentParser()
   decimal_parser.add_argument(dest='value', type=int, help='Binary to decimal conversion')
   @cmd2.with_argparser(decimal_parser)
   def do_decimal(self, args):
      decimal = 0
      power = 1
      while args.value>0:
         resto = args.value%10
         args.value = args.value//10
         decimal += resto*power
         power = power*2
      print(decimal)

   # Decimal to binary conversion
   binary_parser = cmd2.Cmd2ArgumentParser()
   binary_parser.add_argument(dest='value', type=int, help='Decimal to binary conversion')
   @cmd2.with_argparser(binary_parser)
   def do_binary(self, args):
      print(bin(args.value)[2:])

   # Port/protocol finder
   portlist_parser = cmd2.Cmd2ArgumentParser()
   portlist_parser.add_argument(dest='value', help='Port or protocol')
   @cmd2.with_argparser(portlist_parser)
   def do_portlist(self, args):
      with open('csv/service-names-port-numbers.csv', 'r') as file:
         reader = csv.reader(file, delimiter=",")
         # isinstance e' meglio di type
         if isinstance(args.value,str):
            for row in reader:
               if args.value in row:
                  print(row[:4])
         else:
            for row in reader:
               if re.search(r'\b' + args.value + r'\b', str(row)):
                  print(row[:4])


   # tcpRTT calcs TCP RTT to a host usig tcp_latency library
   # common arguments like port number (443 by default), repetitions and timeout (both 5 and 1 by default)
   # if strict is specified only the latency is displayer not the ping-like statistics
   latency_parser = cmd2.Cmd2ArgumentParser()
   latency_parser.add_argument(dest='host', type=str, help='Measure the TCP latency between you to a specified host')
   latency_parser.add_argument('-p', '--port', type=int, default=443, nargs='?', help='Destination port')
   latency_parser.add_argument('-r', '--repeat', type=int, default=5, nargs='?', help='How many time measure_latency runs')
   latency_parser.add_argument('-t', '--timeout', type=int, default=1, nargs='?', help='Measure_latency timeout')
   latency_parser.add_argument('-s', '--strict', default=False, action='store_true', help='Strict output')
   @cmd2.with_argparser(latency_parser)
   def do_tcpRTT(self, args):
      if args.strict:
         latency_results = measure_latency(host=args.host, runs=args.repeat, timeout=args.timeout, port=args.port)
         for i in latency_results:
            print(str(round(i,2)))
      else:
         measure_latency(host=args.host, runs=args.repeat, timeout=args.timeout, port=args.port, human_output=True)

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
   def do_wifistat(self, args):
      CURRENT_TIME = datetime.now()
      CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
      netsh_wifi_stats = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
      outStr = netsh_wifi_stats.stdout.decode('utf-8', 'ignore')
      if "disconnessa" in outStr:
         print("No Wi-fi connection")
      elif "Non disponibile" in outStr:
         print("No Wi-fi connection")
      else:
         # Need improvments
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
         wifi_table = Table(title="Wi-Fi statistics from netsh")
         # Columns
         wifi_table.add_column("⏱️", justify="center", style="white")
         wifi_table.add_column("BSSID", justify="center", style="white")
         wifi_table.add_column("Download rate", justify="center", style="yellow")
         wifi_table.add_column("Upload rate", justify="center", style="yellow")
         wifi_table.add_column("Protocol", justify="center", style="green")
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
   
   # Ping using pythonping + if spw argument is specified the script try to open a shell pinging (NOT WORKING NEEDS ATTENTION)
   # Using uname_output we can check if we are in a Linux o Win machine
   ping_parser = cmd2.Cmd2ArgumentParser()
   ping_parser.add_argument(dest='address',type=str, help='IP Address')
   ping_parser.add_argument('-r', '--repeat', type=int, default=3, nargs='?', help='output [n] times')
   ping_parser.add_argument('-spw', '--spawn', default=False, action="store_true")
   ping_parser.add_argument('-t', '--loop', default=False, action="store_true")
   @cmd2.with_argparser(ping_parser)
   def do_ping(self, args):
      if OPERATING_SYSTEM == "Windows":
         if args.spawn:
            subprocess.run(["start", "cmd", "/K", "ping", "-t", args.address], shell=True)
         else:
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

   # Alias of ping -spw
   def do_pingt(self, args):
      if OPERATING_SYSTEM == "Windows":
         subprocess.run(["start", "cmd", "/K", "ping", "-t", str(args)], shell=True)
      else:
         pass

   # Latency checks
   # latency_parser = cmd2.Cmd2ArgumentParser()
   # latency_parser

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())