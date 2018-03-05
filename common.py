'''
This file contains common constants and methods used by all modules
'''

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# Global flag for debug mode
DEBUG_MODE = False

# Global fixed height of form rows within scroll view
form_row_height = '30dp'

# Checks if a form input is a valid number
def is_valid_value(value):
    if isinstance(value, int):
        return True
    elif isinstance(value, str) or isinstance(value, unicode):
        return value != '' and value.isdigit()
    else:
        return False

# For labels with colored border
class WhiteBorderedLabel(Label):
    pass

class ColoredBorderedLabel(Label):
    pass

class ColoredButton(Button):
    pass

# Global function for bad input handling
def display_error(grid, error, box_height='400dp'):
    error_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=box_height)
    error_label = Label(text="Bad Input:\n" + error, size_hint_x=None, width=Window.width, valign='top', halign='center')
    # error_label.text_size = error_label.size
    error_box.add_widget(error_label)
    grid.add_widget(error_box)
    return error_box
