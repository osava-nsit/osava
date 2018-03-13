'''
This file contains the classes, functions and globals used for visualizing
Contiguous Memory Allocation Strategios
'''

# Kivy libraries
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy.metrics
# Python libraries
from functools import partial
from random import random
# OS Algorithms
from algos import memory_allocation
# OSAVA common constants and methods
from common import *

# Global data for Contiguous Memory Allocation Strategies
data_mem = dict()

# Binder functions for Contiguous Memory Allocation Strategies form
def mem_on_size(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 128
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_mem['size'][i] = int(value)

def mem_on_arrival(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 0
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_mem['arrival'][i] = int(value)

def mem_on_termination(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 10
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_mem['burst'][i] = int(value)

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
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
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
            algo_desc = 'In the First Fit Algorithm, a process is loaded in the first hole that is\nlarge enough for the process to be found.'
        elif data_mem['algo'] == 1:
            algo_desc = 'In the Best Fit Algorithm, a process is loaded in the smallest hole that is\nlarge enough for the process.'
        else:
            algo_desc = 'In the Worst Fit Algorithm, a process is loaded in the largest hole.'

        desc_label = Label(text=algo_desc, padding=(kivy.metrics.dp(20),kivy.metrics.dp(20)), width=Window.width, valign='top', halign='center', size_hint_y=None, height='80dp')
        # desc_label.text_size = desc_label.size
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
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
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
