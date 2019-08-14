#!/bin/usr/env python3

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import gobject
import sys


def Set_Speed(left, right):
    network.SetVariable("thymio-II", "motor.left.target", [left])
    network.SetVariable("thymio-II", "motor.right.target", [right])

def red_distance(data, width, height, w):
	tmp = np.empty((height, width, 3), dtype=np.uint16)
	tmp[:,:,:] = data[:,:,:]
	R = (tmp[:,:,0]-np.full((height, width), w[0])); G = (tmp[:,:,1]- np.full((height, width), w[1])); B = (tmp[:,:,2] - np.full((height, width), w[2]))
	length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
	max_idx = np.argmax(length_idx)
	max_value = np.amax(length_idx)
	max_posistion = np.unravel_index(max_idx, (height, width))
	print('max_value: ', max_value)
	print('w: ', w)
	print('x: ', x)
	ym = max_posistion[0]
	xm =  max_posistion[1]
	if max_value < threshold:
		error = False
	else:
		error = width/2 - xm
	error_idx = [error, data[ym, xm, 0], data[ym, xm, 1], data[ym, xm, 2]]	
	return error_idx

def get_color(width, height, data):
	b = True
	while b:
		print("Place desired color/object infront of the camera such that it is centrally aligned")
		input('Press enter when ready: ')
		camera.capture(data, 'rgb')
		plt.imshow(data)
		plt.show()
		ans = str(input("Would you like to continue? (Y/N)"))
		if ans == 'Y' or ans == 'y':
			b = False
			return data

def init_thymio():
	proxSensorsVal=[0,0,0,0,0]
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SessionBus()
	network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
	return network

def init_camera(width, height):
	camera = PiCamera()
	camera.resolution = (width, height)
	camera.rotation = 180
	camera.start_preview()
	return camera

def update(x, w):
	global alpha
	wi =[0]*3 
	for i in range(3):
		wi[i] = w[i] + alpha*(x[i]-w[i])/((x[0]-w[0])**2+(x[1]-w[1])**2+(x[2]-w[2])**2)**0.5
	return wi

if __name__ == '__main__':	
	threshold = 390
	width = 640
	height = 320
	camera = init_camera(width, height)
	network = init_thymio()
	const_P = 40/(width/2)
	alpha = 0.5
	x = [0]*3
	w = [0]*3
	a = True
	error_prime = 0
	data = np.empty((height, width, 3), dtype=np.uint8)
	print("---------------ROBOTO(he's spanish)--------------")
	ans1 = int(input('Follow Red Strip - [0]\nFollow Blue Cap - [1]\nSelect New Color - [2]\n'))
	if ans1 == 0:
		w[0] = 220
		w[1] = 25
		w[2] = 35
	elif ans1 == 1:
		w[0] = 25
		w[1] = 60
		w[2] = 165
	elif ans1 == 2:
		datan = get_color(width, height, data)		
		w[0] = datan[height/2, width/2, 0]
		w[1] = datan[height/2, width/2, 1]
		w[2] = datan[height/2, width/2, 2]
	else:
		print('Invalid Input')
		sys.exit()
	while a:
		speed = int(input('Speed: '))
		if speed < -500 or speed > 500:
			print('Invalid Input: Speed must be between -500 and 500')
		else:
			a = False
	while True:
		try:
			data = np.empty((height, width, 3), dtype=np.uint8)
			camera.capture(data, 'rgb')
			error_idx = red_distance(data, width, height, w)
			error = error_idx[0]
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
				x[:3] = error_idx[1:4]
				w = update(x, w)
		except:
			print('\nProgram exited')
			Set_Speed(0, 0)
			sys.exit(0)
