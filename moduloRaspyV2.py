import cv2
import time
import sys
import os
import io
import pynmea2
import serial
import telepot          #Para utilizar el bot de Telegram

import numpy as np
import RPi.GPIO as GPIO

from geopy.geocoders import Nominatim
from telepot.loop import MessageLoop

# Capturing video through webcam
webcam = cv2.VideoCapture(0)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
# sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
# geolocator = Nominatim(user_agent="geoapiExercises")
# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()
countR = 0
countG = 0
flagR = 0
flagG = 0

counter = 0
counter2 = 0
check = 0

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

def leetexto(idioma, voz, tono, velocidad, texto):
	print('lectura de texto, idioma: "' + idioma + '", voz: ' + voz + ";")
	scommand='espeak -v' + idioma + '+' + voz + ' -p'+tono+' -s'+velocidad +' "' + texto + '"'
	print("$ " + scommand)
	os.system(scommand)
print("Listo para operar.")
leetexto('es','f5','60','130', 'Dispositivo listo para operar')
# Start a while loop
while(1):
    buttonState = GPIO.input(7)

    if(buttonState == True and check == 0):
        counter = counter + 1

    if(counter > 20000):
        print("Presion prolongada.")
        leetexto('es','f5','60','130', 'Calculando su ubicacion, espere un momento')
        counter = 0
        check =1
        ser = serial.Serial('/dev/ttyS0', 9600, timeout=5.0)
        sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
        geolocator = Nominatim(user_agent="geoapiExercises")
        time.sleep(1)
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
            msgStreet = "Estas en la calle " + addressLocation[0]
            print(msgStreet)
            leetexto('es','f5','60','130', msgStreet)
            time.sleep(1)
    
    buttonState2 = GPIO.input(7)

    if(buttonState2 == False and check == 1):
        check =0

    
    if(buttonState2 == False and counter > 300):
        counter2 = counter2 + 1
        print("Presion corta.")
        counter = 0
        check =1
        if (counter2 % 2 == 0):
            print("Esta Apagado.")
            leetexto('es','f5','60','130', 'Camara Apagada')
            webcam.release()
            cv2.destroyAllWindows()
            webcam = cv2.VideoCapture(0)
            frame_rate_calc = 1
            freq = cv2.getTickFrequency()
        else:
            print("Esta Encendido.")
            leetexto('es','f5','60','130', 'Camara Encendida, espere informacion')
            while(1):
                buttonState3 = GPIO.input(7)
                t1 = cv2.getTickCount()
                # Reading the video from the
                # webcam in image frames
                _, imageFrame = webcam.read()
            
                # Convert the imageFrame in 
                # BGR(RGB color space) to 
                # HSV(hue-saturation-value)
                # color space
                hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)
            
                # Set range for red color and 
                # define mask
                red_lower = np.array([136, 87, 111], np.uint8)
                red_upper = np.array([180, 255, 255], np.uint8)
                red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
            
                # Set range for green color and 
                # define mask
                green_lower = np.array([50, 90, 90], np.uint8)
                green_upper = np.array([100, 255, 255], np.uint8)
                green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
            

                
                # Morphological Transform, Dilation
                # for each color and bitwise_and operator
                # between imageFrame and mask determines
                # to detect only that particular color
                kernal = np.ones((5, 5), "uint8")
                
                # For red color
                red_mask = cv2.dilate(red_mask, kernal)
                res_red = cv2.bitwise_and(imageFrame, imageFrame, 
                                        mask = red_mask)
                
                # For green color
                green_mask = cv2.dilate(green_mask, kernal)
                res_green = cv2.bitwise_and(imageFrame, imageFrame,
                                            mask = green_mask)
                
            
                # Creating contour to track red color
                contours, hierarchy = cv2.findContours(red_mask,
                                                    cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)[-2:]
                
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        countR = countR + 1
                        if(countR > 2 and flagR == 0):
                            print("COLOR ROJO DETECTADO")
                            leetexto('es','f5','60','130', 'Cuidado, luz roja')
                            flagR =1
                            flagG = 0
                            countR =0
                        
                        imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                                (x + w, y + h), 
                                                (0, 0, 255), 2)
                        
                        cv2.putText(imageFrame, "Red Colour", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                                    (0, 0, 255))  

            
                # Creating contour to track green color
                contours, hierarchy = cv2.findContours(green_mask,
                                                    cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)[-2:]
                
                for pic, contour in enumerate(contours):
                    area = cv2.contourArea(contour)
                    if(area > 300):
                        x, y, w, h = cv2.boundingRect(contour)
                        countG = countG + 1
                        if(countG > 2 and flagG ==0):
                            print("COLOR VERDE DETECTADO")
                            leetexto('es','f5','60','130', 'Luz verde, puede cruzar')
                            flagR = 0 
                            flagG = 1
                            countG =0

                        imageFrame = cv2.rectangle(imageFrame, (x, y), 
                                                (x + w, y + h),
                                                (0, 255, 0), 2)
                        
                        cv2.putText(imageFrame, "Green Colour", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 
                                    1.0, (0, 255, 0))

                
                # Draw framerate in corner of frame
                cv2.putText(imageFrame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
                
                # Program Termination
                cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
                
                # Calculate framerate
                t2 = cv2.getTickCount()
                time1 = (t2-t1)/freq
                frame_rate_calc= 1/time1
                buttonState4 = GPIO.input(7)
                if buttonState4 != buttonState3:
                    webcam.release()
                    cv2.destroyAllWindows()
                    leetexto('es','f5','60','130', 'Presione nuevamente para apagar')
                    break

    # print("llegue al final.")
    
    
    # if cv2.waitKey(10) & 0xFF == ord('q'):
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     break
