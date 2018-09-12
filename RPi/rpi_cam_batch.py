from picamera import PiCamera
from time import sleep
import socket
import os

camera = PiCamera()

photo_id = 0
while 1:
	camera.capture('/home/pi/image'+str(photo_id)+'.jpg')
	print("Saved photo "+str(photo_id))
	photo_id += 1