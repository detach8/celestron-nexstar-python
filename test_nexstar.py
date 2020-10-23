#!/usr/bin/python3
import sys
import serial
import datetime
import celestron_nexstar

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} [device]")
    print(f"E.g. : {sys.argv[0]} /dev/ttyUSB0")
    sys.exit()

# Connect to serial port
ser = serial.Serial(sys.argv[1], 9600)

# Create a new NexStarClient instance
nexstar = celestron_nexstar.NexStarClient(ser)

# Ping to check comms
print('Ping:', nexstar.ping())

# Cancel any GOTO action
nexstar.cancel_goto()

# Sync clock with system
now = datetime.datetime.now()
nexstar.set_time(now.year, now.month, now.day, now.hour, now.minute, now.second, 8, 0)

# Get some info
print('Time:', nexstar.get_time())
print('Location:', nexstar.get_location())
print('Model:', nexstar.get_model())
print('Version:', nexstar.get_version())
print('AZM/RA:', nexstar.get_device_version(nexstar.DEVICE_AZM_RA))
print('ALT/DEC:', nexstar.get_device_version(nexstar.DEVICE_ALT_DEC))
print('Is Aligned:', nexstar.is_aligned())
print('GOTO in progress:', nexstar.is_goto_in_progress())
