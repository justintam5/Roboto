#!/bin/usr/env python3

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

l_w = np.array([0, 90, 90]) 
h_w = np.array([10, 160, 160])

webcam = cv2.VideoCapture(0)
while True:
	width = 320
	height = 160
	ret_val, data = webcam.read()
	data = cv2.flip(data, 0)
	data = cv2.flip(data, 1)
	data = cv2.resize(data, (width, height))
	hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, l_w, h_w)
	cv2.imshow('mask', mask)
	cv2.imshow('other frame', data)
	print(data[height/2, width/2])
	print(mask[height/2, width/2])
	if cv2.waitKey(1) == ord('q'):
		break
	time.sleep(1)
	input('Press Enter: ')
cap.release()
cv2.destroyAllWindows()
