#!/usr/bin/env python
import freenect
import cv2
import frame_convert2
import numpy as np
import serial
import time
import RPi.GPIO as GPIO
import os

#rutas para las imagenes
image_route1 = '/home/pi/libfreenect/wrappers/python/static/1.jpg'
image_route2 = '/home/pi/libfreenect/wrappers/python/static/2.jpg'
image_route3 = '/home/pi/libfreenect/wrappers/python/static/3.jpg'

#Configuracion de los puertos de salida
GPIO.setmode(GPIO.BCM)
A = 18
B = 23
C = 24
D = 25
GPIO.setup(A, GPIO.OUT)
GPIO.setup(B, GPIO.OUT)
GPIO.setup(C, GPIO.OUT)
GPIO.setup(D, GPIO.OUT)

#Variables de control de detección 
promedioDetectablePermitido = 180
presicion = 0.7  #smaler will recognize bigger objects
banderaDetener = 0

#creacion de las ventanas
cv2.namedWindow('Depth')
cv2.namedWindow('RGB')
keep_running = True

#Funcion de lectura del sensor de profundidad
def display_depth(dev, data, timestamp):
    global keep_running
    global banderaDetener
    global presicion
    global promedioDetectable
    #se obtiene lectura
    imagen_depth= frame_convert2.pretty_depth_cv(data)

    go_Eddie()

    #se procesa la imagen y se obtiene información
    imagen_depth_editable = imagen_depth
    imagen_depth_editable = imagen_depth_editable [0:480, 49:589]
    imagen_depth_editable = np.array(imagen_depth_editable).flatten()
    promedio = np.mean(imagen_depth_editable)
    print('{0:15}: {1:.3f}'.format('promedio',promedio))
    porcentaje_de_bloqueo = promedio / 255
    print('{0:15}: {1:.3f}'.format('% de bloqueo',porcentaje_de_bloqueo))

    #interpretación de la informacion obtenida
    if porcentaje_de_bloqueo < presicion :
    	banderaDetener = 1

    if banderaDetener == 1:
 	detener_Eddie()
 	girar_Eddie_derecha()
	if promedio > promedioDetectablePermitido:
		detener_Eddie()
 		banderaDetener = 0

    if banderaDetener == 0:
	go_Eddie()

    #la imagen es mostrada en el escritorio de la RPi
    cv2.imshow('Depth', imagen_depth)

    if cv2.waitKey(10) == 27:
	print('stop key pressed')
	detener_Eddie()
        keep_running = False


def display_rgb(dev, data, timestamp):
    global keep_running
    #obtencion de imagen RGB
    image = frame_convert2.video_cv(data)
    cv2.imshow('RGB',image)
    #escritura de imagenes
    cv2.imwrite(image_route1, image)
    cv2.imwrite(image_route2, image)
    cv2.imwrite(image_route3, image)
    if cv2.waitKey(10) == 27:
        print('stop key pressed')
	detener_Eddie()
        keep_running = False
    time.sleep(0.1)

def body(*args):
    if not keep_running:
	print('stop key pressed')
        detener_Eddie()
        raise freenect.Kill

#rutinas de movimiento del eddie
def go_Eddie():
	print('go eddie')
	GPIO.output(A, GPIO.HIGH)
        GPIO.output(B, GPIO.LOW)
        GPIO.output(C, GPIO.LOW)
        GPIO.output(D, GPIO.LOW)
	time.sleep(0.1)

def detener_Eddie():
	print('stop eddie')
	GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.HIGH)
        GPIO.output(C, GPIO.LOW)
        GPIO.output(D, GPIO.LOW)
        time.sleep(0.1)

def girar_Eddie_derecha():
	print ('turn  eddie')
	GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)
        GPIO.output(C, GPIO.HIGH)
        GPIO.output(D, GPIO.LOW)
	time.sleep(0.1)

def girar_Eddie_izquierda():
	print('turn eddie')
	GPIO.output(A, GPIO.LOW)
        GPIO.output(B, GPIO.LOW)
        GPIO.output(C, GPIO.LOW)
        GPIO.output(D, GPIO.HIGH)
	time.sleep(0.1)

print('Press ESC in window to stop')
freenect.runloop(depth=display_depth,
                 video=display_rgb,
                 body=body)
