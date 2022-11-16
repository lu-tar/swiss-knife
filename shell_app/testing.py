import subprocess

netsh_ethernet_if = subprocess.Popen(["C:\Program Files\PuTTY\putty.exe", "-ssh", "146.59.227.195", "-l", "tokyo", "-pw", "100gattiinfila!", "-P", "4545"], stdout=subprocess.PIPE)
ethernet_output = netsh_ethernet_if.communicate()[0]