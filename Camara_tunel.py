'''
	Image provider for web streaming for kinect-RPi-Eddie project

	This class is required to provide images to be streamed by the eddie web streamer included in this project

	Requires 3 imges pre loaded in the desingned route in order to not crash

	Based on: https://blog.miguelgrinberg.com/post/video-streaming-with-flask


	Omar Ali 
	@aoesis 
	aonlov@gmail.com
'''
from time import time

#route where are located the images to be streamed 
route = '/home/pi/libfreenect/wrappers/python/static/'
class Camara_tunel(object):
	global route
	def __init__(self):
		self.frames = [open(route + f + '.jpg').read() for f in ['1','2','3']]

	
	def get_frame(self):
		#gets the immages from the directory
		self.frames = [open(route + f + '.jpg').read() for f in ['1','2','3']]
		#returns one after another repeatedly at one frame per second
		return self.frames[int(time()) % 3]
