#!/bin/usr/env python3

import numpy as np
import cv2
import time
import matplotlib.pyplot as plt



def click(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(x, y)
		print(hsv[y, x])

i = 2

webcam = cv2.VideoCapture(i)
ret_val, data = webcam.read()
width = 320
height = 160
data = cv2.resize(data, (width, height))
hsv = cv2.cvtColor(data, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)


cv2.namedWindow('image')
cv2.setMouseCallback("image", click)

while True:
	cv2.imshow('image', data)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('c'):
		break
	


