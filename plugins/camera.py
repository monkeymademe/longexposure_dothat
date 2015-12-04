#!/usr/bin/env python
"""
Every dot3k.menu plugin is derived from MenuOption
"""
from dot3k.menu import MenuOption



class HelloWorld(MenuOption):
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
