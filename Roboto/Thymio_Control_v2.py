#!/bin/usr/env python

import dbus
import dbus.mainloop.glib
import gobject
from optparse import OptionParser
import time

proxSensorsVal=[0,0,0,0,0]


def Set_Speed(left, right):
    network.SetVariable("thymio-II", "motor.left.target", [left])
    network.SetVariable("thymio-II", "motor.right.target", [right])

def Motor_Control():
    while True:
        a = True
        b = True
        print('---------------THYMIO--------------')
        while a:
            speed = int(input('Speed: '))
            if speed < -500 or speed > 500:
                print('Invalid Input: Speed must be between -500 and 500')
            else:
                a = False
        while b:
            ans = str(input('Control - [w/a/s/d] - [set speed]: '))
            if ans == 'w':
                Set_Speed(speed, speed)
            elif ans == 's':
                Set_Speed(-speed, -speed)
            elif ans == 'a':
                Set_Speed(-speed, speed)
            elif ans == 'd':
                Set_Speed(speed, -speed)
            elif ans == 'set speed':
                b = False
            else:
                print('Invalid Input')
            time.sleep(1)
            Set_Speed(0, 0)
    return True

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
    (options, args) = parser.parse_args()

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    if options.system:
        bus = dbus.SystemBus()
    else:
        bus = dbus.SessionBus()

    #Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')

    Motor_Control()


