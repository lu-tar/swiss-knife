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
from cmd2  import categorize
import subprocess
import re
import requests
import platform
import csv
import calendar
import webbrowser
from pathlib import Path
from pythonping import ping
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print
from tcp_latency import measure_latency
import ipaddress
from ipaddress import ip_network
from time import sleep
from progress.spinner import MoonSpinner

from swiss_conf import *
import swiss_func
import swiss_automation

OPERATING_SYSTEM = platform.system()
RICH_CONSOLE = Console()
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
IP_REGEX = "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
FIREFOX_PATH="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
webbrowser.register('firefox', None,webbrowser.BackgroundBrowser(FIREFOX_PATH))

class SwissKnife(cmd2.Cmd):
    prompt = "# "
    intro = ''

    # Pulling mac vendor from https://api.macvendors.com/FC:FB:FB:01:FA:21
    def do_macvendor(selg, args):
        try:
            print(requests.get("https://api.macvendors.com/" + args).text)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Print current time and a small calendar ------------------------------------------------
    def do_time(self, _):
        CURRENT_TIME = datetime.now()
        year = CURRENT_TIME.strftime("%Y")
        month = CURRENT_TIME.strftime("%m")
        print(CLOCK_TIME)
        print(calendar.month(int(year), int(month)))

    # nslookup of a host ----------------------------------------------------------------------
    nslookup_parser = cmd2.Cmd2ArgumentParser()
    nslookup_parser.add_argument(dest='value', type=str, help='DNS lookup of a hostname')
    @cmd2.with_argparser(nslookup_parser)
    def do_nslookup(self, args):
        nslookup_cmd = subprocess.run(["nslookup", args.value], stdout=subprocess.PIPE)
        print(nslookup_cmd.stdout.decode('utf-8', 'ignore'))

    # subnet printer from decimal value -------------------------------------------------------
    subnet_parser = cmd2.Cmd2ArgumentParser()
    subnet_parser.add_argument(dest='value', type=int, help='From integer to subnet')
    @cmd2.with_argparser(subnet_parser)
    def do_subnet(self, args):
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

    # Putty automation: the command putty will open by default a ssh connection with admin and port 22, telnet is optional
    putty_parser = cmd2.Cmd2ArgumentParser()
    putty_parser.add_argument(dest='host', type=str)
    putty_parser.add_argument('-p', '--port', type=str, default="22", nargs='?', help='Destination port')
    putty_parser.add_argument('-l', '--username', type=str, default="admin", nargs='?', help='Username')
    putty_parser.add_argument('-pw', '--password', type=str, nargs='?', help='SSH password')
    putty_parser.add_argument('-t', '--telnet', default=False, action='store_true', help='telnet session')
    @cmd2.with_argparser(putty_parser)
    def do_putty(self, args):
        if args.telnet == True:
            subprocess.Popen([PATH_TO_PUTTY, "-telnet", args.host], stdout=subprocess.PIPE)
        elif args.password == None:
            subprocess.Popen([PATH_TO_PUTTY, "-ssh", args.host, "-l", args.username, "-P", args.port], stdout=subprocess.PIPE)
        else:
            subprocess.Popen([PATH_TO_PUTTY, "-ssh", args.host, "-l", args.username, "-pw", args.password, "-P", args.port], stdout=subprocess.PIPE)

    # Binary to decimal conversion ----------------------------------------------------------------
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

    # Decimal to binary conversion ----------------------------------------------------------------
    binary_parser = cmd2.Cmd2ArgumentParser()
    binary_parser.add_argument(dest='value', type=int, help='Decimal to binary conversion')
    @cmd2.with_argparser(binary_parser)
    def do_binary(self, args):
        print(bin(args.value)[2:])

    # Port/protocol finder ------------------------------------------------------------------------
    portlist_parser = cmd2.Cmd2ArgumentParser()
    portlist_parser.add_argument(dest='value', help='Port or protocol')
    @cmd2.with_argparser(portlist_parser)
    def do_portlist(self, args):
        try:
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
        except FileNotFoundError:
                print(f"{PATH_TO_PORTS_CSV} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

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

    # Show interfaces:
    # default is eth
    # verbose and wifi with args
    iplist_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(iplist_parser)
    def do_iplist(self, _): 
        swiss_func.list_interfaces()

    # Show wifi statistics from netsh -----------------------------------------------------------
    def do_wifistat(self, args):
        CURRENT_TIME = datetime.now()
        CLOCK_TIME = CURRENT_TIME.strftime("%H:%M:%S")
        netsh_wifi_stats = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
        out_string = netsh_wifi_stats.stdout.decode('utf-8', 'ignore')
        if "disconnessa" in out_string:
            print("No Wi-fi connection")
        # Conflitto con stringa "Stato rete ospitata  : Non disponibile"
        #elif "Non disponibile" in out_string:
        #    print("No Wi-fi connection")
        else:
            # Need improvments
            for e in out_string.splitlines():
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
            wifi_table.add_column("Time", justify="center", style="white")
            wifi_table.add_column("BSSID", justify="center", style="white")
            wifi_table.add_column("Download", justify="center", style="yellow")
            wifi_table.add_column("Upload", justify="center", style="yellow")
            wifi_table.add_column("Protocol", justify="center", style="green")
            wifi_table.add_column("Channel", justify="center", style="green")
            wifi_table.add_column("Signal", justify="center", style="green")
            # Rows
            wifi_table.add_row(CLOCK_TIME, bssid, downRate, upRate, fq, channel, signal)
            RICH_CONSOLE.print(wifi_table)

    # Show my public IP address ---------------------------------------------------------------
    pubip_parser = cmd2.Cmd2ArgumentParser()
    pubip_parser.add_argument('-v', '--verbose', default=False, action='store_true', help='show ip public info from ifconfing.co API')
    @cmd2.with_argparser(pubip_parser)
    def do_pub(self, args):
        if args.verbose:
            try:
                print("Verbose API call")
                print(requests.get("http://ifconfig.co/json").json())
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            try:
                print(requests.get("https://api.ipify.org?format=text").text)
            except Exception as e:
                print(f"An error occurred: {e}")
    # Ping using pythonping + if spw argument is specified the script try to open a shell pinging (NOT WORKING NEEDS ATTENTION)
    # Using uname_output we can check if we are in a Linux o Win machine
    ping_parser = cmd2.Cmd2ArgumentParser()
    ping_parser.add_argument(dest='address', type=str, help='IP Address')
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
                        CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
                        print(CLOCK_TIME, end =" ")
                        ping(args.address, verbose=True, count=1, interval=1)
                else:
                    while True:
                        CURRENT_TIME = datetime.now()
                        CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)
                        print(CLOCK_TIME, end =" ")
                        ping(args.address, verbose=True, count=1, interval=1)
        else:
            if args.spawn:
                subprocess.Popen('x-terminal-emulator -e "bash -c \\"ping 1.1.1.1; exec bash\\""', shell=True)

    # Opening a list of programs with external bat if OS is Windows
    # https://builtin.com/software-engineering-perspectives/python-progress-bar
    openapps_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(openapps_parser)
    def do_openapps(self, _):
        if OPERATING_SYSTEM == "Windows":
            try:
                with open(OPENAPPS_SCRIPT, 'r') as file:
                    line_list = file.read().splitlines()
                    for i in line_list: print (i)
            except FileNotFoundError:
                print(f"{OPENAPPS_SCRIPT} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")
            with MoonSpinner('CTRL+C to stop openapps.bat') as bar:
                for i in range(6):
                    sleep(0.5)
                    bar.next()
            subprocess.call([OPENAPPS_SCRIPT])
        else:
            print(OPERATING_SYSTEM)

    # Grepping file for common strings. Logic change by args. -------------------------------------------
    file_parser = cmd2.Cmd2ArgumentParser()
    file_parser.add_argument(dest='filepath', type=str, help='File path to the debug file')
    file_parser.add_argument('-t', '--template', type=str, default=("debug"), choices=["debug", "log", "techs", "associations", "timeouts", "reason", "state"])
    #grep_parser.add_argument('-fp', '--filepath', type=str, help='Just the filename')
    @cmd2.with_argparser(file_parser)
    def do_fp(self, args):
        if args.template == 'state':
            search_patterns = swiss_func.compile_patterns(CLIENT_STATE_REGEX)
        elif args.template == 'log':
            search_patterns = swiss_func.compile_patterns(LOG_REGEX)
        elif args.template == 'reason':
            search_patterns = swiss_func.compile_patterns(REASON_REGEX)
        elif args.template == 'timeouts':
            search_patterns = swiss_func.compile_patterns(TIMEOUT_REGEX)
        elif args.template == 'associations':
            search_patterns = swiss_func.compile_patterns(ASSOCIATION_REGEX)
        elif args.template == 'debug':
            search_patterns = swiss_func.compile_patterns(DEBUG_REGEX)
        else:
            print("Template non implementato")
        swiss_func.grep_file(args.filepath, search_patterns)
        

    # Change ip on Windows with command line --------------------------------------------------------------
    changeip_parser = cmd2.Cmd2ArgumentParser()
    changeip_parser.add_argument(dest='interface_name', type=str, help='Interface name like "Ethernet"')
    changeip_parser.add_argument('-dhcp', '--dhcp', default=False, action="store_true", help="Change ip to static/dynamic using netsh")
    @cmd2.with_argparser(changeip_parser)
    def do_changeip(self, args):
        if OPERATING_SYSTEM == "Windows":
            if args.dhcp == False:
                # Collect
                print("Working on interface: " + args.interface_name)
                input_ipv4 = input("IP address: ")
                input_subnet = input("Subnet mask: ")
                input_gateway = input("Gateway: ")
                subprocess.run(["netsh", "interface", "ipv4", "set", "address", "name=" + args.interface_name, "static", input_ipv4, input_subnet, input_gateway], shell=True)
            else:
                # -dhcp is True then set the interface to dhcp
                subprocess.run(["netsh", "interface", "ipv4", "set", "address", "name=" + args.interface_name, "source=dhcp"], shell=True)
        else:
            print(OPERATING_SYSTEM)
    
    # WLC Debug parser with DB integration ------------------------------------------------------------------
    debug_parser = cmd2.Cmd2ArgumentParser()
    debug_parser.add_argument('-f', '--filename', type=str, default='debug_parser/debugTrace_1.txt', help='File path to debug trace file, default is debug_parser/debugTrace_1.txt')
    debug_parser.add_argument('-id', '--idname', type=str, default=CURRENT_TIME.strftime("%H%M%S"), help='Set the table name, default is the time as %H%M%S')
    debug_parser.add_argument('-t', '--template', type=str, default=("state"), choices=["state", "EAP", "reasons", "association", "timeouts"], help='Select a template to parse the debug file in the db')
    @cmd2.with_argparser(debug_parser)
    def do_debug(self, args):
        swiss_func.debug_to_db(args.filename, args.idname)

    # Test command ------------------------------------------------------------------------------------------
    hello_parser = cmd2.Cmd2ArgumentParser()
    hello_parser.add_argument('-name', type=str, default='Robot', help='A nice hello to test functions')
    hello_parser.add_argument('-surname', type=str, default='Spaceship', help='A nice hello to test functions')
    hello_parser.add_argument('-t', '--template', type=str, default='red', choices=["red", "green", "blue"], help='Select a hello template')
    @cmd2.with_argparser(hello_parser)
    def do_hello(self, args):
        swiss_func.hello_world(args.name, args.surname, args.template)

    # Open a URL in a new tab in Firefox ----------------------------------------------------------------------
    fire_parser = cmd2.Cmd2ArgumentParser()
    fire_parser.add_argument(dest='url', type=str, default='https://www.cyberciti.biz/faq/howto-run-firefox-from-the-command-line/', help='Opening tabs in Firefox from the commandline')
    #fire_parser.add_argument('-surname', type=str, default='Spaceship', help='A nice fire to test functions')
    @cmd2.with_argparser(fire_parser)
    def do_fire(self, args):
        '''
        - https://ticket.lantechlongwave.it/HDAPortal/
        - https://dashboard.meraki.com/
        - https://translate.google.it/
        - https://www.linkedin.com/feed/
        - https://mycase.cloudapps.cisco.com/case
        - https://chat.openai.com/
        - https://erm.zucchetti.it/ERM/
        - https://mail.google.com/
        - https://software.cisco.com/download/home/
        - https://app.lantechlongwave.it/tec/Clienti
        - https://asp.arubanetworks.com/
        - https://app2-eu.central.arubanetworks.com/
        '''
        try:
            webbrowser.get("firefox").open_new_tab(args.url)
        except Exception as e:
            print(f"An error occurred: {e}")

    # Logging command ------------------------------------------------------------------------------------------
    syslog_parser = cmd2.Cmd2ArgumentParser()
    syslog_parser.add_argument('-l', type=str, default=LOG_FILE, help='Logging to file')
    syslog_parser.add_argument('-s', type=str, default="0.0.0.0", help='Define syslog server host')
    syslog_parser.add_argument('-p', type=int, default=LOG_PORT, help='Define syslog port')
    @cmd2.with_argparser(syslog_parser)
    def do_syslog(self, args):
        swiss_func.start_syslog(args.l, args.s, args.p)
    
    # Fuzzy application ----------------------------------------------------------------------------------------
    # Fuzzy search like everithing + grep files
    fuzzy_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(fuzzy_parser)
    def do_fuzzy(self, _): 
        swiss_func.fuzzy_app()
     
    exit_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(exit_parser)
    def do_exit(self, _): 
        print("Goodbye :) ")
        quit()
    
    q_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(q_parser)
    def do_q(self, _): 
        print("Goodbye :) ")
        quit()

    # Dividing commands in categories (help command)
    categorize((do_debug), "WLC debug parser")
    categorize((do_pub, do_iplist, do_macvendor, do_tcpRTT, do_wifistat, do_nslookup, do_portlist, do_ipcheck, do_ping, do_changeip), "Network")
    categorize((do_binary, do_decimal, do_subnet), "Calc")
    categorize((do_putty), "SSH")
    categorize((do_fp), "Files")
    categorize((do_fire, do_openapps), "Browser and apps")
    categorize((do_time, do_hello), "Miscellanea")
    categorize((do_syslog), "Server")

if __name__ == '__main__':
    import sys
    shell_app = SwissKnife()

    # Pre cmd-loop ----------------------------------------------------------------------
    # Banner ascii
    swiss_func.show_motd()
    # IP list using psutils
    if IP_BANNER == True:
        swiss_func.list_interfaces()
    else:
        pass
    # Subprocess the shell command like route print or ip route
    swiss_func.list_routes()

    sys.exit(shell_app.cmdloop())
    
