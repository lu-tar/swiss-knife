#!/usr/bin/env python
import cmd2
from scapy.all import sr1, IP, ICMP
from pythonping import ping
from datetime import datetime
import subprocess
import re
import requests
# Pre cmd-loop interface info interrogation using netsh windows command
# if ver is empty you are in Linux machines and the script skips netsh commands
# using api.ipify.org to pull the public ip address
print("Public IP:" + str(requests.get("https://api.ipify.org?format=text").text))
uname = subprocess.Popen(["ver"], stdout=subprocess.PIPE, shell=True)
uname_output = uname.communicate()[0]
if uname_output == "":
   pass
else:
   netsh_ethernet_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet"], stdout=subprocess.PIPE, shell=True)
   ethernet_output = netsh_ethernet_if.communicate()[0]
   ethernet_info = re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", str(ethernet_output))
   print("Ethernet IP:", end=" ")
   for i in ethernet_info: print(i, end=" ")
   print("\n")
   netsh_wifi_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Wi-Fi"], stdout=subprocess.PIPE, shell=True)
   wifi_output = netsh_wifi_if.communicate()[0]
   wifi_info = re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", str(wifi_output))
   print("Wi-Fi IP:", end=" ")
   for i in wifi_info: print(i, end=" ")
   print("\n")
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