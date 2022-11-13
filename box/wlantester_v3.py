import subprocess
import time
import re
from datetime import datetime
from tcp_latency import measure_latency
from ping3 import ping

WIFIDATA = []
TARGETS = ["teams.microsoft.com", "openrainbow.com", "n197.meraki.com"]
ICMPDATA = []

try:
    i = 0
    while True:
        t = datetime.now() # current date and time
        clock = t.strftime("%H:%M:%S")
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
        outStr = result.stdout.decode('utf-8', 'ignore')
        for e in outStr.splitlines():
            if "BSSID" in e: bssid = e[29:]
            elif "Canale" in e: channel = e[27:]
            elif "ricezione" in e: downRate = e[32:]
            elif "trasmissione" in e: upRate = e[34:]
            elif "frequenza" in e: fq = e[29:]
            elif "Segnale" in e: signal = e[26:]

        latency_1 = measure_latency(host=TARGETS[0],runs=1, timeout=1)
        latency_2 = measure_latency(host=TARGETS[1],runs=1, timeout=1)
        latency_3 = measure_latency(host=TARGETS[2],runs=1, timeout=1)
        
        icmp1 = ping("google.com", unit='ms', size=500)
        icmp2 = ping("google.com", unit='ms', size=500)
        icmp3 = ping("google.com", unit='ms', size=500)

        print ("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (clock, bssid, channel, downRate, upRate, fq, signal, int(latency_1[0]), int(latency_2[0]), int(latency_3[0]), round(icmp1,2), round(icmp2,2), round(icmp3,2)))

        WIFIDATA.append([clock, bssid, channel, downRate, upRate, fq, signal, str(int(latency_1[0])), str(int(latency_2[0])), str(int(latency_3[0])), str(round(icmp1,2)), str(round(icmp2,2)), str(round(icmp3,2))])
        # 5 seconds delay between pols
        time.sleep(3)

except KeyboardInterrupt:
    #print (WIFIDATA)
    clock = t.strftime("%H%M%S")
    filename = str("C:/Users/luca.tarozzi/Documents/900_Python_scripts/wlantester/csv-output/"+clock+"_wlantester-output.csv")
    with open(filename, "w") as f:
        f.write("time, bssid, ch, downRate, upRate, fq, signal, tcp_latency1, tcp_latency2, tcp_latency3, icmp_latency2, icmp_latency2, icmp_latency3\n")
        for i in WIFIDATA:
            for data in i:
                f.write(data+",")
            f.write("\n")