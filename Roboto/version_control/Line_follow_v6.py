#!/bin/usr/env python3

#follows a black line
#After applying a binary mask to the camera output, the 2D array is then summed along the vertical axis, producing a 1D array repersenting a distribution of 
#true pixels (pixels repersenting the line to follow). The posistion of the mean is used to indicate error
#PD controller is then used to specify a command 

import numpy as np
import dbus
import dbus.mainloop.glib
import sys
import cv2
import threading
import time

#constants
width = 320
height = 160
idx = 0 #camera index (2 is generally Pi camera)
const_P = 70/(width/2)
const_D = 35/(width/2)
c = 0

path = '/media/pi/UUI/DATA'
data_file = open('{}/data_file.csv'.format(path), 'w')

def thread_function():
	global webcam, c
	ret_val0 = webcam.grab()
	ret_val1 = webcam.grab()
	ret_val2 = webcam.grab()

#def thread_function

def Set_Speed(left, right):
	network.SetVariable("thymio-II", "motor.left.target", [left])
	network.SetVariable("thymio-II", "motor.right.target", [right])

def get_posistion(width, height, lw, hw):
	global th, n
	ret_val, data = webcam.read()
	thread = threading.Thread(target=thread_function)
	thread.start()

	data = cv2.resize(data, (width, height))
	data = cv2.flip(data, 0)
	data = cv2.flip(data, 1)
	cv2.imwrite('{}/image_{}.png'.format(path, n), data)

	hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lw, hw)
##
	maskx = mask/255
	mean = maskx.mean()
	sum = maskx.sum()
	#print('Sum: ', sum)
	maskx = (maskx.sum(axis=0))/sum
	maskx = maskx*x
	mean_pos = (maskx.sum())
##
	cv2.imshow('HELLO TRAVLLER!!!!', data)
	cv2.imshow('HELLO AGAIN!!!!!!!!', mask)

	#print('mean: ', mean)
	#print('mean location: ', mean_pos)
	print(data.shape)
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

def calc_derror(error):
	global i, derror
	if i != 0:
		derror = error - i
	if i == 0:
		i = error
	return derror

if __name__ == '__main__':	
	#initailize
	webcam = cv2.VideoCapture(idx)	
	network = init_thymio()
	i = 0
	lw = np.array([70, 0, 0])
	hw = np.array([150, 255, 255])
	derror = 0
	error_prime = 0
	th = 25/(width*height)
	n = 0
	total_time = 0
	x = np.arange(width)
	
	speed = get_input()
	ti = time.time()
	while True:
		try:
			t0 = time.time()
			error = get_posistion(width, height, lw, hw)
			tf = time.time()
			data_file.write('{}, {}, image_{}.png\n'.format(str(error), tf-ti, n))
			if error == False and error_prime < 0:
				Set_Speed(30, -30)
			elif error == False and error_prime > 0:
				Set_Speed(-30, 30)
			elif error != False:
				derror = calc_derror(error)
				left = speed - const_P*error 
				right = speed + const_P*error
				Set_Speed(left, right)
				error_prime = error
			k = cv2.waitKey(60) & 0xFF
			if k == 27:
				break
			t1 = time.time()
			delta_t = t1-t0
			print('Time per Frame:', delta_t)
			total_time += delta_t
			n += 1
		except:
			fps = n/total_time 
			print('\nProgram exited')
			print('AVG FPS: ', fps)
			Set_Speed(0, 0)
			sys.exit(0)
			cap.release()
			cv2.destroyAllWindows()
			data_file.close()

