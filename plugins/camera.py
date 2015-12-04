#!/usr/bin/env python
"""
Every dot3k.menu plugin is derived from MenuOption
"""
from dot3k.menu import MenuOption
import picamera
from time import sleep
from fractions import Fraction

class takeshot(MenuOption):

    def __init__(self):
        MenuOption.__init__(self)
	self.mode = 0
        self.current_iso = 0     

    def setup(self, config):
        self.config = config
	self.current_iso = int(self.get_option('Camera', 'iso', 0))

    def takephoto(self):
	self.mode = 1
    	with picamera.PiCamera() as camera:
		camera.resoluion = (1024, 768)
		camera.hflip = True
		camera.vflip = True
		#camera.framerate = Fraction(1, 6)
		camera.expodure_mode = 'off'
		camera.iso = int(self.current_iso)
		sleep(10)
		camera.capture('/home/pi/test.jpg')
    	print("DONE!")
	self.mode = 2

    def redraw(self, menu):
	if self.mode == 0:
		menu.write_row(0, 'Confirm')
                menu.write_row(1, 'ISO:' + str(self.current_iso))
                menu.clear_row(2)
	elif self.mode == 1:
		menu.write_row(0, 'Snap Snap')
        	menu.clear_row(1)
        	menu.clear_row(2)
        elif self.mode == 2:
		menu.write_row(0, 'DONE')
                menu.clear_row(1)
                menu.clear_row(2)

        """
        If you're not going to use a row, you should clear it!
        menu.clear_row
        """
    def left(self):
	self.mode = 0
	return False

    def select(self):
	if self.mode == 0:
        	self.takephoto()
	else: 
		self.left()

§
class ISO(MenuOption):
    """
    When the menu is redrawn, it calls your plugins
    redraw method and passes an instance of itself.
    """
    def __init__(self):
	MenuOption.__init__(self)
	self.current_iso = 0
	self.display_iso = 0

    def setup(self, config):
	self.config = config
	self.current_iso = int(self.get_option('Camera', 'iso', 0))
	self.display_iso = self.current_iso

    def increase_iso(self):
	if self.display_iso == 800:
	    print('maxxed ISO')
	else:
	    self.display_iso = self.display_iso + 100
	return self.display_iso

    def decrease_iso(self):
	if self.display_iso == 100:
	    print('minum ISO')
	else:
	    self.display_iso = self.display_iso - 100
	return self.display_iso

    def set_iso(self):
	self.set_option('Camera', 'iso', str(self.display_iso))
	#update current
	self.current_iso = int(self.get_option('Camera', 'iso', 0))	

    def redraw(self, menu):
        menu.write_row(0, 'Select ISO')
	menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])
	menu.write_row(1, chr(0) + str(self.display_iso))
        menu.write_option(
            row=2,
            text='Current {}' .format(int(self.current_iso))
        )

        """
        If you're not going to use a row, you should clear it!
        menu.clear_row 
	"""

    def up(self):
	self.display_iso = self.increase_iso()
	
    def down(self):
	self.display_iso = self.decrease_iso()

    def select(self):
	self.set_iso()
