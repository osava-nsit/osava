from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
 
 
kv = '''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 50
        Button:
            text: 'previous'
            on_press:
                manager.current = manager.previous()
        Button:
            text: 'next'
            on_press:
                manager.current = manager.next()

    ScreenManager:
        id: manager

        Screen:
            name: '1'
            FloatLayout:
                Label:
                    text: 'screen 1'
                    size_hint: None, None
                    size: self.texture_size
                    pos_hint: {'center_x': .5, 'top': .8}

                Label:
                    text: 'button in screen 2 is %s' % button.state

        Screen:
            name: '2'
            BoxLayout:
                Label:
                    text: 'hey, this is screen 2'
                ToggleButton:
                    id: button
                    text: 'switch me'

        Screen:
            name: '3'
            TextInput:
                text: app.data
                on_text: app.data = self.text

        Screen:
            name: '4'
            Label:
                text: app.data
'''
 
 
class MyApp(App):
    data = StringProperty('initial text')
 
    def build(self):
        self.bind(data=self.do_something)
        return Builder.load_string(kv)
 
    def do_something(self, *args):
        print 'do_something got called because text changed'
 
 
MyApp().run()