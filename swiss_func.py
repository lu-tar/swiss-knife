import re
import os
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