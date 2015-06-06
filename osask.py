# kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
# python libraries
from functools import partial
# algorithms
import cpu_scheduling

Builder.load_file('osask.kv')
data_cpu = {}

def on_name(instace, value, i):
    data_cpu['name'+str(i)] = value

def on_arrival(instace, value, i):
    data_cpu['arrival'+str(i)] = value

def on_burst(instace, value, i):
    data_cpu['burst'+str(i)] = value

class MainMenuScreen(Screen):
    pass

class CPUSchedulingScreen(Screen):
    num_processes = ObjectProperty(None)

    # Load the form for input
    def load_form(self, *args):
        layout = self.manager.get_screen('fcfs1').layout
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

class FCFSInputScreen(Screen):
    def show_data(self, *args):
        print str(data_cpu)

    def calculate_schedule(self, *args):
        layout = self.manager.get_screen('fcfs2').layout
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

class FCFSOutputScreen(Screen):
    layout = ObjectProperty(None)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUSchedulingScreen(name='cpu1'))
sm.add_widget(FCFSInputScreen(name='fcfs1'))
sm.add_widget(FCFSOutputScreen(name='fcfs2'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()