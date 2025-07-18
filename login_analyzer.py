#!/usr/bin/env python3
import subprocess
import time
from datetime import datetime

OUTPUT_FILE = "/home/mehdi/Desktop/login_monitor.txt"


def check_auth_log():
    try:
        # First try auth.log (Debian/Ubuntu systems)
        logs = (
            subprocess.check_output(["tail", "-n", "10", "/var/log/auth.log"])
            .decode()
            .split("\n")
        )
    except FileNotFoundError:
        try:
            # Checking secure (RHEL/CentOS systems)
            logs = (
                subprocess.check_output(["tail", "-n", "10", "/var/log/secure"])
                .decode()
                .split("\n")
            )
        except FileNotFoundError:
            logs = []
    return logs


def monitor_logins():
    last_seen = set()

    while True:
        current_logs = check_auth_log()
        new_logins = []

        for line in current_logs:
            if (
                "session opened" in line.lower() or "user login" in line.lower()
            ) and line not in last_seen:
                new_logins.append(line)
                last_seen.add(line)

        if new_logins:
            with open(OUTPUT_FILE, "a") as f:
                timestamp = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                f.write(f"\n=== New logins detected at {timestamp} ===\n")
                f.write("\n".join(new_logins) + "\n")
                print(
                    f"Detected {len(new_logins)} new login(s). Saved to {OUTPUT_FILE}"
                )

        time.sleep(60)


if __name__ == "__main__":
    print(f"Monitoring system logins. Output will be saved to {OUTPUT_FILE}")
    try:
        monitor_logins()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
