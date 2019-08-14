#!/bin/usr/env python3

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import time

def red_distance(data, width, height):
	tmp = np.empty((height, width, 3), dtype=np.uint16)
	tmp[:,:,:] = data[:,:,:]
	R = (tmp[:,:,0]-np.full((height, width), 170)); G = (tmp[:,:,1]- np.full((height, width), 20)); B = (tmp[:,:,2] - np.full((height, width), 20))
	length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
	plt.imshow(length_idx, cmap='gray', vmin=0, vmax=442)
	plt.show()
	max_idx = np.argmax(length_idx)
	max_posistion = np.unravel_index(max_idx, (height, width))
	print(max_posistion)

if __name__ == '__main__':
	width = 320
	height = 160
	camera = PiCamera()
	camera.resolution = (width, height)
	camera.rotation = 180
	data = np.empty((height, width, 3), dtype=np.uint8)
	while True:
		camera.capture(data, 'rgb')
		red_distance(data, width, height)
		data = np.empty((height, width, 3), dtype=np.uint8)
		
