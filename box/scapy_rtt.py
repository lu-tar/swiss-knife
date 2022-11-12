import statistics
import os

from scapy.all import Ether, IP, ICMP, srp

if os.geteuid() > 0:
    raise OSError("This script must run as root")

ping_rtt_list = list()
def ping_addr(host, count=3):
    packet = Ether()/IP(dst=host)/ICMP()
    t=0.0
    for x in range(count):
        x += 1  # Start with x = 1 (not zero)
        ans, unans = srp(packet, filter='icmp', verbose=0)
        rx = ans[0][1]
        print(rx)
        tx = ans[0][0]
        print(tx)
        delta = rx.time - tx.sent_time
        print("ping #{0} rtt: {1} second".format(x, round(delta, 6)))
        ping_rtt_list.append(round(delta, 6))
    return ping_rtt_list

if __name__=="__main__":
    ping_rtt_list = ping_addr('1.1.1.1')
    rtt_avg = round(statistics.mean(ping_rtt_list), 6)
    print("Avg ping rtt (seconds):", rtt_avg)
