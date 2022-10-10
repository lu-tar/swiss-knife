from __future__ import print_function, unicode_literals

from netmiko import Netmiko
from getpass import getpass
import time
import re
from datetime import datetime as dt

ap = [
'10.20.120.191',
'10.20.120.192',
'10.20.120.193',
'10.20.120.194',
'10.20.120.195',
'10.20.120.196'
]


for ip in ap:
	my_device = {
		'device_type': 'cisco_ios',
		'host': ip,
		'username': 'admin',
		'password': 'PASSWORD',
		'secret': 'PASSWORD'
	}
	clock = dt.now()
	try:
		print("%s - Connecting to %s..." % (clock, ip))
		net_connect = Netmiko(**my_device)
		net_connect.enable()
	except:
		print("%s - %s is unreachable" % (clock, ip))
	showname = net_connect.send_command("show running-config | i hostname")
	shownameStrip = showname.replace(" ","")
	apname = shownameStrip.replace("hostname","")
	apname = apname.replace("\n","")
	print(apname)

	showlog = net_connect.send_command("show logging | i Oct")
	#print(showlog)
	net_connect.disconnect()
	"""
	for l in showlog:
		showlogGrep = re.findall(r'Sep 21',showlog)[0]
	#print(showlogGrep)
	"""
	with open (apname+".txt","w+") as f:
		f.write(showlog)
	pass