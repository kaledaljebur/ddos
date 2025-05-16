from scapy.all import *
from collections import defaultdict
import time

threshold = 20 
interval = 5   
logFile = "syn-flood-log.txt"

synCounts = defaultdict(int)
lastReset = time.time()

def logAttack(ip, count):
    outText1="""Logs potential SYN flood attacks to a file."""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    logMsg = f"[{timestamp}] Possible SYN flood from {ip} ({count} SYNs in {interval}s)\n"
    print(logMsg, end="")
    with open(logFile, "a") as f:
        f.write(logMsg)

def analyzePacket(packet):
    outText2="""Processes each packet and checks for SYN floods."""
    global lastReset
    
    if time.time() - lastReset > interval:
        synCounts.clear()
        lastReset = time.time()
    
    if packet.haslayer(TCP) and packet[TCP].flags == "S":
        srcIP = packet[IP].src
        synCounts[srcIP] += 1
        
        if synCounts[srcIP] > threshold:
            logAttack(srcIP, synCounts[srcIP])

def startMonitor(interface="eth0"):
    outText3="""Starts the SYN flood monitor."""
    print(f"[+] Monitoring for SYN floods on {interface} (Threshold: {threshold} SYNs/{interval}s)")
    print(f"[+] Logging to {logFile}")
    sniff(iface=interface, prn=analyzePacket, filter="tcp[tcpflags] == tcp-syn")

if __name__ == "__main__":
    startMonitor()