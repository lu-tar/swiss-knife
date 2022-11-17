#!/usr/bin/env python3
#
# Applicare il port-security mac ad x interfacce in accesso
#	"^[GgfF]+[ia]+\d+[/]+\d*"gm
#
from __future__ import print_function, unicode_literals

from netmiko import Netmiko
from getpass import getpass
import time
import re
from datetime import datetime as dt
#clock = time.strftime("%Y%m%d%H%M%S")

#Elenco di switch su cui accedere
switch = ['10.10.140.11','10.10.140.12']

for ip in switch:
	clock = dt.now()
	my_device = {
		'device_type': 'cisco_ios_telnet',
		'host': ip,
		'username': 'virtuale',
		'password': 'virtuale',
		'secret': 'virtuale'
	}
	try:
		print("%s - Connecting to %s..." % (clock, ip))
		net_connect = Netmiko(**my_device)
		net_connect.enable()
	except:
		print("%s - %s is unreachable" % (clock, ip))
	trunkPorts = net_connect.send_command("sh interfaces status | i trunk").split()
	accessPorts = net_connect.send_command("sh interfaces status | e trunk").split()
	macVlan10 = net_connect.send_command("sh mac-address-table dynamic vlan 10")
	net_connect.disconnect()
	print("%s - Disconnected from %s" % (clock, ip) )

	print("%s - Parsing ports from %s" % (clock, ip) )
	rx = re.compile("^[GgfF]+[ia]+\d+[/]+\d*")
	parsedAccess = list(filter(rx.match, accessPorts))
	parsedTrunk = list(filter(rx.match, trunkPorts))
	print("%s - %s access ports:" % (clock, ip) )
	print(parsedAccess)
	print("%s - %s trunk ports:" % (clock, ip) )
	print(parsedTrunk)

    #Creo un set di comandi abbinando le interfacce in accesso
    #al comando interface + port-sec

	"""
	configCmd = []
	for i in parsedAccess:
		configCmd.append("interface "+i)
		configCmd.append("switchport port-security maximum 2")
	print("Config commands loaded...")

	for i in configCmd:print(i)
	exec = input("%s - Execute commands to %s? \n -yes \n -no \n" % (clock, ip) )
	if exec == "yes":
		configset = net_connect.send_config_set(configCmd)
		configset += net_connect.save_config()
		print(configset)
	else:
		print("%s - No commands executed to %s" % (clock, ip) )
	"""
