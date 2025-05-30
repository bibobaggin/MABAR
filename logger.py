# logger.py
import os, csv
from datetime import datetime

AUDIT_LOG = "audit.log"

def log_activity(username, role, action, details=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {username} ({role}) - {action}: {details}\n"
    # pastikan UTF-8 bila menginginkan Unicode
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(entry)

def tampilkan_audit_log():
    if not os.path.exists(AUDIT_LOG):
        print("Belum ada aktivitas yang dicatat.")
        return
    with open(AUDIT_LOG, newline="", encoding="utf-8") as f:
        for line in f:
            print(line.strip())
