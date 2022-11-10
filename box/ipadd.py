import ipaddress, datetime, json, time
from terminaltables import AsciiTable
import requests
import subprocess

def pubCheck():
    domain = "http://ifconfig.co/"
    output = "json"
    try:
        start_time = time.time()
        # proxy ip public
        r = requests.get(domain+output)
        mypub = r.json()
        values = [["pubCheck", "value"]]
        """
        for (k,v) in mypub.items():
            print (k + "\t\t" + str(v))
        """
        for (k, v) in mypub.items():
            values.append([k, str(v)])
        table = AsciiTable(values)
        print(table.table)


        # check real public ip
        r = requests.get('https://ifconfig.co:11443/json')
        mypub = r.json()
        """
        for (k, v) in mypub.items():
            print(k + "\t\t" + str(v))
        """
        realPub = [["pubCheck no proxy", "value"]]
        for (k,v) in mypub.items():
            realPub.append([k,str(v)])
        table = AsciiTable(realPub)
        print (table.table)


        with open("log.txt", "a") as log:
            log.write(str(datetime.datetime.now()) + " GET http://ifconfig.co/ " + str(mypub) +"\n")
        end_time = time.time()
        duration = end_time - start_time
        print("Request time: "+str(duration))

    except Exception as e:
        print(e)

def ipapi():
    while True:
        ip = input("ip: ")
        if ip == "e" or ip == "":
            return None
        else:
            try:
                start_time = time.time()
                r = requests.get("http://ipapi.co/"+ip+"/json")
                mypub = r.json()
                """
                for (k, v) in mypub.items():
                    print(k + "\t" + str(v))
                """
                values = [["", "value"]]
                for (k, v) in mypub.items():
                    values.append([k, str(v)])
                table = AsciiTable(values)
                print(table.table)

                with open("log.txt", "a") as log:
                    log.write(str(datetime.datetime.now()) + " GET http://ipapi.co/ " + str(mypub) +"\n")
                end_time = time.time()
                duration = end_time - start_time
                print("Request time: "+str(duration))

            except Exception as e:
                print(e)


def netCheck():
    while True:
        ip = input("ip/subnet: ")
        if ip == "e" or ip == "":
            return None
        else:
            try:
                add = ipaddress.ip_network(ip)
                checks = {
                    "Network": add.network_address,
                    "Broadcast": add.broadcast_address,
                }
                for key,val in checks.items():
                    print (key, ": ", val)
                check = ("Host values")
                for x in add.hosts():
                    print(x)

                    
                with open("log.txt", "a") as log:
                    log.write(str(datetime.datetime.now()) + " Check on net ip address " + str(add) + " terminated" + "\n")
            except Exception as e:
                print(str(e))

def ipCheck():
    while True:
        ip = input("ip: ")
        if ip == "e" or ip == "":
            return None
        else:
            try:
                add = ipaddress.ip_address(ip)
                checks = {
                    "Version": add.version,
                    "Multicast": add.is_multicast,
                    "Global": add.is_global,
                    "Private": add.is_private,
                    "Reserved": add.is_reserved,
                }
                for key,val in checks.items():
                    print (key, ": ", val)
                with open("log.txt", "a") as log:
                    log.write(str(datetime.datetime.now()) + " Check on ip address " + str(add) + " terminated" + "\n")
            except Exception as e:
                print(str(e))


def pinger ():
    while True:
        target = input("ip: ")
        subnet = input("subnet [/24]: ")
        if target == "e" or target == "":
            return None
        else:
            subprocess.Popen("start cmd /K ping "+ target +" -t", shell=True)
            subprocess.Popen("start cmd /K nmap -sn "+ target+subnet, shell=True)
            with open("log.txt", "a") as log:
                log.write(str(datetime.datetime.now()) + " Ping " + target + "\n")

def subnets():
    print("""
    /8---255.0.0.0
    /9---255.128.0.0
    /10--255.192.0.0
    /11--255.224.0.0
    /12--255.240.0.0
    /13--255.248.0.0
    /14--255.252.0.0
    /15--255.254.0.0
    /16--255.255.0.0
    /17--255.255.128.0
    /18--255.255.192.0
    /19--255.255.224.0
    /20--255.255.240.0
    /21--255.255.248.0
    /22--255.255.252.0
    /23--255.255.254.0
    /24--255.255.255.0
    /25--255.255.255.128
    /26--255.255.255.192
    /27--255.255.255.224
    /28--255.255.255.240
    /29--255.255.255.248
    /30--255.255.255.252
    /31--255.255.255.254
    /32--255.255.255.255""")
