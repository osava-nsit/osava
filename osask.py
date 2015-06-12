# kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.graphics import Color, Rectangle, Line
# python libraries
from functools import partial
# algorithms
import cpu_scheduling

Builder.load_file('osask.kv')
cpu_scheduling_type = 'FCFS'
data_cpu = {}

def on_name(instace, value, i):
    if value == '':
        value = 'a'
    data_cpu['name'+str(i)] = value

def on_arrival(instace, value, i):
    if value == '':
        value = 1
    data_cpu['arrival'+str(i)] = value

def on_burst(instace, value, i):
    if value == '':
        value = 1
    data_cpu['burst'+str(i)] = value

class MainMenuScreen(Screen):
    pass

class CPUSchedulingScreen(Screen):
    num_processes = ObjectProperty(None)
    cpu_type = ''
    # Load the form for input
    def load_form(self, *args):
        cpu_scheduling_type = self.cpu_type
        type_text = self.manager.get_screen('cpu2').type_text
        type_text.clear_widgets()
        label = Label(text=str(self.cpu_type)+' CPU Scheduling')
        type_text.add_widget(label)

        layout = self.manager.get_screen('cpu2').layout
        layout.clear_widgets()
        if (self.num_processes.text == "" or int(self.num_processes.text) == 0):
            self.num_processes.text = "1"
        data_cpu['num_processes'] = int(self.num_processes.text)
        for i in range(int(self.num_processes.text)):
            box = BoxLayout(orientation='horizontal')
            sno_label = Label(text=str(i+1))
            box.add_widget(sno_label)

            # process names
            inp = TextInput(id='name'+str(i))
            inp.bind(text=partial(on_name, i=i))
            box.add_widget(inp)
            # arrival times
            inp = TextInput(id='arrival'+str(i))
            inp.bind(text=partial(on_arrival, i=i))
            box.add_widget(inp)
            # burst times
            inp = TextInput(id='burst'+str(i))
            inp.bind(text=partial(on_burst, i=i))
            box.add_widget(inp)

            layout.add_widget(box)

class CPUInputScreen(Screen):
    def show_data(self, *args):
        print str(data_cpu)

    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('cpu3').layout
        layout.clear_widgets()

        formatted_data = []
        for i in range(data_cpu['num_processes']):
            process = {}
            process['name'] = data_cpu['name'+str(i)]
            process['arrival'] = int(data_cpu['arrival'+str(i)])
            process['burst'] = int(data_cpu['burst'+str(i)])
            formatted_data.append(process)
        schedule = cpu_scheduling.fcfs(formatted_data)
        # print str(schedule)
        curr_time = 0
        wait_time = 0
        turn_time = 0
        sum_time = 0
        for process in schedule:
            box = BoxLayout(orientation='horizontal')
            if (process['arrival'] > curr_time):
                curr_time = process['arrival']

            label = Label(text=process['name']+':')
            box.add_widget(label)

            label = Label(text=str(curr_time))
            box.add_widget(label)

            label = Label(text=str(curr_time+process['burst']))
            box.add_widget(label)

            wait_time += (curr_time - process['arrival'])
            curr_time += process['burst']
            turn_time += (curr_time - process['arrival'])
            sum_time += process['burst']
            layout.add_widget(box)

        label = Label(text='Average waiting time: ' + str(float(wait_time)/data_cpu['num_processes']))
        layout.add_widget(label)
        label = Label(text='Average turnaround time: ' + str(float(turn_time)/data_cpu['num_processes']))
        layout.add_widget(label)
        label = Label(text='Throughput: ' + str(float(data_cpu['num_processes']*1000)/curr_time))
        layout.add_widget(label)
        label = Label(text='CPU Utilization: ' + str(float(sum_time*100)/curr_time) + ' %')
        layout.add_widget(label)

        # Draw Gantt Chart
        gantt = self.manager.get_screen('cpu3').gantt
        with gantt.canvas:
           # draw a line using the default color
           Line(points=(0, 0, 50, 100, 100, 200))

           # lets draw a semi-transparent red square
           # Color(1, 0, 0, .5, mode='rgba')
           Rectangle(pos=gantt.pos, size=(100, 200))

class CPUOutputScreen(Screen):
    layout = ObjectProperty(None)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUSchedulingScreen(name='cpu1'))
sm.add_widget(CPUInputScreen(name='cpu2'))
sm.add_widget(CPUOutputScreen(name='cpu3'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()