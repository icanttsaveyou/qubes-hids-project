import psutil

SUSPICIOUS_PATHS = ["/tmp", "/var/tmp", "/dev/shm"]

def inspect_processes():
    findings = []
    for proc in psutil.process_inter(['pid', 'name', 'exe']):
        try:
            exe_path = proc.info['exe']
            if exe_path:
                for bad_path in SUSPICIOUS_PATHS:
                    if exe_path.startswith(bad_path):
                        findings.append({
                            "type": "SUSPICIOUS_PROCESS",
                            "pid": proc.info['pid'],
                            "name": proc.info['name'],
                            "path": exe_path
                        })   
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue 
    return findings
