#!/bin/usr/env python3

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import gobject

def Set_Speed(left, right):
    network.SetVariable("thymio-II", "motor.left.target", [left])
    network.SetVariable("thymio-II", "motor.right.target", [right])

def red_distance(data, width, height):
	tmp = np.empty((height, width, 3), dtype=np.uint16)
	tmp[:,:,:] = data[:,:,:]
	R = (tmp[:,:,0]-np.full((height, width), 170)); G = (tmp[:,:,1]- np.full((height, width), 20)); B = (tmp[:,:,2] - np.full((height, width), 20))
	length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
#	plt.imshow(length_idx, cmap='gray', vmin=0, vmax=442)
#	plt.show()
	max_idx = np.argmax(length_idx)
	max_posistion = np.unravel_index(max_idx, (height, width))
	error = width/2 - max_posistion[1]
	return error

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

if __name__ == '__main__':	
	width = 320
	height = 160
	camera = init_camera(width, height)
	network = init_thymio()
	const_P = 25/(width/2)
	a = True
	data = np.empty((height, width, 3), dtype=np.uint8)
	print('---------------THYMIO--------------')
	while a:
		speed = int(input('Speed: '))
		if speed < -500 or speed > 500:
			print('Invalid Input: Speed must be between -500 and 500')
		else:
			a = False
	while True:
		camera.capture(data, 'rgb')
		error = red_distance(data, width, height)
		left = speed - const_P*error
		right = speed + const_P*error
		Set_Speed(left, right)
		data = np.empty((height, width, 3), dtype=np.uint8)
		
