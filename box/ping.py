from scapy.all import *
from icecream import ic
import emoji

google = "10.8.8.8"


icmp = IP(dst=google)/ICMP()

resp = sr1(icmp,timeout=2,verbose=False)
if resp == None:
    print((emoji.emojize("Google :red_circle:")))
else:
    print((emoji.emojize("Google :green_circle:")))
