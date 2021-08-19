import io
import pynmea2
import serial
import time

from geopy.geocoders import Nominatim

ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

geolocator = Nominatim(user_agent="geoapiExercises")

while 1:
    try:
        line = sio.readline()
        # msg = pynmea2.parse(line)
        if line[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(line)
            lat=newmsg.latitude
            lng=newmsg.longitude
            gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
            print(gps)
            location = geolocator.reverse(str(lat)+", "+ str(lng))
            addressLocation = location.address.split(',')
            print("Estas en la calle " + addressLocation[0])
            print(newmsg)
            time.sleep(2)

    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break

    except pynmea2.ParseError as e:

        print('Parse error: {}'.format(e))
        continue