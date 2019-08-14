#!/bin/usr/env python3

#Adds a probabilistic controller, removing the need for any convolution. This is simply done by summing the 2D array along the 
#vertical axis, this gives some 1D distribution, then setting the desired point (referenced to as error in the code) as the mean value.

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import sys
import cv2
from scipy import signal

def Set_Speed(left, right):
	network.SetVariable("thymio-II", "motor.left.target", [left])
	network.SetVariable("thymio-II", "motor.right.target", [right])

def get_posistion(width, height, lw, hw):
	global th
	ret_val, data = webcam.read()
	data = cv2.resize(data, (width, height))
	hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lw, hw)
	maskx = mask/255
	mean = maskx.mean()
	sum = maskx.sum()
	print('Sum: ', sum)
	maskx = (maskx.sum(axis=0))/sum
	maskx = maskx*x
	mean_pos = (maskx.sum())

	cv2.imshow('HELLO TRAVLLER!!!!', data)
	cv2.imshow('HELLO AGAIN!!!!!!!!', mask)

	print('mean: ', mean)
	print('mean location: ', mean_pos)
	if mean < th:
		error = False
	else:
		error = width/2 - mean_pos
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
	width = 100
	height = 100
	webcam = cv2.VideoCapture(0)	
	network = init_thymio()
	const_P = 40/(width/2)
	alpha = 0.005
	lw = np.array([0, 160, 68])
	hw = np.array([8, 255, 255])
	error_prime = 0
	th = 25/(width*height)
	
	x = np.arange(width)
	
	speed = get_input()

	while True:
		try:
			error = get_posistion(width, height, lw, hw)
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
			k = cv2.waitKey(60) & 0xFF
			if k == 27:
				break

		except:
			print('\nProgram exited')
			Set_Speed(0, 0)
			sys.exit(0)
