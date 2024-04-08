# Disable "Broad exception" warning
# pylint: disable=W0703

import time
import sys

# Import mavutil
from pymavlink import mavutil

# Create the connection 
master = mavutil.mavlink_connection('com14', baud=57600)

# Wait a heartbeat before sending commands
master.wait_heartbeat()

# Request all parameters
master.mav.param_request_list_send(
    master.target_system, master.target_component
)

# Open a file for writing
with open('logoes.txt', 'w') as f:
    def printlonlat(message):
        f.write(f"{message.lat}\n")
        f.write(f"{message.lon}\n")

    while True:
        time.sleep(0.01)
        try:
            message = master.recv_match(blocking=True)
            print(message)
            f.write(f"{message}\n")  # Write message to file
            """
            # Uncomment the following lines to parse and log specific message fields
            # message = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            # printlonlat(message)
            """
        except Exception as error:
            print(error)
            sys.exit(0)
