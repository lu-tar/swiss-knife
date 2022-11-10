import re
import urllib.request
import datetime

def macFinder():
    mac = input("MAC: ")
    # test
    # mac = "0000-2314-96fc"
    try:
        with urllib.request.urlopen('https://api.macvendors.com/'+mac) as response:
            html = response.read()
            print(html.decode())
            with open("log.txt", "a") as log:
                log.write(str(datetime.datetime.now()) + " " + mac + " --> " + html.decode() + "\n")
    except urllib.error.HTTPError as e:
        print(e.code)
