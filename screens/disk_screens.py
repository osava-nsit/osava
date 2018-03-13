'''
This file contains the classes, functions and globals used for visualizing
Disk Scheduling algorithms
'''

# Kivy libraries
from kivy.core.window import Window
from kivy.graphics import Color, Line
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy.metrics
# Python libraries
from math import sqrt, radians, atan, tan
# OS Algorithms
from algos import disk_scheduling
# OSAVA Common constants and methods
from common import *

# Global data for Disk Scheduling Algorithms
data_disk = dict()

# Binder functions for Disk Scheduling Algorithms
def disk_on_queue(instance, value):
    if(value == ''):
        if DEBUG_MODE:
            value = '98,183,37,122,14,124,65,67'
        else:
            value = ''
    data_disk['disk_queue'] = str(value)

# Input Screen for Disk Scheduling Algorithms
class DiskInputScreen(Screen):
    strategy_type = NumericProperty(None)
    direction_type = NumericProperty(None)
    form = ObjectProperty(None)
    algo_type = 0

    def update_pos_head(self, *args):
        if not self.pos_head.text.isdigit():
            data_disk['pos_head'] = -1
        else:
            data_disk['pos_head'] = int(self.pos_head.text)

    def update_form(self, *args):
        if (self.num_cylinders.text == ""):
            data_disk['num_cylinders'] = 0
        elif not (self.num_cylinders.text.isdigit()):
            data_disk['num_cylinders'] = 0
        else:
            data_disk['num_cylinders'] = int(self.num_cylinders.text)

        # If input is valid, load form else display error message
        if (data_disk['num_cylinders'] > 0):
            self.load_form()
        elif (self.num_cylinders.text != ""):
            form = self.manager.get_screen('disk_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of cylinders.")
            self.visualize_button.disabled = True

    # Binder function for number of cylinders input
    def bind_num_cylinders(self, *args):
        self.num_cylinders.bind(text=self.update_form)

    # Binder function for current position of head
    def bind_pos_head(self, *args):
        self.pos_head.bind(text=self.update_pos_head)

    # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('disk_form').algo_spinner
        spinner.bind(text=self.show_selected_value)
        spinner.bind(text=self.show_direction)

    def bind_widgets(self, *args):
        self.bind_num_cylinders()
        self.bind_pos_head()
        self.bind_spinner()

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        if text == 'First Come First Served':
            self.strategy_type = 0
            self.algo_type = 0
        elif text == 'Shortest Seek Time First':
            self.strategy_type = 1
            self.algo_type = 1
        elif text == 'SCAN':
            self.strategy_type = 2
            self.algo_type = 2
        elif text == 'C-SCAN':
            self.strategy_type = 3
            self.algo_type = 3
        elif text == 'LOOK':
            self.strategy_type = 4
            self.algo_type = 4
        elif text == 'C-LOOK':
            self.strategy_type = 5
            self.algo_type = 5
        data_disk['algo'] = self.strategy_type
        self.load_form()

    #Set appropriate direction type according to the chosen algorithm
    def show_direction(self, spinner, text, *args):
        if text == 'Inward':
            self.direction_type = 0
        elif text == 'Outward':
            self.direction_type = 1
        data_disk['direction'] = self.direction_type

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('disk_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_disk dictionary
        if 'num_cylinders' not in data_disk:
            data_disk['num_cylinders'] = 0
        if 'pos_head' not in data_disk:
            data_disk['pos_head'] = -1
        if 'algo' not in data_disk:
            data_disk['algo'] = 0
        if 'disk_queue' not in data_disk:
            data_disk['disk_queue'] = ''

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10),0), size_hint_x=0.8)

        # Add labels for input
        label = Label(text='Disk queue:', size_hint_x=0.5)
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)

        # Add input
        inp = TextInput(id='disk_queue'+str(0), text=data_disk['disk_queue'], size_hint_x=0.5)
        inp.bind(text=disk_on_queue)
        box.add_widget(inp)

        parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        parent_box.add_widget(box)
        # For occypying space on right
        parent_box.add_widget(BoxLayout(size_hint_x=0.2))

        grid.add_widget(parent_box)

        if self.algo_type !=0 and self.algo_type != 1:
            # Box for direction spinner 
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', padding=(kivy.metrics.dp(10),0), size_hint_x=0.8)

            label = Label(text='Current direction of movement of read/write head:', size_hint_x=0.5)
            label.bind(size=label.setter('text_size'))
            box.add_widget(label)
            direction_spinner = Spinner(
                text='-',
                size_hint_x=0.5,
                size_hint_y=None,
                height='40dp',
                values=('Inward','Outward'))
            direction_spinner.bind(text=self.show_direction)
            box.add_widget(direction_spinner)

            parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
            parent_box.add_widget(box)
            # For occypying space on right
            parent_box.add_widget(BoxLayout(size_hint_x=0.2))

            grid.add_widget(parent_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_disk_output))
        # form.add_widget(box)

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_to_disk_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'disk_output'


# Output Screen for Disk Scheduling Algorithms
class DiskOutputScreen(Screen):
    # Stores the memory chart generated by algorithm
    secondary_memory_chart = {}

    # For drawing lines and arrow heads
    arrows_widget = Widget()

    # Left margin for output
    margin_left = kivy.metrics.dp(65)

    # Increment in width per unit size
    inc = 0

    arrow_head_num = 0

    def get_description(self, *args):
        if data_disk['algo'] == 0:
            return 'In First Come First Served Scheduling, the i/o requests are processed\nin the order in which they arrive.'
        elif data_disk['algo'] == 1:
            return 'In Shortest Seek Time First Scheduling, the i/o request which will need\nthe minimum seek time is processed first.'
        elif data_disk['algo'] == 2:
            return 'In SCAN scheduling, the r/w head scans back and forth across the\ndisk servicing requests as it reaches each cylinder.'
        elif data_disk['algo'] == 3:
            return 'In C-SCAN scheduling, the r/w head scans back and forth across the disk servicing\nrequests as it reaches each cylinder.\nOn reaching the end, the r/w head immediately returns to\nthe beginning without servicing any request on the return trip.'
        elif data_disk['algo'] == 4:
            return 'In LOOK scheduling, the r/w head scans back and forth across the disk servicing\nrequests as it reaches each cylinder moving only up to last requested cylinder\nin the given direction.'
        elif data_disk['algo'] == 5:
            return 'In C-LOOK Scheduling, the r/w head scans back and forth across the disk servicing\nrequests as it reaches each cylinder moving only up to last requested cylinder in the\ngiven direction. On reaching the end, the r/w head immediately returns to the beginning,\nif need be, without servicing any request on the return trip.'

    # Generate formatted data for input to the algo
    def calculate(self, *args):
        self.arrow_head_num = 0

        formatted_data = {}
        formatted_data['curr_pos'] = int(data_disk['pos_head'])
        formatted_data['total_cylinders']= int(data_disk['num_cylinders'])
        formatted_data['algo'] = data_disk['algo']

        disk_queue = []
        disk_queue_data = data_disk['disk_queue']
        if ',' in disk_queue_data: # Comma separated disk_queue
            disk_queue = disk_queue_data.split(",")
        else: # Space separated disk_queue
            disk_queue = disk_queue_data.split()
        formatted_data['disk_queue'] = disk_queue

        if data_disk['algo'] != 0 and data_disk['algo'] != 1:
            formatted_data['direction'] = data_disk['direction']
        self.secondary_memory_chart = disk_scheduling.disk_scheduling(formatted_data)

        layout = self.manager.get_screen('disk_output').layout
        layout.clear_widgets()
        self.arrows_widget = Widget() 

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        error = self.secondary_memory_chart['error_status']
        if error['error_number'] != -1:
            # Inform the user
            display_error(grid, error['error_message'])
        else:
            # Output the algo description
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
            algo_desc = self.get_description()

            desc_label = Label(text=algo_desc, padding=(kivy.metrics.dp(20),kivy.metrics.dp(20)), width=Window.width, valign='top', halign='center')
            # desc_label.text_size = desc_label.size

            box.add_widget(desc_label)
            grid.add_widget(box)

            # Draw secondary storage chart
            self.draw_storage_chart(grid)
            temp = self.secondary_memory_chart

            # Add box for drawing arrows
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='300dp')
            box.add_widget(self.arrows_widget)
            grid.add_widget(box)
        
            # Add total number of cylinders traversed   
            total_cylinders = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            total_cylinders.add_widget(Label(text='Total number of cylinders traversed: '+ str(temp['total_head_moves'])))
            grid.add_widget(total_cylinders)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_disk_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_storage_chart(self, grid, *args):
        # To add path of head
        path_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        path_label = Label(text='Path of the read/write head: ', valign='top', halign='center')
        path_box.add_widget(path_label)
        grid.add_widget(path_box)

        mem_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        grid.add_widget(mem_box)

        self.inc = Window.width/(int(data_disk['num_cylinders'])*1.15)
        movement_list = self.secondary_memory_chart['memory_state']
        new_heads = list(map(int, movement_list))
        sorted_heads=sorted(new_heads)

        # Inserting cylinder 0 and cylinder (total number of cylinders-1) in sorted_heads to facilitate printing of the path of read/write head 
        if(sorted_heads[0]!=0):
            sorted_heads.insert(0,0)
        if(sorted_heads[len(sorted_heads)-1]!=data_disk['num_cylinders']-1):
            sorted_heads.insert(len(sorted_heads), data_disk['num_cylinders']-1)

        # To start printing the path of read/write head from cylinder 0
        cylinder_label = Label(text=str(0),size_hint_x=None, width=self.margin_left , valign='bottom', halign='right', font_size='12sp')

        cylinder_label.text_size = (None, cylinder_label.height)
        cylinder_label.texture_update()
        cylinder_label.text_size = (max(cylinder_label._label.content_width, self.margin_left), kivy.metrics.dp(30))

        mem_box.add_widget(cylinder_label)

        # To print path of read/ write head
        prev_cylinder = -1
        for i, cylinder in enumerate(sorted_heads[1:]):
            if cylinder == prev_cylinder:
                continue
            # To get right value of index
            i = i + 1
            width = self.inc*(cylinder - sorted_heads[i-1])
            # print "width = {} * ({} - {})".format(self.inc, cylinder, sorted_heads[i-1])
            cylinder_label = Label(text=str(cylinder), size_hint_x=None, width=width, halign='right', font_size='12sp')
            
            # Alternate valign for better visibility
            # if (i%2):
            #     cylinder_label.valign = 'top'
            # else:
            #     cylinder_label.valign = 'bottom'

            cylinder_label.text_size = (None, cylinder_label.height)
            cylinder_label.texture_update()
            cylinder_label.text_size = (max(cylinder_label._label.content_width, width), kivy.metrics.dp(30))

            mem_box.add_widget(cylinder_label)

            prev_cylinder = cylinder

        # Initial height of head
        y1 = kivy.metrics.dp(330)

        for i in range(len(movement_list)-1):
            x1 = self.scale_x(movement_list[i])
            x2 = self.scale_x(movement_list[i+1])
            y2 = y1 - kivy.metrics.dp(30)
            if(data_disk['algo'] == 3):
                if(int(movement_list[i]) == 0 and int(movement_list[i+1]) == data_disk['num_cylinders'] -1) or (int(movement_list[i+1]) == 0 and int(movement_list[i]) == data_disk['num_cylinders']-1):
                    self.add_dashed_arrow(x1,y1,x2,y2)
                    y1 = y2
                    continue
            elif(data_disk['algo'] == 5):
               if(int(movement_list[i]) == sorted_heads[1] and int(movement_list[i+1]) == sorted_heads[-2]) or (int(movement_list[i]) == sorted_heads[-2] and int(movement_list[i+1]) == sorted_heads[1]):
                    self.add_dashed_arrow(x1,y1,x2,y2)
                    y1 = y2
                    continue
            self.add_arrow(x1, y1, x2, y2)
            self.add_arrow_head(x1,y1,x2,y2)
            y1 = y2

    def scale_x(self, x, *args):
        return self.margin_left + int(self.inc*float(x))

    # Drawing the arrow line
    def add_arrow(self, x1, y1, x2, y2, *args):
        with self.arrows_widget.canvas:
            Color(1, 1, 1)
            Line(points=[x1,y1,x2,y2], width=1.5)

    # Drawing the dotted arrow line in circular algorithms
    def add_dashed_arrow(self, x1, y1, x2, y2, *args):
        with self.arrows_widget.canvas:
            Color(1, 1, 1)
            Line(points=[x1,y1,x2,y2], width=1, dash_length=kivy.metrics.dp(10), dash_offset=kivy.metrics.dp(20))

    # Drawing the arrow head        
    def add_arrow_head(self, x1, y1, x2, y2, *args):
        self.arrow_head_num += 1

        # Intialising end coordinates and slope for arrow head
        x3 = 0
        y3 = 0
        x4 = 0
        y4 = 0
        m3 = 0
        m4 = 0

        # Length of the arrow head on each side
        len_head = kivy.metrics.dp(8)

        # Angle of the arrow head from main line on each side
        arrow_angle = 45

        # Slope of the arrow line
        if (x2-x1 == 0):
            m = float("inf")
        else:
            m = (float(y2-y1))/(float(x2-x1))

        if m > 0:
            sign = -1
        else:
            sign = 1

        # For debugging
        # print "x2 = {} m = {}".format(x2,m)

        # Coordinates for right half of the head
        # deg = self.calc_normalised_angle(m)
        # m3 = m * cos(radians(deg))#/120
        m3 = tan(atan(m) + radians(arrow_angle))

        if m >= 1.0:
            sign3 = -1*sign
        else:
            sign3 = sign

        # c,s = Cos and Sine of the slope angle
        c = 1/(sqrt(1 + (m3*m3)))
        s = m3 * c
        x3 = x2 - sign3 * len_head * c
        y3 = y2 - sign3 * len_head * s

        # For debugging
        # print str(self.arrow_head_num) + "----------------------------------"
        # print "m = {}, m3 = {}, c = {}, s = {}".format(m, m3, c, s)

        # Coordinates for left half of the head
        # m4 = m * cos(radians(70))#\70
        m4 = tan(atan(m) - radians(arrow_angle))

        if m <= -1.0:
            sign4 = -1*sign
        else:
            sign4 = sign

        c = 1/(sqrt(1 + (m4*m4)))
        s = m4 * c
        x4 = x2 - sign4 * len_head * c
        y4 = y2 - sign4 * len_head * s

        # For debugging
        # print "m = {}, m4 = {}, c = {}, s = {}".format(m, m4, c, s)
        # print "x2 = {}, y2 = {}, x3 = {}, y3 = {}, x4 = {}, y4 = {}".format(x2, y2, x3, y3, x4, y4)
        # print str(self.arrow_head_num) + "----------------------------------\n\n"

        # Drawing the arrow head on each side
        with self.arrows_widget.canvas:
            # Color(0.110, 0.306, 0.643)
            Color(1,1,1,0.7)
            Line(points=[x2,y2,x3,y3], width=1.6)
            Line(points=[x2,y2,x4,y4], width=1.6)

    def calc_normalised_angle(self, slope, *args):
        return abs(slope*30)
    def switch_to_disk_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'disk_form'
