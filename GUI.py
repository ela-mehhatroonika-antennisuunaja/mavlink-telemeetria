import tkinter as tk
from tkinter import END
import serial.tools.list_ports
import time
import main
from pymavlink import mavutil

root = tk.Tk()
root.title("Directional Antenna GUI")

HOME_LAT = 58.3103108
HOME_LON = 26.6899999
ANT_H = -5
INITBEAR = -1
ARDUINO_PORT = 'COM15'
MAVLINKIP = "127.0.0.1"
MAVLINKPORT = 14550

uav = main.Uav()
tracker = main.Tracker()
master = mavutil.mavlink_connection(f'udpin:{MAVLINKIP}:{MAVLINKPORT}')

# Initial values
antenna_longitude = tk.DoubleVar()
antenna_latitude = tk.DoubleVar()
antenna_height = tk.DoubleVar()
port = tk.StringVar()
mavlink_ip = tk.StringVar()
mavlink_port = tk.StringVar()
mag_declination = tk.DoubleVar()
mavproxy_connected = tk.BooleanVar()
initialbear = tk.IntVar()

def connect_button_click():
  global mavproxy_connected
  mavproxy_connected = True  
  connection_status.set("Connected")
  lon = uav.lon
  lat = uav.lat
  h = uav.alt

  longitude_entry.delete(0, END) #deletes the current value
  longitude_entry.insert(0, lon) #inserts new value assigned by 2nd parameter

  latitude_entry.delete(0, END) #deletes the current value
  latitude_entry.insert(0, lat) #inserts new value assigned by 2nd parameter

  height_entry.delete(0, END) #deletes the current value
  height_entry.insert(0, h) #inserts new value assigned by 2nd parameter
  #inihdg = uav

def update_settings():
  global arduino
  tracker.lon = antenna_longitude.get()
  tracker.lat = antenna_latitude.get()
  tracker.antennaheight = antenna_height.get()
  tracker.initbear = initialbear.get()
  arduinoport = ARDUINO_PORT
  arduino = serial.Serial(port=arduinoport, baudrate=9600, timeout=.1)

def set_mavproxy():
  global master
  mavlink_portt = str(mavlink_port.get())
  mavlink_ipp = str(mavlink_ip.get())
  master = mavutil.mavlink_connection(f"udpin:{mavlink_ipp}:{mavlink_portt}")
  master.wait_heartbeat()
  master.mav.param_request_list_send(
      master.target_system, master.target_component
  )

settings_frame = tk.Frame(root)
settings_frame.pack(padx=10, pady=10)


antenna_location_label = tk.Label(settings_frame, text="Antenna Information")
antenna_location_label.pack()

def on_select(selection):
    print(selection)


ports = serial.tools.list_ports.comports()
ports1 = []

for el in ports:
  print(el)
  ports1.append(el[0])

print(ports1)
default = tk.StringVar(root, "Select USB Port")
port_dropdown = tk.OptionMenu(settings_frame, default, *ports1, command=on_select) 
port_dropdown.pack() 

mavlink_ip_label = tk.Label(settings_frame, text="MAVLINK IP:")
mavlink_ip_label.pack()
mavlink_ip_entry = tk.Entry(settings_frame, textvariable=mavlink_ip)
mavlink_ip_entry.insert(0, MAVLINKIP)
mavlink_ip_entry.pack()

mavlink_port_label = tk.Label(settings_frame, text="MAVLINK Port:")
mavlink_port_label.pack()
mavlink_port_entry = tk.Entry(settings_frame, textvariable=mavlink_port)
mavlink_port_entry.insert(0, MAVLINKPORT)
mavlink_port_entry.pack()

connect_button = tk.Button(settings_frame, text="Connect to mavlink", command=set_mavproxy)
connect_button.pack(pady=10)



port_label = tk.Label(settings_frame, text="ANTENNA POSITION")
port_label.pack()

longitude_label = tk.Label(settings_frame, text="Longitude:")
longitude_label.pack()
longitude_entry = tk.Entry(settings_frame, textvariable=antenna_longitude)
longitude_entry.pack()

latitude_label = tk.Label(settings_frame, text="Latitude:")
latitude_label.pack()
latitude_entry = tk.Entry(settings_frame, textvariable=antenna_latitude)
latitude_entry.pack()

height_label = tk.Label(settings_frame, text="Height:")
height_label.pack()
height_entry = tk.Entry(settings_frame, textvariable=antenna_height)
height_entry.pack()

inibear_label = tk.Label(settings_frame, text="Initial true heading:")
inibear_label.pack()
inibear_entry = tk.Entry(settings_frame, textvariable=initialbear)
inibear_entry.pack()

mag_declination_label = tk.Label(settings_frame, text="Magnetic Declination \n (pole kohustuslik):")
mag_declination_label.pack()
mag_declination_entry = tk.Entry(settings_frame, textvariable=mag_declination)
mag_declination_entry.pack()

# Connect button
connect_button = tk.Button(settings_frame, text="Autofill from drone \n -needs mavlink connection- \n hooia drooni antenni kohal", command=connect_button_click)
connect_button.pack(pady=10)

connect_button = tk.Button(settings_frame, text="Send Data To Program", command=update_settings)
connect_button.pack(pady=10)

# Apply button (optional) - link to update_settings function if needed
# apply_button = tk.Button(settings_frame, text="Apply", command=update_settings)
# apply_button.pack()

# Display section
display_frame = tk.Frame(root)
display_frame.pack(padx=10, pady=10)

# MavProxy connection status
connection_status_label = tk.Label(display_frame, text="MavProxy Connection:")
connection_status_label.pack()

connection_status = tk.StringVar()
connection_status.set("Disconnected")
connection_status_display = tk.Label(display_frame, textvariable=connection_status, fg="red")
connection_status_display.pack()

# Data display area (optional)
# Add widgets here to display data received from the drone (e.g., labels, graphs)

# Run the main loop

while True:
  root.update()
  try:
    uav.SetDataFromMessage(master.recv_match(type='GLOBAL_POSITION_INT', blocking=True))
    tracker.sendtotracker(uav)
  except Exception as error:
    print(error)