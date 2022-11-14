import csv
import re
port = "111"
with open('service-names-port-numbers.csv', 'r') as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if re.search(r'\b' + port + r'\b', str(row)):
            print(row[:4])

prot = "telnet"
with open('service-names-port-numbers.csv', 'r') as file:
    reader = csv.reader(file, delimiter=",")
    for row in reader:
        if prot in row:
            print(row[:4])
