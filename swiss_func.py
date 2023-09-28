from swiss_conf import *
import psutil
import subprocess

def list_interfaces():
    print("Public IP: " + INTERNET_IP)
    # Ciclio il dictionary psutil.net_if_addrs()
    for nic, addrs in psutil.net_if_addrs().items():
        # Per ogni interfaccia presente IP_INTERFACES_INCLUDE 
        for i in IP_INTERFACES_INCLUDE:
            if nic == i:
                print(nic + ": ", end=' ')
                for addr in addrs:
                    # Escludere IPv6, da migliorare
                    if 'fe80' in addr.address:
                        pass
                    else:
                        print(addr.address, end=' ')
                    if addr.netmask:
                        print(addr.netmask)
            else:
                pass
    return

def list_routes():
    if LIST_ROUTE == True:
        if OPERATING_SYSTEM == "Windows":
            route_print = subprocess.run(['route', 'print', '0.0.0.0'], stdout=subprocess.PIPE)
            decode_route_print = route_print.stdout.decode('utf-8', 'ignore').splitlines()
            for i in decode_route_print:
                if '0.0.0.0' in i:
                    print("Default route: " + i)
        elif OPERATING_SYSTEM == "Linux":
            route_print = subprocess.run(['ip', 'route'], stdout=subprocess.PIPE)
            decode_route_print = route_print.stdout.decode('utf-8', 'ignore').splitlines()
            for i in decode_route_print:
                if 'default' in i:
                    print(i)
        else:
            print("platform.system() is not Windows or Linux")
    else:
        pass

def show_motd():
    if ASCII_BANNER == True:
        print(ASCII_ART)
    else:
        pass
    return

def debug_parser():

    return

# Testing debug file parsing, see the pseudocodice in note.md

debug_parser()