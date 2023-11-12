from swiss_conf import *
import psutil
import subprocess
import re
import sqlite3
import socket
from datetime import datetime
from pathlib import Path
from rich.panel import Panel
from rich.panel import Style
from rich import print

CLOCK_FORMAT = "%H:%M:%S"
CURRENT_TIME = datetime.now()
CLOCK_TIME = CURRENT_TIME.strftime(CLOCK_FORMAT)

try:
    PUBLIC_IP = requests.get("https://api.ipify.org?format=text").text
except Exception as e:
    PUBLIC_IP = ""

def list_interfaces():
    print(PUBLIC_IP)
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

def list_routes():

    if LIST_ROUTE == True:
        if OPERATING_SYSTEM == "Windows":
            route_print = subprocess.run(['route', 'print', '0.0.0.0'], stdout=subprocess.PIPE)
            decode_route_print = route_print.stdout.decode('utf-8', 'ignore').splitlines()
            for i in decode_route_print:
                if '0.0.0.0' in i:
                    #print(Panel(ASCII_ART, title="Welcome to swiss-knife", subtitle="Version 2.0", border_style=Style(color="#22a6b3")))
                    print(Panel(i, title="Default route", border_style=Style(color="#7ed6df")))
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
    hostname = socket.gethostname()
    active_users = psutil.users()
    user_names = [user.name for user in active_users]

    ASCII_ART = f"""
                        ██                          User: {user_names}
     ▄▄▄▄  ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄   ▄▄▄▄   ▄▄▄▄            Host: {hostname}
    ██▄ ▀   ██  ██  █   ██  ██▄ ▀  ██▄ ▀            OS: {OPERATING_SYSTEM}
    ▄ ▀█▄▄   ███ ███    ██  ▄ ▀█▄▄ ▄ ▀█▄▄           IP_INTERFACES_IGNORE: {IP_INTERFACES_IGNORE}
    █▀▄▄█▀    █   █    ▄██▄ █▀▄▄█▀ █▀▄▄█▀           IP_INTERFACES_INCLUDE: {IP_INTERFACES_INCLUDE}
                                                    Putty path: {PATH_TO_PUTTY}
    	▀██                ██    ▄▀█▄               Public IP: {PUBLIC_IP}
    	 ██  ▄▄  ▄▄ ▄▄▄   ▄▄▄  ▄██▄     ▄▄▄▄        Clock: {CLOCK_TIME}
    	 ██ ▄▀    ██  ██   ██   ██    ▄█▄▄▄██       
    	 ██▀█▄    ██  ██   ██   ██    ██            Author: https://github.com/lu-tar
    	▄██▄ ██▄ ▄██▄ ██▄ ▄██▄ ▄██▄    ▀█▄▄▄▀       
    """
    if ASCII_BANNER == True:
        print(Panel(ASCII_ART, title="Welcome to swiss-knife", subtitle="Version 2.0", border_style=Style(color="#22a6b3")))
    else:
        pass
    return

# Test function
def hello_world(hello_world_surname, hello_world_name, hello_world_template):
    if hello_world_template == 'red':
        print(f"Hello world and {hello_world_surname} {hello_world_name}!")
    if hello_world_template == 'green':
        print(f"Howdy {hello_world_surname} {hello_world_name}!")    
    if hello_world_template == 'blue':
        print(f"Ciao {hello_world_surname} {hello_world_name}!")

# See debug_parser in shell
def debug_to_db(debug_filepath, debug_id_name):
    debug_dataset = []
    # debug_filepath = 'debug_parser/debugTrace_1.txt'
    try:
        with open (debug_filepath,'r') as file:
            line_list = file.read().splitlines()
            # Inserire qui un check per capire se il file e' AireOS o del 9800
            # Cancellare/gestire la prima linea del file 9800
            for i in line_list:
                iosxe_date = re.findall(IOSXE_DATE_REGEX, i)
                iosxe_time = re.findall(IOSXE_TIME_REGEX, i)
                iosxe_daemon = re.findall(IOSXE_DAEMON_REGEX, i)
                iosxe_category = re.findall(IOSXE_CATEGORY_REGEX, i)
                iosxe_log_level = re.findall(IOSXE_LOG_LEVEL_REGEX, i)
                end_log_message = re.search(IOSXE_LOG_LEVEL_REGEX, i).end()
        
                debug_dataset.append([iosxe_date[0], iosxe_time[0], iosxe_daemon[0], iosxe_category[0], iosxe_log_level[0], i[end_log_message:]])
        print("Parsed: " + debug_filepath)
    except FileNotFoundError:
        print(f"{debug_filepath} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # print(debug_dataset)
    
    conn = sqlite3.connect('db/debug_parser.db')
    cursor = conn.cursor()
    cursor.execute('''id INTEGER PRIMARY KEY AUTOINCREMENT, id_name TEXT, date TEXT, time TEXT, daemon TEXT, category TEXT, log_level TEXT, message TEXT)''')
    for data in debug_dataset:
        cursor.execute('''INSERT INTO Table1 (id_name, date, time, daemon, category, log_level, message) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                       (debug_id_name, data[0], data[1], data[2], data[3], data[4], data[5])
                       )
    conn.commit()
    conn.close()

    return

# Dato un array di stringhe/regex in ingresso le compila ignorando il case
def compile_patterns(pattern_strings):
    return [re.compile(pattern, re.IGNORECASE) for pattern in pattern_strings]

def grep_file(file_path, search_patterns):
    try:
        file_path = Path(file_path)
        with file_path.open('r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                for pattern in search_patterns:
                    if pattern.search(line):
                        print(f"{line_number}: {line.strip()}")
                        break  # Esce dal ciclo se c'è una corrispondenza
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Testing database
def testing_database():
    conn = sqlite3.connect('db/debug_parser.db')
    cursor = conn.cursor()
    cursor.execute('''
            SELECT time, message FROM Table1 
            WHERE id_name = 163226 
            AND category LIKE "%client-orch-state%" 
            OR category LIKE "%key%"
            ''')
    matching_rows = cursor.fetchall()
    conn.commit()
    conn.close()
    for row in matching_rows:
        print(row)
    
    return