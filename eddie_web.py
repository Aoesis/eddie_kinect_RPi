'''
	Web streaming code for kinect-RPi-Eddie project

	It requires the instalation of Flask framework
	This code is made tu run on /home/pi/libfreenect/wrappers/python over the RPi
	It requires the creation on that route of 2 directories: Templates, static 

	It requires the Camara_tunel code, included in this project

	Basic algorithm: streaming of 3 images named 1.jpg etc, located at static directory

	To watch the streaming access to RPi IP from a browser specifiying the port
		192.168.137.124:1234

	This code works alone, but the project includes main project code and arduino code 

	Based on: https://blog.miguelgrinberg.com/post/video-streaming-with-flask


	Omar Ali 
	@aoesis 
	aonlov@gmail.com
'''
import cv2
import numpy as np
import os
from flask import Flask, render_template, Response
#Camara_tunel is a class created to provide the frames for streaming, is  included in the project in git
from Camara_tunel import Camara_tunel

#Useless image route
image_route = '/home/pi/libfreenect/wrappers/python/static/image.jpg'

app = Flask(__name__)

#main route 
@app.route('/')
def index():
	#load of the html page to be served
	return render_template('eddie.html')

#
def image_Return(Camara_tunel):
	global image_route
	try:
		while True:
			#returns a yield of images returned from Camara_tunel class, yield is kinda list 
			frame = Camara_tunel.get_frame()
			yield (b'--frame\r\n' 
				  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
	except Exception as e:
		print (e)

#streaming video route, is not direclty used but is needed
@app.route('/video_s')
def video_s():
	return Response(image_Return(Camara_tunel()),
				      mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	#host must be RPi IP, not sure about the port but it worked with thatone 
	app.run(host='192.168.137.124',port = 1234, debug=False)
