"""
from scapy.all import sr1, IP, ICMP, conf, get_if_addr
ip = get_if_addr("Wi-Fi")
print(ip)
print(conf.route.route("0.0.0.0")[2])
print("\n")
import re

import subprocess
netsh_ethernet_if = subprocess.Popen(["netsh","interface","ip","show", "config", "Ethernet"], stdout=subprocess.PIPE, shell=True)
ethernet_output = netsh_ethernet_if.communicate()[0]
#output.decode('utf8', errors='ignore').strip()
ethernet_info = re.findall("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", str(ethernet_output))
for i in ethernet_info: print(i, end=" ")


uname = subprocess.Popen(["ver"], stdout=subprocess.PIPE, shell=True)
uname_output = uname.communicate()[0]
a = uname_output.decode('utf8', errors='ignore').strip()
print(a)
"""
semaforo = "verde"
motore = "acceso"

if semaforo == "verde" and motore != "spento":
    print("gas")