from cmd import Cmd
from scapy.all import sr1
from scapy.all import IP
from scapy.all import ICMP

class MyShell(Cmd):
    prompt = "> "
    intro = "Welcome! This is an intro"

    def do_hello(self, args):
        print("Hello World")

    def  do_ping(self, args):
        ip_address, count = args.rsplit(" ", 1)
        for i in range(0,int(count)):
            icmp = IP(dst=ip_address)/ICMP()
            resp = sr1(icmp,timeout=2,verbose=False)
            if resp == None:
                print("Unreachable")
            else:
                print("OK!")

    def do_exit(self, args):
        raise SystemExit()

if __name__ == "__main__":
    app = MyShell()
    app.cmdloop('Welcome! This is a banner')




