#!/usr/bin/env python
print("""
This advanced example uses the menu framework.
It gives you a basic menu setup with plugins. You should be able to view system info and adjust settings!

Press CTRL+C to exit.
""")

# Include advanced so Python can find the plugins
import sys

import dothat.touch as touch
import dothat.lcd as lcd
import dothat.backlight as backlight
from dot3k.menu import Menu, MenuOption
from plugins.utils import Backlight, Contrast
from plugins.graph import IPAddress, GraphTemp, GraphCPU, GraphNetSpeed
from plugins.clock import Clock
from plugins.wlan import Wlan
from plugins.text import Text
from plugins.camera import takeshot 
from plugins.camera import ISO, Hflip, Vflip
from plugins.camera import Camerasettings

import time

class SpaceInvader(MenuOption):
    """
    A silly example "plug-in" showing an
    animated space invader.
    """

    def __init__(self):
        self.start = self.millis()
        self.invader = [
            [14, 31, 21, 31, 9, 18, 9, 18],
            [14, 31, 21, 31, 18, 9, 18, 9]
        ]
        MenuOption.__init__(self)

    def redraw(self, menu):
        now = self.millis()

        x = int((self.start - now) / 200 % 16)
        menu.lcd.create_char(0, self.invader[int((self.start - now) / 400 % 2)])

        menu.write_row(0, 'Space Invader!')
        menu.write_row(1, (' ' * x) + chr(0))
        menu.clear_row(2)


"""
Using a set of nested lists you can describe
the menu you want to display on dot3k.

Instances of classes derived from MenuOption can
be used as menu items to show information or change settings.

See GraphTemp, GraphCPU, Contrast and Backlight for examples.
"""
my_invader = SpaceInvader()

settings = Camerasettings()

menu = Menu(
    structure={
        'Take Picture': takeshot(settings),
        'Current Time': Clock(backlight),
        'Camera status': {
            'IP': IPAddress()
        },
	'Camera settings': {
	    'ISO': ISO(settings),
	    'Orientation': {
		'Horizontal Flip': Hflip(settings),
		'Vertical Flip': Vflip(settings)}
	},
        'Settings': {
	    'WiFi Setup': Wlan(),
            'Display': {
                'Contrast': Contrast(lcd),
                'Backlight': Backlight(backlight)
            }
        }
    },
    lcd=lcd,
    idle_handler=my_invader,
    idle_timeout=30,
    input_handler=Text())

"""
You can use anything to control dot3k.menu,
but you'll probably want to use dot3k.captouch
"""
touch.bind_defaults(menu)

while 1:
    menu.redraw()
    time.sleep(0.05)
