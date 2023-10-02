# swiss-knife 🇨🇭🔪 a Command Line Utility
A multipurpose shell for networking tasks written in Python cmd2.

**Disclaimer:** This project is in beta and is primarily aimed at providing a command line interface for launching programs and scripts quickly, with the goal of minimizing mouse usage.

## Features 🤖
Swiss Knife offers the following features:
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

## Getting Started 🚀
To get started with Swiss Knife, follow these steps:

1. Install Python: If you don't already have Python installed, download and install it from [python.org](https://www.python.org/downloads/).

2. Clone the repository: 
```sh
git clone https://github.com/lu-tar/swiss-knife.git
```

3. Navigate to the project directory, create a virtual environment and activate it
```
cd swiss-knife
python -m venv venv
```
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
Swiss Knife operates like any other shell-like application, where commands require both mandatory and optional arguments. You can execute various functions by entering the appropriate commands.

```
ping 8.8.8.8
[-h, --help]       [-spw, --spawn]
[-r, --repeat]     [-t, --loop]
```

-h or --help list all the commands available

```
# tcpRTT wikipedia.org
[-h, --help]       [-r, --repeat]     [-t, --timeout]
[-p, --port]       [-s, --strict]

optional arguments:
  -h, --help            show this help message and exit
  -p, --port [PORT]     Destination port
  -r, --repeat [REPEAT]
                        How many time measure_latency runs
  -t, --timeout [TIMEOUT]
                        Measure_latency timeout
  -s, --strict          Strict output
```