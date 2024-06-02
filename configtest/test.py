import configparser
config = configparser.ConfigParser()
config['Mavlink/Mavproxy'] = {'Mavlink_IP': '127.0.0.1',
                     'Mavlink_port': '14551'}
config['Antenna tracker data'] = {'Home_latitude' : '58.310397',
                                  'Home_longitude' : '26.692669',
                                  'Set_location_from_drone' : False,
                                  'Antenna_height' : '0',
                                  'Initial_true_course' : -1}
config['Arduino'] = {'Arduino_port' : 'COM15'}
with open('config.ini', 'w') as configfile:
  config.write(configfile)
