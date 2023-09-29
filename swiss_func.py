from swiss_conf import *
import psutil
import subprocess
import re
import sqlite3
from datetime import datetime

CLOCK_FORMAT = "%H%M%S"
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)

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
    with open ('debug_parser/debugTrace_1.txt','r') as file:
        line_list = file.read().splitlines()
        for i in line_list:
            iosxe_date = re.findall(IOSXE_DATE_REGEX, i)
            iosxe_time = re.findall(IOSXE_TIME_REGEX, i)
            iosxe_daemon = re.findall(IOSXE_DAEMON_REGEX, i)
            iosxe_category = re.findall(IOSXE_CATEGORY_REGEX, i)
            iosxe_log_level = re.findall(IOSXE_LOG_LEVEL_REGEX, i)
            print(iosxe_log_level)
            end_log_message = re.search(IOSXE_LOG_LEVEL_REGEX, i).end()
    
            debug_dataset.append([iosxe_date[0], iosxe_time[0], iosxe_daemon[0], iosxe_category[0], iosxe_log_level[0], i[end_log_message:]])
    print(debug_dataset)
    
    conn = sqlite3.connect('db/debug_parser.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS table1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            daemon TEXT,
            category TEXT,
            log_level TEXT,
            message TEXT
        )
    ''')
    for data in debug_dataset:
        cursor.execute('INSERT INTO table1 (date, time, daemon, category, log_level, message) VALUES (?, ?, ?, ?, ?, ?)', (data[0], data[1], data[2], data[3], data[4], data[5]))
    conn.commit()
    conn.close()

    return
    
debug_parser()