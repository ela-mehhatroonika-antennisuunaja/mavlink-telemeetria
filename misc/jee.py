import socket 
import time
from pymavlink import mavutil
system = mavlink.MAVLink(system_id=255)

UDP_IP = "127.0.0.1" 
UDP_PORT = 14550 
 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT)) 

def handle_message(message):
    if message.get_type() == mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT:
        # Extract relevant data for calculations
        latitude = message.lat / 107
        longitude = message.lon / 107
        altitude = message.alt / 10**3

 
while True: 
    data, addr = sock.recvfrom(1024) 
    handle_message(data)
    time.sleep(0.1)  # Adjust as needed
    print("Received message:", data) 
