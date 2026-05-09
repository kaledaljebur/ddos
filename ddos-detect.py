# https://github.com/kaledaljebur/ddos
from scapy.all import *
from collections import defaultdict
import time
import sys
import os
import queue
import tkinter as tk
from tkinter import ttk

threshold = 20
interval = 5
logFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "syn-flood-log.txt")

def makeAnalyzer(msgQueue=None):
    synCounts = defaultdict(int)
    lastReset = [time.time()]

    def analyzePacket(packet):
        if time.time() - lastReset[0] > interval:
            synCounts.clear()
            lastReset[0] = time.time()
        if packet.haslayer(TCP) and packet[TCP].flags == "S":
            srcIP = packet[IP].src
            synCounts[srcIP] += 1
            if synCounts[srcIP] > threshold:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                msg = f"[{timestamp}] Possible SYN flood from {srcIP} ({synCounts[srcIP]} SYNs in {interval}s)\n"
                if msgQueue:
                    msgQueue.put(msg)
                else:
                    print(msg, end="")
                with open(logFile, "a") as f:
                    f.write(msg)

    return analyzePacket

def startMonitor(interface=None):
    if interface is None:
        interface = conf.iface
    print(f"[+] Monitoring on {interface} (Threshold: {threshold} SYNs/{interval}s)")
    print(f"[+] Logging to {logFile}")
    sniff(iface=interface, prn=makeAnalyzer(), filter="tcp[tcpflags] == tcp-syn")

def guiFunction():
    root = tk.Tk()
    root.title("SYN Flood Detector (Educational)")

    mainFrame = ttk.Frame(root, padding="10")
    mainFrame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainFrame, text="Interface:").grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    interfaces = get_if_list()
    ifaceVar = tk.StringVar(value=str(conf.iface))
    ifaceCombo = ttk.Combobox(mainFrame, textvariable=ifaceVar, values=interfaces, state="readonly", width=25)
    ifaceCombo.grid(column=1, row=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    ttk.Label(mainFrame, text="Output:").grid(column=0, row=1, sticky=tk.W, padx=5)
    outputText = tk.Text(mainFrame, height=15, width=60, state=tk.DISABLED)
    outputText.grid(column=0, row=2, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
    scrollbar = ttk.Scrollbar(mainFrame, command=outputText.yview)
    scrollbar.grid(column=3, row=2, sticky=(tk.N, tk.S))
    outputText.config(yscrollcommand=scrollbar.set)

    msgQueue = queue.Queue()
    sniffer = [None]

    def appendOutput(msg):
        outputText.config(state=tk.NORMAL)
        outputText.insert(tk.END, msg)
        outputText.see(tk.END)
        outputText.config(state=tk.DISABLED)

    def pollQueue():
        while not msgQueue.empty():
            appendOutput(msgQueue.get_nowait())
        root.after(200, pollQueue)

    def startDetection():
        iface = ifaceVar.get()
        outputText.config(state=tk.NORMAL)
        outputText.delete(1.0, tk.END)
        outputText.config(state=tk.DISABLED)
        sniffer[0] = AsyncSniffer(iface=iface, prn=makeAnalyzer(msgQueue), filter="tcp[tcpflags] == tcp-syn")
        sniffer[0].start()
        appendOutput(f"[+] Monitoring on {iface} (Threshold: {threshold} SYNs/{interval}s)\n")
        appendOutput(f"[+] Logging to {logFile}\n\n")
        startButton.config(state=tk.DISABLED)
        stopButton.config(state=tk.NORMAL)

    def stopDetection():
        if sniffer[0]:
            try:
                sniffer[0].stop(join=False)
            except Exception:
                pass
            sniffer[0] = None
        appendOutput("[✓] Monitoring stopped.\n")
        startButton.config(state=tk.NORMAL)
        stopButton.config(state=tk.DISABLED)

    def showHelp():
        helpText = """SYN Flood Detector (Educational Use Only)

This tool monitors network traffic and alerts when a possible
SYN flood attack is detected from any source IP.

How it works:
  - Sniffs TCP SYN packets on the selected interface.
  - Alerts if any single source exceeds the threshold
    (default: 20 SYNs within 5 seconds).
  - Detections are logged to: syn-flood-log.txt
    (saved next to this script).

IMPORTANT: Must be run with high privileges (sudo), otherwise
the sniffer cannot capture packets and will detect nothing.
  sudo python ddos-detect.py

CLI Usage (no GUI):
  sudo python ddos-detect.py <interface>
  Example: sudo python ddos-detect.py eth0

https://github.com/kaledaljebur/ddos
"""
        top = tk.Toplevel(root)
        top.title("Help")
        top.geometry("560x380")
        textFrame = ttk.Frame(top)
        textFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(textFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        helpWidget = tk.Text(textFrame, wrap=tk.WORD, padx=8, pady=8, yscrollcommand=scrollbar.set)
        helpWidget.insert(tk.END, helpText)
        helpWidget.config(state=tk.DISABLED)
        helpWidget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=helpWidget.yview)
        ttk.Button(top, text="Close", command=top.destroy).pack(pady=5)

    buttonFrame = ttk.Frame(mainFrame)
    buttonFrame.grid(column=0, row=3, columnspan=2, pady=5)
    startButton = ttk.Button(buttonFrame, text="Start", command=startDetection)
    startButton.pack(side=tk.LEFT, padx=5)
    stopButton = ttk.Button(buttonFrame, text="Stop", command=stopDetection, state=tk.DISABLED)
    stopButton.pack(side=tk.LEFT, padx=5)
    ttk.Button(buttonFrame, text="Help", command=showHelp).pack(side=tk.LEFT, padx=5)

    pollQueue()

    def onClose():
        if sniffer[0]:
            try:
                sniffer[0].stop(join=False)
            except Exception:
                pass
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", onClose)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        guiFunction()
    else:
        startMonitor(interface=sys.argv[1])
