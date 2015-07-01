# Kivy libraries
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line
# Python libraries
from functools import partial
from random import random
# OS Algorithms
import cpu_scheduling

Builder.load_file('layout.kv')

# Global data for CPU Scheduling agorithms
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive']
cpu_scheduling_type = 0
data_cpu = dict()

# Global data for Deadlock Avoidance algorithms
data_da = dict()

# Binder functions for CPU Scheduling algorithms form, to store data in the global 'data_cpu' dictionary
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
        value = 0
    data_cpu['priority'+str(i)] = value
def cpu_on_quantum(instace, value):
    if value == '':
        value = 2
    data_cpu['quantum'] = int(value)
def cpu_on_aging(instace, value):
    if value == '':
        value = 4
    data_cpu['aging'] = int(value)

# Binder functions for Dead Avoidance algorithm form
def da_on_available(instace, value, i):
    if (value == ''):
        value = 5
    data_da['available'+str(i)] = value
def da_on_request(instance, value, i):
    if (value == ''):
        value = 0
    data_da['request'+str(i)] = value
def da_on_max(instance, value, i, j):
    if (value == ''):
        value = 10
    if 'max' not in data_da:
        data_da['max'] = dict()
    if i not in data_da['max']:
        data_da['max'][i] = dict()
    data_da['max'][i][j] = value
def da_on_allocation(instance, value, i, j):
    if (value == ''):
        value = 10
    if 'allocation' not in data_da:
        data_da['allocation'] = dict()
    if i not in data_da['allocation']:
        data_da['allocation'][i] = dict()
    data_da['allocation'][i][j] = value

# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):
    pass

# Input Screen for CPU Scheduling Algorithms
class CPUInputScreen(Screen):
    layout = ObjectProperty(None)
    cpu_type = 0
    preemptive_flag = False
    def bind_height(self, *args):
        layout = self.manager.get_screen('cpu_form').layout
        self.layout.bind(minimum_height=self.layout.setter('height'))

    # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('cpu_form').algo_spinner
        spinner.bind(text=self.show_selected_value)

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

    # Called when a new value is chosen from spinner. Sets cpu_type to the appropriate index in the cpu_scheduling_types list
    def set_cpu_type(self, new_cpu_type, *args):
        global cpu_scheduling_type
        cpu_scheduling_type = new_cpu_type
        self.cpu_type = new_cpu_type
        # If FCFS or RR
        if new_cpu_type == 0 or new_cpu_type == 1:
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
        layout = self.manager.get_screen('cpu_form').layout
        layout.clear_widgets()
        if (self.num_processes.text == "" or int(self.num_processes.text) == 0):
            self.num_processes.text = "5"
        data_cpu['num_processes'] = int(self.num_processes.text)

        # Add input labels
        box = BoxLayout(orientation='horizontal')
        label = Label(text='Sno.')
        box.add_widget(label)
        label = Label(text='Process name')
        box.add_widget(label)
        label = Label(text='Arrival time (ms)')
        box.add_widget(label)
        label = Label(text='CPU burst time (ms)')
        box.add_widget(label)

        # If Priority scheduling selected
        if self.cpu_type == 4 or self.cpu_type == 5:
            label = Label(text='Priority (Highest = 0)')
            box.add_widget(label)

        layout.add_widget(box)

        for i in range(int(self.num_processes.text)):
            box = BoxLayout(orientation='horizontal', padding=(50,0))
            sno_label = Label(text=str(i+1))
            box.add_widget(sno_label)

            # process names
            inp = TextInput(id='name'+str(i))
            inp.bind(text=partial(cpu_on_name, i=i))
            box.add_widget(inp)
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
            box = BoxLayout(orientation='horizontal', padding=(50,0))
            inp = TextInput(id='quantum')
            inp.bind(text=cpu_on_quantum)
            # inp.font_size = inp.size[1]
            label = Label(text='Time quantum')
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)
        # If Priority scheduling selected
        elif self.cpu_type == 4 or self.cpu_type == 5:
            box = BoxLayout(orientation='horizontal', padding=(50,0))
            inp = TextInput(id='aging')
            inp.bind(text=cpu_on_aging)
            # inp.font_size = inp.size[1]
            label = Label(text='Aging - Promote priority by 1 unit after time: ')
            # label.text_size = label.size
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)

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
        label = Label(text='Average waiting time: ' + str(self.stats['wait_time']))
        layout.add_widget(label)
        label = Label(text='Average turnaround time: ' + str(self.stats['turn_time']))
        layout.add_widget(label)
        label = Label(text='Throughput: ' + str(self.stats['throughput']))
        layout.add_widget(label)
        label = Label(text='CPU Utilization: ' + str(self.stats['cpu_utilization'])+' %')
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
        if (self.num_resource_types.text == "" or int(self.num_resource_types) < 1):
            self.num_resource_types.text = "4"

        # Number of processes
        n = int(self.num_processes.text)
        # Number of resource types
        m = int(self.num_resource_types.text)

        # Add form labels for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        box.add_widget(Label(text='Available:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        form.add_widget(box)

        # Add input fields for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        box.add_widget(Label(text=''))
        for i in range(m):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(da_on_available, i=i))
            box.add_widget(inp)
        form.add_widget(box)

        # Max Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        box.add_widget(Label(text='Max:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        form.add_widget(box)

        # Add input fields for Max matrix (n x m)
        vert_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='max'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_max, i=i, j=j))
                box.add_widget(inp)
            vert_box.add_widget(box)
        form.add_widget(vert_box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        box.add_widget(Label(text='Allocation:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        form.add_widget(box)

        # Add input fields for Allocation matrix (n x m)
        vert_box = BoxLayout(orientation='vertical', size_hint_y=0.4)
        for i in range(n):
            box = BoxLayout(orientation='horizontal', size_hint_y=0.07)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(m):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_allocation, i=i, j=j))
                box.add_widget(inp)
            vert_box.add_widget(box)
        form.add_widget(vert_box)

        # Add labels for resource types in request form:
        request_form = self.manager.get_screen('da_form').request_form
        request_form.clear_widgets()
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='Request:'))
        for i in range(m):
            box.add_widget(Label(text=chr(ord('A')+i)))
        request_form.add_widget(box)

        # Add input fields for resource form
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text=''))
        for i in range(m):
            inp = TextInput(id='request'+str(i))
            inp.bind(text=partial(da_on_request, i=i))
            box.add_widget(inp)
        request_form.add_widget(box)

# Create the screen manager and add all screens to it
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUInputScreen(name='cpu_form'))
sm.add_widget(CPUOutputScreen(name='cpu_output'))
sm.add_widget(DeadlockAvoidanceInputScreen(name='da_form'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()
