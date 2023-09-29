from swiss_conf import *
import psutil
import subprocess
import re

IOSXE_DATE_REGEX = '\d{4}/\d{2}/\d{2}'
IOSXE_TIME_REGEX = '\d{2}:\d{2}:\d{2}\.\d+'
IOSXE_DAEMON_REGEX = '\{[^}]+\}\{\d\}:'
IOSXE_CATEGORY_REGEX = '\[[^\]]+\] \[[0-9]+\]:'
IOSXE_LOG_LEVEL_REGEX = '\(([^)]+)\):'

CISCO_DOTTED_MAC_REGEX = '"\b[\dA-Za-z]{4}\b.\b[\dA-Za-z]{4}\b.\b[\dA-Za-z]{4}\b"gm'

def list_interfaces():
    print("Public IP: " + INTERNET_IP)
    # Ciclio il dictionary psutil.net_if_addrs()
    for nic, addrs in psutil.net_if_addrs().items():
        # Per ogni interfaccia presente IP_INTERFACES_INCLUDE 
        for i in IP_INTERFACES_INCLUDE:
            if nic == i:
                print(nic + ": ", end=' ')
                for addr in addrs:
                    # Escludere IPv6, da migliorare
                    if 'fe80' in addr.address:
                        pass
                    else:
                        print(addr.address, end=' ')
                    if addr.netmask:
                        print(addr.netmask)
            else:
                pass
    return

def list_routes():
    if LIST_ROUTE == True:
        if OPERATING_SYSTEM == "Windows":
            route_print = subprocess.run(['route', 'print', '0.0.0.0'], stdout=subprocess.PIPE)
            decode_route_print = route_print.stdout.decode('utf-8', 'ignore').splitlines()
            for i in decode_route_print:
                if '0.0.0.0' in i:
                    print("Default route: " + i)
        elif OPERATING_SYSTEM == "Linux":
            route_print = subprocess.run(['ip', 'route'], stdout=subprocess.PIPE)
            decode_route_print = route_print.stdout.decode('utf-8', 'ignore').splitlines()
            for i in decode_route_print:
                if 'default' in i:
                    print(i)
        else:
            print("platform.system() is not Windows or Linux")
    else:
        pass

def show_motd():
    if ASCII_BANNER == True:
        print(ASCII_ART)
    else:
        pass
    return

# Testing debug file parsing, see the pseudocodice in note.md
def debug_parser():
    debug_dataset = []
    with open ('debug_parser/debugTrace_small.txt','r') as file:
        line_list = file.read().splitlines()
        for i in line_list:
            line_number = line_list.index(i)
            iosxe_date = re.findall(IOSXE_DATE_REGEX, i)
            iosxe_time = re.findall(IOSXE_TIME_REGEX, i)
            iosxe_daemon = re.findall(IOSXE_DAEMON_REGEX, i)
            iosxe_category = re.findall(IOSXE_CATEGORY_REGEX, i)
            iosxe_log_level = re.findall(IOSXE_LOG_LEVEL_REGEX, i)
            
            end_log_message = re.search(IOSXE_LOG_LEVEL_REGEX, i).end()
    
            debug_dataset.append([line_number, iosxe_date[0], iosxe_time[0], iosxe_daemon[0], iosxe_category[0], iosxe_log_level[0], i[end_log_message:]])
    for i in debug_dataset:
        print(i)
    return

debug_parser()