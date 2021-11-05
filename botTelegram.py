import time, datetime   #Para el tiempo
import RPi.GPIO as GPIO #Para los puertos
import telepot          #Para utilizar el bot de Telegram
import io

import serial   #Para el gps
import time     #Para el gps
import string   #Para el gps
import pynmea2  #Para el gps

from telepot.loop import MessageLoop

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def action(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    gpsURL = "NO INFO"
    print ('Received: %s' % command)
    if 'hola' in command:
        message = "Saludos!, escribe gps para conocer ubicacion"
        telegram_bot.sendMessage (chat_id, message)
    elif 'gracias' in command:
        message = "de nada!"
        telegram_bot.sendMessage (chat_id, message)
    elif 'gps' in command:
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        dataout = pynmea2.NMEAStreamReader()
        line = sio.readline()
        if line[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(line)
            lat=newmsg.latitude
            lng=newmsg.longitude
            gpsURL = "https://maps.google.com/maps?q=" + str(lat) + "+" + str(lng)
            print(gpsURL)
            message = "Ubicacion actual: " + gpsURL 
            telegram_bot.sendMessage (chat_id, message)
    else:
        message = gpsURL + ": Comando erroneo o gps desconectado"
        telegram_bot.sendMessage (chat_id, message)



telegram_bot = telepot.Bot('2080678572:AAHsu8B4SlKQRE2VRJgVagfg_qe8KAP0GG0') # Aqui poner el token del bot.
print (telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running....')

while 1:
    time.sleep(10)
