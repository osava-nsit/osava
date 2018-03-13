'''
This file contains the classes, functions and globals used for visualizing
Page Replacement algorithms
'''

# Kivy libraries
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
import kivy.metrics
# Python libraries
from decimal import Decimal
# OS Algorithms
from algos import page_replacement
# OSAVA common constants and methods
from common import *

# Global data for Page Replacement Algorithms
data_page = dict()

# Binder functions for Page Replacement Algorithm form
def page_on_ref(instance, value):
    if(value == ''):
        if DEBUG_MODE:
            value = '7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1' 
        else:
            value = ''
    data_page['ref_str'] = str(value)

def page_on_modify(instance, value):
    if value == '':
        if DEBUG_MODE:
            value = '0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1'
        else:
            value = ''
    data_page['modify_bit'] = str(value)

#Input screen for Page Replacement Algorithms
class PageInputScreen(Screen):
    strategy_type = NumericProperty(None)
    form = ObjectProperty(None)
    algo_type = 0

    def update_form(self, *args):
        if (self.num_frames.text == ""):
            data_page['num_frames'] = 0
        elif not (self.num_frames.text.isdigit()):
            data_page['num_frames'] = 0
        else:
            data_page['num_frames'] = int(self.num_frames.text)

        # If input is valid, load form else display error message
        if (data_page['num_frames'] > 0):
            self.load_form()
        elif (self.num_frames.text != ""):
            form = self.manager.get_screen('page_form').form
            form.clear_widgets()
            display_error(form, "Invalid number of processes/resource types.")
            self.visualize_button.disabled = True

    # Binder function for number of processes input
    def bind_num_frames(self, *args):
        self.num_frames.bind(text=self.update_form)

        # Binder function for algorithm type selection from Spinner (Dropdown)
    def bind_spinner(self, *args):
        spinner = self.manager.get_screen('page_form').algo_spinner
        spinner.bind(text=self.show_selected_value)

    def bind_widgets(self, *args):
        self.bind_num_frames()
        self.bind_spinner()

    #Set appropriate strategy type according to the chosen algorithm by the user
    def show_selected_value(self, spinner, text, *args):
        form_reload_flag = False
        if self.strategy_type == 4:
            form_reload_flag = True

        if text == 'First In First Out':
            self.strategy_type = 0
            self.algo_type = 0
        elif text == 'Optimal':
            self.strategy_type = 1
            self.algo_type = 1
        elif text == 'Least Recently Used':
            self.strategy_type = 2
            self.algo_type = 2
        elif text == 'Second Chance':
            self.strategy_type = 3
            self.algo_type = 3
        elif text == 'Enhanced Second Chance':
            self.strategy_type = 4
            self.algo_type = 4
            # Toggle form reload flag for this algo since we require modify bit input here
            form_reload_flag = not form_reload_flag
        elif text == 'Least Frequently Used':
            self.strategy_type = 5
            self.algo_type = 5
        elif text == 'Most Frequently Used':
            self.strategy_type = 6
            self.algo_type = 6
        data_page['algo'] = self.strategy_type
        if form_reload_flag:
            self.load_form()

    # Load the input form based on input
    def load_form(self, *args):
        form = self.manager.get_screen('page_form').form
        form.clear_widgets()

        self.visualize_button.disabled = False

        # Initialize the global data_page dictionary
        if 'algo' not in data_page:
            data_page['algo'] = 0
        if 'num_frames' not in data_page:
            data_page['num_frames'] = 0
        if 'ref_str' not in data_page:
            data_page['ref_str'] = ''
        if 'modify_bit' not in data_page:
            data_page['modify_bit'] = ''

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(15), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))

        # Box for algo spinner
        #box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp', padding=(kivy.metrics.dp(5),kivy.metrics.dp(20)))
        #box.add_widget(Label(text='Algorithm - ', padding=(10,10), size_hint_x=0.3))
        #algo_spinner = Spinner(
        #    text='Select an Algorithm',
        #    values=('First In First Out', 'Optimal', 'Least Recently Used', 'Second Chance', 'Enhanced Second Chance', 'Least Frequently Used', 'Most Frequently Used'))
        #algo_spinner.bind(text=self.show_selected_value)
        #box.add_widget(algo_spinner)
        #grid.add_widget(box)

        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10), 0), size_hint_x=0.6)
        
        # Add label for input
        label = Label(text='Reference string:', size_hint_x=0.4, halign='left')
        label.bind(size=label.setter('text_size'))
        box.add_widget(label)

        # Add input
        inp = TextInput(id='ref_str'+str(0), text=data_page['ref_str'], size_hint_x=0.6)
        inp.bind(text=page_on_ref)
        box.add_widget(inp)

        parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
        parent_box.add_widget(box)
        # For occypying space on right
        parent_box.add_widget(BoxLayout(size_hint_x=0.4))

        grid.add_widget(parent_box)

        # Modify bit for enhanced second chance algo
        if self.algo_type == 4:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(kivy.metrics.dp(10), 0), size_hint_x=0.6)
        
            # Add label for input
            label = Label(text='Modify bit string:', size_hint_x=0.4, halign='left')
            label.bind(size=label.setter('text_size'))
            box.add_widget(label)

            # Add input
            inp = TextInput(id='modify_bit'+str(0), text=data_page['modify_bit'], size_hint_x=0.6)
            inp.bind(text=page_on_modify)
            box.add_widget(inp)

            parent_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            parent_box.add_widget(box)
            # For occypying space on right
            parent_box.add_widget(BoxLayout(size_hint_x=0.4))

            grid.add_widget(parent_box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp')
        sv.add_widget(grid)
        form.add_widget(sv)

        # Add Visualize and back button at the end of form
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_main_menu))
        # box.add_widget(Button(text='Visualize', on_release=self.switch_to_page_output))
        # form.add_widget(box)

    def switch_to_main_menu(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def switch_to_page_output(self, *args):
        self.manager.transition.direction = 'left'
        self.manager.current = 'page_output'


# Output screen for Page Replacement Algorithms
class PageOutputScreen(Screen):
    
   # Stores the memory chart generated by algorithm
    memory_chart = []

    # Margins for memory chart output
    margin_left = kivy.metrics.dp(125)
    margin_bottom = kivy.metrics.dp(255)

    # Width of frame box
    frame_width = kivy.metrics.dp(65)

    # Increment in width per unit size
    inc = 0

    def get_description(self, *args):
        if data_page['algo'] == 0:
            return 'In First In First Out Page Replacement Algorithm, the page that\nwas loaded earliest in the memory is replaced.'
        elif data_page['algo'] == 1:
            return 'In Optimal Page Replacement Algorithm, the page that will not\nbe referenced for the longest period of time is replaced.'
        elif data_page['algo'] == 2:
            return 'In Least Recently Used Page Replacement Algorithm, the page that\nhas not been referenced for the longest period of time is replaced.'
        elif data_page['algo'] == 3:
            return 'In Second Chance Page Replacement Algorithm, the page that was loaded earliest in the\nmemory is replaced. However, if the reference bit of the page is set then that page is\ngiven a second chance and the next possible page is replaced. When a page is given a\nsecond chance, its reference bit is reset and its arrival time is set to the current time.'
        elif data_page['algo'] == 4:
            return 'In Enhanced Second Chance Page Replacement Algorithm, the pages are divided in four\nclasses using their reference bit and modify bit as ordered pairs.\nThe page of the lowest nonempty class which was loaded earliest in the memory is replaced.'
        elif data_page['algo'] == 5:
            return 'In Least Frequently Used Page Replacement Algorithm, the page\nthat has been referenced the least number of times is replaced.'
        elif data_page['algo'] == 6:
            return 'In Most Frequently Used Page Replacement Algorithm, the page\nthat has been referenced the most number of times is replaced.'
            

    # Generate formatted data for input to the algo
    def calculate(self, *args):
        formatted_data = {}

        formatted_data['num_frames'] = int(data_page['num_frames'])
        page_numbers_data = data_page['ref_str']
        page_numbers = []
        if ',' in page_numbers_data: # Comma separated ref_str
            page_numbers = page_numbers_data.split(",")
        else: # Space separated ref_str
            page_numbers = page_numbers_data.split()
        formatted_data['ref_str'] = page_numbers
        formatted_data['algo'] = data_page['algo']
        if data_page['algo'] == 4:
            modify_bits = []
            modify_bits_data = data_page['modify_bit']
            if ',' in page_numbers_data: # Comma separated ref_str
                modify_bits = modify_bits_data.split(",")
            else: # Space separated ref_str
                modify_bits = modify_bits_data.split()
            formatted_data['modify_bits'] = modify_bits

        self.memory_chart = page_replacement.page_replacement(formatted_data)

        layout = self.manager.get_screen('page_output').layout
        layout.clear_widgets()

        grid = GridLayout(cols=1, spacing=kivy.metrics.dp(5), size_hint_y=None)
        # Make sure the height is such that there is something to scroll.
        grid.bind(minimum_height=grid.setter('height'))


        error = self.memory_chart[0]['error_status']
        if error['error_number'] != -1:
            # Inform the user
            display_error(grid, error['error_message'])
        else:
            # Output the algo description
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height='100dp')
            algo_desc = self.get_description()
            desc_label = Label(text=algo_desc, padding=(kivy.metrics.dp(20),kivy.metrics.dp(20)), width=Window.width, valign='top', halign='center')
            # desc_label.text_size = desc_label.size
            box.add_widget(desc_label)
            grid.add_widget(box)

            # To add frame labels
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            grid.add_widget(box)
            frames_label = Label(text='', size_hint_x=None, width=self.margin_left+kivy.metrics.dp(125), valign='middle', halign='right')
            frames_label.text_size = frames_label.size
            box.add_widget(frames_label)

            for i in range(formatted_data['num_frames']):
                frames_label = Label(text='Frame' + str(i+1), size_hint_x=None, width=self.frame_width, valign='middle', halign='right')
                frames_label.text_size = frames_label.size
                box.add_widget(frames_label)

            for idx, temp_memory in enumerate(self.memory_chart):
                page_number = temp_memory['page_number']
                page_fault = temp_memory['page_fault']
                allocated_frame = temp_memory['frame_number']
                memory_state = temp_memory['memory_frames']

                # Add page referenced label
                page_ref_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                page_label = Label(text='Page number referenced:  ', size_hint_x=None, width=self.margin_left + kivy.metrics.dp(110), valign='middle', halign='center')
                page_label.text_size = page_label.size
                page_ref_box.add_widget(page_label)
                page_label = Label(text=str(page_number), size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
                page_label.text_size = page_label.size
                page_ref_box.add_widget(page_label)
                grid.add_widget(page_ref_box)

                # Draw the memory chart
                mem_box = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
                page_fault_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
                
                grid.add_widget(mem_box)
                grid.add_widget(page_fault_box)

                self.draw_memory_state(mem_box, page_fault_box, temp_memory)
            
            # Add total number of page faults   
            temp = self.memory_chart[-1]
            total_page_fault_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            total_page_fault_box.add_widget(Label(text='Total number of page faults: '+ str(temp['page_fault_count'])))
            grid.add_widget(total_page_fault_box) 

            # Add page fault ratio
            total_hits = len(page_numbers) - temp['page_fault_count'] 
            output = Decimal(float(temp_memory['page_fault_count'])/len(page_numbers))
            page_fault_ratio_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height)
            page_fault_ratio_box.add_widget(Label(text='Page fault ratio: '+ str(round(output, 3))))
            grid.add_widget(page_fault_ratio_box) 

        # Add back button
        # box = BoxLayout(orientation='horizontal', size_hint_y=None, height=form_row_height, padding=(0, kivy.metrics.dp(5)))
        # box.add_widget(Button(text='Back', on_release=self.switch_to_page_form))
        # grid.add_widget(box)

        # Add ScrollView
        sv = ScrollView(size=self.size, scroll_type=['bars', 'content'], bar_width='12dp', bar_inactive_color=[0.7,0.7,0.7,0.45])
        sv.add_widget(grid)
        layout.add_widget(sv)

    def draw_memory_state(self, mem_box, page_fault_box, temp_memory, *args):
        page_number = temp_memory['page_number']
        page_fault = temp_memory['page_fault']
        allocated_frame = temp_memory['frame_number']
        memory_state = temp_memory['memory_frames']

        mem_label = Label(text='', size_hint_x=None, width=self.margin_left - kivy.metrics.dp(25), valign='middle', halign='center')
        mem_label.text_size = mem_label.size
        mem_box.add_widget(mem_label)
        mem_label = Label(text='Memory state: ', size_hint_x=None, width=self.margin_left + kivy.metrics.dp(35), valign='middle', halign='left')
        mem_label.text_size = mem_label.size
        mem_box.add_widget(mem_label)

        for idx, state in enumerate(memory_state):
            if state == -1:
                state = 'X'
            if allocated_frame - 1 == idx and page_fault == 1:
                mem_label = ColoredBorderedLabel(text='[b][color=DEC41B]'+str(state)+'[/color][/b]', markup=True, size_hint_x=None, width=self.frame_width, valign='middle', halign='center')
            else:
                mem_label = WhiteBorderedLabel(text=str(state), size_hint_x=None, width=self.frame_width, valign='middle', halign='center')

            mem_label.text_size = mem_label.size
            mem_box.add_widget(mem_label)

        # To add page fault (Y/N)
        page_f_label = Label(text='', size_hint_x=None, width=self.margin_left - kivy.metrics.dp(25), valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        page_f_label = Label(text='Page fault: ', size_hint_x=None, width=self.margin_left, valign='middle', halign='center')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

        if page_fault == 1:
            page_f_label = Label(text='[color=DEC41B]Yes[/color]', markup=True, size_hint_x=None, width=self.margin_left, valign='middle', halign='left')
        else:
            page_f_label = Label(text='No', markup=True, size_hint_x=None
                , width=self.margin_left, valign='middle', halign='left')
        page_f_label.text_size = page_f_label.size
        page_fault_box.add_widget(page_f_label)

    def switch_to_page_form(self, *args):
        self.manager.transition.direction = 'right'
        self.manager.current = 'page_form'
