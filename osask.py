from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

Builder.load_file('osask.kv')

class MainMenuScreen(Screen):
    pass

class CPUSchedulingScreen(Screen):
    num_processes = ObjectProperty(None)
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
            box.add_widget(inp)
            inp = TextInput(id='arrival'+str(i))
            box.add_widget(inp)
            inp = TextInput(id='burst'+str(i))
            box.add_widget(inp)
            layout.add_widget(box)
            # layout.add_widget(Button(text=str(i+1))) 

class FCFSInputScreen(Screen):
	layout = ObjectProperty(None)

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