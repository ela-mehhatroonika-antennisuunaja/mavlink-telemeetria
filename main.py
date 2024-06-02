import time
import serial
import math
import pyproj
import json
import configparser
from pymavlink import mavutil

config = configparser.ConfigParser()
config.read('config.ini')

MAVLINK_IP = str(config['Mavlink/Mavproxy']['mavlink_ip'])
MAVLINK_PORT = str(config['Mavlink/Mavproxy']['mavlink_port'])
HOME_LAT = float(config['Antenna tracker data']['home_latitude'])
HOME_LON = float(config['Antenna tracker data']['home_longitude'])
SET_GPS_FROM_DRONE = bool(config['Antenna tracker data']['set_location_from_drone'])
ANT_H = int(config['Antenna tracker data']['antenna_height'])
INITBEAR = int(config['Antenna tracker data']['initial_true_course'])
ARDUINO_PORT = str(config['Arduino']['arduino_port'])

class Tracker:
    def __init__(self, lat = 0, lon = 0, antennaheight = 0, initbear = 0):
        self.lat = lat
        self.lon = lon
        self.antennaheight = antennaheight
        self.elev = 0
        self.initbear = initbear
        self.geodesic = pyproj.Geod(ellps='WGS84')

        self.dist_from_drone = 0
        self.antennadirection = 0
        self.arduino = None

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
        self.arduino.write((json_data + "\n").encode())
        print("Data sent")

    def sendtotrackerTEST(self, message):
        json_data = json.dumps(message)
        self.arduino.write((json_data + "\n").encode())
        print("Data sent")

class Uav:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.lat_rad = 0
        self.lon_rad = 0
        self.alt = 0
        self.relative_alt = 0
    
    def SetDataFromMessage(self, message):
        self.lon = int(message.lon)/10000000
        self.lat = int(message.lat)/10000000
        self.lon_rad = math.radians(self.lon)
        self.lat_rad = math.radians(self.lat)
        self.relative_alt = message.relative_alt/1000

def main():
    print(f"Ootan mavlinki heartbeati {MAVLINK_IP}:{MAVLINK_PORT}")
    master.wait_heartbeat()
    master.mav.param_request_list_send(
        master.target_system, master.target_component
    )
    print("Heartbeat olemas (süsteem %u komponent %u)" % (master.target_system, master.target_component))

    if SET_GPS_FROM_DRONE == True:
        input("PANE MÕS või MÕS-i GPS TÄPSELT ANTENNI TORNI KOHALE, seejärel vajuta enter.")
        message = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        HOME_LAT = int(message.lat)/10000000
        HOME_LON = int(message.lon)/10000000
        print(f"Antenni asukoht seatud drooni asukohast: {HOME_LAT} {HOME_LON}")

    try:
        message = master.mav.command_long_encode(
                master.target_system,  # Target system ID
                master.target_component,  # Target component ID
                mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,  # ID of command to send
                0,  # Confirmation
                mavutil.mavlink.GLOBAL_POSITION_INT,  # param1: Message ID to be streamed
                500_000, # param2: Interval in microseconds
                0,       # param3 (unused)
                0,       # param4 (unused)
                0,       # param5 (unused)
                0,       # param5 (unused)
                0        # param6 (unused)
                )

        # Send the COMMAND_LONG
        master.mav.send(message)
    except Exception as error:
        print(error)


    while True:
        try:
            uav.SetDataFromMessage(master.recv_match(type='GLOBAL_POSITION_INT', blocking=True))
            print(tracker.antennadirection)
            tracker.sendtotracker(uav)
            master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS, 
                                      mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0) #Peab kontrollima
        except Exception as error:
            print(error)

if __name__ == "__main__":
    uav = Uav()
    tracker = Tracker(HOME_LAT, HOME_LON, ANT_H, INITBEAR)
    master = mavutil.mavlink_connection(f'udpin:{MAVLINK_IP}:{MAVLINK_PORT}')
    tracker.arduino = serial.Serial(port=ARDUINO_PORT, baudrate=9600, timeout=.1) 
    main()