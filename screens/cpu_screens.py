# Kivy libraries
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy.metrics
# Python libraries
from functools import partial
from random import random
# OS Algorithms
from algos import cpu_scheduling
# OSAVA common constants and methods
from common import *

# Global data for CPU Scheduling Algorithms
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive', 'Multilevel Queue', 'Multilevel Feedback Queue']
cpu_scheduling_type = 0
data_cpu = dict()

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
    if not is_valid_value(value):
        value = -1
    data_cpu['arrival'+str(i)] = int(value)

def cpu_on_burst(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['burst'+str(i)] = int(value)

def cpu_on_priority(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 10
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['priority'+str(i)] = int(value)

def cpu_on_quantum(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['quantum'] = int(value)

def cpu_on_aging(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 4
        else:
            value = 1000000000000000
    if not is_valid_value(value):
        value = -1
    data_cpu['aging'] = int(value)

def cpu_on_num_queues(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['num_queues'] = int(value)

def cpu_on_queue_quantum(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['queue_quantum'][i] = int(value)

def cpu_on_queue_assigned(instance, value, i):
    if value == '':
        if DEBUG_MODE:
            value = 1
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_cpu['queue_assigned'][i] = int(value)

# Input Screen for CPU Scheduling Algorithms with partial scrolling
class CPUInputScreen(Screen):
    layout = ObjectProperty(None)
    layout_form = ObjectProperty(None)
    queue_type = NumericProperty(None)
    cpu_type = 0
    preemptive_flag = False

    multilevel_input_widgets = []

    # Update dispatch_latency and set to default value if empty
    def update_dispatch_latency(self, instance, value, *args):
        if value == '':
            data_cpu['dispatch_latency'] = 0
        elif not is_valid_value(value):
            data_cpu['dispatch_latency'] = -1
        else:
            data_cpu['dispatch_latency'] = int(value)

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
    # def bind_dispatch_latency(self, *args):
    #     self.dispatch_latency.bind(text=self.update_dispatch_latency)

    # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinners(self, *args):
        self.algo_spinner.bind(text=self.show_selected_value)
        self.variant_spinner.bind(text=self.show_variant)

    # Wrapper function that calls binder functions for the required widgets
    def bind_widgets(self, *args):
        self.bind_num_processes()
        # self.bind_dispatch_latency()
        self.bind_spinners()

    # Call set_cpu_type method with appropriate index of scheduling algorithm
    def show_selected_value(self, spinner, text, *arg):
        if text == 'First Come First Served':
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

        if self.cpu_type != 7 and self.cpu_type != 8:
            # Add dispatch latency input
            parent_box = BoxLayout(size_hint_y=None, height='60dp')
            box = BoxLayout(orientation='horizontal', size_hint_x=0.5, size_hint_y=None, height='40dp', padding=(kivy.metrics.dp(10), kivy.metrics.dp(5)))
            label = Label(text='Dispatch latency (ms):', size_hint_x=0.5, halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))
            inp = TextInput(size_hint_x=0.5)
            inp.bind(text=self.update_dispatch_latency)
            box.add_widget(label)
            box.add_widget(inp)

            parent_box.add_widget(box)
            parent_box.add_widget(BoxLayout(size_hint_x=0.5))

            layout.add_widget(parent_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
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
            label = Label(text='Information about intra queue scheduling algorithms:')
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

        # Add dispatch latency input
        parent_box = BoxLayout(size_hint_y=None, height='60dp')
        box = BoxLayout(orientation='horizontal', size_hint_x=0.5, size_hint_y=None, height='40dp', padding=(kivy.metrics.dp(10), kivy.metrics.dp(5)))
        label = Label(text='Dispatch latency (ms):', size_hint_x=0.5, halign='left', valign='middle')
        label.bind(size=label.setter('text_size'))
        inp = TextInput(size_hint_x=0.5)
        inp.bind(text=self.update_dispatch_latency)
        box.add_widget(label)
        box.add_widget(inp)

        parent_box.add_widget(box)
        parent_box.add_widget(BoxLayout(size_hint_x=0.5))

        grid_layout.add_widget(parent_box)
        self.multilevel_input_widgets.append(parent_box)
        
    def switch_to_cpu_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'cpu_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'


# Output Screen for CPU Scheduling algorithms
class CPUOutputScreen(Screen):
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
            return 'In First Come First Served Scheduling, the processor is allocated to the process\nwhich has arrived first. It is a non-preemptive algorithm.'
        elif cpu_scheduling_type == 1:
            return 'In Round Robin Scheduling, the processor is allocated to a process for a small\ntime quantum. The processes are logically arranged in a circular queue.\nIt is a preemptive algorithm.'
        elif cpu_scheduling_type == 2:
            return 'In Non-Preemptive Shortest Job First Scheduling, the processor is allocated to\nthe process which has the shortest next CPU burst.'
        elif cpu_scheduling_type == 3:
            return 'In  Preemptive Shortest Job First Scheduling, the processor is allocated to the\nprocess which has the shortest next CPU burst.\nIt is also known as shortest remaining time first scheduling.'
        elif cpu_scheduling_type == 4:
            return 'In Non-Preemptive Priority Scheduling, the processor is allocated to the process\nwhich has the highest priority.'
        elif cpu_scheduling_type == 5:
            return 'In Preemptive Priority Scheduling, the processor is allocated to the process\nwhich has the highest priority.'
        elif cpu_scheduling_type == 7:
            return 'In Multilevel Queue Scheduling, the ready queue is partitioned into several queues.\nA process is permanently assigned to a queue.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is often used for inter-queue scheduling.'
        elif cpu_scheduling_type == 8:
            return 'In Multilevel Feedback Queue Scheduling, the ready queue is partitioned into several queues.\nThe processes can move between the queues.\nEach queue has its own scheduling algorithm.\nPreemptive priority scheduling is typically used for inter-queue scheduling.'

    # Prints the details of the process schedule and statistics
    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('cpu_output').layout
        layout.clear_widgets()
        # self.gantt.clear_widgets()
        # self.time.clear_widgets()

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

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

        if self.error_status['error_number'] != -1:
            # Inform the user
            display_error(self.layout, self.error_status['error_message'])
            pass
        else:
            row_height = '30dp'

            self.draw_gantt(grid)

            box = BoxLayout(orientation='vertical', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Timeline -'))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Process'))
            box.add_widget(Label(text='Start/resume time'))
            box.add_widget(Label(text='Suspend/termination time'))
            box.add_widget(Label(text='', size_hint_x=None, width='120dp'))
            grid.add_widget(box)

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
                        content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+" ms\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+" ms\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])) + " ms"
                    else:
                        if process['next_queue'] == 0:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+" ms\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+" ms\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+" ms\n"+
                            "Process "+process['name']+" is completed.")
                        else:
                            content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+" ms\n"+
                            "Response time: "+str(self.details[process['name']]['resp_time'])+" ms\n"+
                            "Turnaround time: "+str(self.details[process['name']]['turn_time'])+" ms\n"+
                            process['name']+" moved to queue Q"+str(process['next_queue']+1)+".")

                    content_label = Label(text=content_str)
                    popup = Popup(title='Details of '+str(process['name']), content=content_label, size_hint=(None, None), size=(kivy.metrics.dp(200), kivy.metrics.dp(200)))
                    label_name.bind(on_ref_press=popup.open)
                    details_button.bind(on_release=popup.open)
                    popup.open()
                    popup.dismiss()
                else:
                    details_button.disabled = True

                grid.add_widget(box)

            # Display statistics
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average turnaround time: ' + str(int((self.stats['turn_time']*100)+0.5)/100.0) + ' ms'))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average waiting time: ' + str(int((self.stats['wait_time']*100)+0.5)/100.0) + ' ms'))
            grid.add_widget(box)
            
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Average response time: ' + str(int((self.stats['resp_time']*100)+0.5)/100.0) + ' ms'))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='Throughput: ' + str(int((self.stats['throughput']*100)+0.5)/100.0) + ' processes/ms'))
            grid.add_widget(box)

            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
            box.add_widget(Label(text='CPU Utilization: ' + str(int((self.stats['cpu_utilization']*100)+0.5)/100.0) + '%'))
            grid.add_widget(box)

    def draw_gantt(self, grid, *args):
        # Area for displaying description.
        desc = BoxLayout(orientation='vertical', size_hint_y=None, height='100dp')

        # Area for drawing gantt chart
        gantt = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        chart_wid = Widget()

        # Area for displaying time values
        time = BoxLayout(orientation='horizontal', size_hint_y=None, height='15dp')

        grid.add_widget(desc)
        grid.add_widget(gantt)
        grid.add_widget(time)

        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        # box.add_widget(Label(text='Visualization results' ))
        # desc.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='70dp')
        algo_desc = self.get_description()
        desc_label = Label(text=algo_desc, padding=(kivy.metrics.dp(20),kivy.metrics.dp(20)), width=Window.width, valign='top', halign='center')
        # desc_label.text_size = desc_label.size
        box.add_widget(desc_label)
        desc.add_widget(box)

        # Error checking 
        if self.error_status['error_number'] != -1:
            display_error(gantt, self.error_status['error_message'], box_height='120dp')
            return

        start_height = 15   # For time labels
        start_height += 35*5    # For average stats
        start_height += len(self.cpu_schedule)*25   # For timeline
        start_height += 35*3    # For other labels

        margin_left = kivy.metrics.dp(125)
        margin_bottom = kivy.metrics.dp(start_height)

        if cpu_scheduling_type == 7 or cpu_scheduling_type == 8:
            # Area for drawing queue gantt chart
            gantt_queue = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
            queue_wid = Widget()

            # Area for displaying queue time values
            time_queue = BoxLayout(orientation='horizontal', size_hint_y=None, height='15dp')

            grid.add_widget(gantt_queue)
            grid.add_widget(time_queue)

            with queue_wid.canvas:
                # Starting position of rectangle
                pos_x = gantt_queue.pos[0]+margin_left
                # Increment in width per unit time
                inc = Window.width/(self.cpu_schedule[-1]['end']*1.5)

                # Add description labels
                label = Label(text='Gantt Chart: ', size_hint_x=None, width=margin_left)
                gantt_queue.add_widget(label)
                t_label = Label(text='Time: ', size_hint_x=None, width=margin_left, valign='middle', halign='center')
                t_label.text_size = t_label.size
                time_queue.add_widget(t_label)
                queue_schedule = list()
                start = 0
                end = 0
                
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
                    if end > start:
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

                        t_label = Label(text=str(start), size_hint_x=None, width=inc*(end - start), halign='left', valign='middle')
                        t_label.text_size = t_label.size
                        time_queue.add_widget(t_label)

                        Color(self.colors_queue[name][0], self.colors_queue[name][1], self.colors_queue[name][2], 0.4, mode='rgba')
                        Rectangle(pos=(pos_x, gantt_queue.pos[1]+margin_bottom), size=(inc*(end - start), gantt_queue.size[1]/2))
                        pos_x += (inc*(end - start))
                    else:   # Odd behaviour due to dispatch latency
                        i += 1

                # Add time label for the end time of last process
                queue = queue_schedule[-1]
                t_label = Label(text=str(queue['end']), size_hint_x=None, width=inc*(end - start), halign='left', valign='middle')
                t_label.text_size = t_label.size
                time_queue.add_widget(t_label)

            # Add the widget used to draw the gantt chart on the screen
            gantt_queue.add_widget(queue_wid)

            start_height += 125 # For queue gantt chart and timeline

        margin_bottom = kivy.metrics.dp(start_height)

        with chart_wid.canvas:
            # Starting position of rectangle
            pos_x = gantt.pos[0]+margin_left
            # Increment in width per unit time
            inc = Window.width/(self.cpu_schedule[-1]['end']*1.5)

            # Add description labels
            label = Label(text='Gantt Chart: ', size_hint_x=None, width=margin_left, valign='top')
            gantt.add_widget(label)
            t_label = Label(text='Time: ', size_hint_x=None, width=margin_left, valign='middle', halign='center')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

            # Draw the gantt chart rectangles and add time labels
            for process in self.cpu_schedule:
                if process['end'] > process['start']:
                    label = Label(text=process['name'], size_hint_x=None, width=inc*(process['end']-process['start']))
                    gantt.add_widget(label)

                    t_label = Label(text=str(process['start']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='middle')
                    t_label.text_size = t_label.size
                    time.add_widget(t_label)

                    Color(self.colors[process['name']][0], self.colors[process['name']][1], self.colors[process['name']][2], 0.4, mode='rgba')
                    Rectangle(pos=(pos_x, gantt.pos[1]+margin_bottom), size=(inc*(process['end']-process['start']), gantt.size[1]/2))
                    pos_x += (inc*(process['end']-process['start']))
                else: # Odd behaviour due to dispatch_latency
                    pass

            # Add time label for the end time of last process
            process = self.cpu_schedule[-1]
            t_label = Label(text=str(process['end']), size_hint_x=None, width=inc*(process['end']-process['start']), halign='left', valign='middle')
            t_label.text_size = t_label.size
            time.add_widget(t_label)

        # Add the widget used to draw the gantt chart on the screen
        gantt.add_widget(chart_wid)
