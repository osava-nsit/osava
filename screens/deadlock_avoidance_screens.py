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

# Global data for Deadlock Avoidance Algorithm
data_da = dict()

# Binder functions for Deadlock Avoidance Algorithm form
def da_on_available(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 5
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_da['available'][i] = int(value)

def da_on_request(instance, value, i):
    if (value == ''):
        if DEBUG_MODE:
            value = 0
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_da['request'][i] = int(value)

def da_on_max(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 8
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_da['max'][i][j] = int(value)

def da_on_allocation(instance, value, i, j):
    if (value == ''):
        if DEBUG_MODE:
            value = 4
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_da['allocation'][i][j] = int(value)

def da_request_on_process_id(instance, value):
    if (value == ''):
        if DEBUG_MODE:
            value = 1
        else:
            value = -1
    if not is_valid_value(value):
        value = -1
    data_da['request_process'] = int(value)-1

# Input Screen for Deadlock Avoidance algorithm
class DeadlockAvoidanceInputScreen(Screen):
    form = ObjectProperty(None)
    request_form = ObjectProperty(None)

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
            data_da['num_processes'] = 0
        elif not (self.num_processes.text.isdigit()):
            data_da['num_processes'] = 0
        else:
            data_da['num_processes'] = int(self.num_processes.text)

        if (self.num_resource_types.text == ""):
            data_da['num_resource_types'] = 0
        elif not (self.num_resource_types.text.isdigit()):
            data_da['num_resource_types'] = 0
        else:
            data_da['num_resource_types'] = int(self.num_resource_types.text)

        # If input is valid, load form else display error message
        if (data_da['num_processes'] > 0 and data_da['num_resource_types'] > 0):
            self.load_form()
        elif (self.num_processes.text != "" and self.num_resource_types.text != ""):
            form = self.manager.get_screen('da_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    def load_form(self, *args):
        form = self.manager.get_screen('da_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_da dictionary
        data_da['available'] = [5] * data_da['num_resource_types']
        data_da['request'] = [0] * data_da['num_resource_types']
        data_da['max'] = [[10 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]
        data_da['allocation'] = [[4 for x in range(data_da['num_resource_types'])] for x in range(data_da['num_processes'])]

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Add form labels for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Available array (n)
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Available:'))
        for i in range(data_da['num_resource_types']):
            inp = TextInput(id='available'+str(i))
            inp.bind(text=partial(da_on_available, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Max Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Max:'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for Max matrix (n x m)
        for i in range(data_da['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_da['num_resource_types']):
                inp = TextInput(id='max'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_max, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Allocation Matrix (n x m)
        # Add form labels for resource types
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Allocation:'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # # Add input fields for Allocation matrix (n x m)
        for i in range(data_da['num_processes']):
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            box.add_widget(Label(text='P'+str(i+1)))
            for j in range(data_da['num_resource_types']):
                inp = TextInput(id='allocation'+str(i)+':'+str(j))
                inp.bind(text=partial(da_on_allocation, i=i, j=j))
                box.add_widget(inp)
            box.add_widget(Label(size_hint_x=None, width=self.margin_right))
            grid.add_widget(box)

        # Add labels for resource types in request form:
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text=''))
        box.add_widget(Label(text='Process no.'))
        for i in range(data_da['num_resource_types']):
            box.add_widget(Label(text=chr(ord('A')+i)))
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add input fields for resource form
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text='Request:'))
        inp = TextInput(id='process_id')
        inp.bind(text=da_request_on_process_id)
        box.add_widget(inp)
        for i in range(data_da['num_resource_types']):
            inp = TextInput(id='request'+str(i))
            inp.bind(text=partial(da_on_request, i=i))
            box.add_widget(inp)
        box.add_widget(Label(size_hint_x=None, width=self.margin_right))
        grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Uncomment to add buttons on scroll view
        # # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_da_output))
        # form.add_widget(box)
        

    def switch_to_da_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'da_output'

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'


# Output screen for Deadlock Avoidance algorithm
class DeadlockAvoidanceOutputScreen(Screen):
    def calculate(self, *args):
        available = deepcopy(data_da['available'])
        maximum = deepcopy(data_da['max'])
        allocation = deepcopy(data_da['allocation'])
        request = deepcopy(data_da['request'])

        layout = self.manager.get_screen('da_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
        box.add_widget(Label(text="Banker's Algorithm: When a process requests a set of resources, the system must\ndetermine whether granting the request will keep the system in a safe state."))
        grid.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        box.add_widget(Label(text="Resource-Request Algorithm -"))
        grid.add_widget(box)

        # Check if the request can be granted or not
        grantable, message, error_status = deadlock.check_request(available, maximum, allocation, request, data_da['request_process'], data_da['num_processes'], data_da['num_resource_types'])

        if error_status['error_number'] != -1:
            # Inform the user
            display_error(grid, error_status['error_message'])
        else:
            # If request is grantable, check if the state is safe or not
            if grantable:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='If the request is granted, the system will be in the following state -'))
                grid.add_widget(box)

                for j in range(data_da['num_resource_types']):
                    # print "Request["+str(j)+"] = "+str(request[j])
                    available[j] -= request[j]
                    allocation[data_da['request_process']][j] += request[j]

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Available'))
                grid.add_widget(box)

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                available_text = ''
                for i in range(data_da['num_resource_types']):
                    available_text += (str(available[i])+'   ')
                box.add_widget(Label(text=available_text))
                grid.add_widget(box)

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Allocation'))
                box.add_widget(Label(text='Need'))
                grid.add_widget(box)

                for i in range(data_da['num_processes']):
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    allocation_text = ''
                    for j in range(data_da['num_resource_types']):
                        allocation_text += (str(allocation[i][j])+'   ')
                    box.add_widget(Label(text=allocation_text))

                    need_text = ''
                    for j in range(data_da['num_resource_types']):
                        need_text += (str(maximum[i][j] - allocation[i][j])+'   ')
                    box.add_widget(Label(text=need_text))
                    grid.add_widget(box)

                safe, schedule, need = deadlock.is_safe(available, maximum, allocation, data_da['num_processes'], data_da['num_resource_types'])
                work = deepcopy(available)
                finish = ['F'] * data_da['num_processes']

                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Safety Algorithm -'))
                grid.add_widget(box)

                # Output table labels
                # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Process selected'))
                # box.add_widget(Label(text='Need'))
                # box.add_widget(Label(text='Allocation'))
                box.add_widget(Label(text='Work'))
                box.add_widget(Label(text='Finish'))
                grid.add_widget(box)

                # Display initial work vector
                # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text='Initial'))

                # Need for current process
                # box.add_widget(Label(text='-'))
                # Allocation for current process
                # box.add_widget(Label(text='-'))

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
                    finish[schedule[i]] = 'T'
                    # box = BoxLayout(orientation='horizontal', size_hint_x=0.6, padding=(20,0))
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='P'+str(schedule[i]+1)))

                    # Need for current process
                    # need_text = ''
                    # for j in range(len(need[i])):
                    #     need_text += (str(need[i][j])+'  ')
                    # box.add_widget(Label(text=need_text))

                    # # Allocation for current process
                    # allocation_text = ''
                    # for j in range(len(allocation[i])):
                    #     allocation_text += (str(allocation[i][j])+'  ')
                    # box.add_widget(Label(text=allocation_text))

                    # Work vector after current process is allocated resources
                    work_text = '[  '
                    for j in range(len(work)):
                        work_text += (str(work[j])+'  ')
                    work_text += ']'
                    box.add_widget(Label(text=work_text))

                    # Finish vector after current process is allocated resources
                    finish_text = '[  '
                    for j in range(len(finish)):
                        finish_text += (finish[j]+'  ')
                    finish_text += ']'
                    box.add_widget(Label(text=finish_text))
                    grid.add_widget(box)

                if safe:
                    # Show safe sequence
                    grid.add_widget(BoxLayout(size_hint_y=None, height='10dp'))
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)

                    safe_sequence_text = '<'
                    for idx, process_no in enumerate(schedule):
                        if idx > 0:
                            safe_sequence_text += ',  P' + str(process_no+1)
                        else:
                            safe_sequence_text += 'P' +str(process_no+1)
                    safe_sequence_text += '>'

                    box.add_widget(Label(text='Safe sequence:  ' + safe_sequence_text))
                    grid.add_widget(box)

                    box = BoxLayout(size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text="The resultant state is safe."))
                    grid.add_widget(box)
                else:
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                    box.add_widget(Label(text='The resultant state is unsafe.'))
                    grid.add_widget(box)
            # Request not grantable
            else:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                box.add_widget(Label(text=message))
                grid.add_widget(box)

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_da_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        layout.add_widget(sv)

    def switch_to_da_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'da_form'
