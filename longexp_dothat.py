#!/usr/bin/env python
print("""
This example shows the Display-o-Tron HAT touch inputs in action.
Touch an input and you should see the LCD change accordingly.

Press CTRL+C to exit.
""")

import dothat.touch as j
import dothat.lcd as l
import dothat.backlight as b
import signal

"""
Captouch provides the @captouch.on() decorator
to make it super easy to attach handlers to each button.

It's also a drop-in replacement for joystick, with one exception: 
it has a "cancel" method.

The handler will receive "channel" ( corresponding to a particular
button ID ) and "event" ( corresponding to press/release ) arguments.
"""

import picamera
from time import sleep
from fractions import Fraction

filenum = 1
shutter = 500000

@j.on(j.UP)
def handle_up(ch, evt):
    settings = (int(filenum), int(shutter))
    temp = settings[0]
    temp += 1 
    print('filenum is {}'.format(int(temp)) )
    l.clear()
    b.rgb(0, 255, 0)
    l.write('filenum is {}'.format(int(temp)))
    global filenum
    filenum = int(temp)

@j.on(j.DOWN)
def handle_down(ch, evt):
    settings = (int(filenum), int(shutter))
    temp = settings[0]
    if int(temp) == 1:
    	print("Can't do more")
        l.clear()
        b.rgb(255, 0, 0)
        l.write("Can't go lower")
    else:
	temp -= 1
        print('filenum is {}'.format(int(temp)))
        l.clear()
        b.rgb(0, 255, 0)
        l.write('filenum is {}'.format(int(temp)))
	global filenum
	filenum = int(temp)

@j.on(j.LEFT)
def handle_left(ch, evt):
    settings = (int(filenum), int(shutter))
    temp = settings[1]
    if int(temp) == 500000:
        print("Can't do more")
        l.clear()
        b.rgb(255, 0, 0)
        l.write("Can't go lower")
    else:
        temp = int(temp) - 500000
        print('shutter is {}'.format(int(temp)))
        l.clear()
        b.rgb(0, 0, 255)
        l.write('shutter is {}'.format(int(temp)))
	global shutter
	shutter = int(temp)


@j.on(j.RIGHT)
def handle_right(ch, evt):
    settings = (int(filenum), int(shutter))
    temp = settings[1]
    if int(temp) == 6000000:
        print("Can't do more")
        l.clear()
        b.rgb(255, 0, 0)
        l.write("Can't go higher")
    else:
        temp = int(temp) + 500000
        print('shutter is {}'.format(int(temp)))
        l.clear()
        b.rgb(0, 0, 255)
        l.write('shutter is {}'.format(int(temp)))
	global shutter
        shutter = int(temp)

@j.on(j.BUTTON)
def handle_button(ch, evt):
    print("Confirm settings!")
    l.clear()
    b.rgb(255, 255, 255)
    settings = (int(filenum), int(shutter))
    l.write('filename = %s and shutter = %s' % settings)


@j.on(j.CANCEL)
def handle_cancel(ch, evt):
    takelongphoto()

def takelongphoto():
    print("Takeing Photo")
    l.clear()
    b.rgb(255, 255, 255)
    l.write("Taking Photo Don't Move")
    settings = (int(filenum), int(shutter))
    with picamera.PiCamera() as camera:
	camera.resoluion = (1024, 768)
	camera.hflip = True
	camera.vflip = True
	camera.framerate = Fraction(1, 6)
	camera.shutter_speed = settings[1]
	camera.expodure_mode = 'off'
	camera.iso = 100
	sleep(10)
	camera.capture('/home/pi/photo/longexp_{}.jpg'.format(int(settings[0])))
    print("DONE!")
    l.clear()
    b.rgb(0, 255, 255)
    l.write("We are done")

# Prevent the script exiting!
signal.pause()
