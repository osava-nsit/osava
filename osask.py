# Kivy libraries
from kivy.app import App
from kivy.lang import Builder
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
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line
# Python libraries
from functools import partial
from random import random
import copy
# OS Algorithms
import cpu_scheduling, deadlock

Builder.load_file('layout.kv')

# Global data for CPU Scheduling Algorithms
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive']
cpu_scheduling_type = 0
data_cpu = dict()

# Global data for Deadlock Avoidance Algorithm
data_da = dict()

# Global data for Deadlock Detection Algorithm
data_dd = dict()

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


# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):
    def load_ribbon(self, *args):
        title = self.manager.get_screen('menu').title
        with title.canvas:
            Color(1, 0, 0, 0.4, mode='rgba')
            Rectangle(pos=(0,1100), size=(1600,100))
        # title.add_widget(Label(text='OS - Algo Visualization App'))

# Input Screen for CPU Scheduling Algorithms with partial scrolling
# class CPUInputScreen(Screen):
#     layout = ObjectProperty(None)
#     layout_form = ObjectProperty(None)
#     cpu_type = 0
#     preemptive_flag = False

#     def bind_height(self, *args):
#         #layout = self.manager.get_screen('cpu_form').layout
#         #self.layout.bind(minimum_height=self.layout.setter('height'))
#         return

#     # Binder function for algorithm type selection from Spinner (Dropdown)
#     def bind_spinner(self, *args):
#         spinner = self.manager.get_screen('cpu_form').algo_spinner
#         spinner.bind(text=self.show_selected_value)
#         variant_spinner = self.manager.get_screen('cpu_form').variant_spinner
#         variant_spinner.bind(text=self.show_variant)

#     # Call set_cpu_type method with appropriate index of scheduling algorithm
#     def show_selected_value(self, spinner, text, *args):
#         if text == 'First Come First Serve':
#             self.set_cpu_type(0)
#         elif text == 'Shortest Job First':
#             self.set_cpu_type(2)
#         elif text == 'Priority':
#             self.set_cpu_type(4)
#         elif text == 'Round Robin':
#             self.set_cpu_type(1)

#     def show_variant(self, spinner, text, *args):
#         if text == 'Preemptive':
#             self.preemptive_flag = True
#             self.update_cpu_type(True)
#         elif text == 'Non-Preemptive':
#             self.preemptive_flag = False
#             self.update_cpu_type(False)

#     # Called when a new value is chosen from spinner. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
#     def set_cpu_type(self, new_cpu_type, *args):
#         global cpu_scheduling_type
#         cpu_scheduling_type = new_cpu_type
#         self.cpu_type = new_cpu_type
#         # variant_spinner = self.manager.get_screen('cpu_form').variant_spinner
#         # If FCFS or RR
#         if new_cpu_type == 0 or new_cpu_type == 1:
#             cpu_scheduling_type = new_cpu_type
#             self.cpu_type = new_cpu_type
#             # variant_spinner.disabled = True
#         elif self.preemptive_flag == True and new_cpu_type%2 == 0:
#             new_cpu_type += 1
#             cpu_scheduling_type = new_cpu_type
#             self.cpu_type = new_cpu_type
#             # variant_spinner.disabled = False
#         elif self.preemptive_flag == False and new_cpu_type%2 != 0:
#             new_cpu_type -= 1
#             cpu_scheduling_type = new_cpu_type
#             self.cpu_type = new_cpu_type
#             # variant_spinner.disabled = False
#         self.load_form()

#     # Called when preemptive or non-preemtive option is clicked. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
#     def update_cpu_type(self, *args):
#         global cpu_scheduling_type
#         # If FCFS or RR Scheduling
#         if self.cpu_type == 0 or self.cpu_type == 1:
#             pass
#         elif self.preemptive_flag == True and self.cpu_type%2 == 0:
#             self.cpu_type += 1
#             cpu_scheduling_type = self.cpu_type
#         elif self.preemptive_flag == False and self.cpu_type%2 != 0:
#             self.cpu_type -= 1
#             cpu_scheduling_type = self.cpu_type

#     # Load the appropriate form inputs according to the CPU Scheduling algorithm selected
#     def load_form(self, *args):
#         # Layout is the area where the form is placed on the screen
#         layout_form = self.manager.get_screen('cpu_form').layout_form
#         layout_form.clear_widgets()
#         if (self.num_processes.text == "" or int(self.num_processes.text) == 0):
#             self.num_processes.text = "5"
#         data_cpu['num_processes'] = int(self.num_processes.text)

#         layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
#         # Make sure the height is such that there is something to scroll.
#         layout.bind(minimum_height=layout.setter('height'))

#         # Fixed height of form rows within scroll view
#         form_row_height = '40dp'

#         # Add input labels
#         box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
#         # label = Label(text='Sno.')
#         # box.add_widget(label)
#         label = Label(text='Process name')
#         box.add_widget(label)
#         label = Label(text='Arrival time (ms)')
#         box.add_widget(label)
#         label = Label(text='CPU burst time (ms)')
#         box.add_widget(label)

#         # If Priority scheduling selected
#         if self.cpu_type == 4 or self.cpu_type == 5:
#             label = Label(text='Priority (0 being highest)')
#             box.add_widget(label)

#         layout.add_widget(box)

#         for i in range(int(self.num_processes.text)):
#             box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)

#             # sno_label = Label(text=str(i+1))
#             # box.add_widget(sno_label)

#             # process names
#             # inp = TextInput(id='name'+str(i))
#             # inp.bind(text=partial(cpu_on_name, i=i))
#             # box.add_widget(inp)
#             # Fixed process names
#             pname = Label(text='P'+str(i+1))
#             box.add_widget(pname)
#             data_cpu['name'+str(i)] = 'P'+str(i+1)

#             # arrival times
#             inp = TextInput(id='arrival'+str(i))
#             inp.bind(text=partial(cpu_on_arrival, i=i))
#             box.add_widget(inp)
#             # burst times
#             inp = TextInput(id='burst'+str(i))
#             inp.bind(text=partial(cpu_on_burst, i=i))
#             box.add_widget(inp)

#             # If Priority scheduling selected
#             if self.cpu_type == 4 or self.cpu_type == 5:
#                 inp = TextInput(id='priority'+str(i))
#                 inp.bind(text=partial(cpu_on_priority, i=i))
#                 box.add_widget(inp)

#             layout.add_widget(box)

#         # If Round Robin scheduling selected
#         if self.cpu_type == 1:
#             box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)
#             inp = TextInput(id='quantum')
#             inp.bind(text=cpu_on_quantum)
#             # inp.font_size = inp.size[1]
#             label = Label(text='Time quantum (ms)')
#             box.add_widget(label)
#             box.add_widget(inp)
#             layout.add_widget(box)
#         # If Priority scheduling selected
#         elif self.cpu_type == 4 or self.cpu_type == 5:
#             box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)
#             inp = TextInput(id='aging', size_hint_x=0.3)
#             inp.bind(text=cpu_on_aging)
#             # inp.font_size = inp.size[1]
#             label = Label(text='Aging: Promote priority by 1 unit each time after waiting (ms) - ', size_hint_x=0.7)
#             # label.text_size = label.size
#             box.add_widget(label)
#             box.add_widget(inp)
#             layout.add_widget(box)

#         # Add Visualize and back button at the end of form
#         box = BoxLayout(orientation='horizontal', padding=(0, 10), size_hint_y=None, height='50dp')
#         box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
#         box.add_widget(Button(text='Visualize', on_release=self.switch_to_cpu_output))
#         layout.add_widget(box)

#         # Add ScrollView
#         # sv = ScrollView(size_hint=(None, None), size=(400, 400))
#         sv = ScrollView(size=self.size)
#         sv.add_widget(layout)
#         layout_form.add_widget(sv)
        

#     def switch_to_cpu_output(self, *args):
#         self.manager.transition.direction = 'left'
#         self.manager.current = 'cpu_output'

#     def switch_to_main_menu(self, *args):
#         self.manager.transition.direction = 'right'
#         self.manager.current = 'menu'

# Input Screen 2 for CPU Scheduling Algorithms
class CPUInputScreen2(Screen):
    layout_fixed = ObjectProperty(None)
    layout_form = ObjectProperty(None)
    layout = ObjectProperty(None)
    cpu_type = NumericProperty(None)
    preemptive_flag = False
    sv = ScrollView()
    num_processes = NumericProperty(None)

    # Update num_process when text is entered in the text input
    # Figure out the parameters required for this
    def update_num_processes(self, instance, value, *args):
        if value == '':
            value = 5
        self.num_processes = int(value)
        # self.load_form()

    def load_layout(self, *args):
        self.num_processes = 5
        if 'num_processes' not in data_cpu:
            data_cpu['num_processes'] = 5
        layout_fixed = self.manager.get_screen('cpu_form').layout_fixed
        layout_fixed.clear_widgets()
        self.sv = ScrollView(size=self.size)
        self.layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        self.layout.bind(minimum_height=self.layout.setter('height'))
        
        # Box for number of processes input
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        box.add_widget(Label(id='num_processes', text='Number of process: '))
        inp = TextInput(multiline=False, text=str(data_cpu['num_processes']))
        inp.bind(text=self.update_num_processes)
        box.add_widget(inp)
        box.add_widget(Button(text='Load Form', halign='center', valign='middle', on_release=self.load_form))
        self.layout.add_widget(box)

        self.layout.add_widget(Label(text='Information about the scheduling algorithm -', size_hint_y=None, height='60dp', padding=(20,40), halign='left'))

        # Box for algo spinner
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='80dp', padding=(10,40))
        box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        algo_spinner = Spinner(
            text='Select an Algorithm',
            values=('First Come First Serve', 'Shortest Job First', 'Priority', 'Round Robin', 'Multilevel Queue', 'Multilevel Feedback Queue'))
        algo_spinner.bind(text=self.show_selected_value)
        box.add_widget(algo_spinner)
        self.layout.add_widget(box)

        # Box for variant spinner
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='80dp', padding=(10,40))
        box.add_widget(Label(text='Variant - ', padding=(10,10), size_hint_x=0.3))
        variant_spinner = Spinner(
            text='-',
            values=('Preemptive', 'Non-Preemptive'))
        variant_spinner.bind(text=self.show_selected_value)
        box.add_widget(variant_spinner)
        self.layout.add_widget(box)

        # Adding box for rest of the form
        # self.layout_form = BoxLayout(orientation='vertical', height='1000dp')
        # self.layout_form.add_widget(Label(text='Lets do this!'))
        # self.layout.add_widget(self.layout_form)

        self.sv.add_widget(self.layout)
        layout_fixed.add_widget(self.sv)

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
            new_cpu_type += 1
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
        self.layout.clear_widgets()
        data_cpu['num_processes'] = self.num_processes
        self.load_layout()
        self.num_processes = data_cpu['num_processes']

        # Fixed height of form rows within scroll view
        form_row_height = '40dp'

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

        self.layout.add_widget(box)

        for i in range(data_cpu['num_processes']):
            box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)
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

            self.layout.add_widget(box)

        # If Round Robin scheduling selected
        if self.cpu_type == 1:
            box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)
            inp = TextInput(id='quantum')
            inp.bind(text=cpu_on_quantum)
            # inp.font_size = inp.size[1]
            label = Label(text='Time quantum (ms)')
            box.add_widget(label)
            box.add_widget(inp)
            self.layout.add_widget(box)
        # If Priority scheduling selected
        elif self.cpu_type == 4 or self.cpu_type == 5:
            box = BoxLayout(orientation='horizontal', padding=(50,0), size_hint_y=None, height=form_row_height)
            inp = TextInput(id='aging', size_hint_x=0.3)
            inp.bind(text=cpu_on_aging)
            # inp.font_size = inp.size[1]
            label = Label(text='Aging: Promote priority by 1 unit each time after waiting (ms) - ', size_hint_x=0.7)
            # label.text_size = label.size
            box.add_widget(label)
            box.add_widget(inp)
            self.layout.add_widget(box)

        # Add Visualize and back button at the end of form
        box = BoxLayout(orientation='horizontal', padding=(0, 10), size_hint_y=None, height='50dp')
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_cpu_output))
        self.layout.add_widget(box)        

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
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.fcfs(formatted_data)
        elif cpu_scheduling_type == 1:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.round_robin(formatted_data, data_cpu['quantum'])
        elif cpu_scheduling_type == 2:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.shortest_job_non_prempted(formatted_data)
        elif cpu_scheduling_type == 3:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.shortest_job_prempted(formatted_data)
        elif cpu_scheduling_type == 4:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.priority_non_preemptive(formatted_data, data_cpu['aging'])
        elif cpu_scheduling_type == 5:
            self.cpu_schedule, self.stats, self.details = cpu_scheduling.priority_preemptive(formatted_data, data_cpu['aging'])

        # Display process schedule details
        for process in self.cpu_schedule:
            box = BoxLayout(orientation='horizontal')
            label_name = Label(text='[ref=click]'+process['name']+':[/ref]', markup=True)
            box.add_widget(label_name)
            label = Label(text=str(process['start']))
            box.add_widget(label)
            label = Label(text=str(process['end']))
            box.add_widget(label)

            # Popup showing details of process when box is clicked
            if process['name'] != 'Idle':
                content_str = ("Wait time: "+str(self.details[process['name']]['wait_time'])+"\n"+
                    "Response time: "+str(self.details[process['name']]['resp_time'])+"\n"+
                    "Turnaround time: "+str(self.details[process['name']]['turn_time']))
                content_label = Label(text=content_str)
                popup = Popup(title='Details of '+str(process['name']), content=content_label, size_hint=(None, None), size=(400, 400))
                label_name.bind(on_ref_press=popup.open)
                popup.open()
                popup.dismiss()

            layout.add_widget(box)

        # Display statistics
        label = Label(text='Average turnaround time: ' + str(int((self.stats['turn_time']*100)+0.5)/100.0))
        layout.add_widget(label)
        label = Label(text='Average waiting time: ' + str(int((self.stats['wait_time']*100)+0.5)/100.0))
        layout.add_widget(label)
        label = Label(text='Average response time: ' + str(int((self.stats['resp_time']*100)+0.5)/100.0))
        layout.add_widget(label)
        label = Label(text='Throughput: ' + str(int((self.stats['throughput']*100)+0.5)/100.0))
        layout.add_widget(label)
        label = Label(text='CPU Utilization: ' + str(int((self.stats['cpu_utilization']*100)+0.5)/100.0) + '%')
        layout.add_widget(label)

    def draw_gantt(self, *args):
        # Area for drawing gantt chart
        gantt = self.manager.get_screen('cpu_output').gantt
        chart_wid = Widget()
        # Area for displaying time values
        time = self.manager.get_screen('cpu_output').time
        gantt.clear_widgets()
        time.clear_widgets()
        # gantt.canvas.clear()
        margin_left = 250
        margin_bottom = 100
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

        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))
        # Fixed height of form rows within scroll view
        form_row_height = '40dp'

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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, 10))
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

        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))
        # Fixed height of form rows within scroll view
        form_row_height = '40dp'

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
            work = copy.deepcopy(available)
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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, 10))
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

        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))
        # Fixed height of form rows within scroll view
        form_row_height = '40dp'

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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, 10))
        box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        box.add_widget(Button(text='Visualize', on_release=self.switch_to_dd_output))
        form.add_widget(box)
        

    def switch_to_dd_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'dd_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

class DeadlockDetectionOutputScreen(Screen):
    def calculate(self, *args):
        available = data_dd['available']
        allocation = data_dd['allocation']
        request = data_dd['request']

        layout = self.manager.get_screen('dd_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))
        # Fixed height of form rows within scroll view
        form_row_height = '40dp'

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        box.add_widget(Label(text='Deadlock Detection Algorithm: This algorithm examines the state\nof the system and determines whether a deadlock has occurred.'))
        grid.add_widget(box)

        # Check if the system is deadlocked
        deadlock_safe, schedule = deadlock.detect(available, allocation, request, data_dd['num_processes'], data_dd['num_resource_types'])

        work = copy.deepcopy(available)
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
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, 10))
        box.add_widget(Button(text='Back', on_release=self.switch_to_dd_form))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size)
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_dd_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dd_form'

# Create the screen manager and add all screens to it
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUInputScreen2(name='cpu_form'))
sm.add_widget(CPUOutputScreen(name='cpu_output'))
sm.add_widget(DeadlockAvoidanceInputScreen(name='da_form'))
sm.add_widget(DeadlockAvoidanceOutputScreen(name='da_output'))
sm.add_widget(DeadlockDetectionInputScreen(name='dd_form'))
sm.add_widget(DeadlockDetectionOutputScreen(name='dd_output'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()
