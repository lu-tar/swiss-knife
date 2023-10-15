# swiss-knife 🇨🇭🔪
A multipurpose shell for networking/sysadmin tasks written in Python [cmd2](https://cmd2.readthedocs.io/en/latest/) with the goal of minimizing mouse usage and launching programs and scripts quickly from the terminal.

**Disclaimer 🐞**
This is a personal project to test my programming skills as a network engineer.

## Features 🤖
swiss-knife offers the following features:
- Binary/decimal conversion
- Subnet calculator
- MAC OUI identification using macvendors.com
- Lightweight TCP and UDP port list browser
- TCP latency ping
- What's my IP address
- Wi-Fi statistics
- SSH integration with Putty
- Text file parsing

In the future, the following features are planned for implementation:
- Automation with Norninr or Netmiko
- HTTP/FTP/SFTP/TFTP portable server
- MD5/SHA256 calculator
- Obsidian and markdown access
- Port scanner
- File manager with fuzzy finder

## Getting Started 🚀
To get started with swiss-knife, follow these steps:

1. Install Python: If you don't already have Python installed, download and install it from [python.org](https://www.python.org/downloads/).

2. Clone the repository: 
```sh
git clone https://github.com/lu-tar/swiss-knife.git
```
or download the [ZIP file](https://github.com/lu-tar/swiss-knife/archive/refs/heads/main.zi).

3. Navigate to the project directory, create a virtual environment and activate it. This step is optional but using virtual environments in Python ensures isolation and package version control.

```
cd swiss-knife
```
The command python -m venv venv creates a virtual environment named "venv" using Python's built-in [venv module](https://docs.python.org/3.10/library/venv.html).
```
python -m venv venv
```

The command `source venv/bin/activate` activates the virtual environment named "venv," allowing you to work within its isolated environment. To exit the environment, you can use the deactivate command.
On Windows
```
venv\Scripts\activate
```
On Linux
```
source venv/bin/activate
```

4. Install the required packages using the requirements.txt file:
```
pip install -r requirements.txt
```

## How It Works 🛠️
swiss-knife operates like any other shell-like application, where commands require both mandatory or optional arguments. You can execute various functions by entering the appropriate commands.

Navigate into the project home directory and start the shell using
```
py swiss_shell.py
```
a `#` symbol should appear. Use `help` to list all the available commands and `-h` to list the arguments. The shell supports tab completion.

### A preview of the available commands
#### tcpRTT
A TCP latency ping utility
```
# tcpRTT wikipedia.org -p 443 -r 6
Repetitions: 6, Timeout: 1, Port: 443
tcp-latency wikipedia.org
wikipedia.org: tcp seq=0 port=443 timeout=1 time=155.99999999994907 ms
wikipedia.org: tcp seq=1 port=443 timeout=1 time=94.00000000005093 ms
wikipedia.org: tcp seq=2 port=443 timeout=1 time=110.00000000012733 ms
wikipedia.org: tcp seq=3 port=443 timeout=1 time=108.9999999999236 ms
wikipedia.org: tcp seq=4 port=443 timeout=1 time=92.9999999998472 ms
wikipedia.org: tcp seq=5 port=443 timeout=1 time=94.00000000005093 ms
--- wikipedia.org tcp-latency statistics ---
5 out of 6 packets transmitted successfully
rtt min/avg/max = 92.9999999998472/112.39999999997963/155.99999999994907 ms
#
#
# tcpRTT wikipedia.org -p 443 -r 2 -s
Repetitions: 2, Timeout: 1, Port: 443
109.0
94.0
# 
```

#### ipcheck
Given an IP address, the command returns the category to which it belongs as output.
```
# ipcheck 224.0.0.2
224.0.0.2
is_private: False
is_multicast: True
is_reserved: False
[IPv4Address('224.0.0.2')]
```

#### macvendor
Translates MAC to its vendor using https://macvendors.com/
```
# macvendor E0-D5-5E-2F-F9-12
GIGA-BYTE TECHNOLOGY CO.,LTD.
#
```

#### iplist
List interfaces based on the `IP_INTERFACES_INCLUDE = ["Ethernet", "Ethernet 4"]` in the `swiss_conf.py` configuration file.
```
# iplist
Public IP: 37.161.***.***
Ethernet:  E0-D5-5E-2F-F9-44 169.254.79.46 255.255.0.0
Ethernet 4:  B2-54-C2-1F-13-10 192.168.4.159 255.255.255.0
```

#### portlist
Search the IANA port and services list
``` 
# portlist 666
['mdqs', '666', 'tcp', '']
['mdqs', '666', 'udp', '']
['doom', '666', 'tcp', 'doom Id Software']
['doom', '666', 'udp', 'doom Id Software']
#
#
#
# portlist smtp
['smtp', '25', 'tcp', 'Simple Mail Transfer']
['smtp', '25', 'udp', 'Simple Mail Transfer']
#
#
```
## Configuration file ⚙️
The configuration file `swiss_conf.py` includes a list of easily adjustable variables that will alter the behavior of the shell and its commands.