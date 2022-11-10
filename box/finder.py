import subprocess

index = input(">> ")
var = index[5:]

subprocess.Popen('explorer' + r'C:\Users\TARLUC\Documents\'+var)
# C:\Users\TARLUC\Documents\PY
"""
# This line is not correct
'explorer /n, /select r"\\192.168.0.27\\Project_Data\\Projects_2013\\"'+fldrname
#                      ^you start a new string without ending previous one
# this one is correct
'explorer /n, /select ' + r'\192.168.0.27\Project_Data\Projects_2013\' + fldrname
#                     ^first ending string start
"""
