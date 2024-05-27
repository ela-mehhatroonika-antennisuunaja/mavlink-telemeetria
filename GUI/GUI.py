import tkinter as tk
import serial.tools.list_ports
import time

root = tk.Tk()
root.title("Directional Antenna GUI")

# Initial values
antenna_longitude = tk.DoubleVar()
antenna_latitude = tk.DoubleVar()
antenna_height = tk.DoubleVar()
port = tk.StringVar()
mavlink_ip = tk.StringVar()
mavlink_port = tk.StringVar()
mag_declination = tk.DoubleVar()
mavproxy_connected = tk.BooleanVar()

def connect_button_click():
  global mavproxy_connected
  mavproxy_connected = True  
  connection_status.set("Connected")

def update_settings():
    antenna_longitudee = antenna_longitude.get()
    antenna_latitudee = antenna_latitude.get()
    antenna_heightt = antenna_height.get()
    mag_declinationn = mag_declination.get()

def set_mavproxy():
  mavlink_portt = mavlink_port.get()
  mavlink_ipp = mavlink_ip.get()

settings_frame = tk.Frame(root)
settings_frame.pack(padx=10, pady=10)


antenna_location_label = tk.Label(settings_frame, text="Antenna Information")
antenna_location_label.pack()

def on_select(selection):
    print(selection)

ports = serial.tools.list_ports.comports()
ports1 = []
for el in ports:
   ports1.append(el[0])
default = tk.StringVar(root, "Select USB Port")
port_dropdown = tk.OptionMenu(settings_frame, default, ports1, command=on_select) 
port_dropdown.pack() 

mavlink_ip_label = tk.Label(settings_frame, text="MAVLINK IP:")
mavlink_ip_label.pack()
mavlink_ip_entry = tk.Entry(settings_frame, textvariable=mavlink_ip)
mavlink_ip_entry.pack()

mavlink_port_label = tk.Label(settings_frame, text="MAVLINK Port:")
mavlink_port_label.pack()
mavlink_port_entry = tk.Entry(settings_frame, textvariable=mavlink_port)
mavlink_port_entry.pack()

connect_button = tk.Button(settings_frame, text="Connect to drone", command=connect_button_click)
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

mag_declination_label = tk.Label(settings_frame, text="Magnetic Declination:")
mag_declination_label.pack()
mag_declination_entry = tk.Entry(settings_frame, textvariable=mag_declination)
mag_declination_entry.pack()

# Connect button
connect_button = tk.Button(settings_frame, text="Get Position Data From Drone", command=connect_button_click)
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