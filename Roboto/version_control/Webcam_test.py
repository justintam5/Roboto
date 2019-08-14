#!/bin/usr/env python3

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

th = 420
w = [117, 50, 45]


def red_distance(data, width, height, w):
	tmp = np.empty((height, width, 3), dtype=np.uint16)
	tmp[:,:,:] = data[:,:,:]
	R = (tmp[:,:,2]-np.full((height, width), w[0])); G = (tmp[:,:,1]- np.full((height, width), w[1])); B = (tmp[:,:,0] - np.full((height, width), w[2]))
	length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
	print(length_idx[height/2, width/2])
	sum = [0]*3
	n = 0
	for i in range(0, width):
		for j in range(0, height):
			if length_idx[j, i] < th:
				length_idx[j, i] = 0
			elif length_idx[j, i] > th:
				n = n + 1
				sum = (sum + data[j, i])
				length_idx[j, i] = 1
	print(sum/n)
	data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB) 
	red = np.empty((height, width, 3), dtype=np.uint8)
	red[:,:,2] = 33; red[:,:,1] = 33; red[:,:,0] = 93
	#plt.imshow(red)
	plt.imshow(length_idx, cmap='gray', vmin=0, vmax=1)
	plt.show()

webcam = cv2.VideoCapture(1)
while True:
	width = 320
	height = 160
	ret_val, data = webcam.read()
	data = cv2.flip(data, 0)
	data = cv2.resize(data, (width, height))
	red_distance(data, width, height, w)
cap.release()
cv2.destroyAllWindows()
