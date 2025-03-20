# FloodStrike v1.0

## Overview
FloodStrike v1.0 is a tool designed to simulate high traffic loads on a server for testing and evaluation purposes. It helps in analyzing how a server handles multiple simultaneous requests. **Use this tool responsibly and only with explicit permission.**

## Features
- Customizable user-agent requests
- Multi-threaded execution for stress testing
- Proxy bot-based request simulation
- Configurable target IP, port, and thread count
- Logs successful request attempts

## Usage
```
python3 floodstrike.py -s <server_ip> -p <port> -t <threads>
```
### Options:
- `-s` or `--server` : Target server IP address
- `-p` or `--port` : Target port (default: 80)
- `-t` or `--threads` : Number of concurrent threads (default: 135)
- `-h` or `--help` : Display usage information

### Example:
```
python3 floodstrike.py -s 192.168.1.1 -p 8080 -t 200
```

## Prerequisites
- Python 3.x
- Required libraries: `socket`, `threading`, `queue`, `urllib.request`

## Legal Disclaimer
This tool is intended for educational and authorized testing purposes only. Unauthorized use against public systems is illegal and may result in legal consequences. **Use it only on systems you own or have explicit permission to test.**

## License
This tool is provided as-is without any warranty. Use it responsibly and at your own risk.

