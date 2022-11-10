import time
import sys
from termcolor import colored, cprint
def escape():
    while True:
        test = input("# test per uscita dal metodo")
        if test == "e":
            print("e pressed")
        if test == "exit":
            return None
        else:
            pass

def color():
    print (colored('RED TEXT', 'red'), colored('GREEN TEXT', 'green'))
color()