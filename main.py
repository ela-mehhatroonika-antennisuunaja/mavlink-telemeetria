import time
import sys
import asyncio
import math
import pyproj
import serial
import json
import struct
from pymavlink import mavutil
HOME_LAT = 583103823/10000000
HOME_LON = 266901429/10000000
ANT_H = 3
ARDUINO_PORT = 'COM10'

class Tracker:
    def __init__(self, lat, lon, antennaheight):
        self.lat = lat
        self.lon = lon
        self.antennaheight = antennaheight
        self.elev = 0

        self.dist_from_drone = 0
        self.antennadirection = 0

    def setdirdist(self, long2, lat2):
        fwd_azimuth,back_azimuth,distance = geodesic.inv(self.lon, self.lat, long2, lat2) #fwd_azimuth,back_azimuth,distance
        if fwd_azimuth < 0:
            fwd_azimuth = 360 + fwd_azimuth
        self.antennadirection = fwd_azimuth
        self.dist_from_drone  = distance
        return(fwd_azimuth)

    def verticaldirection(self, alt):
        h = self.antennaheight
        dist = self.dist_from_drone
        alt = alt - dist*0.08
        angle = math.atan((int(alt)-h)/dist)
        angle_deg = angle * 180/math.pi
        return(angle_deg)

class Uav:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.lat_rad = 0
        self.lon_rad = 0
        self.alt = 0
        self.relative_alt = 0
        #self.message = "test"
    
    def SetDataFromMessage(self, message):
        #print(f"lon: {message.lon}, lat: {message.lat}, alt: {message.alt}, relalt: {message.relative_alt}")
        self.lon = int(message.lon)/10000000
        self.lat = int(message.lat)/10000000
        self.lon_rad = math.radians(self.lon)
        self.lat_rad = math.radians(self.lat)
        self.relative_alt = message.relative_alt/1000

uav = Uav()
tracker = Tracker(HOME_LAT, HOME_LON, ANT_H)
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
arduino = serial.Serial(port=ARDUINO_PORT, baudrate=9600, timeout=.1) 
geodesic = pyproj.Geod(ellps='WGS84')
"""
master.wait_heartbeat()
master.mav.param_request_list_send(
    master.target_system, master.target_component
)
"""

def datafromtelemetry():
    while True:
        time.sleep(2)
        try:
            DataToSend = {}
            message = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            uav.SetDataFromMessage(message)
            horis_dir = tracker.setdirdist(uav.lon, uav.lat)
            vert_dir = tracker.verticaldirection(uav.relative_alt)
            print(f"suund: {horis_dir} vert suund: {vert_dir} alt {uav.relative_alt}")
            """
            #DataToSend = {"hor_dir" : horis_dir, "vert_dir" : vert_dir} Äkki saab seda kasutada, kaks rida veits jama
            DataToSend["hor_dir"] = horis_dir
            DataToSend["vert_dir"] = vert_dir
            DataToSend = str(json.dumps(DataToSend))
            print(DataToSend)
            #sendtoarduino(DataToSend)
            """
        except Exception as error:
            print(error)
            sys.exit(0)

def sendtoarduino(hor, vert, initialbear):
    data = serialize_data(hor, vert, initialbear)
    print(data)
    arduino.write(data)
    arduino.flush()
    data1 = arduino.readline().decode()
    print(f"rec: {data1}")

def serialize_data(hor_dir, vert_dir, initialbear):
    data = struct.pack('fff', hor_dir, vert_dir, initialbear)
    return data

while True:
    sendtoarduino(1.2, 2.0, 50.0)
    time.sleep(0.2)
#datafromtelemetry()
#lat : 583103823, lon : 266901429
