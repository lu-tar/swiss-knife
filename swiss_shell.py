#!/usr/bin/env python
#
#
# 
#                   ▀██     
#             ▄▄▄▄   ██  ▄▄ 
#            ██▄ ▀   ██ ▄▀   
#            ▄ ▀█▄▄  ██▀█▄   
#            █▀▄▄█▀ ▄██▄ ██▄
#    ---------swiss-knife---------
#   Author: https://github.com/lu-tar
#
#
#
#
#
import cmd2
import os
import re
import requests
from platform import system
import csv
from pathlib import Path
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
from tcp_latency import measure_latency
from ipaddress import ip_network, ip_address, is_multicast, is_private, is_reserved, IPv4Network
from time import sleep

from swiss_conf import *

CLOCK_FORMAT = "%H:%M:%S"
# Banner stuff
IP_BANNER = False
ASCII_BANNER = False
OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"

class SwissKnife(cmd2.Cmd):
    prompt = "# "
    intro = ''

    # subnet printer from decimal value -------------------------------------------------------
    subnet_parser = cmd2.Cmd2ArgumentParser()
    subnet_parser.add_argument(dest='value', type=int, help='From integer to subnet')
    @cmd2.with_argparser(subnet_parser)
    def do_subnet(self, args):
        prefix_length = args.value
        if prefix_length < 0 or prefix_length > 32:
            self.perror(f"Error: CIDR prefix length must be between 0 and 32, got {prefix_length}")
            return
        try:
            # Use ipaddress module for cleaner implementation
            network = ipaddress.IPv4Network(f"0.0.0.0/{prefix_length}", strict=False)
            subnet_mask = str(network.netmask)
            self.poutput(f"/{prefix_length} = {subnet_mask}")
            
        except Exception as e:
            self.perror(f"Error calculating subnet mask: {e}")

    # ipaddress — IPv4/IPv6 manipulation library -----------------------------------------------
    ipcheck_parser = cmd2.Cmd2ArgumentParser()
    ipcheck_parser.add_argument(dest='ipcheck', type=str, nargs='?', help='Apply is_multicast, is_private ecc')
    @cmd2.with_argparser(ipcheck_parser)
    def do_ipcheck(ipcheck, args):
        only_ip = re.findall(IP_REGEX, args.ipcheck)
        print(only_ip[0])
        print("is_private: %s\nis_multicast: %s\nis_reserved: %s" %
            (ipaddress.ip_address(only_ip[0]).is_private,
            ipaddress.ip_address(only_ip[0]).is_multicast,
            ipaddress.ip_address(only_ip[0]).is_reserved
            )
        )
        print(list(ip_network(args.ipcheck).hosts()))

    # Binary to decimal conversion ----------------------------------------------------------------
    decimal_parser = cmd2.Cmd2ArgumentParser()
    decimal_parser.add_argument(dest='value', type=int, help='Binary to decimal conversion')
    @cmd2.with_argparser(decimal_parser)
    def do_decimal(self, args):
        binary_str = args.value.strip()
        try:
            # Method 1: Using Python's built-in int() function (recommended)
            decimal = int(binary_str, 2)
            self.poutput(f"Binary {args.value} = Decimal {decimal}")
        except ValueError as e:
            self.perror(f"Error converting binary to decimal: {e}")

    # Decimal to binary conversion ----------------------------------------------------------------
    binary_parser = cmd2.Cmd2ArgumentParser()
    binary_parser.add_argument(dest='value', type=int, help='Decimal to binary conversion')
    @cmd2.with_argparser(binary_parser)
    def do_binary(self, args):
        print(bin(args.value)[2:])

    # tcpRTT calcs TCP RTT to a host usig tcp_latency library
    # common arguments like port number (443 by default), repetitions and timeout (both 5 and 1 by default)
    # if strict is specified only the latency is displayer not the ping-like statistics
    latency_parser = cmd2.Cmd2ArgumentParser()
    latency_parser.add_argument(dest='host', type=str, help='Measure the TCP latency between you to a specified host. Port 443, 5 repetitions and 1 s timeout is the default)')
    latency_parser.add_argument('-p', '--port', type=int, default=443, nargs='?', help='Destination port')
    latency_parser.add_argument('-r', '--repeat', type=int, default=5, nargs='?', help='How many time measure_latency runs')
    latency_parser.add_argument('-t', '--timeout', type=int, default=1, nargs='?', help='Measure_latency timeout')
    latency_parser.add_argument('-s', '--strict', default=False, action='store_true', help='Strict output')
    @cmd2.with_argparser(latency_parser)
    def do_tcpRTT(self, args):
        #print ("%s, %s, %s, %s, %s, %s" % (bssid, channel, downRate, upRate, fq, signal))
        print("Repetitions: %s, Timeout: %s, Port: %s" % (args.repeat, args.timeout, args.port))
        if args.strict:
            latency_results = measure_latency(host=args.host, runs=args.repeat, timeout=args.timeout, port=args.port)
            for i in latency_results:
                print(str(round(i,2)))
        else:
            measure_latency(host=args.host, runs=args.repeat, timeout=args.timeout, port=args.port, human_output=True)

    # Dividing commands in categories (help command)
    # categorize((do_debug), "WLC debug parser")
    # categorize((do_pub, do_iplist, do_macvendor, do_tcpRTT, do_wifistat, do_nslookup, do_portlist, do_ipcheck, do_ping, do_changeip), "Network")
    # categorize((do_binary, do_decimal, do_subnet), "Calc")
    # categorize((do_putty), "SSH")
    # categorize((do_fp), "Files")
    # categorize((do_fire, do_openapps), "Browser and apps")
    # categorize((do_time, do_hello), "Miscellanea")
    # categorize((do_syslog), "Server")

if __name__ == '__main__':
    import sys
    shell_app = SwissKnife()

    # Pre cmd-loop ----------------------------------------------------------------------
    # Banner ascii
    swiss_func.show_motd()
    
    sys.exit(shell_app.cmdloop())