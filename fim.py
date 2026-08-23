import os
import hashlib
import json

CHECKSUM_DB = "fim_baseline.json"

def calculate_sha256(filepath):
  sha256_hash = hashlib.sha256()
  try:
      with open(filepath, "rb") as f: 
          for byte_block in iter(lambda: f.read(4096), b''):
              sha256_hash.update(byte_block)
      return sha256_hash.hexdigest()
  except (PermissionError, FileNotFoundError):
      return None

def build_baseline(directories):
    baseline = {}
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                file_hash = calculate_sha256(full_path)
                if file_hash: 
                    baseline[full_path] = file_hash
    with open(CHECKSUM_DB, "w") as f:
         json.dump(baseline, f, indent=4)
    print("Baseline saved.")

def verify_integrity():
    if not os.path.exists(CHECKSUM_DB):
        return []
    with open(CHECKSUM_DB, "r") as f:
        baseline = json.load(f)
    alerts = []
    for filepath, expected_hash in baseline.items():
        if not os.path.exists(filepath):
            alerts.append({"type": "FILE_DELETED", "path": filepath})
        else: 
            if calculate_sha256(filepath) != expected_hash:
                alerts.append({"type": "FILE_MODIFIED", "path": filepath})
    return alerts
