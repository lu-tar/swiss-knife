#!/usr/bin/env python3
#
# Inventory con Netmiko
#
from __future__ import print_function, unicode_literals

from netmiko import Netmiko
#from getpass import getpass
import time
import re
from datetime import datetime as dt
#clock = time.strftime("%Y%m%d%H%M%S")

switch = ['10.20.150.11']

for ip in switch:
	clock = dt.now()
	my_device = {
		'device_type': 'cisco_ios_telnet',
		'host': ip,
		'username': '',
		'password': '',
		'secret': ''
	}
	try:
		print("%s - Connecting to %s..." % (clock, ip))
		net_connect = Netmiko(**my_device)
		net_connect.enable()
		hostname = net_connect.send_command("show running-config | i hostname")
		uptime = net_connect.send_command("show version | i uptime")
		inventory = net_connect.send_command("show inventory")
		cdp = net_connect.send_command("show cdp neighbors")
		print("%s\n%s\n%s\n%s" % (hostname, uptime, inventory, cdp))
		net_connect.disconnect()
		print("%s - Disconnected from %s" % (clock, ip) )
		print("\n")
	except:
		print("%s - %s is unreachable" % (clock, ip))

