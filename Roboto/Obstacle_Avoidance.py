#!/bin/usr/env python3

import dbus
import dbus.mainloop.glib
import sys
import time

proxSensorsVal = [0,0,0,0,0]
left_speed = 0
right_speed = 0

def Set_Speed(left, right):
	global network
	network.SetVariable("thymio-II", "motor.left.target", [left])
	network.SetVariable("thymio-II", "motor.right.target", [right])

def init_thymio():
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SessionBus()
	network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')

def get_error(e):
	print('error: ', e)
	sys.exit(0)

def get_prox(x):
	global proxSensorsVal
	proxSensorsVal = x

def get_left_speed(l):
	global left_speed
	left_speed = l

def get_right_speed(r):
	global right_speed
	right_speed = r

def obstacle_avoid():
	network.GetVariable("thymio-II", "motor.left.speed", reply_handler=get_left_speed, error_handler=get_error)
	network.GetVariable("thymio-II", "motor.right.speed", reply_handler=get_right_speed, error_handler=get_error)
	network.GetVariable("thymio-II", "prox.horizontal", reply_handler=get_prox, error_handler=get_error)
	print(proxSensorsVal)
	print(left_speed, right_speed)
	if proxSensorsVal[1] > 0:
		print(left)
		Set_Speed(0, 0)
		time.sleep(0.5)
		Set_Speed(-20, -20)
		time.sleep(1)
		Set_Speed(50, -50)
		time.sleep(1)
		Set_Speed(left_speed, right_speed)
	elif proxSensorsVal[3] > 0:
		print(right)
		Set_Speed(0, 0)
		time.sleep(0.5)
		Set_Speed(-20, -20)
		time.sleep(1)
		Set_Speed(-50, 50)
		time.sleep(1)
		Set_Speed(left_speed, right_speed)
def get_input_speed():
	print("---------------ROBOTO(he's spanish)--------------")
	while True:
		speed = int(input('Speed: '))
		if speed < -500 or speed > 500:
			print('Invalid Input: Speed must be between -500 and 500')
		else:
			return speed


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
speed = get_input_speed()
Set_Speed(speed, speed)
time.sleep(2)
while True:
#	try:
		obstacle_avoid()
		time.sleep(1)
#	except:
#		print('Program exited ')
#		Set_Speed(0, 0)
#		sys.exit(0)
