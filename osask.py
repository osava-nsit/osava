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
# OS Algorithms
import cpu_scheduling, deadlock, memory_allocation, page_replacement

Builder.load_file('layout.kv')

# Global flag for debug mode
DEBUG_MODE = False

# Global fixed height of form rows within scroll view
form_row_height = '40dp'

# Global data for CPU Scheduling Algorithms
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive']
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

# Binder functions for CPU Scheduling Algorithms form, to store data in the global 'data_cpu' dictionary
def cpu_on_name(instace, value, i):
    if value == '':
        value = 'P'+str(i+1)
    data_cpu['name'+str(i)] = value
def cpu_on_arrival(instace, value, i):
    if value == '':
        value = 1
    data_cpu['arrival'+str(i)] = value
def cpu_on_burst(instace, value, i):
    if value == '':
        value = 4
    data_cpu['burst'+str(i)] = value
def cpu_on_priority(instace, value, i):
    if value == '':
        value = 10
    data_cpu['priority'+str(i)] = value
def cpu_on_quantum(instace, value):
    if value == '':
        value = 2
    data_cpu['quantum'] = int(value)
def cpu_on_aging(instace, value):
    if value == '':
        value = 4
    data_cpu['aging'] = int(value)

# Binder functions for Deadlock Avoidance Algorithm form
def da_on_available(instace, value, i):
    if (value == ''):
        value = 5
    data_da['available'][i] = int(value)
def da_on_request(instance, value, i):
    if (value == ''):
        value = 0
    data_da['request'][i] = int(value)
def da_on_max(instance, value, i, j):
    if (value == ''):
        value = 8
    data_da['max'][i][j] = int(value)
def da_on_allocation(instance, value, i, j):
    if (value == ''):
        value = 4
    data_da['allocation'][i][j] = int(value)
def da_request_on_process_id(instance, value):
    if (value == ''):
        value = 1
    data_da['request_process'] = int(value)-1

# Binder functions for Deadlock Detection Algorithm form
def dd_on_available(instance, value, i):
    if (value == ''):
        value = 5
    data_dd['available'][i] = int(value)
def dd_on_request(instance, value, i, j):
    if (value == ''):
        value = 2
    data_dd['request'][i][j] = int(value)
def dd_on_allocation(instance, value, i, j):
    if (value == ''):
        value = 4
    data_dd['allocation'][i][j] = int(value)

# Binder functions for Contiguous Memory Allocation Strategies form
def mem_on_size(instance, value, i):
    if (value == ''):
        value = 128
    data_mem['size'][i] = value
def mem_on_arrival(instance, value, i):
    if (value == ''):
        value = 0
    data_mem['arrival'][i] = value
def mem_on_termination(instance, value, i):
    if (value == ''):
        value = 10
    data_mem['burst'][i] = value

# Binder functions for Page Replacement Algorithm form
def page_on_ref(instance, value):
    if(value == ''):
        value = '7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1' 
    data_page['ref_str'] = str(value)

class WhiteBorderedLabel(Label):
    pass

class ColoredBorderedLabel(Label):
    pass

# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):
    ribbon_added = False
    def load_ribbon(self, *args):
        title = self.manager.get_screen('menu').title
        if not self.ribbon_added:
            with title.canvas:
                Color(1, 0, 0, 0.4, mode='rgba')
                Rectangle(pos=(0,Window.height-kivy.metrics.dp(40)), size=(Window.width,kivy.metrics.dp(40)))
                self.ribbon_added = True
        # title.add_widget(Label(text='OS - Algo Visualization App'))

# Input Screen for CPU Scheduling Algorithms with partial scrolling
class CPUInputScreen(Screen):
    layout = ObjectProperty(None)
    layout_form = ObjectProperty(None)
    cpu_type = 0
    preemptive_flag = False

    # Called when the number of processes input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        self.load_form()

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for dispatch latency input
    def bind_dispatch_latency(self, *args):
        self.dispatch_latency.bind(text=self.update_form)

    # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('cpu_form').algo_spinner
        spinner.bind(text=self.show_selected_value)
        variant_spinner = self.manager.get_screen('cpu_form').variant_spinner
        variant_spinner.bind(text=self.show_variant)

    # Wrapper function that calls binder functions for the required widgets
    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_dispatch_latency()
        self.bind_spinner()

    # Call set_cpu_type method with appropriate index of scheduling algorithm
    def show_selected_value(self, spinner, text, *args):
        if text == 'First Come First Serve':
            self.set_cpu_type(0)
        elif text == 'Shortest Job First':
            self.set_cpu_type(2)
        elif text == 'Priority':
            self.set_cpu_type(4)
        elif text == 'Round Robin':
            self.set_cpu_type(1)

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
        # variant_spinner = self.manager.get_screen('cpu_form').variant_spinner
        # If FCFS or RR
        if new_cpu_type == 0 or new_cpu_type == 1:
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
            # variant_spinner.disabled = True
        elif self.preemptive_flag == True and new_cpu_type%2 == 0:
            new_cpu_type += 10
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
            # variant_spinner.disabled = False
        elif self.preemptive_flag == False and new_cpu_type%2 != 0:
            new_cpu_type -= 1
            cpu_scheduling_type = new_cpu_type
            self.cpu_type = new_cpu_type
            # variant_spinner.disabled = False
        self.load_form()

    # Called when preemptive or non-preemtive option is clicked. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
    def update_cpu_type(self, *args):
        global cpu_scheduling_type
        # If FCFS or RR Scheduling
        if self.cpu_type == 0 or self.cpu_type == 1:
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

        # Update num_processes and set to default value if empty
        if DEBUG_MODE:
            if (self.num_processes.text == "" or int(self.num_processes.text) == 0):
                self.num_processes.text = "5"
        if not self.num_processes.text.isdigit():
            print "Invalid number of processes. Please enter valid input."
            data_cpu['num_processes'] = 0
        else:
            data_cpu['num_processes'] = int(self.num_processes.text)

        # If num_processes is zero, stop
        # TODO: Prompt the user to enter number of processes
        if data_cpu['num_processes'] == 0:
            print "Number of processes is zero. Cannot load form."
            return

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
            inp = TextInput(id='aging', size_hint_x=0.3)
            inp.bind(text=cpu_on_aging)
            # inp.font_size = inp.size[1]
            label = Label(text='Aging: Promote priority by 1 unit each time after waiting (ms) - ', size_hint_x=0.7)
            # label.text_size = label.size
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', padding=(0, kivy.metrics.dp(5)), size_hint_y=None, height='50dp')
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_cpu_output))
        layout.add_widget(box)

        # Add ScrollView
        # sv = ScrollView(size_hint=(None, None), size=(400, 400))
        sv = ScrollView(size=self.size)
        sv.add_widget(layout)
        layout_form.add_widget(sv)
        

    def switch_to_cpu_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'cpu_output'

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
    # Stores the process schedule generated by scheduling algorithm
    cpu_schedule = {}
    # Stores the stats related to schedule like average waiting time
    stats = {}
    # Stores the individual per process stats
    details = {}

    # Prints the details of the process schedule and statistics
    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('cpu_output').layout
        layout.clear_widgets()

        formatted_data = []
        for i in range(data_cpu['num_processes']):
            process = {}
            process['name'] = data_cpu['name'+str(i)]
            process['arrival'] = int(data_cpu['arrival'+str(i)])
            process['burst'] = int(data_cpu['burst'+str(i)])
            if cpu_scheduling_type == 4 or cpu_scheduling_type == 5:
                process['priority'] = int(data_cpu['priority'+str(i)])
            formatted_data.append(process)
            self.colors[process['name']] = [random(), random(), random()]
        self.colors['Idle'] = [0.2, 0.2, 0.2]

        if cpu_scheduling_type == 0:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.fcfs(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 1:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.round_robin(formatted_data, data_cpu['quantum'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 2:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.shortest_job_non_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 3:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.shortest_job_prempted(formatted_data, dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 4:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.priority_non_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])
        elif cpu_scheduling_type == 5:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.priority_preemptive(formatted_data, data_cpu['aging'], dispatch_latency=data_cpu['dispatch_latency'])

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll
        grid.bind(minimum_height=grid.setter('height'))

        row_height = '30dp'

        # Display process schedule details
        for process in self.cpu_schedule:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='20dp')

            label_name = Label(text='[ref=click]'+process['name']+':[/ref]', markup=True)
            box.add_widget(label_name)
            label = Label(text=str(process['start']))
            box.add_widget(label)
            label = Label(text=str(process['end']))
            box.add_widget(label)

            # Add view details button for each process
            details_button = Button(text='Details', size_hint_x=None, width='100dp')
            box.add_widget(details_button)

            # Blank label for padding on right
            box.add_widget(Label(text='', size_hint_x=None, width='20dp'))

            # Popup showing details of process when box is clicked
            if process['name'] != 'Idle':
                content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                    "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                    "Turnaround time: "+str(self.details[process['name']]['turn_time']))
                content_label = Label(text=content_str)
                popup = Popup(title='Details of '+str(process['name']), content=content_label, size_hint=(None, None), size=(kivy.metrics.dp(200), kivy.metrics.dp(200)))
                label_name.bind(on_ref_press=popup.open)
                details_button.bind(on_release=popup.open)
                popup.open()
                popup.dismiss()
                print "Bound popup for process: "+str(label_name.text)

            grid.add_widget(box)

        # Display statistics
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=row_height)
        box.add_widget(Label(text='Statistics -'))
        grid.add_widget(box)

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

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_gantt(self, *args):
        # Area for drawing gantt chart
        gantt = self.manager.get_screen('cpu_output').gantt
        chart_wid = Widget()
        # Area for displaying time values
        time = self.manager.get_screen('cpu_output').time
        gantt.clear_widgets()
        time.clear_widgets()
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

# Input Screen for Deadlock Avoidance algorithm
class DeadlockAvoidanceInputScreen(Screen):
    form = ObjectProperty(None)
    request_form = ObjectProperty(None)
    def load_form(self, *args):
        form = self.manager.get_screen('da_form').form
        form.clear_widgets()
        if (self.num_processes.text == "" or int(self.num_processes.text) < 1):
            self.num_processes.text = "4"
        if (self.num_resource_types.text == "" or int(self.num_resource_types.text) < 1):
            self.num_resource_types.text = "4"

        # Number of processes
        n = int(self.num_processes.text)
        # Number of resource types
        m = int(self.num_resource_types.text)

        # Initialize the global data_da dictionary
        data_da['num_processes'] = n
        data_da['num_resource_types'] = m
        data_da['available'] = [5] * data_da['num_resource_types']
        data_da['request'] = [0] * data_da['num_resource_types']
        data_da['max'] = [[10 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]
        data_da['allocation'] = [[4 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # Add input fields for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(m):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(da_on_available, i=i))
            box.add_widget(inp)
        grid.add_widget(box)

        # Max Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Max:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # Add input fields for Max matrix (n x m)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='max'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_max, i=i, j=j))
                box.add_widget(inp)
            grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_allocation, i=i, j=j))
                box.add_widget(inp)
            grid.add_widget(box)

        # Add labels for resource types in request form:
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        box.add_widget(Label(text='Process No.'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # Add input fields for resource form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        inp = TextInput(id='process_id')
        inp.bind(text=da_request_on_process_id)
        box.add_widget(inp)
        for i in range(m):
            inp = TextInput(id='request'+str(i))
            inp.bind(text=partial(da_on_request, i=i))
            box.add_widget(inp)
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_da_output))
        form.add_widget(box)
        

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
        box.add_widget(Label(text="Banker's Algorithm: When a process requests a set of resources,\nthe system must determine whether granting the request will keep the system in a safe state."))
        grid.add_widget(box)

        # Check if the request can be granted or not
        grantable, message = deadlock.check_request(available, maximum, allocation, request, data_da['request_process'], data_da['num_processes'], data_da['num_resource_types'])

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

            safe, schedule = deadlock.is_safe(available, maximum, allocation, data_da['num_processes'], data_da['num_resource_types'])
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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_da_form))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_da_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'da_form'

# Input Screen for Deadlock Detection algorithm
class DeadlockDetectionInputScreen(Screen):
    form = ObjectProperty(None)
    def load_form(self, *args):
        form = self.manager.get_screen('dd_form').form
        form.clear_widgets()
        if (self.num_processes.text == "" or int(self.num_processes.text) < 1):
            self.num_processes.text = "4"
        if (self.num_resource_types.text == "" or int(self.num_resource_types.text) < 1):
            self.num_resource_types.text = "4"

        # Number of processes
        n = int(self.num_processes.text)
        # Number of resource types
        m = int(self.num_resource_types.text)

        # Initialize the global data_dd dictionary
        data_dd['num_processes'] = n
        data_dd['num_resource_types'] = m
        data_dd['available'] = [5] * data_dd['num_resource_types']
        data_dd['request'] = [[10 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]
        data_dd['allocation'] = [[4 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # Add input fields for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(m):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(dd_on_available, i=i))
            box.add_widget(inp)
        grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_allocation, i=i, j=j))
                box.add_widget(inp)
            grid.add_widget(box)

        # Request Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        grid.add_widget(box)

        # Add input fields for Request matrix (n x m)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='request'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_request, i=i, j=j))
                box.add_widget(inp)
            grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_dd_output))
        form.add_widget(box)

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
        deadlock_safe, schedule = deadlock.detect(available, allocation, request, data_dd['num_processes'], data_dd['num_resource_types'])

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
            box.add_widget(Label(text='Deadlock Detected. Deadlocked processes: '))
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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_dd_form))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_dd_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dd_form'

# Input screen for Contiguous Memory Allocation Strategies
class MemoryInputScreen(Screen):
    strategy_type = NumericProperty(None)
    form = ObjectProperty(None)

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        if text == 'First Fit':
            self.strategy_type = 0
        elif text == 'Best Fit':
            self.strategy_type = 1
        elif text == 'Worst Fit':
            self.strategy_type = 2
        data_mem['algo'] = self.strategy_type

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('mem_form').form
        form.clear_widgets()
        if (self.num_processes.text == "" or int(self.num_processes.text) < 1):
            self.num_processes.text = "4"
        if (self.mem_size.text == "" or int(self.mem_size.text) < 1):
            self.mem_size.text = "200"

        # Number of processes
        n = int(self.num_processes.text)
        # Memory size
        m = int(self.mem_size.text)

        # Initialize the global data_mem dictionary
        data_mem['algo'] = 0
        data_mem['num_processes'] = n
        data_mem['mem_size'] = m
        data_mem['size'] = [128] * n
        data_mem['arrival'] = [0] * n
        data_mem['burst'] = [10] * n

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Box for algo spinner
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=(kivy.metrics.dp(5),kivy.metrics.dp(20)))
        box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        algo_spinner = Spinner(
            text='Select an Algorithm',
            values=('First Fit', 'Best Fit', 'Worst Fit'))
        algo_spinner.bind(text=self.show_selected_value)
        box.add_widget(algo_spinner)
        grid.add_widget(box)

        # Add labels for input
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(5), 0))
        box.add_widget(Label(text='Process name'))
        box.add_widget(Label(text='Size (KB)'))
        box.add_widget(Label(text='Arrival time (ms)'))
        box.add_widget(Label(text='CPU-I/O burst time (ms)'))
        grid.add_widget(box)

        # Add inputs
        for i in range(data_mem['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(5), 0))

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
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_mem_output))
        form.add_widget(box)

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
    margin_bottom = kivy.metrics.dp(255)

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

        box.add_widget(Label(text=algo_desc))
        grid.add_widget(box)

        # Display each element of memroy chart timeline
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
            start_height = self.get_start_height(idx, len(self.memory_chart), kivy.metrics.dp(330))
            self.draw_memory_state(mem_box, size_box, start_height, temp_memory)
            self.draw_wait_queue(wait_box, status_box, wait_to_memory_box, start_height, temp_memory)

        # Add back button
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_mem_form))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
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
        label = Label(text='Memory State: ', size_hint_x=None, width=self.margin_left)
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

    # Called when num_frames input is changed
    def update_num_frames(self, *args):
        if not self.num_frames.text.isdigit():
            data_page['num_frames'] = 0
        else:
            data_page['num_frames'] = int(self.num_frames.text)

    # Binder function for number of processes input
    def bind_num_frames(self, *args):
        self.num_frames.bind(text=self.update_num_frames)

    def bind_widgets(self, *args):
        self.bind_num_frames()

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        if text == 'First In First Out':
            self.strategy_type = 0
        elif text == 'Optimal':
            self.strategy_type = 1
        elif text == 'Least Recently Used':
            self.strategy_type = 2
        elif text == 'Second Chance':
            self.strategy_type = 3
        elif text == 'Enhanced Second Chance':
            self.strategy_type = 4
        elif text == 'Least Frequently Used':
            self.strategy_type = 5
        elif text == 'Most Frequently Used':
            self.strategy_type = 6
        data_page['algo'] = self.strategy_type

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('page_form').form
        form.clear_widgets()

        if (self.num_frames.text == "" or int(self.num_frames.text) < 1):
            self.num_frames.text = "4"

        # Number of frames
        n = int(self.num_frames.text)

        # Initialize the global data_page dictionary
        data_page['algo'] = 0
        data_page['num_frames'] = n
        data_page['ref_str'] = ''

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Box for algo spinner
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=(kivy.metrics.dp(5),kivy.metrics.dp(20)))
        box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        algo_spinner = Spinner(
            text='Select an Algorithm',
            values=('First In First Out', 'Optimal', 'Least Recently Used', 'Second Chance', 'Enhanced Second Chance', 'Least Frequently Used', 'Most Frequently Used'))
        algo_spinner.bind(text=self.show_selected_value)
        box.add_widget(algo_spinner)
        grid.add_widget(box)
        
        # Add labels for input
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(5), 0))
        box.add_widget(Label(text='Reference String'))
        grid.add_widget(box)


        # Add inputs
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(200), 0))
        inp = TextInput(id='ref_str'+str(0))
        inp.bind(text=page_on_ref)
        box.add_widget(inp)
        grid.add_widget(box)

        
        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_page_output))
        form.add_widget(box)

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_to_page_output(self, *args):
        if (data_page['num_frames'] == 0):
            print "Invalid number of frames. Enter valid input."
            return
        self.manager.transition.direction = 'left'
        self.manager.current = 'page_output'
    
# Output screen for Page Replacement Algorithms
class PageOutputScreen(Screen):
    
   # Stores the memory chart generated by algorithm
    memory_chart = []

    # Margins for memory chart output
    margin_left = kivy.metrics.dp(125)
    margin_bottom = kivy.metrics.dp(255)

    # Increment in width per unit size
    inc = 0

    def get_description(self, *args):
        if data_page['algo'] == 0:
            return 'FIFO: First In First Out'
        elif data_page['algo'] == 1:
            return 'Optimal Page Replacement'
        else:
            return 'TBA'

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

        self.memory_chart = page_replacement.page_replacement(formatted_data)

        layout = self.manager.get_screen('page_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Output the algo description
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        algo_desc = self.get_description()
        
        box.add_widget(Label(text=algo_desc))
        grid.add_widget(box)

        # To add frame labels
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        grid.add_widget(box)
        frames_label = Label(text='', size_hint_x=None, width=self.margin_left+kivy.metrics.dp(100), valign='middle', halign='right')
        frames_label.text_size = frames_label.size
        box.add_widget(frames_label)

        for i in range(formatted_data['num_frames']):
            frames_label = Label(text='Frame' + str(i+1), size_hint_x=None, width=self.margin_left, valign='middle', halign='right')
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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        box.add_widget(Button(text='Back', on_release=self.switch_to_page_form))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
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
        mem_label = Label(text='Memory State: ', size_hint_x=None, width=self.margin_left + kivy.metrics.dp(35), valign='middle', halign='left')
        mem_label.text_size = mem_label.size
        mem_box.add_widget(mem_label)

        for idx, state in enumerate(memory_state):
            if state == -1:
                state = 'X'
            if allocated_frame - 1 == idx and page_fault == 1:
                mem_label = ColoredBorderedLabel(text='[b][color=ff0b3c]'+str(state)+'[/color][/b]', markup=True, size_hint_x=None, width=self.margin_left, valign='middle', halign='center')
            else:
                mem_label = WhiteBorderedLabel(text=str(state), size_hint_x=None, width=self.margin_left, valign='middle', halign='center')

            mem_label.text_size = mem_label.size
            mem_box.add_widget(mem_label)

        # To add page fault (Y/N)
        page_f_label = Label(text='', size_hint_x=None, width=self.margin_left - kivy.metrics.dp(25), valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        page_f_label = Label(text='Page Fault: ', size_hint_x=None, width=self.margin_left, valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        if page_fault == 1:
            page_f_label = Label(text='[color=ff0b3c]Yes[/color]', markup=True, size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
        else:
            page_f_label = Label(text='No', markup=True, size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

    def switch_to_page_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'page_form'

# Create the screen manager and add all screens to it
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUInputScreen(name='cpu_form'))
sm.add_widget(CPUOutputScreen(name='cpu_output'))
sm.add_widget(DeadlockAvoidanceInputScreen(name='da_form'))
sm.add_widget(DeadlockAvoidanceOutputScreen(name='da_output'))
sm.add_widget(DeadlockDetectionInputScreen(name='dd_form'))
sm.add_widget(DeadlockDetectionOutputScreen(name='dd_output'))
sm.add_widget(MemoryInputScreen(name='mem_form'))
sm.add_widget(MemoryOutputScreen(name='mem_output'))
sm.add_widget(PageInputScreen(name='page_form'))
sm.add_widget(PageOutputScreen(name='page_output'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()
