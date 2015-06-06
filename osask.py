from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from functools import partial

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
        for i in range(int(self.num_processes.text)):
            box = BoxLayout(orientation='horizontal')
            sno_label = Label(text=str(i+1))
            box.add_widget(sno_label)

            inp = TextInput(id='name'+str(i))
            inp.bind(text=partial(on_name, i=i))
            box.add_widget(inp)

            inp = TextInput(id='arrival'+str(i))
            inp.bind(text=partial(on_arrival, i=i))
            box.add_widget(inp)

            inp = TextInput(id='burst'+str(i))
            inp.bind(text=partial(on_burst, i=i))
            box.add_widget(inp)

            layout.add_widget(box)

class FCFSInputScreen(Screen):
    layout = ObjectProperty(None)
    def show_data(self, *args):
        print str(data_cpu)

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUSchedulingScreen(name='cpu1'))
sm.add_widget(FCFSInputScreen(name='fcfs1'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()