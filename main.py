# Kivy libraries
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import kivy.metrics
# OSAVA screens
from screens import *
# Common constants and methods
from common import *

Builder.load_file('layout.kv')

# Main Menu Screen with options to choose an OS Algorithm
class MainMenuScreen(Screen):
    module_button_height = kivy.metrics.dp(42)
    about_visible = False

    def toggle_about_text(self, *args):
        if self.about_visible:
            self.about_label.text = ""
            self.about_visible = False
        else:
            self.about_label.text = 'Developers: Udit Arora, Namrata Mukhija, Priyanka, Rohit Takhar\nAdvisor: Dr. Pinaki Chakraborty\n'
            self.about_visible = True

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
sm.add_widget(DiskInputScreen(name='disk_form'))
sm.add_widget(DiskOutputScreen(name='disk_output'))

# Dictionary to store which screen to navigate to when back button is pressed in android
back_screen = {
    'menu': False,
    'cpu_form': 'menu',
    'cpu_output': 'cpu_form',
    'da_form': 'menu',
    'da_output': 'da_form',
    'dd_form': 'menu',
    'dd_output': 'dd_form',
    'mem_form': 'menu',
    'mem_output': 'mem_form',
    'page_form': 'menu',
    'page_output': 'page_form',
    'disk_form': 'menu',
    'disk_output': 'disk_form'
}

class OSAVA(App):
    def build(self):
        Window.bind(on_keyboard=self.handle_key)
        return sm

    def handle_key(self, window, key, *args):
        if key == 27: # Escape in desktop and back button in android
            if sm.current != 'menu':
                sm.transition.direction = 'right'
                sm.current = back_screen[sm.current]
                return True

if __name__ == '__main__':
    OSAVA().run()
