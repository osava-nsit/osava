# kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line
# python libraries
from functools import partial
from random import random
# algorithms
import cpu_scheduling

Builder.load_file('layout.kv')
cpu_scheduling_types = ['FCFS', 'Round Robin', 'SJF Non-Preemptive', 'SJF Preemptive', 'Priority Non-Preemptive', 'Priority Preemptive']
cpu_scheduling_type = 0
data_cpu = {}

def on_name(instace, value, i):
    if value == '':
        value = 'P'+str(i+1)
    data_cpu['name'+str(i)] = value

def on_arrival(instace, value, i):
    if value == '':
        value = 1
    data_cpu['arrival'+str(i)] = value

def on_burst(instace, value, i):
    if value == '':
        value = 4
    data_cpu['burst'+str(i)] = value

def on_priority(instace, value, i):
    if value == '':
        value = 0
    data_cpu['priority'+str(i)] = value

def on_quantum(instace, value):
    if value == '':
        value = 2
    data_cpu['quantum'] = int(value)

def on_aging(instace, value):
    if value == '':
        value = 4
    data_cpu['aging'] = int(value)

class MainMenuScreen(Screen):
    pass

class CPUSchedulingScreen(Screen):
    num_processes = ObjectProperty(None)
    cpu_type = 0
    # Load the form for input
    # def load_form(self, *args):
    #     global cpu_scheduling_type;
    #     cpu_scheduling_type = self.cpu_type
    #     cpu_scheduling_type_text = cpu_scheduling_types[self.cpu_type]
    #     type_text = self.manager.get_screen('cpu2').type_text
    #     type_text.clear_widgets()
    #     label = Label(text=str(cpu_scheduling_type_text)+' CPU Scheduling')
    #     type_text.add_widget(label)

    #     layout = self.manager.get_screen('cpu2').layout
    #     layout.clear_widgets()
    #     if (self.num_processes.text == "" or int(self.num_processes.text) == 0):
    #         self.num_processes.text = "5"
    #     data_cpu['num_processes'] = int(self.num_processes.text)

    #     for i in range(int(self.num_processes.text)):
    #         box = BoxLayout(orientation='horizontal')
    #         sno_label = Label(text=str(i+1))
    #         box.add_widget(sno_label)

    #         # process names
    #         inp = TextInput(id='name'+str(i))
    #         inp.bind(text=partial(on_name, i=i))
    #         box.add_widget(inp)
    #         # arrival times
    #         inp = TextInput(id='arrival'+str(i))
    #         inp.bind(text=partial(on_arrival, i=i))
    #         box.add_widget(inp)
    #         # burst times
    #         inp = TextInput(id='burst'+str(i))
    #         inp.bind(text=partial(on_burst, i=i))
    #         box.add_widget(inp)

    #         layout.add_widget(box)
    #     if self.cpu_type == 1:
    #         box = BoxLayout(orientation='horizontal')
    #         inp = TextInput(id='quantum')
    #         inp.bind(text=on_quantum)
    #         label = Label(text='Time quantum')
    #         box.add_widget(label)
    #         box.add_widget(inp)
    #         layout.add_widget(box)

class CPUInputScreen_old(Screen):
    def show_data(self, *args):
        print str(data_cpu)

class CPUInputScreen(Screen):
    layout = ObjectProperty(None)
    cpu_type = 0
    preemptive_flag = False
    def bind_height(self, *args):
        layout = self.manager.get_screen('cpu_form').layout
        self.layout.bind(minimum_height=self.layout.setter('height'))

    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('cpu_form').algo_spinner
        spinner.bind(text=self.show_selected_value)

    def show_selected_value(self, spinner, text, *args):
        if text == 'First Come First Serve':
            self.set_cpu_type(0)
        elif text == 'Shortest Job First':
            self.set_cpu_type(2)
        elif text == 'Priority':
            self.set_cpu_type(4)
        elif text == 'Round Robin':
            self.set_cpu_type(1)

    # Called when a new value is chosen from spinner
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

    # Called when preemptive or non-preemtive option is clicked
    def update_cpu_type(self, *args):
        global cpu_scheduling_type
        # If FCFS or RR
        if self.cpu_type == 0 or self.cpu_type == 1:
            pass
        elif self.preemptive_flag == True and self.cpu_type%2 == 0:
            self.cpu_type += 1
            cpu_scheduling_type = self.cpu_type
        elif self.preemptive_flag == False and self.cpu_type%2 != 0:
            self.cpu_type -= 1
            cpu_scheduling_type = self.cpu_type
        # print 'updated cpu_type:', self.cpu_type

    def load_form(self, *args):
        # cpu_scheduling_type_text = cpu_scheduling_types[self.cpu_type]
        # type_text = self.manager.get_screen('cpu2').type_text
        # type_text.clear_widgets()
        #label = Label(text=str(cpu_scheduling_type_text)+' CPU Scheduling')
        #type_text.add_widget(label)

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
            inp.bind(text=partial(on_name, i=i))
            # inp.font_size = inp.size[1]
            box.add_widget(inp)
            # arrival times
            inp = TextInput(id='arrival'+str(i))
            inp.bind(text=partial(on_arrival, i=i))
            # inp.font_size = inp.size[1]
            box.add_widget(inp)
            # burst times
            inp = TextInput(id='burst'+str(i))
            inp.bind(text=partial(on_burst, i=i))
            # inp.font_size = inp.size[1]
            box.add_widget(inp)

            # If Priority scheduling selected
            if self.cpu_type == 4 or self.cpu_type == 5:
                inp = TextInput(id='priority'+str(i))
                inp.bind(text=partial(on_priority, i=i))
                box.add_widget(inp)

            layout.add_widget(box)

        # If Round Robin scheduling selected
        if self.cpu_type == 1:
            box = BoxLayout(orientation='horizontal', padding=(50,0))
            inp = TextInput(id='quantum')
            inp.bind(text=on_quantum)
            # inp.font_size = inp.size[1]
            label = Label(text='Time quantum')
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)
        # If Priority scheduling selected
        elif self.cpu_type == 4 or self.cpu_type == 5:
            box = BoxLayout(orientation='horizontal', padding=(50,0))
            inp = TextInput(id='aging')
            inp.bind(text=on_aging)
            # inp.font_size = inp.size[1]
            label = Label(text='Aging - Promote priority by 1 unit after time: ')
            # label.text_size = label.size
            box.add_widget(label)
            box.add_widget(inp)
            layout.add_widget(box)

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
            self.cpu_schedule, self.stats = cpu_scheduling.fcfs(formatted_data)
        elif cpu_scheduling_type == 1:
            self.cpu_schedule, self.stats = cpu_scheduling.round_robin(formatted_data, data_cpu['quantum'])
        elif cpu_scheduling_type == 2:
            self.cpu_schedule, self.stats = cpu_scheduling.shortest_job_non_prempted(formatted_data)
        elif cpu_scheduling_type == 3:
            self.cpu_schedule, self.stats = cpu_scheduling.shortest_job_prempted(formatted_data)
        elif cpu_scheduling_type == 4:
            self.cpu_schedule, self.stats = cpu_scheduling.priority_non_preemptive(formatted_data, data_cpu['aging'])
        elif cpu_scheduling_type == 5:
            self.cpu_schedule, self.stats = cpu_scheduling.priority_preemptive(formatted_data, data_cpu['aging'])

        # Display process schedule details
        for process in self.cpu_schedule:
            box = BoxLayout(orientation='horizontal')
            label = Label(text=process['name']+':')
            box.add_widget(label)
            label = Label(text=str(process['start']))
            box.add_widget(label)
            label = Label(text=str(process['end']))
            box.add_widget(label)
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
        margin_left = 400
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

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUInputScreen(name='cpu_form'))
sm.add_widget(CPUSchedulingScreen(name='cpu1'))
sm.add_widget(CPUInputScreen_old(name='cpu2'))
sm.add_widget(CPUOutputScreen(name='cpu_output'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()
