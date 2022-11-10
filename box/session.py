import os
import time
import pathlib
import datetime
purepath = pathlib.Path(r"C:\Users\TARLUC\Desktop\putty-0.exe")
path = str(purepath)
from subprocess import Popen
import subprocess

#ask ssh or telnet

def secureshell():
	while True:
		target = input("ip: ")
		user = input("username: ")
		if target == "e" or target=="":
			return None
		else:
			with open("log.txt", "a") as log:
				log.write(str(datetime.datetime.now()) +" "+ user + " started ssh session to " + target + "\n")
			proc = Popen(path + " -ssh "+user+"@"+target, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def telnet():
	while True:
		target = input("ip: ")
		if target == "e" or target=="":
			return None
		else:
			with open("log.txt", "a") as log:
				log.write(str(datetime.datetime.now()) + " Started telnet session to " + target + "\n")
			proc = Popen(path + " -telnet "+target, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

def nmap():
	while True:
		target = input("ip/domain: ")
		print ("nmap -v")
		if target == "e" or target=="":
			return None
		else:
			subprocess.Popen("start cmd /K nmap -v scanme.nmap.org ", shell=True)
			with open("log.txt", "a") as log:
				log.write(str(datetime.datetime.now()) + " Nmap to scanme.nmap.org" + "\n")

def remoteshell():
	target=input("ip: ")
	with open("log.txt", "a") as log:
		log.write(str(datetime.datetime.now())+" Started "+protocol+" session to "+target+"\n")
	if protocol == "s":
		user=input("username: ")
		os.system(path+" -ssh "+user+"@"+target)
	else:
		os.system(path+" -telnet "+target)
	time.sleep(1)
