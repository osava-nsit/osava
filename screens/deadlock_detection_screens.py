'''
This file contains the classes, functions and globals used for visualizing
Deadlock Detection algorithms
'''

# Kivy libraries
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import kivy.metrics
# Python libraries
from functools import partial
from copy import deepcopy
# OS Algorithms
from algos import deadlock
# OSAVA common constants and methods
from common import *

# Global data for Deadlock Detection Algorithm
data_dd = dict()

# Binder functions for Deadlock Detection Algorithm form
def dd_on_available(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 5
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_dd['available'][i] = int(value)

def dd_on_request(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 2
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_dd['request'][i][j] = int(value)

def dd_on_allocation(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_dd['allocation'][i][j] = int(value)

# Input Screen for Deadlock Detection algorithm
class DeadlockDetectionInputScreen(Screen):
    form = ObjectProperty(None)

    margin_right = '15dp'

    def bind_widgets(self, *args):
        self.bind_num_processes()
        self.bind_num_resource_types()

    # Binder function for number of processes input
    def bind_num_processes(self, *args):
        self.num_processes.bind(text=self.update_form)

    # Binder function for number of processes input
    def bind_num_resource_types(self, *args):
        self.num_resource_types.bind(text=self.update_form)

    # Called when the number of processes or number of resources input is changed
    # (Wrapper function to allow for condition checking if required)
    def update_form(self, *args):
        if (self.num_processes.text == ""):
            data_dd['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_dd['num_processes'] = 0
        else:
            data_dd['num_processes'] = int(self.num_processes.text)

        if (self.num_resource_types.text == ""):
            data_dd['num_resource_types'] = 0
        elif not (self.num_resource_types.text.isdigit()):
            data_dd['num_resource_types'] = 0
        else:
            data_dd['num_resource_types'] = int(self.num_resource_types.text)

        # If input is valid, load form else display error message
        if (data_dd['num_processes'] > 0 and data_dd['num_resource_types'] > 0):
            self.load_form()
        elif (self.num_processes.text != "" and self.num_resource_types.text != ""):
            form = self.manager.get_screen('dd_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    def load_form(self, *args):
        form = self.manager.get_screen('dd_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_dd dictionary
        data_dd['available'] = [5] * data_dd['num_resource_types']
        data_dd['request'] = [[10 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]
        data_dd['allocation'] = [[4 for x in range(data_dd['num_resource_types'])] for x in range(data_dd['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (m)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Available array (m)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(data_dd['num_resource_types']):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(dd_on_available, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(data_dd['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_dd['num_resource_types']):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_allocation, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Request Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        for i in range(data_dd['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Request matrix (n x m)
        for i in range(data_dd['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_dd['num_resource_types']):
                inp = TextInput(id='request'+str(i)+':'+str(j))
                inp.bind(text=partial(dd_on_request, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_dd_output))
        # form.add_widget(box)

    def switch_to_dd_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'dd_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

# Output screen for Deadlock Detection algorithm
class DeadlockDetectionOutputScreen(Screen):
    def calculate(self, *args):
        available = data_dd['available']
        allocation = data_dd['allocation']
        request = data_dd['request']

        layout = self.manager.get_screen('dd_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        box.add_widget(Label(text='Deadlock Detection Algorithm: This algorithm examines the state\nof the system and determines whether a deadlock has occurred.'))
        grid.add_widget(box)

        # Check if the system is deadlocked
        deadlock_safe, schedule, error_status = deadlock.detect(available, allocation, request, data_dd['num_processes'], data_dd['num_resource_types'])

        if error_status['error_number'] != -1:
            # Inform the user
            display_error(grid, error_status['error_message'])
        else:
            work = deepcopy(available)
            finish = ['F'] * data_dd['num_processes']

            # Display schedule
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='The processes can be scheduled as follows: '))
            grid.add_widget(box)

            # Output table labels
            # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Process'))
            box.add_widget(Label(text='Work'))
            box.add_widget(Label(text='Finish'))
            grid.add_widget(box)

            # Display initial work vector
            # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='Initial'))
            work_text = '[  '
            for i in range(len(work)):
                work_text += (str(work[i])+'  ')
            work_text += ']'
            box.add_widget(Label(text=work_text))

            finish_text = '[  '
            for i in range(len(finish)):
                finish_text += (finish[i]+'  ')
            finish_text += ']'
            box.add_widget(Label(text=finish_text))
            grid.add_widget(box)

            # Display step by step changes in work vector according to process scheduled
            for i in range(len(schedule)):
                for j in range(len(work)):
                    work[j] += allocation[schedule[i]][j]
                # print "Schedule["+str(i)+"] = "+str(schedule[i])
                finish[schedule[i]] = 'T'
                # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='P'+str(schedule[i]+1)))

                work_text = '[  '
                for j in range(len(work)):
                    work_text += (str(work[j])+'  ')
                work_text += ']'
                box.add_widget(Label(text=work_text))

                finish_text = '[  '
                for j in range(len(finish)):
                    finish_text += (finish[j]+'  ')
                finish_text += ']'
                box.add_widget(Label(text=finish_text))
                grid.add_widget(box)

            # Not deadlocked
            if deadlock_safe:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='No deadlocked detected.'))
                grid.add_widget(box)
            else:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Deadlock detected. Deadlocked processes: '))
                grid.add_widget(box)
                processes_string = ''
                for j in range(data_dd['num_processes']):
                    if finish[j] == 'F':
                        processes_string += "P"+str(j+1)+", "
                processes_string = processes_string[:-2]
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text=processes_string))
                grid.add_widget(box)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_dd_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_dd_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dd_form'
