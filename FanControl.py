#!/usr/bin/env python3
import subprocess
import sys
import termios
import tty
import os

# Adjust for your server's ipmitool device, usually /dev/ipmi0
IPMI_CMD = ["ipmitool", "raw", "0x30", "0x30", "0x02", "0xff"]

def set_manual_mode():
    subprocess.run(["ipmitool", "raw", "0x30", "0x30", "0x01", "0x00"])

def set_auto_mode():
    subprocess.run(["ipmitool", "raw", "0x30", "0x30", "0x01", "0x01"])

def set_fan_speed(percent):
    # Convert percent (1–100) to hex (0x01 – 0x64)
    hex_val = format(percent, "02x")
    subprocess.run(IPMI_CMD + [f"0x{hex_val}"])

def getch():
    """Wait for a single keypress"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    print("=== Dell iDRAC Fan Control Utility ===")
    print("Keys: 1–9 = fan speed 1%–9%, 0 = 10%")
    print("r = restore auto (iDRAC), q = quit\n")

    set_manual_mode()
    print("Manual fan control enabled.")

    while True:
        key = getch()
        if key in "1234567890":
            percent = int(key)
            if percent == 0:
                percent = 10
            set_fan_speed(percent)
            print(f"\nFan speed set to {percent}%")
        elif key.lower() == "r":
            set_auto_mode()
            print("\nRestored automatic fan control to iDRAC")
        elif key.lower() == "q":
#            set_auto_mode()
            print("\nExiting and keeping fan control settings.")
            break

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Run this program as root (sudo).")
        sys.exit(1)
    main()
