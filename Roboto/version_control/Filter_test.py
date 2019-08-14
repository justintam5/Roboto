#!/bin/usr/env python3

from picamera import PiCamera
import matplotlib.pyplot as plt
import numpy as np
import dbus
import dbus.mainloop.glib
import sys
import cv2

def red_distance(data, width, height, w):
        tmp = np.empty((height, width, 3), dtype=np.uint16)
        tmp[:,:,:] = data[:,:,:]
        R = (tmp[:,:,2]-np.full((height, width), w[0])); G = (tmp[:,:,1]- np.full((height, width), w[1])); B = (tmp[:,:,0] - np.full((height, width), w[2]))
        length_idx = np.full((height, width), 442) - (R**2 + G**2 + B**2)**0.5
#        cv2.imshow('WebCam :)', length_idx)
        max_idx = np.argmax(length_idx)
        max_value = np.amax(length_idx)
        max_posistion = np.unravel_index(max_idx, (height, width))
        print('centre value (length_idx): ', length_idx[height/2, width/2])
        print('centre value (RGB value): ', data[height/2, width/2])
        print(height/2, width/2)
        b,g,r = cv2.split(data)
        data_rgb = cv2.merge([r,g,b])
        plt.imshow(data_rgb)
        plt.show()

if __name__ == '__main__':
        width = 640
        w = [0]*3
        x = [0]*3
        height = 320
        webcam = cv2.VideoCapture(0)
        w[0] = 220
        w[1] = 25
        w[2] = 35
        #while True:
        #        try:
        ret_val, data = webcam.read()
        data = cv2.flip(data, 0)
        data = cv2.resize(data, (width, height))
        red_distance(data, width, height, w)
#        if cv2.waitKey(1) == ord('q'):
#               break

