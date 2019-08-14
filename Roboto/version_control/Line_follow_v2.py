
#!/bin/usr/env python3

#follows a black line
#After applying a binary mask to the camera output, the 2D array is then summed along the vertical axis, producing a 1D array repersenting a distribution of 
#true pixels (pixels repersenting the line to follow). The posistion of the mean is used to indicate error, as well as the total magnitude (non-normaloized), 
#since a vertical line (following is straight) will have the highest magnitude(narrow distribution), and a horizontal line will have the lowest(spread distribution)

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import sys
import cv2
from scipy import signal

def Set_Speed(left, right):
	network.SetVariable("thymio-II", "motor.left.target", [left])
	network.SetVariable("thymio-II", "motor.right.target", [right])



if __name__ == '__main__':

try:
	camera = PiCamera()
	width = 100
	height = 100
	webcam = cv2.VideoCapture(0)
	network = init_thymio()
	const_P = 40/(width/2)
	k = cv2.waitKey(60) & 0xFF
	if k == 27:
		break


except:
	print('\nProgram exited')
	Set_Speed(0, 0)
	sys.exit(0)


