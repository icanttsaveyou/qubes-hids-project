import time 
import json
from fim import build_baseline, verify_integrity 
from process_monitor import inspect_processes 

MONITOR_PATHS = ["/etc"]

def run_hids():
    print("Building initial files baseline...")
    build_baseline(MONITOR_PATHS)
    print("HIDS Engine running! Checking every 5 seconds...")

    while True:
        file_alerts = verify_integrity()
        for alert in file_alerts:
            print(json.dumps({"severity": "CRITICAL", "event": alert}))

        time.sleep(5)

if __name__ == "__main__":
    runs_hids() 
