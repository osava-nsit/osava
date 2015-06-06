from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('osask.kv')

class MainMenuScreen(Screen):
    pass

class CPUSchedulingInputScreen(Screen):
	pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainMenuScreen(name='menu'))
sm.add_widget(CPUSchedulingInputScreen(name='cpu1'))

class OSASK(App):
    def build(self):
        return sm

if __name__ == '__main__':
    OSASK().run()