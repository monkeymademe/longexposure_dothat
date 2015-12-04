#!/usr/bin/env python
"""
Every dot3k.menu plugin is derived from MenuOption
"""
from dot3k.menu import MenuOption
import picamera
from time import sleep
from fractions import Fraction

class Camerasettings():
    def __init__(self):
	self.iso = 0
	self.hflip = False
	self.vflip = False
	

class takeshot(MenuOption):

    def __init__(self, settings):
        MenuOption.__init__(self)
	self.settings=settings
	self.mode = 0
	self.current_iso = 0
	self.current_hflip = False
	self.current_vflip = False

    def setup(self, config):
        self.config = config
	#i = ISO()

    def begin(self):
	self.current_iso = self.settings.iso
	self.current_hflip = self.settings.hflip
	self.current_vflip = self.settings.vflip

    def takephoto(self):
	self.mode = 1
    	with picamera.PiCamera() as camera:
		camera.resoluion = (1024, 768)
		camera.hflip = self.current_hflip
		camera.vflip = self.current_vflip
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
	if self.mode == 0:
		return False
	else:
		return True

    def select(self):
	if self.mode == 0:
        	self.takephoto()
	else: 
		self.mode = 0
		return True


class ISO(MenuOption):
    """
    When the menu is redrawn, it calls your plugins
    redraw method and passes an instance of itself.
    """
    def __init__(self, setting):
	MenuOption.__init__(self)
	self.iso=setting
	self.iso.iso = 0
	self.display_iso = 0
	self.current_iso = 0

    def setup(self, config):
	self.config = config
	self.current_iso = int(self.get_option('Camera', 'iso', 0))
	self.display_iso = self.current_iso
	self.iso.iso = self.current_iso

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
	self.iso.iso = self.current_iso

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

class Hflip(MenuOption):

    def __init__(self, setting):
        MenuOption.__init__(self)
        self.flip = setting 
        self.hflip = False
        self.display_flip = False
        self.current_flip = False

    def setup(self, config):
        self.config = config
        self.current_flip = str(self.get_option('Camera', 'hflip', False))
        self.display_flip = self.current_flip
        self.flip.hflip = self.current_flip

    def set_flip(self):
        self.set_option('Camera', 'hflip', str(self.display_flip))
        #update current
        self.current_flip = str(self.get_option('Camera', 'hflip', False))
        self.flip.hflip = self.current_flip

    def redraw(self, menu):
        menu.write_row(0, 'Set horizontal flip')
        menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])
        menu.write_row(1, chr(0) + str(self.display_flip))
        menu.write_option(
            row=2,
            text='Current {}' .format(str(self.current_flip))
        )

        """
        If you're not going to use a row, you should clear it!
        menu.clear_row
        """

    def up(self):
        self.display_flip = True

    def down(self):
        self.display_flip = False

    def select(self):
        self.set_flip()

class Vflip(MenuOption):

    def __init__(self, setting):
        MenuOption.__init__(self)
        self.flip = setting
        self.vflip = False
	self.display_flip = False
	self.current_flip = False

    def setup(self, config):
        self.config = config
        self.current_flip = str(self.get_option('Camera', 'vflip', False))
        self.display_flip = self.current_flip
        self.flip.vflip = self.current_flip

    def set_flip(self):
        self.set_option('Camera', 'vflip', str(self.display_flip))
        #update current
        self.current_flip = str(self.get_option('Camera', 'vflip', False))
        self.flip.vflip = self.current_flip

    def redraw(self, menu):
        menu.write_row(0, 'Set vertical flip')
        menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])
        menu.write_row(1, chr(0) + str(self.display_flip))
        menu.write_option(
            row=2,
            text='Current {}' .format(str(self.current_flip))
        )

        """
        If you're not going to use a row, you should clear it!
        menu.clear_row
        """

    def up(self):
        self.display_flip = True

    def down(self):
        self.display_flip = False

    def select(self):
        self.set_flip()
