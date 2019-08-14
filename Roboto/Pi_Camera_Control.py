#!/bin/usr/env python3

import time
from picamera import PiCamera
import numpy as np

if __name__ == '__main__':
	camera = PiCamera()
	camera.rotation = 180
	time.sleep(1)
	camera.start_preview()
	input('enter')
