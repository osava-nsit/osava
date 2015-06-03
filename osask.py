from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class MainMenuScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.rows = 5

class OSASK(App):
    def build(self):
        return MainMenuScreen()

if __name__ == '__main__':
    OSASK().run()