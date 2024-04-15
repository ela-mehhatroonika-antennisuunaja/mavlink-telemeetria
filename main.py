import time
import sys
import asyncio
import math
from pymavlink import mavutil

class message:
    def __init__(self):
        self.lat = 0
        self.lon = 0
        self.alt = 0
        self.message = "test"
    
    def getlonlat(self, message):
        print(f"lon: {message.lon}, lat: {message.lat}, alt: {message.alt}, relalt: {message.relative_alt}")
        self.lon = int(message.lon)/10000000
        self.lat = int(message.lat)/10000000
    
message = message()

master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
master.mav.param_request_list_send(
    master.target_system, master.target_component
)

def getlonlat(message):
    print(f"lon: {message.lon}, lat: {message.lat}, alt: {message.alt}, relalt: {message.relative_alt}")
    lon = message.lon
    lat = message.lat
    lon = lon/10000000
    lat = lat/10000000
    print(lon, lat)


def distance(glon, glat, dlon, dlat):
    R = 6372.795477598
    dist = R*math.acos(math.sin(glat)*math.sin(dlat)+math.cos(glat)*math.cos(dlat)*math.cos(glon-dlon))
    print(dist)
    return(dist)

def direction(glon, glat, dlon, dlat):
    # Calculate difference in longitude, considering the shortest angular distance
    deltalon = dlon - glon
    if abs(deltalon) > math.pi:
        if deltalon > 0:
            deltalon -= 2 * math.pi
        else:
            deltalon += 2 * math.pi

    # Calculate bearing
    deltafi = math.log((math.tan((dlat*0.5) + (math.pi*0.25))) / (math.tan(glat*0.5 + math.pi*0.25)))
    bear = math.atan2(deltalon, deltafi)
    bear_deg = bear * 180/math.pi
    print(bear_deg)

def verticaldirection(glon, glat, dlon, dlat, alt):
    h = 3
    dist = distance(glon, glat, dlon, dlat)
    alt = alt - dist*0.08
    angle = math.atan((int(alt)-h)/dist)
    angle_deg = angle * 180/math.pi
    print(angle_deg)

def datafromtelemetry():
    while True:
        time.sleep(0.01)
        try:
            #message = master.recv_match(blocking=True)
            #print(message)
            message = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            getlonlat(message)
            """
            print('name: %s\tvalue: %d' % (message['param_id'],
                                        message['param_value']))
            """
        except Exception as error:
            print(error)
            sys.exit(0)

def ll(coord):
    coord = coord/10000000
    coord = coord*math.pi/180
    return(coord)

datafromtelemetry()
direction(ll(266901429),ll(583103823),ll(242818695),ll(594573600))
distance(ll(266901429),ll(583103823),ll(242818695),ll(594573600))
verticaldirection(ll(266901429),ll(583103823),ll(242818695),ll(594573600), 10)

#lat : 583103823, lon : 266901429
