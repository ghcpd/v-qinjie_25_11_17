import os

def run(command):
    # Vulnerable if command contains user input
    os.system('ls ' + command)
