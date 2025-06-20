# Prepare Wireshark for analysis
- Run Wireshark with `tcp.port == 80` filter to see the attacking traffic.
- Instead of `80`, use the right port you are using in the attacking tool.
- You may need to use `ip.addr == 192.168.8.40 and tcp.port == 80` to shorten the displayed traffic, where `192.168.8.40` is the target IP.
- Make sure the service in the targeted machine is running and not blocked by firewall, otherwise you will see the expected traffic or flags like `[SYN, ACK]` in Wireshark.
    - To make sure the service is accessible, check in Kali using `nmap 192.168.8.40 -p 80`. The port status should be `open`, not `closed` nor `filtered`.

<!-- # DDoS types
- SYN Flood, see the next section.
- UDP Flood.
    - Using `sudo hping3 -c 1000 -u -p 53 targetIP -d 1024 --fast`.
        - `-u` for UDP.        
        - `-p` for port number.
        - `-d` for packet size, the default 56.
        - `--fast` for more aggressive faster attack.
- ACK Flood.
- HTTP Flood.
    - Using ApacheBench `ab -n 1000 -c 100 http://targetIP/`.
        - `-n` is total requests.
        - `-c` is how many requests will be sent at a time, `-c` can't be be grater than `-n`.
        - This will send starting and finishing TCP handshake.
    - Siege (not in Kali by default) `siege -c 200 -t 60s http://targetIP/`.
        - `-c` is how many requests will be sent at a time.
        - `-t` attack time limit.
- DNS Amplification.
- DNS Flood.
- Slowloris.
- Ping of Death (Outdated).
- ICMP Flood using `ping -f <targetIP>` or `sudo hping3 <targetIP> --icmp --flood`.
- Smurf Attack. 
- QUIC Flood.
-->

<!-- # SYN DoS attack methods in Kali for practising:
Using Ettercap:
- `sudo ettercap -TQP dos_attack`. 
    - `dos_attack` for DoS attack plugin, more plugins [here](https://linux.die.net/man/8/ettercap_plugins).
    - `-TQ` is two options, `-T` and `-Q`:
        - `-T` means text mode without GUI.
        - `-Q` means quiet mode with minimal displayed info in the terminal.

Using Metasploit SYN Flood:
- `sudo msfconsole`.
- `search dos` or `search dos syn`.
- `use auxiliary/dos/tcp/synflood`.
- `options` or `info`.
- `set rhosts 192.168.8.40` remote host.
- `set rport 80`remote port.
- `set num 30`number of packets, skip this step for unlimited.
- Check the options again using `options`.
- Run using `run` or `exploit`.

Using hping3
- `sudo hping3 192.168.8.40 --rand-source --destport 80 --syn`.
- More aggressive and not suitable for VM `sudo hping3 10.20.0.10 --flood --rand-source --destport 80 --syn -d 120 -w 64`. -->

# ddos-attack-app.py
This script is to simulate the SYN DoS attack, it has the option to run it with command and arguments only, or with GUI window.
This file can be helpful to show how to utilise Python Tkinter for GUI Window.
- With GUI option: `sudo python ~/Downloads/ddos-attack-app.py`.
- Without GUI option: `sudo python ~/Downloads/ddos-attack-app.py 192.168.8.40 80 30`.
    - `192.168.8.40` is the target IP.
    - `80` is the services port in the target machine.
    - `30` is the number of attacking packets.
- A random source IP `192.168.x.x` will be generated and used each time the command implemented.

# ddos-attack.py
For simplicity and class discussions, this file is like `ddos-attack-app.py` but without GUI.
- Download, then use `sudo python ~/Downloads/ddos-attack.py 192.168.8.40 80 30` to run it. 

# attackd-repeater.py
This file is to simulate the distribution in DDoS attack, it will run `ddos-attack-app.py` multiple times almost simultaneously with multithreading capability.
- Move to where is `ddos-attack-app.py` located, like using `cd Downloads`.
- Download, then use `sudo python attackd-repeater.py -a` to run it then follow the prompt.
- You have the option to use the GUI window via `sudo python attackd-repeater.py`.
- Use `python attackd-repeater.py -h` to see the help menu.
- Notice that `attackd-repeater.py` is general and can repeat the running of any command.

# ddos-detect.py
- Just run this script using `sudo python ~/Downloads/ddos-detect.py`, it will detect SYN DoS traffic, it will show the detection in the terminal and save the output in `syn-flood-log.txt`.