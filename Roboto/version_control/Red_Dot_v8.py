#!/bin/usr/env python3

#Using HSV color base, the filter no longer outputs a value inversely proportional to the euclidian distance from the desired color, but instead applys a binary mask 
#according to a set bandwidth. The result is then convoluted with a 2x2 matrix of 1's, elminating small amounts of noise (using an additional threshold) and adding 
#a bias towards high density pixels that make it past the mask. Note that the camera used and calibrated for in this script (and all future scripts) is the 
#Microsft LifeCam VX-2000
#FPS: ~ 2

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import sys
import cv2
from scipy import signal

th = 766

def Set_Speed(left, right):
    network.SetVariable("thymio-II", "motor.left.target", [left])
    network.SetVariable("thymio-II", "motor.right.target", [right])

def get_posistion(width, height, lw, hw, filter):
	global th
	ret_val, data = webcam.read()
	data = cv2.resize(data, (width, height))
	hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lw, hw)
	conv = signal.convolve(mask, filter, mode='same')
	max_idx = np.argmax(conv)
	max_value = np.amax(conv)
	max_posistion = np.unravel_index(max_idx, (height, width))
	cv2.imshow('HELLO TRAVLLER!!!!', data)
	cv2.imshow('HELLO AGAIN!!!!!!!!', mask)
	print(max_posistion)
	print(max_value)
	if max_value < th:
		error = False
	else:
		error = width/2 - max_posistion[1]
	return error

def init_thymio():
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SessionBus()
	network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	return network

def get_input():
        a = True
        print("---------------ROBOTO(he's spanish)--------------")
        while a:
                speed = int(input('Speed: '))
                if speed < -500 or speed > 500:
                        print('Invalid Input: Speed must be between -500 and 500')
                else:
                        a = False
        return speed

if __name__ == '__main__':	
	#initailize
	camera = PiCamera()
	filter = np.full((2, 2), 1)
	width = 100
	height = 100
	webcam = cv2.VideoCapture(0)	
	network = init_thymio()
	const_P = 40/(width/2)
	alpha = 0.005
	x = [0]*3
	lw = np.array([0, 160, 68])
	hw = np.array([8, 255, 255])

	error_prime = 0
	
	speed = get_input()

	while True:
#		try:
			error = get_posistion(width, height, lw, hw, filter)
			if error == False and error_prime < 0:
				camera.led = False
				Set_Speed(30, -30)
			elif error == False and error_prime > 0:
				camera.led = False
				Set_Speed(-30, 30)
			elif error != False:
				camera.led = True
				left = speed - const_P*error
				right = speed + const_P*error
				Set_Speed(left, right)
				error_prime = error
#				w = update(x, w)
			k = cv2.waitKey(60) & 0xFF
			if k == 27:
				break

#		except:
#			print('\nProgram exited')
#			Set_Speed(0, 0)
#			sys.exit(0)
