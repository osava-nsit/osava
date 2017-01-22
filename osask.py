# Kivy libraries
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.graphics import Color, Rectangle, Line
from decimal import Decimal
import kivy.metrics
# Python libraries
from functools import partial
from random import random
from copy import deepcopy
from math import sqrt, radians, atan, tan
# OS Algorithms
import cpu_scheduling, deadlock, memory_allocation, page_replacement, disk_scheduling

Builder.load_file('layout.kv')

# Global flag for debug mode
DEBUG_MODE = False

# Global fixed height of form rows within scroll view
form_row_height = '30dp'

# Global data for CPU Scheduling Algorithms
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive', 'Multilevel Queue', 'Multilevel Feedback Queue']
cpu_scheduling_type = 0
data_cpu = dict()

# Global data for Deadlock Avoidance Algorithm
data_da = dict()

# Global data for Deadlock Detection Algorithm
data_dd = dict()

# Global data for Contiguous Memory Allocation Strategies
data_mem = dict()

# Global data for Page Replacement Algorithms
data_page = dict()

# Global data for Disk Scheduling Algorithms
data_disk = dict()

# Binder functions for CPU Scheduling Algorithms form, to store data in the global 'data_cpu' dictionary
def cpu_on_name(instance, value, i):
    if value == '':
        value = 'P'+str(i+1)
    data_cpu['name'+str(i)] = value
def cpu_on_arrival(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 1
        else:
            value = -1
    data_cpu['arrival'+str(i)] = value
def cpu_on_burst(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    data_cpu['burst'+str(i)] = value
def cpu_on_priority(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 10
        else:
            value = -1
    data_cpu['priority'+str(i)] = value
def cpu_on_quantum(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    data_cpu['quantum'] = int(value)
def cpu_on_aging(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 4
        else:
            value = 1000000000000000
    data_cpu['aging'] = int(value)
def cpu_on_num_queues(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    data_cpu['num_queues'] = int(value)
def cpu_on_queue_quantum(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    data_cpu['queue_quantum'][i] = int(value)
def cpu_on_queue_assigned(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 1
        else:
            value = -1
    data_cpu['queue_assigned'][i] = int(value)

# Binder functions for Deadlock Avoidance Algorithm form
def da_on_available(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 5
        else:
            value = -1
    data_da['available'][i] = int(value)
def da_on_request(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 0
        else:
            value = -1
    data_da['request'][i] = int(value)
def da_on_max(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 8
        else:
            value = -1
    data_da['max'][i][j] = int(value)
def da_on_allocation(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    data_da['allocation'][i][j] = int(value)
def da_request_on_process_id(instance, value):
    if (value == ''):
        if DEBUG_MODE:
            value = 1
        else:
            value = -1
    data_da['request_process'] = int(value)-1

# Binder functions for Deadlock Detection Algorithm form
def dd_on_available(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 5
        else:
            value = -1
    data_dd['available'][i] = int(value)
def dd_on_request(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    data_dd['request'][i][j] = int(value)
def dd_on_allocation(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    data_dd['allocation'][i][j] = int(value)

# Binder functions for Contiguous Memory Allocation Strategies form
def mem_on_size(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 128
        else:
            value = -1
    data_mem['size'][i] = value
def mem_on_arrival(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 0
        else:
            value = -1
    data_mem['arrival'][i] = value
def mem_on_termination(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 10
        else:
            value = -1
    data_mem['burst'][i] = value

# Binder functions for Page Replacement Algorithm form
def page_on_ref(instance, value):
    if(value == ''):
        if DEBUG_MODE:
            value = '7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1' 
        else:
            value = ''
    data_page['ref_str'] = str(value)
def page_on_modify(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = '0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1'
        else:
            value = ''
    data_page['modify_bit'] = str(value)

# Binder functions for Disk Scheduling Algorithms
def disk_on_queue(instance, value):
    if(value == ''):
        if DEBUG_MODE:
            value = '98,183,37,122,14,124,65,67'
        else:
            value = ''
    data_disk['disk_queue'] = str(value)

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
    error_label.text_size = error_label.size
    error_box.add_widget(error_label)
    grid.add_widget(error_box)
    return error_box

# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):
    about_visible = False
    def toggle_about_text(self, *args):
        if self.about_visible:
            self.about_label.text = ""
            self.about_visible = False
        else:
            self.about_label.text = 'Developers: Udit Arora, Namrata Mukhija, Priyanka, Rohit Takhar\nAdvisor: Dr. Pinaki Chakraborty'
            self.about_visible = True

# Input Screen for CPU Scheduling Algorithms with partial scrolling
class CPUInputScreen(Screen):
    layout = ObjectProperty(None)
    layout_form = ObjectProperty(None)
    queue_type = NumericProperty(None)
    cpu_type = 0
    preemptive_flag = False

    multilevel_input_widgets = []

    # Update dispatch_latency and set to default value if empty
    def update_dispatch_latency(self, *args):
        if not self.dispatch_latency.text.isdigit():
            data_cpu['dispatch_latency'] = -1
        else:
            data_cpu['dispatch_latency'] = int(self.dispatch_latency.text)

    # Called when the number of processes input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        if (self.num_processes.text == ""):
            data_cpu['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_cpu['num_processes'] = 0
        else:
            data_cpu['num_processes'] = int(self.num_processes.text)

        # If input is valid, load form else display error message
        if (data_cpu['num_processes'] > 0):
            self.load_form()
        elif (self.num_processes.text != ""):
            self.layout_form.clear_widgets()
            display_error(self.layout_form, "Invalid number of processes.")
            self.visualize_button.disabled = True

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for dispatch latency input
    def bind_dispatch_latency(self, *args):
        self.dispatch_latency.bind(text=self.update_dispatch_latency)

    # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinners(self, *args):
        self.algo_spinner.bind(text=self.show_selected_value)
        self.variant_spinner.bind(text=self.show_variant)

    # Wrapper function that calls binder functions for the required widgets
    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_dispatch_latency()
        self.bind_spinners()

    # Call set_cpu_type method with appropriate index of scheduling algorithm
    def show_selected_value(self, spinner, text, *arg):
        if text == 'First Come First Serve':
            self.set_cpu_type(0)
            self.variant_spinner.disabled = True
        elif text == 'Shortest Job First':
            self.set_cpu_type(2)
            self.variant_spinner.disabled = False
        elif text == 'Priority':
            self.set_cpu_type(4)
            self.variant_spinner.disabled = False
        elif text == 'Round Robin':
            self.set_cpu_type(1)
            self.variant_spinner.disabled = True
        elif text == 'Multilevel Queue':
            self.set_cpu_type(7)
            self.variant_spinner.disabled = True
        elif text == 'Multilevel Feedback Queue':
            self.set_cpu_type(8)
            self.variant_spinner.disabled = True

    def show_variant(self, spinner, text, *args):
        if text == 'Preemptive':
            self.preemptive_flag = True
            self.update_cpu_type(True)
        elif text == 'Non-Preemptive':
            self.preemptive_flag = False
            self.update_cpu_type(False)

    # Called when a new value is chosen from spinner. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
    def set_cpu_type(self, new_cpu_type, *args):
        global cpu_scheduling_type
        cpu_scheduling_type = new_cpu_type
        self.cpu_type = new_cpu_type
        # If FCFS or RR
        if new_cpu_type == 0 or new_cpu_type == 1 or new_cpu_type == 7 or new_cpu_type == 8:
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
        elif self.preemptive_flag == True and new_cpu_type%2 == 0:
            new_cpu_type += 1
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
        elif self.preemptive_flag == False and new_cpu_type%2 != 0:
            new_cpu_type -= 1
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
        if ('num_processes' in data_cpu and data_cpu['num_processes'] > 0):
            self.load_form()

    # Called when preemptive or non-preemtive option is clicked. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
    def update_cpu_type(self, *args):
        global cpu_scheduling_type
        # If FCFS or RR Scheduling
        if self.cpu_type == 0 or self.cpu_type == 1 or self.cpu_type == 7 or self.cpu_type == 8:
            pass
        elif self.preemptive_flag == True and self.cpu_type%2 == 0:
            self.cpu_type += 1
            cpu_scheduling_type = self.cpu_type
        elif self.preemptive_flag == False and self.cpu_type%2 != 0:
            self.cpu_type -= 1
            cpu_scheduling_type = self.cpu_type

    # Load the appropriate form inputs according to the CPU Scheduling algorithm selected
    def load_form(self, *args):
        # Layout is the area where the form is placed on the screen
        layout_form = self.manager.get_screen('cpu_form').layout_form
        layout_form.clear_widgets()

        # Enable visualize button - load_form will only be called when form load input is correct
        self.visualize_button.disabled = False

        # If algo selected is one of multilevel, update output screen reference in visualize_button
        if self.cpu_type == 7 or self.cpu_type == 8:
            self.visualize_button.on_release = self.switch_to_cpu_output_multilevel
        else:
            self.visualize_button.on_release = self.switch_to_cpu_output

        # Update dispatch_latency and set to default value if empty
        if (self.dispatch_latency.text == ""):
            data_cpu['dispatch_latency'] = 0
        else:
            data_cpu['dispatch_latency'] = int(self.dispatch_latency.text)

        layout = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        layout.bind(minimum_height=layout.setter('height'))

        # Add input labels
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        # label = Label(text='Sno.')
        # box.add_widget(label)
        label = Label(text='Process name')
        box.add_widget(label)
        label = Label(text='Arrival time (ms)')
        box.add_widget(label)
        label = Label(text='CPU burst time (ms)')
        box.add_widget(label)

        # If Priority scheduling selected
        if self.cpu_type == 4 or self.cpu_type == 5:
            label = Label(text='Priority (0 being highest)')
            box.add_widget(label)

        layout.add_widget(box)

        for i in range(int(self.num_processes.text)):
            box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)

            # sno_label = Label(text=str(i+1))
            # box.add_widget(sno_label)

            # Inputted process names
            # inp = TextInput(id='name'+str(i))
            # inp.bind(text=partial(cpu_on_name, i=i))
            # box.add_widget(inp)

            # Fixed process names
            pname = Label(text='P'+str(i+1))
            box.add_widget(pname)
            data_cpu['name'+str(i)] = 'P'+str(i+1)

            # arrival times
            inp = TextInput(id='arrival'+str(i))
            inp.bind(text=partial(cpu_on_arrival, i=i))
            box.add_widget(inp)
            # burst times
            inp = TextInput(id='burst'+str(i))
            inp.bind(text=partial(cpu_on_burst, i=i))
            box.add_widget(inp)

            # If Priority scheduling selected
            if self.cpu_type == 4 or self.cpu_type == 5:
                inp = TextInput(id='priority'+str(i))
                inp.bind(text=partial(cpu_on_priority, i=i))
                box.add_widget(inp)

            layout.add_widget(box)

        # If Round Robin scheduling selected
        if self.cpu_type == 1:
            box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)
            inp = TextInput(id='quantum')
            inp.bind(text=cpu_on_quantum)
            # inp.font_size = inp.size[1]
            label = Label(text='Time quantum (ms)')
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)
        # If Priority scheduling selected
        elif self.cpu_type == 4 or self.cpu_type == 5:
            box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)
            inp = TextInput(id='aging', size_hint_x=0.5)
            inp.bind(text=cpu_on_aging)
            # inp.font_size = inp.size[1]
            label = Label(text='Aging - Promote priority after (ms):', size_hint_x=0.5, halign='center', padding=(kivy.metrics.dp(10),0))
            label.bind(size=label.setter('text_size'))
            box.add_widget(label)
            box.add_widget(inp)

            layout.add_widget(box)
        # If Multilevel Queue scheduling is selected
        elif self.cpu_type == 7 or self.cpu_type == 8:
            self.visualize_button.disabled = True

            layout.add_widget(BoxLayout(size_hint_y=None, height='10dp'))

            box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(10),0), size_hint_y=None, height=form_row_height, size_hint_x=0.67)
            label = Label(text='Number of queues:', valign='middle', size_hint_x=0.513)
            # label.bind(size=label.setter('text_size'))
            inp = TextInput(id='num_queues', size_hint_x=0.487)

            box.add_widget(label)
            box.add_widget(inp)

            parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            parent_box.add_widget(box)
            # For occupying space on right side
            parent_box.add_widget(BoxLayout(size_hint_x=0.33))

            layout.add_widget(parent_box)

            inp.bind(text=partial(self.update_multilevel_form, layout, inp))

        # Uncomment to insert buttons at end of scroll view
        # if self.cpu_type != 7 and self.cpu_type != 8:
        #     # Add Visualize and back button at the end of form
        #     button_box = BoxLayout(orientation='horizontal', padding=(0, kivy.metrics.dp(5)), size_hint_y=None, height='50dp')
        #     button_box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        #     button_box.add_widget(Button(text='Visualize', on_release=self.switch_to_cpu_output))
        #     layout.add_widget(button_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(layout)
        layout_form.add_widget(sv)

    # Clear the multilevel scheduling sub-form
    def remove_multilevel_widgets(self, grid_layout, *args):
        for widget in self.multilevel_input_widgets:
            grid_layout.remove_widget(widget)
        self.multilevel_input_widgets = []

    # Sets the algo of a queue in multilevel queue scheduling
    def set_queue_type(self, spinner, text, inp, idx, *args):
        if text == 'FCFS':
            data_cpu['queue_algo'][idx] = 0
            inp.disabled = True
            inp.text = ''
        elif text == 'Round Robin':
            data_cpu['queue_algo'][idx] = 1
            inp.disabled = False

    # Called when the number of queues input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_multilevel_form(self, layout, num_queues_input, *args):
        if not num_queues_input.text.isdigit():
            data_cpu['num_queues'] = 0
        else:
            data_cpu['num_queues'] = int(num_queues_input.text)

        if (data_cpu['num_queues'] > 0):
            self.load_multilevel_form(layout, num_queues_input)
        elif (num_queues_input.text != ""):
            self.remove_multilevel_widgets(layout)
            error_box = display_error(layout, "Invalid number of queues.", box_height='100dp')
            self.multilevel_input_widgets.append(error_box)
            self.visualize_button.disabled = True

    def load_multilevel_form(self, grid_layout, num_queues_input, *args):
        # Remove previous multilevel form widgets
        self.remove_multilevel_widgets(grid_layout)

        self.visualize_button.disabled = False

        if self.cpu_type == 7:
            # Iniatilize queue algo data_cpu dictionary lists
            data_cpu['queue_algo'] = [0] * data_cpu['num_queues']
            data_cpu['queue_quantum'] = [2] * data_cpu['num_queues']
            data_cpu['queue_assigned'] = [1] * data_cpu['num_processes']

            # Adding descriptive features
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Information about intra queue scheduling algorithms:')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Queue number')
            box.add_widget(label)
            label = Label(text='Algorithm chosen')
            box.add_widget(label)
            label = Label(text='Time quantum (ms)')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            # Adding input rows for intra queue scheduling algorithm for each queue 
            for i in range(data_cpu['num_queues']):
                box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)
                qnum = Label(text='Q'+str(i+1))
                box.add_widget(qnum)

                data_cpu['qnum'+str(i)] = 'Q'+str(i+1)
             
                queue_spinner = Spinner(
                    text='-',
                    values=('FCFS','Round Robin'),
                    padding=(kivy.metrics.dp(50), 0))
                box.add_widget(queue_spinner)

                inp = TextInput(id='queue_quantum'+str(i), disabled=True)
                inp.bind(text=partial(cpu_on_queue_quantum, i=i))
                box.add_widget(inp)

                queue_spinner.bind(text=partial(self.set_queue_type, inp=inp, idx=i))

                grid_layout.add_widget(box)
                self.multilevel_input_widgets.append(box)

            # Descriptive features for assigning a queue to every process
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Queue assigned:')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Process name')
            box.add_widget(label)
            label = Label(text='Queue assigned')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            # Adding input rows to assign a queue to each process
            for i in range(data_cpu['num_processes']):
                box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)
                qnum = Label(text='P'+str(i+1))
                box.add_widget(qnum)
                inp = TextInput(id='queue_assigned'+str(i))
                inp.bind(text=partial(cpu_on_queue_assigned, i=i))
                box.add_widget(inp)
                grid_layout.add_widget(box)
                self.multilevel_input_widgets.append(box)
        elif self.cpu_type == 8:
            # Iniatilize queue algo data_cpu dictionary lists
            data_cpu['queue_quantum'] = [0] * (data_cpu['num_queues']-1)

            # Descriptive features for assigning a queue to every process
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Queue assigned:')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            label = Label(text='Queue number')
            box.add_widget(label)
            label = Label(text='Time quantum (ms)')
            box.add_widget(label)
            grid_layout.add_widget(box)
            self.multilevel_input_widgets.append(box)

            for i in range(data_cpu['num_queues']-1):
                box = BoxLayout(orientation='horizontal', padding=(kivy.metrics.dp(25),0), size_hint_y=None, height=form_row_height)
                qnum = Label(text='Q'+str(i+1))
                box.add_widget(qnum)
                data_cpu['qnum'+str(i)] = 'Q'+str(i+1)

                inp = TextInput(id='queue_quantum'+str(i))
                inp.bind(text=partial(cpu_on_queue_quantum, i=i))
                box.add_widget(inp)

                grid_layout.add_widget(box)
                self.multilevel_input_widgets.append(box)
             
        # Uncomment to insert buttons at end of scroll view
        # # Add Visualize and back button at the end of form
        # button_box = BoxLayout(orientation='horizontal', padding=(0, kivy.metrics.dp(5)), size_hint_y=None, height='50dp')
        # button_box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # button_box.add_widget(Button(text='Visualize', on_release=self.switch_to_cpu_output))
        # grid_layout.add_widget(button_box)
        # self.multilevel_input_widgets.append(button_box)
        
    def switch_to_cpu_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'cpu_output'

    def switch_to_cpu_output_multilevel(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'cpu_output_multilevel'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

# Output Screen for CPU Scheduling algorithms
class CPUOutputScreen(Screen):
    layout = ObjectProperty(None)
    gantt = ObjectProperty(None)
    time = ObjectProperty(None)
    # Stores the colours assigned to each process indexed by name
    colors = {}
    # Stores the colours assigned to each queue indexed by name
    colors_queue = {}
    # Stores the process schedule generated by scheduling algorithm
    cpu_schedule = {}
    # Stores the stats related to schedule like average waiting time
    stats = {}
    # Stores the individual per process stats
    details = {}
    # Stores information related to bad input data
    error_status = {}

    def get_description(self, *args):
        if cpu_scheduling_type == 0:
            return 'In First Come First Served Scheduling, the processor is allocated to the process which has arrived first.\nIt is a non-preemptive algorithm.'
        elif cpu_scheduling_type == 1:
            return 'In Round Robin Scheduling, the processor is allocated to a process for a small time quantum.\nThe processes are logically arranged in a circular queue.\nIt is a preemptive algorithm.'
        elif cpu_scheduling_type == 2:
            return 'In Non-Preemptive Shortest Job First Scheduling, the processor is allocated to the process which has the shortest next CPU burst.'
        elif cpu_scheduling_type == 3:
            return 'In  Preemptive Shortest Job First Scheduling, the processor is allocated to the process which has the shortest next CPU burst.\nIt is also known as shortest remaining time first scheduling.'
        elif cpu_scheduling_type == 4:
            return 'In Non-Preemptive Priority Scheduling, the processor is allocated to the process which has the highest priority.'
        elif cpu_scheduling_type == 5:
            return 'In Preemptive Priority Scheduling, the processor is allocated to the process which has the highest priority.'
        elif cpu_scheduling_type == 7:
            return 'In Multilevel Queue Scheduling, the ready queue is partitioned into several queues.\nA process is permanently assigned to a queue.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is often used for inter-queue scheduling.'
        elif cpu_scheduling_type == 8:
            return 'In Multilevel Feedback Queue Scheduling, the ready queue is partitioned into several queues.\nThe processes can move between the queues.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is typically used for inter-queue scheduling.'

    # Prints the details of the process schedule and statistics
    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('cpu_output').layout
        layout.clear_widgets()
        self.gantt.clear_widgets()
        self.time.clear_widgets()

        formatted_data = []
        for i in range(data_cpu['num_processes']):
            process = {}
            process['name'] = data_cpu['name'+str(i)]
            process['arrival'] = int(data_cpu['arrival'+str(i)])
            process['burst'] = int(data_cpu['burst'+str(i)])
            if cpu_scheduling_type == 4 or cpu_scheduling_type == 5:
                process['priority'] = int(data_cpu['priority'+str(i)])
            elif cpu_scheduling_type == 7:
                process['queue_assigned'] = data_cpu['queue_assigned'][i]
            formatted_data.append(process)
            self.colors[process['name']] = [random(), random(), random()]
        self.colors['Idle'] = [0.2, 0.2, 0.2]
        self.colors['DL'] = [0.2, 0.2, 0.2]
        if cpu_scheduling_type == 7 or cpu_scheduling_type == 8:
            for i in range(data_cpu['num_queues']):
                self.colors_queue[i+1] = [random(), random(), random()]
                self.colors_queue[0] = [0.2, 0.2, 0.2]
        
        if cpu_scheduling_type == 0:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.fcfs(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 1:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.round_robin(formatted_data, data_cpu['quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 2:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.shortest_job_non_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 3:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.shortest_job_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 4:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.priority_non_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 5:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.priority_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 7:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.multilevel(formatted_data, data_cpu['num_queues'], data_cpu['queue_algo'], data_cpu['queue_quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 8:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.multilevel_feedback(formatted_data, data_cpu['num_queues'], data_cpu['queue_quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        
        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll
        grid.bind(minimum_height=grid.setter('height'))

        if self.error_status['error_number'] != -1:
            # Inform the user
            # display_error(self.gantt, self.error_status['error_message'])
            pass
        else:
            row_height = '30dp'

            # Display process schedule details
            for process in self.cpu_schedule:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height='20dp')

                if (process['name'] == 'DL'):
                    label_name = Label(text='[ref=click]'+'Dispatch Latency'+':[/ref]', markup=True)
                else:
                    label_name = Label(text='[ref=click]'+process['name']+':[/ref]', markup=True)
                box.add_widget(label_name)
                label = Label(text=str(process['start']))
                box.add_widget(label)
                label = Label(text=str(process['end']))
                box.add_widget(label)
            
                # Add view details button for each process
                details_button = ColoredButton(text='Details', size_hint_x=None, width='100dp')
                box.add_widget(details_button)

                # Blank label for padding on right
                box.add_widget(Label(text='', size_hint_x=None, width='20dp'))

                # Popup showing details of process when box is clicked
                if process['name'] != 'Idle' and process['name'] != 'DL':
                    if cpu_scheduling_type != 8:
                        content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time']))
                    else:
                        if process['next_queue'] == 0:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+"\n"+
                            "Process "+process['name']+" is completed.")
                        else:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+"\n"+
                            process['name']+" moved to queue Q"+str(process['next_queue']+1)+".") 
                    content_label = Label(text=content_str)
                    popup = Popup(title='Details of '+str(process['name']), content=content_label, size_hint=(None, None), size=(kivy.metrics.dp(200), kivy.metrics.dp(200)))
                    label_name.bind(on_ref_press=popup.open)
                    details_button.bind(on_release=popup.open)
                    popup.open()
                    popup.dismiss()
                    # print "Bound popup for process: "+str(label_name.text)
                else:
                    details_button.disabled = True

                grid.add_widget(box)

            # Display statistics
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average turnaround time: ' + str(int((self.stats['turn_time']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average waiting time: ' + str(int((self.stats['wait_time']*100)+0.5)/100.0)))
            grid.add_widget(box)
            
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average response time: ' + str(int((self.stats['resp_time']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Throughput: ' + str(int((self.stats['throughput']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='CPU Utilization: ' + str(int((self.stats['cpu_utilization']*100)+0.5)/100.0) + '%'))
            grid.add_widget(box)

            self.draw_gantt()

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_gantt(self, *args):
        
        # Area for drawing gantt chart
        gantt = self.gantt
        chart_wid = Widget()

        # Area for displaying time values
        time = self.time

        # Area for displaying description.
        desc = self.desc

        gantt.clear_widgets()
        time.clear_widgets()
        desc.clear_widgets()

        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        # box.add_widget(Label(text='Visualization results' ))
        # desc.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp')
        algo_desc = self.get_description()
        desc_label = Label(text=algo_desc, width=Window.width, valign='top', halign='center')
        desc_label.text_size = desc_label.size
        box.add_widget(desc_label)
        desc.add_widget(box)

        # Error checking 
        if self.error_status['error_number'] != -1:
            display_error(self.gantt, self.error_status['error_message'], box_height='120dp')
            return

        # gantt.canvas.clear()
        margin_left = kivy.metrics.dp(125)
        margin_bottom = kivy.metrics.dp(50)

        with chart_wid.canvas:
            # Starting position of rectangle
            pos_x = gantt.pos[0]+margin_left
            # Increment in width per unit time
            # inc = gantt.size[0]/(self.stats['sum_time']*2)
            inc = gantt.size[0]/(self.cpu_schedule[-1]['end']*1.5)

            # Add description labels
            label = Label(text='Gantt Chart: ', size_hint_x=None, width=margin_left, valign='top')
            gantt.add_widget(label)
            t_label = Label(text='Time: ', size_hint_x=None, width=margin_left, valign='top', halign='center')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

            # Draw the gantt chart rectangles and add time labels
            for process in self.cpu_schedule:
                if process['end'] > process['start']:
                    label = Label(text=process['name'], size_hint_x=None, width=inc*(process['end']-process['start']))
                    gantt.add_widget(label)

                    t_label = Label(text=str(process['start']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='top')
                    t_label.text_size = t_label.size
                    time.add_widget(t_label)

                    Color(self.colors[process['name']][0], self.colors[process['name']][1], self.colors[process['name']][2], 0.4, mode='rgba')
                    Rectangle(pos=(pos_x, gantt.pos[1]+margin_bottom), size=(inc*(process['end']-process['start']), gantt.size[1]/2))
                    pos_x += (inc*(process['end']-process['start']))
                else: # Odd behaviour due to dispatch_latency
                    pass

            # Add time label for the end time of last process
            process = self.cpu_schedule[-1]
            t_label = Label(text=str(process['end']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='top')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

        # Add the widget used to draw the gantt chart on the screen
        gantt.add_widget(chart_wid)
                        
# Output screen for Multilevel CPU Scheduling algorithms
class CPUOutputScreenMultilevel(Screen):
    layout = ObjectProperty(None)
    gantt = ObjectProperty(None)
    time = ObjectProperty(None)
    # Stores the colours assigned to each process indexed by name
    colors = {}
    # Stores the colours assigned to each queue indexed by name
    colors_queue = {}
    # Stores the process schedule generated by scheduling algorithm
    cpu_schedule = {}
    # Stores the stats related to schedule like average waiting time
    stats = {}
    # Stores the individual per process stats
    details = {}
    # Stores information related to bad input data
    error_status = {}

    def get_description(self, *args):
        if cpu_scheduling_type == 0:
            return 'In First Come First Served Scheduling, the processor is allocated to the process which has arrived first.\nIt is a non-preemptive algorithm.'
        elif cpu_scheduling_type == 1:
            return 'In Round Robin Scheduling, the processor is allocated to a process for a small time quantum.\nThe processes are logically arranged in a circular queue.\nIt is a preemptive algorithm.'
        elif cpu_scheduling_type == 2:
            return 'In Non-Preemptive Shortest Job First Scheduling, the processor is allocated to the process which has the shortest next CPU burst.'
        elif cpu_scheduling_type == 3:
            return 'In  Preemptive Shortest Job First Scheduling, the processor is allocated to the process which has the shortest next CPU burst.\nIt is also known as shortest remaining time first scheduling.'
        elif cpu_scheduling_type == 4:
            return 'In Non-Preemptive Priority Scheduling, the processor is allocated to the process which has the highest priority.'
        elif cpu_scheduling_type == 5:
            return 'In Preemptive Priority Scheduling, the processor is allocated to the process which has the highest priority.'
        elif cpu_scheduling_type == 7:
            return 'In Multilevel Queue Scheduling, the ready queue is partitioned into several queues.\nA process is permanently assigned to a queue.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is often used for inter-queue scheduling.'
        elif cpu_scheduling_type == 8:
            return 'In Multilevel Feedback Queue Scheduling, the ready queue is partitioned into several queues.\nThe processes can move between the queues.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is typically used for inter-queue scheduling.'

    # Prints the details of the process schedule and statistics
    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('cpu_output_multilevel').layout
        layout.clear_widgets()
        self.gantt.clear_widgets()
        self.gantt_queue.clear_widgets()
        self.time.clear_widgets()
        self.time_queue.clear_widgets()

        formatted_data = []
        for i in range(data_cpu['num_processes']):
            process = {}
            process['name'] = data_cpu['name'+str(i)]
            process['arrival'] = int(data_cpu['arrival'+str(i)])
            process['burst'] = int(data_cpu['burst'+str(i)])
            if cpu_scheduling_type == 4 or cpu_scheduling_type == 5:
                process['priority'] = int(data_cpu['priority'+str(i)])
            elif cpu_scheduling_type == 7:
                process['queue_assigned'] = data_cpu['queue_assigned'][i]
            formatted_data.append(process)
            self.colors[process['name']] = [random(), random(), random()]
        self.colors['Idle'] = [0.2, 0.2, 0.2]
        self.colors['DL'] = [0.2, 0.2, 0.2]
        if cpu_scheduling_type == 7 or cpu_scheduling_type == 8:
            for i in range(data_cpu['num_queues']):
                self.colors_queue[i+1] = [random(), random(), random()]
                self.colors_queue[0] = [0.2, 0.2, 0.2]
        
        if cpu_scheduling_type == 0:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.fcfs(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 1:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.round_robin(formatted_data, data_cpu['quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 2:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.shortest_job_non_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 3:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.shortest_job_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 4:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.priority_non_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 5:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.priority_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 7:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.multilevel(formatted_data, data_cpu['num_queues'], data_cpu['queue_algo'], data_cpu['queue_quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 8:
            self.cpu_schedule, self.stats, self.details, self.error_status = cpu_scheduling.multilevel_feedback(formatted_data, data_cpu['num_queues'], data_cpu['queue_quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        
        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll
        grid.bind(minimum_height=grid.setter('height'))

        if self.error_status['error_number'] != -1:
            # Inform the user
            #display_error(grid, self.error_status['error_message'])
            pass
        else:
            row_height = '30dp'

            # Display process schedule details
            for process in self.cpu_schedule:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height='20dp')

                if (process['name'] == 'DL'):
                    label_name = Label(text='[ref=click]'+'Dispatch Latency'+':[/ref]', markup=True)
                else:
                    label_name = Label(text='[ref=click]'+process['name']+':[/ref]', markup=True)
                box.add_widget(label_name)
                label = Label(text=str(process['start']))
                box.add_widget(label)
                label = Label(text=str(process['end']))
                box.add_widget(label)
            
                # Add view details button for each process
                details_button = ColoredButton(text='Details', size_hint_x=None, width='100dp')
                box.add_widget(details_button)

                # Blank label for padding on right
                box.add_widget(Label(text='', size_hint_x=None, width='20dp'))

                # Popup showing details of process when box is clicked
                if process['name'] != 'Idle' and process['name'] != 'DL':
                    if cpu_scheduling_type != 8:
                        content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time']))
                    else:
                        if process['next_queue'] == 0:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+"\n"+
                            "Process "+process['name']+" is completed.")
                        else:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+"\n"+
                            process['name']+" moved to queue Q"+str(process['next_queue']+1)+".") 
                    content_label = Label(text=content_str)
                    popup = Popup(title='Details of '+str(process['name']), content=content_label, size_hint=(None, None), size=(kivy.metrics.dp(200), kivy.metrics.dp(200)))
                    label_name.bind(on_ref_press=popup.open)
                    details_button.bind(on_release=popup.open)
                    popup.open()
                    popup.dismiss()
                    # print "Bound popup for process: "+str(label_name.text)
                else:
                    details_button.disabled = True

                grid.add_widget(box)

            # Display statistics
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average turnaround time: ' + str(int((self.stats['turn_time']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average waiting time: ' + str(int((self.stats['wait_time']*100)+0.5)/100.0)))
            grid.add_widget(box)
            
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average response time: ' + str(int((self.stats['resp_time']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Throughput: ' + str(int((self.stats['throughput']*100)+0.5)/100.0)))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='CPU Utilization: ' + str(int((self.stats['cpu_utilization']*100)+0.5)/100.0) + '%'))
            grid.add_widget(box)

            self.draw_gantt()

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_gantt(self, *args):
        # Area for drawing gantt chart
        gantt = self.gantt
        gantt_queue = self.gantt_queue

        chart_wid = Widget()
        queue_wid = Widget()

        # Area for displaying time values
        time = self.time
        time_queue = self.time_queue

        # Area for displaying description.
        desc = self.desc

        gantt.clear_widgets()
        gantt_queue.clear_widgets()
        time.clear_widgets()
        time_queue.clear_widgets()
        desc.clear_widgets()

        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        # box.add_widget(Label(text='Visualization results' ))
        # desc.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp')
        algo_desc = self.get_description()
        desc_label = Label(text=algo_desc, width=Window.width, valign='top', halign='center')
        desc_label.text_size = desc_label.size
        box.add_widget(desc_label)
        desc.add_widget(box)

        # Error checking 
        if self.error_status['error_number'] != -1:
            display_error(self.gantt, self.error_status['error_message'], box_height='40dp')
            return

        # gantt.canvas.clear()
        margin_left = kivy.metrics.dp(125)
        margin_bottom = kivy.metrics.dp(50)

        with chart_wid.canvas:
            # Starting position of rectangle
            pos_x = gantt.pos[0]+margin_left
            # Increment in width per unit time
            # inc = gantt.size[0]/(self.stats['sum_time']*2)
            inc = gantt.size[0]/(self.cpu_schedule[-1]['end']*1.5)

            # Add description labels
            label = Label(text='Gantt Chart: ', size_hint_x=None, width=margin_left)
            gantt.add_widget(label)
            t_label = Label(text='Time: ', size_hint_x=None, width=margin_left, valign='top', halign='center')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

            # Draw the gantt chart rectangles and add time labels
            for process in self.cpu_schedule:
                label = Label(text=process['name'], size_hint_x=None, width=inc*(process['end']-process['start']))
                gantt.add_widget(label)

                t_label = Label(text=str(process['start']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='top')
                t_label.text_size = t_label.size
                time.add_widget(t_label)

                Color(self.colors[process['name']][0], self.colors[process['name']][1], self.colors[process['name']][2], 0.4, mode='rgba')
                Rectangle(pos=(pos_x, gantt.pos[1]+margin_bottom), size=(inc*(process['end']-process['start']), gantt.size[1]/2))
                pos_x += (inc*(process['end']-process['start']))

            # Add time label for the end time of last process
            process = self.cpu_schedule[-1]
            t_label = Label(text=str(process['end']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='top')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

        # Add the widget used to draw the gantt chart on the screen
        gantt.add_widget(chart_wid)

        if cpu_scheduling_type == 7 or cpu_scheduling_type == 8:
            with queue_wid.canvas:
                # Starting position of rectangle
                pos_x = gantt_queue.pos[0]+margin_left
                # Increment in width per unit time
                inc = gantt_queue.size[0]/(self.cpu_schedule[-1]['end']*1.5)

                # Add description labels
                label = Label(text='Gantt Chart: ', size_hint_x=None, width=margin_left)
                gantt_queue.add_widget(label)
                t_label = Label(text='Time: ', size_hint_x=None, width=margin_left, valign='top', halign='center')
                t_label.text_size = t_label.size
                time_queue.add_widget(t_label)
                queue_schedule = list()
                start = 0
                end = 0
                flag = False
                
                for process in self.cpu_schedule:
                    queue_name = 0
                    if process['name'] != 'Idle' and process['name'] != 'DL':
                        if cpu_scheduling_type == 7:
                            for i in range(data_cpu['num_processes']):
                                if process['name'] == data_cpu['name'+str(i)]:
                                    queue_name = data_cpu['queue_assigned'][i]
                        else:
                            queue_name = process['queue_name']
                    queue = dict()
                    queue['name'] = queue_name
                    queue['start'] = process['start']
                    queue['end'] = process['end']
                    queue_schedule.append(queue)
                i = 0
                # Draw the gantt chart rectangles and add time labels
                while (i < len(queue_schedule)):
                    name = queue_schedule[i]['name']
                    start = queue_schedule[i]['start']
                    end = queue_schedule[i]['end']
                    if queue_schedule[i]['name'] == 0:
                        label = Label(text='-', size_hint_x=None, width=inc*(end - start))
                        i = i+1
                    else:
                        j = i
                        while (j < len(queue_schedule)):
                            if name == queue_schedule[j]['name']:
                                end = queue_schedule[j]['end']
                                j = j+1
                            else:
                                break
                        label = Label(text='Q' + str(name), size_hint_x=None, width=inc*(end - start))
                        i = j
                    gantt_queue.add_widget(label)

                    t_label = Label(text=str(start), size_hint_x=None, width=inc*(end - start), halign='left', valign='top')
                    t_label.text_size = t_label.size
                    time_queue.add_widget(t_label)

                    Color(self.colors_queue[name][0], self.colors_queue[name][1], self.colors_queue[name][2], 0.4, mode='rgba')
                    Rectangle(pos=(pos_x, gantt_queue.pos[1]+margin_bottom), size=(inc*(end - start), gantt_queue.size[1]/2))
                    pos_x += (inc*(end - start))

                # Add time label for the end time of last process
                queue = queue_schedule[-1]
                t_label = Label(text=str(queue['end']), size_hint_x=None, width=inc*(end - start), halign='left', valign='top')
                t_label.text_size = t_label.size
                time_queue.add_widget(t_label)

            # Add the widget used to draw the gantt chart on the screen
            gantt_queue.add_widget(queue_wid)


# Input Screen for Deadlock Avoidance algorithm
class DeadlockAvoidanceInputScreen(Screen):
    form = ObjectProperty(None)
    request_form = ObjectProperty(None)

    margin_right = '15dp'

    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_num_resource_types()

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for number of processes input
    def bind_num_resource_types(self, *args):
        self.num_resource_types.bind(text=self.update_form)

    # Called when the number of processes or number of resources input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        if (self.num_processes.text == ""):
            data_da['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_da['num_processes'] = 0
        else:
            data_da['num_processes'] = int(self.num_processes.text)

        if (self.num_resource_types.text == ""):
            data_da['num_resource_types'] = 0
        elif not (self.num_resource_types.text.isdigit()):
            data_da['num_resource_types'] = 0
        else:
            data_da['num_resource_types'] = int(self.num_resource_types.text)

        # If input is valid, load form else display error message
        if (data_da['num_processes'] > 0 and data_da['num_resource_types'] > 0):
            self.load_form()
        elif (self.num_processes.text != "" and self.num_resource_types.text != ""):
            form = self.manager.get_screen('da_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    def load_form(self, *args):
        form = self.manager.get_screen('da_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_da dictionary
        data_da['available'] = [5] * data_da['num_resource_types']
        data_da['request'] = [0] * data_da['num_resource_types']
        data_da['max'] = [[10 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]
        data_da['allocation'] = [[4 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(data_da['num_resource_types']):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(da_on_available, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Max Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Max:'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Max matrix (n x m)
        for i in range(data_da['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_da['num_resource_types']):
                inp = TextInput(id='max'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_max, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(data_da['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_da['num_resource_types']):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_allocation, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Add labels for resource types in request form:
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        box.add_widget(Label(text='Process No.'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for resource form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        inp = TextInput(id='process_id')
        inp.bind(text=da_request_on_process_id)
        box.add_widget(inp)
        for i in range(data_da['num_resource_types']):
            inp = TextInput(id='request'+str(i))
            inp.bind(text=partial(da_on_request, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Uncomment to add buttons on scroll view
        # # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_da_output))
        # form.add_widget(box)
        

    def switch_to_da_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'da_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

class DeadlockAvoidanceOutputScreen(Screen):
    def calculate(self, *args):
        available = data_da['available']
        maximum = data_da['max']
        allocation = data_da['allocation']
        request = data_da['request']

        layout = self.manager.get_screen('da_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        box.add_widget(Label(text="Banker's Algorithm: When a process requests a set of resources, the system must\ndetermine whether granting the request will keep the system in a safe state."))
        grid.add_widget(box)

        # Check if the request can be granted or not
        grantable, message, error_status = deadlock.check_request(available, maximum, allocation, request, data_da['request_process'], data_da['num_processes'], data_da['num_resource_types'])

        if error_status['error_number'] != -1:
            # Inform the user
            display_error(grid, error_status['error_message'])
        else:
            # If request is grantable, check if the state is safe or not
            if grantable:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='If the request can be granted, the system will be in the following state -'))
                grid.add_widget(box)

                for j in range(data_da['num_resource_types']):
                    # print "Request["+str(j)+"] = "+str(request[j])
                    available[j] -= request[j]
                    allocation[data_da['request_process']][j] += request[j]

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Available'))
                grid.add_widget(box)

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                available_text = ''
                for i in range(data_da['num_resource_types']):
                    available_text += (str(available[i])+'   ')
                box.add_widget(Label(text=available_text))
                grid.add_widget(box)

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Allocation'))
                box.add_widget(Label(text='Need'))
                grid.add_widget(box)

                for i in range(data_da['num_processes']):
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    allocation_text = ''
                    for j in range(data_da['num_resource_types']):
                        allocation_text += (str(allocation[i][j])+'   ')
                    box.add_widget(Label(text=allocation_text))

                    need_text = ''
                    for j in range(data_da['num_resource_types']):
                        need_text += (str(maximum[i][j] - allocation[i][j])+'   ')
                    box.add_widget(Label(text=need_text))
                    grid.add_widget(box)

                safe, schedule, need = deadlock.is_safe(available, maximum, allocation, data_da['num_processes'], data_da['num_resource_types'])
                work = deepcopy(available)
                finish = ['F'] * data_da['num_processes']

                if safe:
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='The state is safe. Hence the request can be granted. The processes can be scheduled as follows:'))
                    grid.add_widget(box)

                    # Output table labels
                    # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='Process'))
                    box.add_widget(Label(text='Need'))
                    box.add_widget(Label(text='Allocation'))
                    box.add_widget(Label(text='Work'))
                    box.add_widget(Label(text='Finish'))
                    grid.add_widget(box)

                    # Display initial work vector
                    # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='Initial'))

                    # Need for current process
                    box.add_widget(Label(text='-'))
                    # Allocation for current process
                    box.add_widget(Label(text='-'))

                    work_text = ''
                    for i in range(len(work)):
                        work_text += (str(work[i])+'  ')
                    box.add_widget(Label(text=work_text))
                    finish_text = ''
                    for i in range(len(finish)):
                        finish_text += (finish[i]+'  ')
                    box.add_widget(Label(text=finish_text))
                    grid.add_widget(box)

                    # Display step by step changes in work vector according to process scheduled
                    for i in range(len(schedule)):
                        for j in range(len(work)):
                            work[j] += allocation[schedule[i]][j]
                        finish[schedule[i]] = 'T'
                        # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                        box.add_widget(Label(text='P'+str(schedule[i]+1)))

                        # Need for current process
                        need_text = ''
                        for j in range(len(need[i])):
                            need_text += (str(need[i][j])+'  ')
                        box.add_widget(Label(text=need_text))

                        # Allocation for current process
                        allocation_text = ''
                        for j in range(len(allocation[i])):
                            allocation_text += (str(allocation[i][j])+'  ')
                        box.add_widget(Label(text=allocation_text))

                        # Work vector after current process is allocated resources
                        work_text = ''
                        for j in range(len(work)):
                            work_text += (str(work[j])+'  ')
                        box.add_widget(Label(text=work_text))

                        # Finish vector after current process is allocated resources
                        finish_text = ''
                        for j in range(len(finish)):
                            finish_text += (finish[j]+'  ')
                        box.add_widget(Label(text=finish_text))
                        grid.add_widget(box)
                else:
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='The state is unsafe and will result in a deadlock. Hence the request cannot be granted.'))
                    grid.add_widget(box)
            # Request not grantable
            else:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text=message))
                grid.add_widget(box)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_da_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_da_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'da_form'

# Input Screen for Deadlock Detection algorithm
class DeadlockDetectionInputScreen(Screen):
    form = ObjectProperty(None)

    margin_right = '15dp'

    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_num_resource_types()

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for number of processes input
    def bind_num_resource_types(self, *args):
        self.num_resource_types.bind(text=self.update_form)

    # Called when the number of processes or number of resources input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        if (self.num_processes.text == ""):
            data_dd['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_dd['num_processes'] = 0
        else:
            data_dd['num_processes'] = int(self.num_processes.text)

        if (self.num_resource_types.text == ""):
            data_dd['num_resource_types'] = 0
        elif not (self.num_resource_types.text.isdigit()):
            data_dd['num_resource_types'] = 0
        else:
            data_dd['num_resource_types'] = int(self.num_resource_types.text)

        # If input is valid, load form else display error message
        if (data_dd['num_processes'] > 0 and data_dd['num_resource_types'] > 0):
            self.load_form()
        elif (self.num_processes.text != "" and self.num_resource_types.text != ""):
            form = self.manager.get_screen('dd_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    def load_form(self, *args):
        form = self.manager.get_screen('dd_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_dd dictionary
        data_dd['available'] = [5] * data_dd['num_resource_types']
        data_dd['request'] = [[10 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]
        data_dd['allocation'] = [[4 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (m)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Available array (m)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(data_dd['num_resource_types']):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(dd_on_available, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(data_dd['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_dd['num_resource_types']):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_allocation, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Request Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Request matrix (n x m)
        for i in range(data_dd['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_dd['num_resource_types']):
                inp = TextInput(id='request'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_request, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_dd_output))
        # form.add_widget(box)

    def switch_to_dd_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'dd_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

# Output screen for Deadlock Detection Algorithm
class DeadlockDetectionOutputScreen(Screen):
    def calculate(self, *args):
        available = data_dd['available']
        allocation = data_dd['allocation']
        request = data_dd['request']

        layout = self.manager.get_screen('dd_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        box.add_widget(Label(text='Deadlock Detection Algorithm: This algorithm examines the state\nof the system and determines whether a deadlock has occurred.'))
        grid.add_widget(box)

        # Check if the system is deadlocked
        deadlock_safe, schedule, error_status = deadlock.detect(available, allocation, request, data_dd['num_processes'], data_dd['num_resource_types'])

        if error_status['error_number'] != -1:
            # Inform the user
            display_error(grid, error_status['error_message'])
        else:
            work = deepcopy(available)
            finish = ['F'] * data_dd['num_processes']

            # Display schedule
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='The processes can be scheduled as follows: '))
            grid.add_widget(box)

            # Output table labels
            # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Process'))
            box.add_widget(Label(text='Work'))
            box.add_widget(Label(text='Finish'))
            grid.add_widget(box)

            # Display initial work vector
            # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Initial'))
            work_text = ''
            for i in range(len(work)):
                work_text += (str(work[i])+'   ')
            box.add_widget(Label(text=work_text))
            finish_text = ''
            for i in range(len(finish)):
                finish_text += (finish[i]+'   ')
            box.add_widget(Label(text=finish_text))
            grid.add_widget(box)

            # Display step by step changes in work vector according to process scheduled
            for i in range(len(schedule)):
                for j in range(len(work)):
                    work[j] += allocation[schedule[i]][j]
                # print "Schedule["+str(i)+"] = "+str(schedule[i])
                finish[schedule[i]] = 'T'
                # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='P'+str(schedule[i]+1)))
                work_text = ''
                for j in range(len(work)):
                    work_text += (str(work[j])+'   ')
                box.add_widget(Label(text=work_text))
                finish_text = ''
                for j in range(len(finish)):
                    finish_text += (finish[j]+'   ')
                box.add_widget(Label(text=finish_text))
                grid.add_widget(box)

            # Not deadlocked
            if deadlock_safe:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='No deadlocked detected.'))
                grid.add_widget(box)
            else:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Deadlock detected. Deadlocked processes: '))
                grid.add_widget(box)
                processes_string = ''
                for j in range(data_dd['num_processes']):
                    if finish[j] == 'F':
                        processes_string += "P"+str(j+1)+", "
                processes_string = processes_string[:-2]
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text=processes_string))
                grid.add_widget(box)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_dd_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_dd_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dd_form'

# Input screen for Contiguous Memory Allocation Strategies
class MemoryInputScreen(Screen):
    strategy_type = NumericProperty(None)
    form = ObjectProperty(None)

    margin_right = '15dp'

    # Update memory size and set to default value if empty
    def update_mem_size(self, *args):
        if not self.mem_size.text.isdigit():
            data_mem['mem_size'] = 0
        else:
            data_mem['mem_size'] = int(self.mem_size.text)

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        if text == 'First Fit':
            self.strategy_type = 0
        elif text == 'Best Fit':
            self.strategy_type = 1
        elif text == 'Worst Fit':
            self.strategy_type = 2
        data_mem['algo'] = self.strategy_type

    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_mem_size()
        self.bind_algo_spinner()

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for memory size input
    def bind_mem_size(self, *args):
        self.mem_size.bind(text=self.update_mem_size)

    def bind_algo_spinner(self, *args):
        self.algo_spinner.bind(text=self.show_selected_value)

    # Called when the number of processes or number of resources input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        if (self.num_processes.text == ""):
            data_mem['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_mem['num_processes'] = 0
        else:
            data_mem['num_processes'] = int(self.num_processes.text)

        # If input is valid, load form else display error message
        if (data_mem['num_processes'] > 0):
            self.load_form()
        elif (self.num_processes.text != ""):
            form = self.manager.get_screen('mem_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('mem_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_mem dictionary
        data_mem['algo'] = 0
        if 'mem_size' not in data_mem:
            data_mem['mem_size'] = 0
        data_mem['size'] = [128] * data_mem['num_processes']
        data_mem['arrival'] = [0] * data_mem['num_processes']
        data_mem['burst'] = [10] * data_mem['num_processes']

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Box for algo spinner
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=(kivy.metrics.dp(5),kivy.metrics.dp(20)))
        # box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        # algo_spinner = Spinner(
        #     text='Select an Algorithm',
        #     values=('First Fit', 'Best Fit', 'Worst Fit'))
        # algo_spinner.bind(text=self.show_selected_value)
        # box.add_widget(algo_spinner)
        # grid.add_widget(box)

        # Add labels for input
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(5), 0))
        box.add_widget(Label(text='Process name'))
        box.add_widget(Label(text='Size (KB)'))
        box.add_widget(Label(text='Arrival time (ms)'))
        box.add_widget(Label(text='Turnaround time (ms)'))
        grid.add_widget(box)

        # Add inputs
        for i in range(data_mem['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10), 0))

            box.add_widget(Label(text='P'+str(i+1)))

            inp = TextInput(id='size'+str(i))
            inp.bind(text=partial(mem_on_size, i=i))
            box.add_widget(inp)

            inp = TextInput(id='arrival'+str(i))
            inp.bind(text=partial(mem_on_arrival, i=i))
            box.add_widget(inp)

            inp = TextInput(id='burst'+str(i))
            inp.bind(text=partial(mem_on_termination, i=i))
            box.add_widget(inp)

            grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_mem_output))
        # form.add_widget(box)

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_to_mem_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'mem_output'

# Output screen for Continuous Memory Allocation Strategies
class MemoryOutputScreen(Screen):
    # Stores the colours assigned to each process indexed by name
    colors = {}

    # Stores the memory chart generated by algorithm
    memory_chart = []

    # Margins for memory chart output
    margin_left = kivy.metrics.dp(125)
    margin_bottom = kivy.metrics.dp(175)

    # Increment in width per unit size
    inc = 0

    def get_start_height(self, idx, total, height):
        pos = (total-idx-1)*height
        return pos
    
    def calculate(self, *args):
        # Generate formatted data for input to the algo and assign random colours to processes
        formatted_data = []
        for i in range(data_mem['num_processes']):
            process = {}
            process['name'] = 'P'+str(i+1)
            process['arrival'] = int(data_mem['arrival'][i])
            process['size'] = int(data_mem['size'][i])
            process['burst'] = int(data_mem['burst'][i])
            process['mem_size'] = int(data_mem['mem_size'])
            formatted_data.append(process)
            self.colors[process['name']] = [random(), random(), random()]
        self.colors['hole'] = [0.3, 0.3, 0.3]
        # self.colors['hole'] = [0, 0, 0]

        if data_mem['algo'] == 0:
            self.memory_chart = memory_allocation.first_fit(formatted_data)
        elif data_mem['algo'] == 1:
            self.memory_chart = memory_allocation.best_fit(formatted_data)
        elif data_mem['algo'] == 2:
            self.memory_chart = memory_allocation.worst_fit(formatted_data)

        layout = self.manager.get_screen('mem_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Output the algo description
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        algo_desc = ''
        if data_mem['algo'] == 0:
            algo_desc = 'In the First Fit Algorithm, a process is loaded in the first hole that is large enough for the process to be found.'
        elif data_mem['algo'] == 1:
            algo_desc = 'In the Best Fit Algorithm, a process is loaded in the smallest hole that is large enough for the process.'
        else:
            algo_desc = 'In the Worst Fit Algorithm, a process is loaded in the largest hole.'

        desc_label = Label(text=algo_desc, width=Window.width, valign='top', halign='center')
        desc_label.text_size = desc_label.size
        box.add_widget(desc_label)
        grid.add_widget(box)

        error = self.memory_chart[0]['error_status']
        if error['error_number'] != -1:
            # Inform the user
            display_error(grid, error['error_message'])
        else:
            # Display each element of memory chart timeline
            for idx,temp_memory in enumerate(self.memory_chart):
                # print str(temp_memory)
                wait_queue = temp_memory['processes_waiting']
                event_details = temp_memory['event']
                external_fragmentation = temp_memory['external_fragmentation']
                memory_state = temp_memory['memory_state']
                process_id,arrival_bit,curr_time,burst_time,process_size = event_details

                if (arrival_bit == 1): # new process has arrived
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='At time T = '+ str(curr_time) + 'ms,  process '+str(process_id)+' requests for a memory slot.'))
                    grid.add_widget(box)
                else: # process is leaving
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='At time T = '+ str(curr_time) + 'ms,  process '+str(process_id)+' leaving memory.'))
                    grid.add_widget(box)

                # Draw the memory state
                mem_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
                size_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                wait_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                status_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                wait_to_memory_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)

                grid.add_widget(mem_box)
                grid.add_widget(size_box)
                grid.add_widget(wait_box)
                grid.add_widget(status_box)
                grid.add_widget(wait_to_memory_box)
                # TODO: Better tracking of total height
                start_height = self.get_start_height(idx, len(self.memory_chart), kivy.metrics.dp(280))
                self.draw_memory_state(mem_box, size_box, start_height, temp_memory)
                self.draw_wait_queue(wait_box, status_box, wait_to_memory_box, start_height, temp_memory)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_mem_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_memory_state(self, mem_box, size_box, start_height, temp_memory, *args):
        # Unpack memory state details
        memory_state = temp_memory['memory_state']
        # wait_queue = temp_memory['processes_waiting']
        event_details = temp_memory['event']
        process_id,arrival_bit,curr_time,burst_time,process_size = event_details

        chart_wid = Widget()
        # Increment in width per unit size
        self.inc = Window.width/(int(data_mem['mem_size'])*1.5)

        # Add description labels
        label = Label(text='Memory state: ', size_hint_x=None, width=self.margin_left)
        mem_box.add_widget(label)
        s_label = Label(text='Size: ', size_hint_x=None, width=self.margin_left, valign='top', halign='center')
        s_label.text_size = s_label.size
        size_box.add_widget(s_label)

        # Draw the memory state rectangles and add size labels
        if not memory_state:
            self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', 0, data_mem['mem_size'])
        else:
            for i,memory_slot in enumerate(memory_state):
                process_id1, start1, end1 = memory_slot       

                if(len(memory_state) == 1): # only tuple in list
                    if(start1 > 0):
                        self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', 0, start1)
                    self.add_process(chart_wid, mem_box, size_box, start_height, process_id1, start1, (end1-start1))

                    if(data_mem['mem_size']-end1 > 0):
                        self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', end1, (data_mem['mem_size']-end1))
                elif(i == len(memory_state)-1): #last tuple, more tuples preceded
                    self.add_process(chart_wid, mem_box, size_box, start_height, process_id1, start1, (end1-start1))
                    if(data_mem['mem_size']-end1 > 0):
                        self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', end1, (data_mem['mem_size']-end1))
                else:
                    process_id2,start2,end2 = memory_state[i+1]
                    if(i == 0): # first tuple, more tuples follow
                        if(start1 > 0):
                            self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', 0, start1)
                    self.add_process(chart_wid, mem_box, size_box, start_height, process_id1, start1, (end1-start1))
                    if(start2-end1 > 0):
                        self.add_process(chart_wid, mem_box, size_box, start_height, 'hole', end1, (start2-end1))

        # Add size label for the end of memory
        s_label = Label(text=str(data_mem['mem_size']), size_hint_x=None, width=self.inc*(data_mem['mem_size']), halign='left', valign='top')
        s_label.text_size = s_label.size
        size_box.add_widget(s_label)

        # Add the widget used to draw the meomory state on the screen
        mem_box.add_widget(chart_wid)
    # Drawing the wait queue
    def draw_wait_queue(self, wait_box, status_box, wait_to_memory_box, start_height, temp_memory, *args):
        wait_queue = temp_memory['processes_waiting']
        event_details = temp_memory['event']
        process_id,arrival_bit,curr_time,burst_time,process_size = event_details
        wait_to_memory = temp_memory['wait_to_memory']
        external_fragmentation = temp_memory['external_fragmentation']

        wait_flag=0 # to check whether process was added to the wait queue

        label = Label(text='Wait Queue: ', size_hint_x=None, width=self.margin_left, valign='top', halign='center')
        label.text_size = label.size
        wait_box.add_widget(label)

        s_label = Label(text='Status: ', size_hint_x=None, width=self.margin_left, valign='top', halign='center')
        s_label.text_size = s_label.size
        status_box.add_widget(s_label)

        wm_label = Label(text='Processes loaded into memory from wait queue: ', size_hint_x=None, width=self.margin_left  + kivy.metrics.dp(230), valign='top', halign='center')
        wm_label.text_size = wm_label.size
        wait_to_memory_box.add_widget(wm_label)

        if not wait_queue:
            w_label = Label(text='Empty', size_hint_x=None, width='50dp', halign='left', valign='top')
            w_label.text_size = w_label.size
            wait_box.add_widget(w_label)

        for process in wait_queue:
            process_name, process_s,process_burst = process
            if(process_name == process_id):# will only happen if arrival_bit=1
                wait_flag=1 # process was added to wait queue
            w_label = Label(text=str(process_name), size_hint_x=None, width='40dp', halign='left', valign='top')
            w_label.text_size = w_label.size
            wait_box.add_widget(w_label)

        if(arrival_bit == 1):
            if(wait_flag == 1 and external_fragmentation == 1):
                ss_label = Label(text='Process ' + str(process_id) + ' was added to the wait queue because of external fragmentation though enough free memory is available.', size_hint_x=None, width='800dp', halign='left', valign='top') 
            elif(wait_flag == 1 and external_fragmentation == 0):
                ss_label = Label(text='Process ' + str(process_id) + ' was added to the wait queue due to insufficient memory available.', size_hint_x=None, width='800dp', halign='left', valign='top')       
            else:
                ss_label = Label(text='Process ' + str(process_id) + ' was assigned a slot in the main memory.', size_hint_x=None, width='800dp', halign='left', valign='top') 

            wm_label = Label(text='None', size_hint_x=None, width='50dp', valign='top', halign='left')
            wm_label.text_size = wm_label.size
            wait_to_memory_box.add_widget(wm_label)    
        else:
            if not wait_to_memory:
                ss_label = Label(text='Process ' + str(process_id) + ' has succesfully been deallocated memory.', size_hint_x=None, width='800dp', halign='left', valign='top')
                wm_label = Label(text='None', size_hint_x=None, width='50dp', valign='top', halign='left')
                wm_label.text_size = wm_label.size
                wait_to_memory_box.add_widget(wm_label)    
            else: 
                ss_label = Label(text='Process ' + str(process_id) + ' has succesfully been deallocated memory. ', size_hint_x=None, width='800dp', halign='left', valign='top')
                for processes in wait_to_memory: 
                    wm_label =  Label(text= str(processes), size_hint_x=None, width='40dp', halign='left', valign='top')
                    wm_label.text_size = wm_label.size
                    wait_to_memory_box.add_widget(wm_label)

        ss_label.text_size = ss_label.size
        status_box.add_widget(ss_label)


    def add_process(self, chart_wid, mem_box, size_box, start_height, process_name, mem_start, rect_width, *args):
        # print "Drawing {} rectangle from {} to {}".format(process_name, mem_start, rect_width)
        with chart_wid.canvas:
            label = Label(text=process_name, size_hint_x=None, width=rect_width*self.inc)
            mem_box.add_widget(label)

            s_label = Label(text=str(mem_start), size_hint_x=None, width=rect_width*self.inc, halign='left', valign='top')
            s_label.text_size = s_label.size
            size_box.add_widget(s_label)

            Color(self.colors[process_name][0], self.colors[process_name][1], self.colors[process_name][2], 0.4, mode='rgba')
            Rectangle(pos=(self.margin_left+(mem_start*self.inc), start_height+self.margin_bottom), size=(rect_width*self.inc, kivy.metrics.dp(35)))

    def switch_to_mem_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'mem_form'

#Input screen for Page Replacement Algorithms
class PageInputScreen(Screen):
    strategy_type = NumericProperty(None)
    form = ObjectProperty(None)
    algo_type = 0

    def update_form(self, *args):
        if (self.num_frames.text == ""):
            data_page['num_frames'] = 0
        elif not (self.num_frames.text.isdigit()):
            data_page['num_frames'] = 0
        else:
            data_page['num_frames'] = int(self.num_frames.text)

        # If input is valid, load form else display error message
        if (data_page['num_frames'] > 0):
            self.load_form()
        elif (self.num_frames.text != ""):
            form = self.manager.get_screen('page_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    # Binder function for number of processes input
    def bind_num_frames(self, *args):
        self.num_frames.bind(text=self.update_form)

        # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('page_form').algo_spinner
        spinner.bind(text=self.show_selected_value)

    def bind_widgets(self, *args):
        self.bind_num_frames()
        self.bind_spinner()

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        form_reload_flag = False
        if self.strategy_type == 4:
            form_reload_flag = True

        if text == 'First In First Out':
            self.strategy_type = 0
            self.algo_type = 0
        elif text == 'Optimal':
            self.strategy_type = 1
            self.algo_type = 1
        elif text == 'Least Recently Used':
            self.strategy_type = 2
            self.algo_type = 2
        elif text == 'Second Chance':
            self.strategy_type = 3
            self.algo_type = 3
        elif text == 'Enhanced Second Chance':
            self.strategy_type = 4
            self.algo_type = 4
            # Toggle form reload flag for this algo since we require modify bit input here
            form_reload_flag = not form_reload_flag
        elif text == 'Least Frequently Used':
            self.strategy_type = 5
            self.algo_type = 5
        elif text == 'Most Frequently Used':
            self.strategy_type = 6
            self.algo_type = 6
        data_page['algo'] = self.strategy_type
        if form_reload_flag:
            self.load_form()

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('page_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_page dictionary
        if 'algo' not in data_page:
            data_page['algo'] = 0
        if 'num_frames' not in data_page:
            data_page['num_frames'] = 0
        if 'ref_str' not in data_page:
            data_page['ref_str'] = ''
        if 'modify_bit' not in data_page:
            data_page['modify_bit'] = ''

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(15), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Box for algo spinner
        #box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=(kivy.metrics.dp(5),kivy.metrics.dp(20)))
        #box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        #algo_spinner = Spinner(
        #    text='Select an Algorithm',
        #    values=('First In First Out', 'Optimal', 'Least Recently Used', 'Second Chance', 'Enhanced Second Chance', 'Least Frequently Used', 'Most Frequently Used'))
        #algo_spinner.bind(text=self.show_selected_value)
        #box.add_widget(algo_spinner)
        #grid.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10), 0), size_hint_x=0.6)
        
        # Add label for input
        label = Label(text='Reference string:', size_hint_x=0.4, halign='left')
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)

        # Add input
        inp = TextInput(id='ref_str'+str(0), text=data_page['ref_str'], size_hint_x=0.6)
        inp.bind(text=page_on_ref)
        box.add_widget(inp)

        parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        parent_box.add_widget(box)
        # For occypying space on right
        parent_box.add_widget(BoxLayout(size_hint_x=0.4))

        grid.add_widget(parent_box)

        # Modify bit for enhanced second chance algo
        if self.algo_type == 4:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10), 0), size_hint_x=0.6)
        
            # Add label for input
            label = Label(text='Modify bit string:', size_hint_x=0.4, halign='left')
            label.bind(size=label.setter('text_size'))
            box.add_widget(label)

            # Add input
            inp = TextInput(id='modify_bit'+str(0), text=data_page['modify_bit'], size_hint_x=0.6)
            inp.bind(text=page_on_modify)
            box.add_widget(inp)

            parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            parent_box.add_widget(box)
            # For occypying space on right
            parent_box.add_widget(BoxLayout(size_hint_x=0.4))

            grid.add_widget(parent_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_page_output))
        # form.add_widget(box)

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_to_page_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'page_output'
    
# Output screen for Page Replacement Algorithms
class PageOutputScreen(Screen):
    
   # Stores the memory chart generated by algorithm
    memory_chart = []

    # Margins for memory chart output
    margin_left = kivy.metrics.dp(125)
    margin_bottom = kivy.metrics.dp(255)

    # Width of frame box
    frame_width = kivy.metrics.dp(65)

    # Increment in width per unit size
    inc = 0

    def get_description(self, *args):
        if data_page['algo'] == 0:
            return 'In First In First Out Page Replacement Algorithm, the page that was loaded earliest in the memory is replaced.'
        elif data_page['algo'] == 1:
            return 'In Optimal Page Replacement Algorithm,\nthe page that will not be referenced for the longest period of time is replaced.'
        elif data_page['algo'] == 2:
            return 'In Least Recently Used Page Replacement Algorithm,\nthe page that has not been referenced for the longest period of time is replaced.'
        elif data_page['algo'] == 3:
            return 'In Second Chance Page Replacement Algorithm,\nthe page that was loaded earliest in the memory is replaced.\nHowever, if the reference bit of the page is set then that page is given a second chance and the next possible page is replaced.\nWhen a page is given a second chance, its reference bit is reset and its arrival time is set to the current time.'
        elif data_page['algo'] == 4:
            return 'In Enhanced Second Chance Page Replacement Algorithm,\nthe pages are divided in four classes using their reference bit and modify bit as ordered pairs.\nThe page of the lowest nonempty class which was loaded earliest in the memory is replaced.'
        elif data_page['algo'] == 5:
            return 'In Least Frequently Used Page Replacement Algorithm,\nthe page that has been referenced the least number of times is replaced.'
        elif data_page['algo'] == 6:
            return 'In Most Frequently Used Page Replacement Algorithm,\nthe page that has been referenced the most number of times is replaced.'
            

    # Generate formatted data for input to the algo
    def calculate(self, *args):
        formatted_data = {}

        formatted_data['num_frames'] = int(data_page['num_frames'])
        page_numbers_data = data_page['ref_str']
        page_numbers = []
        if ',' in page_numbers_data: # Comma separated ref_str
            page_numbers = page_numbers_data.split(",")
        else: # Space separated ref_str
            page_numbers = page_numbers_data.split()
        formatted_data['ref_str'] = page_numbers
        formatted_data['algo'] = data_page['algo']
        if data_page['algo'] == 4:
            modify_bits = []
            modify_bits_data = data_page['modify_bit']
            if ',' in page_numbers_data: # Comma separated ref_str
                modify_bits = modify_bits_data.split(",")
            else: # Space separated ref_str
                modify_bits = modify_bits_data.split()
            formatted_data['modify_bits'] = modify_bits

        self.memory_chart = page_replacement.page_replacement(formatted_data)

        layout = self.manager.get_screen('page_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))


        error = self.memory_chart[0]['error_status']
        if error['error_number'] != -1:
            # Inform the user
            display_error(grid, error['error_message'])
        else:
            # Output the algo description
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
            algo_desc = self.get_description()
            desc_label = Label(text=algo_desc, width=Window.width, valign='top', halign='center')
            desc_label.text_size = desc_label.size
            box.add_widget(desc_label)
            grid.add_widget(box)

            # To add frame labels
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            grid.add_widget(box)
            frames_label = Label(text='', size_hint_x=None, width=self.margin_left+kivy.metrics.dp(125), valign='middle', halign='right')
            frames_label.text_size = frames_label.size
            box.add_widget(frames_label)

            for i in range(formatted_data['num_frames']):
                frames_label = Label(text='Frame' + str(i+1), size_hint_x=None, width=self.frame_width, valign='middle', halign='right')
                frames_label.text_size = frames_label.size
                box.add_widget(frames_label)

            for idx, temp_memory in enumerate(self.memory_chart):
                page_number = temp_memory['page_number']
                page_fault = temp_memory['page_fault']
                allocated_frame = temp_memory['frame_number']
                memory_state = temp_memory['memory_frames']

                # Add page referenced label
                page_ref_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                page_label = Label(text='Page number referenced:  ', size_hint_x=None, width=self.margin_left + kivy.metrics.dp(110), valign='middle', halign='center')
                page_label.text_size = page_label.size
                page_ref_box.add_widget(page_label)
                page_label = Label(text=str(page_number), size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
                page_label.text_size = page_label.size
                page_ref_box.add_widget(page_label)
                grid.add_widget(page_ref_box)

                # Draw the memory chart
                mem_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
                page_fault_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                
                grid.add_widget(mem_box)
                grid.add_widget(page_fault_box)

                self.draw_memory_state(mem_box, page_fault_box, temp_memory)
            
            # Add total number of page faults   
            temp = self.memory_chart[-1]
            total_page_fault_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            total_page_fault_box.add_widget(Label(text='Total number of page faults: '+ str(temp['page_fault_count'])))
            grid.add_widget(total_page_fault_box) 

            # Add page fault ratio
            total_hits = len(page_numbers) - temp['page_fault_count'] 
            output = Decimal(float(temp_memory['page_fault_count'])/len(page_numbers))
            page_fault_ratio_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            page_fault_ratio_box.add_widget(Label(text='Page fault ratio: '+ str(round(output, 3))))
            grid.add_widget(page_fault_ratio_box) 

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_page_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp', bar_inactive_color=[0.7,0.7,0.7,0.45])
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_memory_state(self, mem_box, page_fault_box, temp_memory, *args):
        page_number = temp_memory['page_number']
        page_fault = temp_memory['page_fault']
        allocated_frame = temp_memory['frame_number']
        memory_state = temp_memory['memory_frames']

        mem_label = Label(text='', size_hint_x=None, width=self.margin_left - kivy.metrics.dp(25), valign='middle', halign='center')
        mem_label.text_size = mem_label.size
        mem_box.add_widget(mem_label)
        mem_label = Label(text='Memory state: ', size_hint_x=None, width=self.margin_left + kivy.metrics.dp(35), valign='middle', halign='left')
        mem_label.text_size = mem_label.size
        mem_box.add_widget(mem_label)

        for idx, state in enumerate(memory_state):
            if state == -1:
                state = 'X'
            if allocated_frame - 1 == idx and page_fault == 1:
                mem_label = ColoredBorderedLabel(text='[b][color=DEC41B]'+str(state)+'[/color][/b]', markup=True, size_hint_x=None, width=self.frame_width, valign='middle', halign='center')
            else:
                mem_label = WhiteBorderedLabel(text=str(state), size_hint_x=None, width=self.frame_width, valign='middle', halign='center')

            mem_label.text_size = mem_label.size
            mem_box.add_widget(mem_label)

        # To add page fault (Y/N)
        page_f_label = Label(text='', size_hint_x=None, width=self.margin_left - kivy.metrics.dp(25), valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        page_f_label = Label(text='Page fault: ', size_hint_x=None, width=self.margin_left, valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        if page_fault == 1:
            page_f_label = Label(text='[color=DEC41B]Yes[/color]', markup=True, size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
        else:
            page_f_label = Label(text='No', markup=True, size_hint_x=None
                , width=self.margin_left, valign='middle', halign='left')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

    def switch_to_page_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'page_form'

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

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10),0), size_hint_x=0.7)

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
        parent_box.add_widget(BoxLayout(size_hint_x=0.3))

        grid.add_widget(parent_box)

        if self.algo_type !=0 and self.algo_type != 1:
            # Box for direction spinner 
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', padding=(kivy.metrics.dp(10),0), size_hint_x=0.7)

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
            parent_box.add_widget(BoxLayout(size_hint_x=0.3))

            grid.add_widget(parent_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
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
            return 'In First Come First Served Scheduling, the i/o requests are processed in the order in which they arrive.'
        elif data_disk['algo'] == 1:
            return 'In Shortest Seek Time First Scheduling, the i/o request which will need the minimum seek time is processed first.'
        elif data_disk['algo'] == 2:
            return 'In SCAN scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder.'
        elif data_disk['algo'] == 3:
            return 'In C-SCAN scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder. On reaching the end, the r/w head immediately returns to the beginning without servicing any request on the return trip.'
        elif data_disk['algo'] == 4:
            return 'In LOOK scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder moving only up to last requested cylinder in the given direction.'
        elif data_disk['algo'] == 5:
            return 'In C-LOOK Scheduling, the r/w head scans back and forth across the disk servicing requests as it reaches each cylinder moving only up to last requested cylinder in the given direction.On reaching the end, the r/w head immediately returns to the beginning, if need be, without servicing any request on the return trip.'

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
            desc_label = Label(text=algo_desc, padding=(kivy.metrics.dp(20),kivy.metrics.dp(20)), size_hint_x=None, width=Window.width, valign='middle', halign='center')
            desc_label.bind(size=desc_label.setter('text_size'))

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
        sv = ScrollView(size=self.size, scroll_type=['bars'], bar_width='12dp')
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

        self.inc = Window.width/(int(data_disk['num_cylinders'])*1.1)
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

# Create the screen manager and add all screens to it
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUInputScreen(name='cpu_form'))
sm.add_widget(CPUOutputScreen(name='cpu_output'))
sm.add_widget(CPUOutputScreenMultilevel(name='cpu_output_multilevel'))
sm.add_widget(DeadlockAvoidanceInputScreen(name='da_form'))
sm.add_widget(DeadlockAvoidanceOutputScreen(name='da_output'))
sm.add_widget(DeadlockDetectionInputScreen(name='dd_form'))
sm.add_widget(DeadlockDetectionOutputScreen(name='dd_output'))
sm.add_widget(MemoryInputScreen(name='mem_form'))
sm.add_widget(MemoryOutputScreen(name='mem_output'))
sm.add_widget(PageInputScreen(name='page_form'))
sm.add_widget(PageOutputScreen(name='page_output'))
sm.add_widget(DiskInputScreen(name='disk_form'))
sm.add_widget(DiskOutputScreen(name='disk_output'))

class OSAVA(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSAVA().run()
