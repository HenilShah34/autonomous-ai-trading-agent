import subprocess
import sys
import time
import threading

# Scripts to run
SCRIPTS = [
    "silver.py",
    "gold.py",
    "crude.py",
    "sp500.py"
]


def run_and_monitor(script_name):
    """
    Runs a script and restarts it immediately if it crashes.
    """
    while True:
        print(f"🚀 Starting {script_name}...")

        process = subprocess.Popen([sys.executable, script_name])

        # Wait until the process exits
        process.wait()

        exit_code = process.returncode

        if exit_code == 0:
            print(f"⚠️ {script_name} exited normally. Restarting...")
        else:
            print(f"❌ {script_name} crashed (code {exit_code}). Restarting immediately...")

        time.sleep(1)  # Small safety delay before restart


def main():
    threads = []

    for script in SCRIPTS:
        thread = threading.Thread(
            target=run_and_monitor,
            args=(script,),
            daemon=True
        )
        thread.start()
        threads.append(thread)

    print("\n✅ All scripts are being monitored and auto-restarted.\n")

    # Keep main thread alive forever
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()