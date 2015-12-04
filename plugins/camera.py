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
	self.current_iso = 300

    def setup(self, config):
	self.config = config
	self.current_iso = int(self.get_option('Camera', 'iso', 0))

    def redraw(self, menu):
        menu.write_row(0, 'Select ISO')
	menu.lcd.create_char(0, [0, 4, 14, 0, 0, 14, 4, 0])
	menu.write_row(1, chr(0) + str(self.current_iso))
        menu.write_option(
            row=2,
            text='Current {}' .format(int(self.get_option('Camera', 'iso', 300)))
        )

        """
        If you're not going to use a row, you should clear it!
        menu.clear_row()
	"""
	
