#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import argparse
from datetime import datetime
from scapy.all import sr1
from scapy.all import IP
from scapy.all import ICMP

class FirstApp(cmd2.Cmd):
   prompt = "# "
   intro = "Welcome! This is an intro"

   ping_parser = cmd2.Cmd2ArgumentParser()
   ping_parser.add_argument('-a', '--address', type=str, help='IP Address')
   ping_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')

   @cmd2.with_argparser(ping_parser)
   def do_ping(self, args):
      for i in range(0,int(args.repeat)):
         icmp = IP(dst=args.address)/ICMP()
         resp = sr1(icmp,timeout=2,verbose=False)
         if resp == None:
            print("Unreachable")
         else:
            print("OK!")
if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())