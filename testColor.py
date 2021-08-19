import numpy as np
import cv2
import time
import sys
import os

# Capturing video through webcam

webcam = cv2.VideoCapture(0)

# Initialize frame rate calculation

frame_rate_calc = 1
freq = cv2.getTickFrequency()
count = 0
flag = 0

def leetexto(idioma, voz, tono, velocidad, texto):
	print('lectura de texto, idioma: "' + idioma + '", voz: ' + voz + ";")
	scommand='espeak -v' + idioma + '+' + voz + ' -p'+tono+' -s'+velocidad +' "' + texto + '"'
	print("$ " + scommand)
	os.system(scommand)

# Start a while loop
while(1):
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
            count = count + 1
            if(count > 2 and flag == 0):
                print("COLOR ROJO DETECTADO")
                leetexto('es','f5','60','130', 'Cuidado, luz roja')
                flag =1
                count =0

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
            count = count + 1
            if(count > 2 and flag ==1):
                print("COLOR VERDE DETECTADO")
                leetexto('es','f5','60','130', 'Luz verde, puede cruzar')
                flag =0
                count =0

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

    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break