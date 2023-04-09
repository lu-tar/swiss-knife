# Custom configuration
from swiss_conf import *
import psutil

def interfaces_banner():
    if IP_BANNER == True:
        print(INTERNET_IP)
        for nic, addrs in psutil.net_if_addrs().items():
            for i in IP_INTERFACES_INCLUDE:
                if nic == i:
                    print(nic, end=' ')
                    for addr in addrs:
                        if 'fe80' in addr.address:
                            pass
                        else:
                            print(addr.address, end=' ')
                        if addr.netmask:
                            print(addr.netmask)     
                else:
                    pass
    else:
        pass
    return

def show_motd():
    if ASCII_BANNER == True:
        print(ASCII_ART)
    else:
        pass
    return