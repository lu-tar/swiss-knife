#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import argparse
from scapy.all import sr1, IP, ICMP
from pythonping import ping
from datetime import datetime
import time
import subprocess
from subprocess import Popen, PIPE
print("Ho")
class FirstApp(cmd2.Cmd):
   CURRENT_TIME = datetime.now()
   CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
   prompt = "# "
   intro = "Welcome! This is an intro " + CLOCK_TIME 

   sping_parser = cmd2.Cmd2ArgumentParser()
   sping_parser.add_argument(dest='sping_ip',type=str, help='IP Address')
   sping_parser.add_argument('-r', '--repeat', type=int, default=3, nargs='?', help='output [n] times')

   ping_parser = cmd2.Cmd2ArgumentParser()
   ping_parser.add_argument(dest='address',type=str, help='IP Address')
   ping_parser.add_argument('-r', '--repeat', type=int, default=3, nargs='?', help='output [n] times')
   ping_parser.add_argument('-spw', '--spawn', default=False, action="store_true")

   @cmd2.with_argparser(sping_parser)
   def do_sping(self, args):
      for i in range(0,args.repeat):
         icmp = IP(dst=args.sping_ip)/ICMP()
         resp = sr1(icmp,timeout=2,verbose=False)
         if resp == None:
            print("Unreachable")
         else:
            print("OK!")

   @cmd2.with_argparser(ping_parser)
   def do_ping(self, args):
      if args.spawn:
         #with open ("ping_conf", "w") as file:
         #   file.write(args.address + "\n" + args.repeat)
         subprocess.Popen('x-terminal-emulator -e "bash -c \\"ping 1.1.1.1; exec bash\\""', shell=True)
      else:
         for i in range(0,args.repeat):
            CURRENT_TIME = datetime.now()
            CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
            print(CLOCK_TIME, end =" ")
            ping(args.address, verbose=True, count=1, interval=1)
"""
parser = argparse.ArgumentParser()
parser.add_argument("--do-something", default=False, action="store_true")
arguments = parser.parse_args()
if arguments.do_something:
     print("Do something")
else:
     print("Don't do something")
"""

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())