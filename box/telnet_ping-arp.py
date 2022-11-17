#!/usr/bin/env python3
#
# Data una lista di ip:
# - Automazione di telnet in Netmiko su switch Cisco
# - ping + arp
# - collezione e parse dei dati
#
from __future__ import print_function, unicode_literals

from netmiko import Netmiko
#from getpass import getpass
import time
import re
from datetime import datetime as dt
from scapy.all import IP, ICMP, sr1
import re
import requests
#clock = time.strftime("%Y%m%d%H%M%S")

with open("proxy_hosts_6-10.txt") as file:
	hosts = file.read().splitlines()

#print (hosts)
iteration = len(hosts)

for ip in hosts:
	clock = dt.now()
	network_reg = re.search(r"10.\d{1,2}.\d{1,3}.", ip)
	switch_ip = network_reg.group()+"11"
	
	my_device = {
		'device_type': 'cisco_ios_telnet',
		'host': switch_ip,
		'username': '',
		'password': '',
		'secret': '',
	}
	print("%s - #%s - Pinging %s" % (clock, iteration, ip))
	icmp = IP(dst=ip)/ICMP()
	resp = sr1(icmp,timeout=3, verbose=False)
	if resp == None:
		print(ip + " ICMP down")
		with open("arp_output.txt","a") as output:
				output.write(ip + ",down\n")
		pass
	else:
		try:
			print("%s - #%s - Connecting to %s..." % (clock, iteration, switch_ip))
			net_connect = Netmiko(**my_device)
			net_connect.enable()
			ping_host = net_connect.send_command("ping " + ip, read_timeout=15)
			arp_host = net_connect.send_command("sh arp | include " + ip)
			net_connect.disconnect()
			print("%s - #%s - Disconnected from %s" % (clock, iteration, ip) )
			#print("%s\n%s" % (ping_host, arp_host))
			
			# Cerco il mac
			arp_mac = re.search(r"([0-9A-Fa-f]){4}\.([0-9A-Fa-f]){4}\.([0-9A-Fa-f]){4}", arp_host)
			#print(ip + "," + arp_mac.group() + "\n")
			
			mac_vendor = requests.get("https://api.macvendors.com/" + arp_mac.group())
			print("%s - #%s - %s %s" % (clock, iteration, ip, mac_vendor.text) )

			with open("arp_output.txt","a") as output:
				output.write(ip + "," + mac_vendor.text + "\n")

		except Exception as e:
			print("%s - #%s - Host %s - Exception raised: %s" % (clock, iteration, ip, e))
			with open("arp_output.txt","a") as output:
				output.write(ip + "," + switch_ip + " down\n")
	iteration -= 1 
