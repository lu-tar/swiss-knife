#!/usr/bin/env python
import cmd2
from cmd2  import categorize
import subprocess
import re
import requests
import platform
import csv
import calendar
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
from tcp_latency import measure_latency
import ipaddress
from ipaddress import ip_network

from swiss_conf import *
import swiss_func

OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"

# Pre cmd-loop
# Banner ascii
swiss_func.show_motd()
# IP list using psutils
if IP_BANNER == True:
    swiss_func.list_interfaces()
else:
    pass
# Subprocess the shell command like route print or ip route
swiss_func.list_routes()

# Cmd loop app
class SwissKnife(cmd2.Cmd):
    prompt = "# "
    intro = ''
    # Pulling mac vendor from https://api.macvendors.com/FC:FB:FB:01:FA:21
    def do_macvendor(selg, args):
        print(requests.get("https://api.macvendors.com/" + args).text)

    # Print current time and a small calendar
    def do_time(self, _):
        CURRENT_TIME = datetime.now()
        year = CURRENT_TIME.strftime("%Y")
        month = CURRENT_TIME.strftime("%m")
        print(CLOCK_TIME)
        print(calendar.month(int(year), int(month)))

    # nslookup of a host
    def do_nslookup(self, args):
        nslookup_cmd = subprocess.run(["nslookup",str(args)], stdout=subprocess.PIPE, help='nslookup [hostname]')
        print(nslookup_cmd.stdout.decode('utf-8', 'ignore'))

    # subnet printer from decimal value
    sub_parser = cmd2.Cmd2ArgumentParser()
    sub_parser.add_argument(dest='value', type=int, help='From integer to subnet')
    @cmd2.with_argparser(sub_parser)
    def do_sub(self, args):
        mask = int(args.value)
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
            subprocess.Popen([PATH_TO_PUTTY, "-telnet", args.host], stdout=subprocess.PIPE)
        elif args.password == None:
            subprocess.Popen([PATH_TO_PUTTY, "-ssh", args.host, "-l", args.username, "-P", args.port], stdout=subprocess.PIPE)
        else:
            subprocess.Popen([PATH_TO_PUTTY, "-ssh", args.host, "-l", args.username, "-pw", args.password, "-P", args.port], stdout=subprocess.PIPE)

    # Binary to decimal conversion
    decimal_parser = cmd2.Cmd2ArgumentParser()
    decimal_parser.add_argument(dest='value', type=int, help='Binary to decimal conversion')
    @cmd2.with_argparser(decimal_parser)
    def do_decimal(self, args):
        decimal = 0
        power = 1
        while args.value > 0:
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
        with open(PATH_TO_PORTS_CSV, 'r') as file:
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
    iplist_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(iplist_parser)
    def do_iplist(self, _): 
        swiss_func.list_interfaces()

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
                if args.loop == False:
                    for i in range(0, args.repeat):
                        CURRENT_TIME = datetime.now()
                        CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
                        print(CLOCK_TIME, end =" ")
                        ping(args.address, verbose=True, count=1, interval=1)
                else:
                    while True:
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
    def do_spawnping(self, args):
        if OPERATING_SYSTEM == "Windows":
            subprocess.run(["start", "cmd", "/K", "ping", "-t", str(args)], shell=True)
        else:
            pass
    
    # Change ip on Windows with command line
    def do_changeip(self, args):
        if OPERATING_SYSTEM == "Windows":
            ipv4 = input("IP address: ")
            subnet = input("Subnet mask: ")
            gateway = input("Gateway: ")
            subprocess.run(["netsh", "interface", "ipv4", "set", "name=" + str(args), "static"], shell=True)
            


    # Dividing commands in categories (help command)
    categorize((do_pub, do_iplist, do_macvendor, do_spawnping, do_tcpRTT, do_wifistat, do_nslookup, do_portlist, do_ipcheck, do_ping), "Network")
    categorize((do_binary, do_decimal, do_sub), "Calc")
    categorize((do_putty), "SSH")
    categorize((do_time), "Miscellanea")

if __name__ == '__main__':
    import sys
    c = SwissKnife()
    sys.exit(c.cmdloop())
