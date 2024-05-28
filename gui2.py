import tkinter as tk
from tkinter import END, messagebox
import serial.tools.list_ports
from pymavlink import mavutil
import main
import threading

class DirectionalAntennaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Directional Antenna GUI")

        self.HOME_LAT = 58.3103108
        self.HOME_LON = 26.6899999
        self.ANT_H = -5
        self.INITBEAR = -1
        self.ARDUINO_PORT = 'COM15'
        self.MAVLINKIP = "127.0.0.1"
        self.MAVLINKPORT = 14551

        self.uav = main.Uav()
        self.tracker = main.Tracker()

        # Initial values
        self.antenna_longitude = tk.DoubleVar()
        self.antenna_latitude = tk.DoubleVar()
        self.antenna_height = tk.DoubleVar()
        self.port = tk.StringVar()
        self.mavlink_ip = tk.StringVar()
        self.mavlink_port = tk.StringVar()
        self.mag_declination = tk.DoubleVar()
        self.mavproxy_connected = tk.BooleanVar()
        self.initialbear = tk.IntVar()

        self.setup_gui()
        self.start_background_task()

    def setup_gui(self):
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(padx=10, pady=10)

        tk.Label(settings_frame, text="Antenna Information").pack()

        ports = serial.tools.list_ports.comports()
        ports1 = [el[0] for el in ports]

        default = tk.StringVar(self.root, "Select USB Port")
        port_dropdown = tk.OptionMenu(settings_frame, default, *ports1, command=self.on_select)
        port_dropdown.pack()

        tk.Label(settings_frame, text="MAVLINK IP:").pack()
        mavlink_ip_entry = tk.Entry(settings_frame, textvariable=self.mavlink_ip)
        mavlink_ip_entry.insert(0, self.MAVLINKIP)
        mavlink_ip_entry.pack()

        tk.Label(settings_frame, text="MAVLINK Port:").pack()
        mavlink_port_entry = tk.Entry(settings_frame, textvariable=self.mavlink_port)
        mavlink_port_entry.insert(0, self.MAVLINKPORT)
        mavlink_port_entry.pack()

        tk.Button(settings_frame, text="Connect to mavlink", command=self.set_mavproxy).pack(pady=10)

        tk.Label(settings_frame, text="ANTENNA POSITION").pack()

        tk.Label(settings_frame, text="Longitude:").pack()
        self.longitude_entry = tk.Entry(settings_frame, textvariable=self.antenna_longitude)
        self.longitude_entry.pack()

        tk.Label(settings_frame, text="Latitude:").pack()
        self.latitude_entry = tk.Entry(settings_frame, textvariable=self.antenna_latitude)
        self.latitude_entry.pack()

        tk.Label(settings_frame, text="Height:").pack()
        self.height_entry = tk.Entry(settings_frame, textvariable=self.antenna_height)
        self.height_entry.pack()

        tk.Label(settings_frame, text="Initial true heading:").pack()
        self.inibear_entry = tk.Entry(settings_frame, textvariable=self.initialbear)
        self.inibear_entry.pack()

        tk.Label(settings_frame, text="Magnetic Declination \n (pole kohustuslik):").pack()
        mag_declination_entry = tk.Entry(settings_frame, textvariable=self.mag_declination)
        mag_declination_entry.pack()

        tk.Button(settings_frame, text="Autofill from drone \n -needs mavlink connection- \n hooia drooni antenni kohal", command=self.connect_button_click).pack(pady=10)

        tk.Button(settings_frame, text="Send Data To Program", command=self.update_settings).pack(pady=10)

        display_frame = tk.Frame(self.root)
        display_frame.pack(padx=10, pady=10)

        tk.Label(display_frame, text="MavProxy Connection:").pack()

        self.connection_status = tk.StringVar()
        self.connection_status.set("Disconnected")
        self.connection_status_display = tk.Label(display_frame, textvariable=self.connection_status, fg="red")
        self.connection_status_display.pack()

    def connect_button_click(self):
        self.mavproxy_connected.set(True)
        self.connection_status.set("Connected")

        lon = self.uav.lon
        lat = self.uav.lat
        h = self.uav.alt

        self.longitude_entry.delete(0, END)
        self.longitude_entry.insert(0, lon)

        self.latitude_entry.delete(0, END)
        self.latitude_entry.insert(0, lat)

        self.height_entry.delete(0, END)
        self.height_entry.insert(0, h)

    def update_settings(self):
        self.tracker.lon = self.antenna_longitude.get()
        self.tracker.lat = self.antenna_latitude.get()
        self.tracker.antennaheight = self.antenna_height.get()
        self.tracker.initbear = self.initialbear.get()
        arduinoport = self.ARDUINO_PORT
        self.arduino = serial.Serial(port=arduinoport, baudrate=9600, timeout=.1)

    def set_mavproxy(self):
        threading.Thread(target=self.connect_mavproxy, daemon=True).start()

    def connect_mavproxy(self):
        try:
            mavlink_portt = str(self.mavlink_port.get())
            mavlink_ipp = str(self.mavlink_ip.get())
            self.master = mavutil.mavlink_connection(f"udpin:{mavlink_ipp}:{mavlink_portt}")
            self.master.wait_heartbeat(timeout=10)
            self.master.mav.param_request_list_send(self.master.target_system, self.master.target_component)
            self.root.after(0, self.update_connection_status, "Connected", "green")
        except Exception as e:
            print("Error connecting to MAVLink:", e)
            self.root.after(0, self.update_connection_status, "Disconnected", "red")
            messagebox.showerror("Connection Error", f"Failed to connect to MAVLink: {e}")

    def update_connection_status(self, status, color):
        self.connection_status.set(status)
        self.connection_status_display.config(fg=color)

    def on_select(self, selection):
        print(selection)

    def background_task(self):
        print("Background task started!")
        while True:
            try:
                message = self.master.recv_match(type='GLOBAL_POSITION_INT', blocking=True, timeout=1)
                if message:
                    print("Received message:", message)
                    self.uav.SetDataFromMessage(message)
                    self.tracker.sendtotracker(self.uav)
                else:
                    print("No message received within the timeout period.")
            except Exception as error:
                print("Error in background task:", error)

    def start_background_task(self):
        threading.Thread(target=self.background_task, daemon=True).start()
        print("Background task thread started!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DirectionalAntennaGUI(root)
    root.mainloop()
