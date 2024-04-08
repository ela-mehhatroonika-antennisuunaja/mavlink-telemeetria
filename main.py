import time
import sys
import asyncio
import math
from pymavlink import mavutil

"""
master = mavutil.mavlink_connection('com14', baud=57600)
master.wait_heartbeat()
master.mav.param_request_list_send(
    master.target_system, master.target_component
)
"""

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
    print(bear)


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

direction(ll(266901429),ll(583103823),ll(242818695),ll(594573600))
#lat : 583103823, lon : 266901429
