import ipaddress
ip = "192.168.20.0/27"
add = ipaddress.ip_network(ip)
checks = {
    "Network": add.network_address,
    "Broadcast": add.broadcast_address,
}
for key,val in checks.items():
    print (key, ": ", val)
check = ("Host values")
list = []
for x in add.hosts():
    list.append(x)
#print(ipaddress.ip_address(list))
