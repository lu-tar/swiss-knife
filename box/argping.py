from scapy.all import *
#from icecream import ic
import argparse
import emoji

def ping(host):
    icmp = IP(dst=host)/ICMP()
    resp = sr1(icmp,timeout=2,verbose=False)
    if resp == None:
        print((emoji.emojize(host+" :red_circle:")))
    else:
        print((emoji.emojize(host+" :green_circle:")))

def main():
    #ip = input("Give me the IP: ")
    #ping(ip)
    ip = "1.1.1.1"
    # Create the parser
    my_parser = argparse.ArgumentParser(description='Network automation with Netmiko')
    # Add the arguments
    my_parser.add_argument('--ping',action='store_const', const=ip, help='Ping a single ip')
    args = my_parser.parse_args()
    
    if args.ip: ping(arg.ip)
    
if __name__ == '__main__':
    main()