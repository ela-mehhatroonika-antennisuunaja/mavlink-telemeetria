import time
import sys
import asyncio
import math
import pyproj
import serial
import json
import struct
from pymavlink import mavutil

TESTMODE = False
HOME_LAT = 58.3103108
HOME_LON = 26.6899999
ANT_H = -5
INITBEAR = -1
ARDUINO_PORT = 'COM15'

class Tracker:
    def __init__(self, lat, lon, antennaheight, initbear):
        self.lat = lat
        self.lon = lon
        self.antennaheight = antennaheight
        self.elev = 0
        self.initbear = initbear
        self.geodesic = pyproj.Geod(ellps='WGS84')

        self.dist_from_drone = 0
        self.antennadirection = 0

    def setdirdist(self, long2, lat2):
        fwd_azimuth,back_azimuth,distance = self.geodesic.inv(self.lon, self.lat, long2, lat2) #fwd_azimuth,back_azimuth,distance
        if fwd_azimuth < 0:
            fwd_azimuth = 360 + fwd_azimuth
        self.antennadirection = fwd_azimuth
        self.dist_from_drone  = distance
        return(fwd_azimuth)

    def verticaldirection(self, alt):
        h = self.antennaheight
        dist = self.dist_from_drone
        alt = alt - dist*0.00008
        angle = math.atan((int(alt)-h)/dist)
        angle_deg = angle * 180/math.pi
        return(angle_deg)
    
    def sendtotracker(self, uav):
        datatosend = {}
        horis_dir = self.setdirdist(uav.lon, uav.lat)
        vert_dir = self.verticaldirection(uav.relative_alt)
        datatosend["hor_dir"] = horis_dir
        datatosend["vert_dir"] = vert_dir
        datatosend["initialbear"] = self.initbear
        json_data = json.dumps(datatosend)
        arduino.write((json_data + "\n").encode())
        print("Data sent")

    def sendtotrackerTEST(self, message):
        json_data = json.dumps(message)
        arduino.write((json_data + "\n").encode())
        print("Data sent")

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
tracker = Tracker(HOME_LAT, HOME_LON, ANT_H, INITBEAR)
master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
arduino = serial.Serial(port=ARDUINO_PORT, baudrate=9600, timeout=.1) 

def main():
    if TESTMODE == True:
        data1 = {"hor_dir": 202, "vert_dir": 0, "initialbear": 180}
        while True:
            time.sleep(0.1)
            tracker.sendtotrackerTEST(data1)
    
    master.wait_heartbeat()
    master.mav.param_request_list_send(
        master.target_system, master.target_component
    )

    while True:
        #time.sleep(0.1)
        try:
            uav.SetDataFromMessage(master.recv_match(type='GLOBAL_POSITION_INT', blocking=True))
            print(tracker.antennadirection)
            #corr = 101 - tracker.initbear + tracker.antennadirection
            #print(corr)
            tracker.sendtotracker(uav)
            """
            corr = 0
            corr = 101 - tracker.initbear + tracker.antennadirection
            print(corr)
            if (corr > 360):
                corr = corr - 360
            print(corr)
            print(tracker.antennadirection-tracker.initbear)
            if (corr > 202):
                corr = 202

            if (corr < 0):
                corr = 1
            """
        except Exception as error:
            print(error)
            sys.exit(0)

main()
