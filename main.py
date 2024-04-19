import time
import sys
import asyncio
import math
from pymavlink import mavutil
#https://stackoverflow.com/questions/54873868/python-calculate-bearing-between-two-lat-long
HOME_LAT = 583103823/10000000
HOME_LON = 266901429/10000000

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
    
#message = message()

#master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master = mavutil.mavlink_connection('udpin:127.0.0.1:14551')
master.wait_heartbeat()
master.mav.param_request_list_send(
    master.target_system, master.target_component
)

def getlonlatalt(message):
    #print(f"lon: {message.lon}, lat: {message.lat}, alt: {message.alt}, relalt: {message.relative_alt}")
    lon = message.lon
    lat = message.lat
    alt = message.relative_alt
    alt = alt/1000
    lon = lon/10000000
    lat = lat/10000000
    pos = [lat, lon, alt]
    return(pos)


def distance(glon, glat, dlon, dlat):
    #print(glon, glat, dlon, dlat)
    R = 6372.795477598
    dist = R*math.acos(math.sin(glat)*math.sin(dlat)+math.cos(glat)*math.cos(dlat)*math.cos(glon-dlon))
    print(f"dist: {dist}")
    return(dist)

def direction(glon, glat, dlon, dlat):
    # Calculate difference in longitude, considering the shortest angular distance
    print(glon, glat, dlon, dlat)
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
    return(bear_deg)

def direction_A(glon, glat, dlon, dlat):
    # Calculate difference in longitude, considering the shortest angular distance
    deltalon = dlon - glon
    if abs(deltalon) > math.pi:
        if deltalon > 0:
            deltalon -= 2 * math.pi
        else:
            deltalon += 2 * math.pi
    
    # Calculate heading using atan2
    heading = math.atan2(math.sin(deltalon), math.cos(glat) * math.tan(dlat) - math.sin(glat) * math.cos(deltalon))
    
    # Convert heading from radians to degrees
    heading_degrees = math.degrees(heading)
    
    # Adjust heading to make 0 degrees represent true north
    heading_degrees = (heading_degrees + 360) % 360
    
    return heading_degrees
    
    # Calculate heading using atan2
    heading = math.atan2(math.sin(deltalon), math.cos(glat) * math.tan(dlat) - math.sin(glat) * math.cos(deltalon))
    
    # Convert heading from radians to degrees
    heading_degrees = math.degrees(heading)
    
    return heading_degrees

def verticaldirection(glon, glat, dlon, dlat, alt):
    h = 3
    dist = distance(glon, glat, dlon, dlat)*1000
    alt = alt - dist*0.08
    angle = math.atan((int(alt)-h)/dist)
    angle_deg = angle * 180/math.pi
    return(angle_deg)

def datafromtelemetry():
    while True:
        time.sleep(0.2)
        try:
            #message = master.recv_match(blocking=True)
            #print(message)
            message = master.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            pos = getlonlatalt(message)
            lat, lon, alt = pos[0], pos[1], pos[2]
            dir = direction_A(ll(HOME_LON), ll(HOME_LAT), ll(lon), ll(lat))
            vdir = verticaldirection(ll(HOME_LON),ll(HOME_LAT), ll(lon), ll(lat), alt)
            print(f"suund: {dir}")
            print(f"vert suund: {vdir}")

        except Exception as error:
            print(error)
            sys.exit(0)

def ll(coord):
    coord = coord
    coord = coord*math.pi/180
    return(coord)

datafromtelemetry()
direction(ll(266901429),ll(583103823),ll(242818695),ll(594573600))
distance(ll(266901429),ll(583103823),ll(242818695),ll(594573600))
verticaldirection(ll(266901429),ll(583103823),ll(242818695),ll(594573600), 10)

#lat : 583103823, lon : 266901429
