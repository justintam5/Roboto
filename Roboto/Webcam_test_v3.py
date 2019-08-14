#!/bin/usr/env python3

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
import threading

#Pi camera:
#l_w = np.array([70, 0, 0]) 
#h_w = np.array([150, 255, 255])

#Web camera:
l_w = np.array([0, 0, 0]) 
h_w = np.array([150, 255, 100])
i = 0

def thread_function():
	global webcam, i
	ret_val0 = webcam.grab()
	if i == 2:
		ret_val1 = webcam.grab()
		i = 0
	else:
		i = i + 1	


webcam = cv2.VideoCapture(0)

while True:
	width = 320
	height = 160
	t0 = time.time()
	retval, data = webcam.read()
#	ret_val = webcam.grab()
	t1 = time.time()

	thread = threading.Thread(target=thread_function)
	thread.start()

#	ret_val0, data = webcam.retrieve()
	t2 = time.time()
#	data = cv2.flip(data, 0)
#	data = cv2.flip(data, 1)
	#data = cv2.resize(data, (width, height))
	hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, l_w, h_w)
#	print('center: ', hsv[height/2, width/2])
	#filter = np.full((2, 2), 1)
	#conv = signal.convolve(mask, filter, mode='same')	
	cv2.imshow('mask', mask)
	cv2.imshow('other frame', data)
	#cv2.imshow('conv', conv/12495)
	k = cv2.waitKey(1) & 0xFF 
	if k == ord('q'):
		break
#	time.sleep(1)
#	input('Press Enter: ')
	print('time to read', t1-t0)
	print('time to show', t2-t1)
cap.release()
cv2.destroyAllWindows()
