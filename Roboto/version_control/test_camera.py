#!/bin/usr/env python3

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import time
import math
#import cv2

def red_distance(data, width, height, thresh_hold):
	for x in range(width):
		for y in range(height):
			R, G, B = data[y, x]
			length = math.sqrt((R-255)**2+(G)**2+(B)**2)
			if length < thresh_hold:
				data[y, x] = 255, 255, 255
			else:
				data[y, x] = 0, 0, 0
#	print('o_0')
	plt.imshow(data)
	plt.show()
#	max_idx = np.argmax(red_idx)
#	max_posistion = np.unravel_index(max_idx, (height, width))
#	print(max_posistion)
	#return distance

if __name__ == '__main__':
	width = 96
	height = 64
	thresh_hold = 120 #threshold
	camera = PiCamera()
	camera.resolution = (width, height)
	camera.rotation = 180
	data = np.empty((height, width, 3), dtype=np.uint8)
	#time.sleep(10)
	while True:
		camera.capture(data, 'rgb')
		camera.capture('Figure2.jpg')
		red_distance(data, width, height, thresh_hold)
		#plt.imshow(data)
		data = np.empty((height, width, 3), dtype=np.uint8)
		#plt.show()
#		input('Press enter to save another photo')
		
