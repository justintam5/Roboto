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

def red_distance(data, width, height, Rn, Gn, Bn):
	tmp = np.empty((height, width, 3), dtype=np.uint16)
	tmp[:,:,:] = data[:,:,:]
	R = (tmp[:,:,0]-np.full((height, width), Rn)); G = (tmp[:,:,1]- np.full((height, width), Gn)); B = (tmp[:,:,2] - np.full((height, width), Bn))
	length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
#	plt.imshow(length_idx, cmap='gray', vmin=0, vmax=442)
#	plt.show()
	max_idx = np.argmax(length_idx)
	max_value = np.amax(length_idx)
	max_posistion = np.unravel_index(max_idx, (height, width))
	print(max_value)
	if max_value < 400:
		error = False
	else:
		error = width/2 - max_posistion[1]
	return error

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
	#camera.start_preview()
	return camera

if __name__ == '__main__':	
	width = 320
	height = 160
	camera = init_camera(width, height)
	network = init_thymio()
	const_P = 40/(width/2)
	a = True
	error_prime = 0
	data = np.empty((height, width, 3), dtype=np.uint8)
	print("---------------ROBOTO(he's spanish)--------------")
	ans1 = int(input('Follow Red Strip - [0]\nFollow Blue Cap - [1]\nSelect New Color - [2]\n'))
	if ans1 == 0:
		Rn = 190
		Gn = 20
		Bn = 20
	elif ans1 == 1:
		Rn = 20
		Gn = 20
		Bn = 190
	elif ans1 == 2:
		datan = get_color(width, height, data)		
		Rn = datan[height/2, width/2, 0]
		Gn = datan[height/2, width/2, 1]
		Bn = datan[height/2, width/2, 2]
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
			error = red_distance(data, width, height, Rn, Gn, Bn)
			if error == False and error_prime < 0:
				Set_Speed(30, -30)
			elif error == False and error_prime > 0:
				Set_Speed(-30, 30)
			elif error != False:
				left = speed - const_P*error
				right = speed + const_P*error
				Set_Speed(left, right)
				error_prime = error
		except:
			print('\nProgram exited')
			Set_Speed(0, 0)
			sys.exit(0)
