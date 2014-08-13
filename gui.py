# // Copyright (c) <2014> <Brian Wheatman>

import simulator as sim
import inputs as rl
import kivy
import random
import copy
import datetime


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Ellipse, Line, Color, Rectangle
from kivy.uix.image import AsyncImage
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.dropdown import DropDown
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemLabel, ListView
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.graphics import BorderImage
from kivy.uix.dropdown import DropDown
from kivy.uix.progressbar import ProgressBar
from functools import partial




# the view for each task in the tree
class add_task_view(FloatLayout): # the screen shown for each task
    def __init__(self, task, color, task_group, task_combo, task_successors, **kwargs):
        super(add_task_view, self).__init__(**kwargs)
        self.task = task # keep track of which task this screen is talking about

        # the dicription of the inputs is put in the top left
        self.input_labels = input_labels(task)
        self.input_labels.size_hint=(.3, .25) # how big the label is
        self.input_labels.pos_hint={'x':.15, 'y':.7} # where in the box it goes, describes the bottom left of the label

        # the dicription of the outputs is put in the top right
        self.output_labels = output_labels(task)
        self.output_labels.size_hint=(.3, .25) # how big the label is
        self.output_labels.pos_hint={'x':.65, 'y':.7} # where in the box it goes, describes the bottom left of the label

        # showing the image if the task is off and a gif if it is on
        self.image_gif = image_gif(task)
        self.image_gif.size_hint=(.9, .9) # how big the label is
        self.image_gif.pos_hint={'x':.05, 'y':.05} # where in the box it goes, describes the bottom left of the label

        self.progress_bar_back = yellow_cell()
        self.progress_bar_back.size_hint=(1, .05) # how big the label is
        self.progress_bar_back.pos_hint={'x':0, 'y':.95} # where in the box it goes, describes the bottom left of the label

        self.progress_bar = progress_bar(task)
        self.progress_bar.size_hint=(1, .05) # how big the label is
        self.progress_bar.pos_hint={'x':0, 'y':.95} # where in the box it goes, describes the bottom left of the label

        # to turn the task on and off, displayed over the image/gif
        self.on_block = on_block(task, task_group)
        self.on_block.size_hint=(.9, .9) # how big the label is
        self.on_block.pos_hint={'x':.05, 'y':.05} # where in the box it goes, describes the bottom left of the label
        
        # the dropdown menu where addition buttons are stored
        self.dropdown = dropdown(task, task_combo, task_successors, task_group)
        self.dropdown_btn = Button(text = "Info. / Controls")
        self.dropdown_btn.bind(on_release=self.dropdown.open)
        
       
        # the buy button shown on the main task's screen
        
        self.buy_btns = self.dropdown.buy_block.buy_btns_block
        self.buy_btns.size_hint=(.3, .15) # how big the label is
        self.buy_btns.pos_hint={'x':.05, 'y':.2} # where in the box it goes, describes the bottom left of the label

        
        # the sell button shown on the main screen
        self.sell_btn = self.dropdown.sell_block.sell_btn
        self.sell_btn.size_hint=(.3, .15) # how big the label is
        self.sell_btn.pos_hint={'x':.65, 'y':.2} # where in the box it goes, describes the bottom left of the label

        
        
        # the size and position of the dopdown button itself
        self.dropdown_btn.size_hint=(.9, .15)  # how big the label is
        self.dropdown_btn.pos_hint={'x':.05, 'y':.05} # where in the box it goes, describes the bottom left of the label

        # add the different items to the creen itself
        self.add_widget(self.image_gif) # put the image first to ensure it is back
        self.add_widget(self.on_block) # adding the on off button
        self.add_widget(self.dropdown_btn) # adding the dropdown
        self.add_widget(self.input_labels) # adding the input labels
        self.add_widget(self.output_labels) # adding the otput labels
        self.add_widget(self.buy_btns) # adding the buy buttons
        self.add_widget(self.sell_btn) # adding the sell buttons
        self.add_widget(self.progress_bar_back)
        self.add_widget(self.progress_bar) # adding the progress bar
        
        # give it a color that will apear as a border
        (red, green, blue, trans) = color
        self.red = red
        self.green = green
        self.blue = blue
        self.trans = trans
        with self.canvas.before: # draw it before so it is a background color that appears as a border
            Color(self.red, self.green, self.blue, self.trans)  
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# the dropdown menu that tells about the task
class dropdown(DropDown):
    def __init__(self, task, task_combo, task_successors, task_group, **kwargs):
        # make sure we aren't overriding any important functionality
        super(dropdown, self).__init__(**kwargs)
        self.container.padding = 10
        # the info that will be displayed by the dropdown
        self.info_block = info_block(task)
        self.info_block.size_hint_y=None
        self.info_block.height=95
        self.info_block.padding = 2

        # to control the buying amount
        self.buy_block = buy_block(task, task_combo)
        self.buy_block.size_hint_y=None
        self.buy_block.height=55
        self.buy_block.padding = 4

        # the push block
        self.push_block = push_block(task, task_combo, task_successors, task_group)
        self.push_block.size_hint_y=None
        self.push_block.height=115
        self.push_block.padding = 2

        # the sell block
        self.sell_block = sell_block(task, task_combo)
        self.sell_block.size_hint_y=None
        self.sell_block.height=15
        self.sell_block.padding = 2

        self.add_widget(self.info_block) # add the info block to the dropdown
        
        dummy = False
        for i in range(len(task.input_price)):
            if task.input_price[i] != 0:
                dummy = True
        if dummy == True:
            self.add_widget(self.buy_block) # adding the buy buttons if you can buy the inputs
            
        if task.output_price != 0:
            self.add_widget(self.sell_block) # adding sell buttons if you can sell the outputs

        if task in task_successors:
            self.add_widget(self.push_block) # adding the push button if the task can push

                
        
        with self.canvas.before:
            Color(0, .2, 0, 1)  # dark green background, it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# the information block that tells about the task
class info_block(BoxLayout):
    def __init__(self, task, **kwargs):
        # make sure we aren't overriding any important functionality
        super(info_block, self).__init__(**kwargs)
                
        self.size_hint=(1, .25)
        # the text of the info block
        data = [{'text':"Task " +task.task_name},
                    {'text': "Robot: " + str(task.id)},
                    {'text': "Inputs: " + str(task.startState[1])},
                    {'text': "Set up:  " + str(task.startState[2])},
                    {'text': "Process: " + str(task.startState[3])},
                    {'text': "Outputs: " + str(task.startState[5])},
                    ]
        if task.input_price != [0]* len(task.input_price): # if you can buy the inputs
            data.append({'text': "Inputs cost: " + str(task.input_price)}) 
        if task.output_price != 0: # if you can sell the outputs
            data.append({'text': "Output price: " + str(task.output_price) })

        # required code gotten out of documentation that controls size
        args_converter = lambda row_index, rec: {'text': rec['text'],
                                                 'size_hint_y': None,
                                                 'height': 13, 'font_size':13}

        list_adapter = ListAdapter(data=data,
                                   args_converter=args_converter,
                                   cls=ListItemLabel,
                                   selection_mode='single',
                                   allow_empty_selection=False)
        # the scrollable list
        list_view = ListView(adapter=list_adapter)
        self.add_widget(list_view)
        with self.canvas.before:
            Color(0, 0, 0, 1)  # black background so it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# the input labels that show both what the task imports and how much it currently has in its queue
class input_labels(BoxLayout):
    def __init__(self, task, **kwargs):
        # make sure we aren't overriding any important functionality
        super(input_labels, self).__init__(**kwargs)
        self.orientation = 'vertical' # stack the two labels on top of each other
        inp_name_lbl = Label(text= str(','.join(task.startState[0])), color = [0,1,0,1], bold = True) # what the imports are
        self.inp_lbl = Label(text=str(task.startState[6]), color = [0,1,0,1], bold = True) # how many of them there are
        # add the labels
        self.add_widget(inp_name_lbl)
        self.add_widget(self.inp_lbl)
        
        with self.canvas.before:
            Color(0, 0, 0, 0)  # clear so the picture/gif can be seen behind it
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class output_labels(BoxLayout):
    def __init__(self, task, **kwargs):
        # make sure we aren't overriding any important functionality
        super(output_labels, self).__init__(**kwargs)
        self.orientation = 'vertical'
        out_name_lbl = Label(text= str(task.startState[4]), color = [0,1,0,1], bold = True)# what the exports are
        self.out_lbl = Label(text=str(task.startState[7]), color = [0,1,0,1], bold = True) # how many of them there are
        # add the labels
        self.add_widget(out_name_lbl)
        self.add_widget(self.out_lbl)
        
        
        with self.canvas.before:
            Color(0, 0, 0, 0)  # clear so the picture/gif can be seen behind it
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class image_gif(BoxLayout):
    def __init__(self, task,  **kwargs):
        # make sure we aren't overriding any important functionality
        super(image_gif, self).__init__(**kwargs)
        # add an image if off and a gif if on
        if task.startState[10][0]: # if it is off
            self.image = Image(source='robot.png') # display the image
        else: # if on
            self.image = Image(source ='robot_gif.gif', anim_delay = .08) # diplay the gif, control the speed of the gif
        
        self.add_widget(self.image)
        
        with self.canvas.before:
            Color(.2, 0, 0, 1)  # dark red background, it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class progress_bar(BoxLayout):
    def __init__(self, task,  **kwargs):
        # make sure we aren't overriding any important functionality
        super(progress_bar, self).__init__(**kwargs)
        # add an image if off and a gif if on
        if task.startState[8]: # if setting up
            self.pb = ProgressBar(max=task.startState[2]) # max is set up time
        else: # if not setting up
            self.pb = ProgressBar(max=task.startState[3]) # make is proccessing time
        self.add_widget(self.pb)
        
        with self.canvas.before:
            Color(0, 0, 0, 0)  # see through background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class buy_block(BoxLayout):
    def __init__(self, task, task_combo, **kwargs):
        # make sure we aren't overriding any important functionality
        super(buy_block, self).__init__(**kwargs)
        def buy_item(instance, **kwargs):
            for i in range(int(buy_slid.value)): # call this function repeatedly to buy multile items
                if task_combo.cash >= task.input_price[kwargs['index']]: # only buy if you have enough cas
                    task_combo.cash -= task.input_price[kwargs['index']] # remove cash
                    task.add_items_to_queue(kwargs['index'], 1) # add item
                    
        def OnBuySliderValueChange(instance,value): # what happens when the slider is changed
                buy_slid_lbl.text = "Buy #: " + str(value) # change the label above it to show the amount

        buy_slid = Slider(min=1, max=100, value=1, step = 1) # can buy betwen 1 and 100
        buy_slid.bind(value=OnBuySliderValueChange) # the slider cahnges the buy amount
        buy_slid_lbl = Label(text = "Buy #: " + str(getattr(buy_slid, 'value'))) # show what the slider is set to
        self.orientation = 'vertical' # place slider and label vertically
        buy_btns_block = GridLayout(cols=len(task.input_price)) # place the buy buttons vertically and keep position even if some can't be bought

        # add the buy buttons for all the imports that can be bought
        for i in range(len(task.input_price)):
            buy_btn = Button(text='Buy')
            buy_btn.bind(on_press = partial(buy_item, index = i))
            if task.input_price[i] != 0:
                buy_btns_block.add_widget(buy_btn)
            else:
                buy_btns_block.add_widget(Label(text = ""))

            
        self.buy_btns_block = buy_btns_block # make the buy buttons so they can be added to the main screen
        self.add_widget(buy_slid_lbl) # adding the buy slider label
        self.add_widget(buy_slid) # adding the buy slider
        with self.canvas.before:
            Color(0, 0, 0, 1)  # black background so it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class sell_block(BoxLayout):
    def __init__(self, task, task_combo, **kwargs):
        # make sure we aren't overriding any important functionality
        super(sell_block, self).__init__(**kwargs)
        # check if the task is limited by its sell amount
        def sell_limit():
            if task_combo.sell_amounts[task] < task_combo.sell_amounts[task_combo.limitations[task]]:
                return True
            else:
                return False
        # sell an item
        def sell_item(instance):
            if task in task_combo.limitations: # if it might have a limitaion
                if sell_limit(): # check the limitaion
                    if task.startState[7][0] > 0: # if it has something to sell
                        task_combo.cash += task.output_price # add the outpus price to the cash
                        task.remove_items(1) # take away an item
                        task_combo.sell_amounts[task] +=1 # keep track of it in the sell amounts
            else: # same but not worrying about the limitation
                if task.startState[7][0] > 0:
                    task_combo.cash += task.output_price
                    task.remove_items(1)
                    task_combo.sell_amounts[task] +=1

        def sell_all_item(instance): # to sell all
            if task in task_combo.limitations: # if it has a limit
                if sell_limit(): # if it can sell any
                    if task.startState[7][0] > 0: # if there is something to sell
                        # how many can be sold, the min of the limit - the amount already sold and how many have been made
                        can_sell = task_combo.sell_amounts[task_combo.limitations[task]]- task_combo.sell_amounts[task]
                        can_sell = min([can_sell, task.startState[7][0]]) 
                        task_combo.cash += task.output_price*can_sell
                        task.remove_items(can_sell)
                        task_combo.sell_amounts[task] += can_sell
                        
            else: # same but not worrying about the limitation
                if task.startState[7][0] > 0:
                    task_combo.sell_amounts[task] += task.startState[7][0]
                    task_combo.cash += task.output_price*task.startState[7][0]
                    task.remove_items(task.startState[7][0])

        
        sell_btn = Button(text='Sell')
        sell_btn.bind(on_press = sell_item)
        sell_all_btn = Button(text='Sell all')
        sell_all_btn.bind(on_press = sell_all_item)
        
        
        
        if task.output_price == 0:
            sell_btn = Label(text="") # if it can't be sold make the sell just a clear label so sell_btn is defined
        else:
            self.add_widget(sell_all_btn) # ading the sell all button if it can be sold

        self.sell_btn = sell_btn # make it so you can add thr sell button to the main screen
            
        with self.canvas.before:
            Color(0, 0, 0, 1)  # black background, it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
class on_block(BoxLayout):
    def __init__(self, task, task_group, **kwargs):
        # make sure we aren't overriding any important functionality
        super(on_block, self).__init__(**kwargs)
        def pressed_on_off(instance):
            # change the value in the back end
            task.on_off()
            # check to see if other tasks have to be turned off, if so turn them off
            if not task.startState[10][0]:
                for other_task in task_group: # two of the same robots can't be on at the same time
                    if other_task.id == task.id and other_task != task: # any task done by the same robot that not is the same robot is turned off
                        if not other_task.startState[10][0]:
                            other_task.on_off()
        if task.startState[10][0]: # if off
            self.on_off_btn = Button(text='Turn on') # show turn on
        else: # if on
            self.on_off_btn = Button(text='Turn off') # show turn off
        
        self.on_off_btn.bind(on_release=pressed_on_off) # the on off button changes the state of that task (and all tasks assosiated with it)
        self.on_off_btn.background_color = [0,0,0,0] # make it clear so the image/gif can be seen
        self.on_off_btn.color = [0,1,0,1] # show the text as green to make it easy to see
        self.add_widget(self.on_off_btn)

        with self.canvas.before:
            Color(0, 0, 0, 0)  # see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size



class push_block(BoxLayout):
    def __init__(self, task, task_combo, task_successors, task_group, **kwargs):
        # make sure we aren't overriding any important functionality
        super(push_block, self).__init__(**kwargs)
        self.size_hint = (1,2)
        def pressed_push(instance):
            task_combo.push_action(task, task.number_push, task_combo.push_direction[task]) # push action is done for the back end
            
        def pressed_push_dir(instance):
            task_combo.change_push_direction(task) 
            setattr(push_dir_btn, 'text', 'Pushing to ' + str(task_combo.push_direction[task][0].task_name))

        def pressed_auto_push(instance):
            if auto_push_btn.text == "Manual":
                task.push = True
                setattr(auto_push_btn, 'text', "Auto")
            else:
                task.push = False
                setattr(auto_push_btn, 'text',  "Manual")

        def OnPushSliderValueChange(instance,value): # what happens when the slider is changed
                push_slid_lbl.text = "Push #: " + str(value) # change the label above it to show the amount
                task.set_push_number(value)

        self.orientation = 'vertical'
        push_btn = Button(text='Push') # used to push the items to the next task
        push_slid = Slider(min=1, max=100, value=1, step = 1) # can buy betwen 1 and 100
        push_slid.bind(value=OnPushSliderValueChange) # the slider cahnges the buy amount
        push_slid_lbl = Label(text = "Push #: " + str(getattr(push_slid, 'value'))) # show what the slider is set to

        
        auto_push = Clock
        
        auto_push_btn = Button(text = "Manual")
        
            
        auto_push_btn.bind(on_release=pressed_auto_push)  
        push_btn.bind(on_release=pressed_push) # pushes immediatly
        
        if task not in task_successors: # if it has no successors it can't push
            auto_push_btn = Label(text = "")

        if task in task_successors: # if it does, add the buttons
            self.add_widget(push_btn)
            self.add_widget(push_slid_lbl)
            self.add_widget(push_slid)
            
            if task_successors[task][0] not in task_group:
                push_dir_btn = Button(text='Pushing to ' + str(task_combo.push_direction[task][0].task_name))
                push_dir_btn.bind(on_release= pressed_push_dir)
                self.add_widget(push_dir_btn)
        self.add_widget(auto_push_btn)
          
        with self.canvas.before:
            Color(0, 0, 0, 1)  # black background, it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size


        
# adding the pointing arrows
class add_arrows_up_right(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_up_right, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(ellipse=(0, 0, 0, 0, 0, 0))
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x_pos = x_pos + x_size/2.0
        y_pos = y_pos - y_size/2.0
        self.arrow.ellipse = (x_pos, y_pos, x_size, y_size, 270, 360) # shape the arrow

# adding the pointing arrows
class add_arrows_right_up(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_right_up, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(ellipse=(0, 0, 0, 0, 0, 0))
        
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x_pos = x_pos - x_size/2.0
        y_pos = y_pos + y_size/2.0
        self.arrow.ellipse = (x_pos, y_pos, x_size, y_size, 90, 180) # shape the arrow

class add_arrows_down_right(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_down_right, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(ellipse=(0, 0, 0, 0, 0, 0))
        
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x_pos = x_pos + x_size/2.0
        y_pos = y_pos + y_size/2.0
        self.arrow.ellipse = (x_pos, y_pos, x_size, y_size, 180, 270) # shape the arrow

class add_arrows_right_down(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_right_down, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(ellipse=(0, 0, 0, 0, 0, 0))
        
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x_pos = x_pos - x_size/2.0
        y_pos = y_pos - y_size/2.0
        self.arrow.ellipse = (x_pos, y_pos, x_size, y_size, 0, 90) # shape the arrow

class add_arrows_right(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_right, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(points=[0,0,0,0])
        
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x1 = x_pos
        x2 = x_pos + x_size
        y1 = y_pos + y_size/2
        y2 = y_pos + y_size/2
        self.arrow.points = [x1,y1,x2,y2] # shape the arrow

class add_arrows_down(BoxLayout):
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(add_arrows_down, self).__init__(**kwargs)
        with self.canvas.before:
            Color(0,0,0,0)  # see through other than the arrow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        with self.canvas.after:
            Color(1,1,1,1)  # white
            self.arrow = Line(points=[0,0,0,0])
        
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        (x_pos, y_pos) = instance.pos
        self.rect.size = instance.size
        (x_size, y_size) = instance.size
        x1 = x_pos + x_size/2
        x2 = x_pos + x_size/2
        y1 = y_pos
        y2 = y_pos + y_size
        self.arrow.points = [x1,y1,x2,y2] # shape the arrow


    
 # to add a color widget
class empty_cell(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(empty_cell, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 0, 0, 0)  # black, clear
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

 # to add a color widget
class green_cell(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(green_cell, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 1, 0, 1)  # green
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

 # to add a color widget
class yellow_cell(FloatLayout):

    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(yellow_cell, self).__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 0, 1)  # yellow
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size

# the game itself
class game(BoxLayout):
    def __init__(self,task_group, task_combo, task_successors, following_task, task_grid, grid_width, grid_length, **kwargs):
        super(game, self).__init__(**kwargs)
        # the full screen is made up of two layouts
        self.orientation='vertical'
        self.spacing=10
        # the first is the orginisation of all of the tasks in a tree
        task_layout = GridLayout(cols=(grid_length*2-1), size_hint=(1, .85))
        # the second is a grid of the buttons used to control the simulation
        top_bar_layout = BoxLayout(size_hint=(1, .03))
        controls_layout = BoxLayout(size_hint=(1, 1))
        clock = Clock # adding the clock

        # make a number of time steps look like a nice clock
        def clock_label(time, length_period = task_combo.length_period, number_periods = task_combo.number_periods ):
            if time/length_period == number_periods: # if the game is over
                return "Out of Time"
            period = time/length_period
            time_in_period = time%length_period
            hours = time_in_period/60
            minutes = time_in_period%60
            label = ""
            # add the only the needed labels
            if period != 0:
                if period == 1:
                    label +=  str(period) + " Period: "
                else:
                    label +=  str(period) + " Periods: "
            if hours != 0:
                if hours == 1:
                    label += str(hours) +  " Hour: "
                else:
                    label += str(hours) +  " Hours: " 
            if minutes != 0:
                if minutes == 1:
                    label += str(minutes) + " Minute"
                else:
                    label += str(minutes) + " Minutes" 
            return label

        # find up to 512 colors that are as different as possible
        def color_picker(num_colors):  
            options = []
            for r in [1,.9,.8,.7,.3,.2,.1,0]:
                for g in [0,.1,.2,.3,.7,.8,.9,1]:
                    for b in [1,.9,.8,.7,.3,.2,.1,0]:
                        options.append((r,g,b,1))
            color_options = [term for term in options if options.index(term)%(int(512/(num_colors)+1)) == 0]
            return color_options

        # give each robot a spicific color
        def map_bot_to_color(task_group):
            dif_bots = [] # all of the different robots
            for task in task_group:
                if task.id not in dif_bots:
                    dif_bots.append(task.id)
            color_options = color_picker(len(dif_bots)) # the color options
            map_bot_to_color = {}
            i = 0
            for robot in dif_bots:
                map_bot_to_color[robot] = color_options[i] # each robot is given a color
                i += 1
            return map_bot_to_color
                
                
        color_map = map_bot_to_color(task_group) # which robot is which color
        shown_grid = task_grid[:] # the grid that will be diplayed
        # make the grid longer to include spaces for the lines
        for row in shown_grid:
            for index in range(grid_length-1, 0, -1):
                row.insert(index, None)
        # check if the goal task is in a certain column
        def in_column(grid, start_row, goal, column):
            for row in grid:
                if goal == row[column]:
                    if grid.index(row) < start_row:
                        return 'up'
                        print goal
                    if grid.index(row) > start_row:
                        return 'down'
            return False
        # find what row the goal task is in
        def which_row(grid, start_row, goal):
            for row in grid:
                if goal in row:
                    if grid.index(row) < start_row:
                        return 'up'
                    if grid.index(row) > start_row:
                        return 'down'
                      
        # figure out where all the arrows go
        def find_arrows(grid):
            # make room to store arrows
            for i in range(grid_width):
                for j in range(grid_length*2-1):
                    if grid[i][j] == None:
                        grid[i][j] = []
            # place the right arrows next to a task
            for i in range(grid_width):
                for j in range(grid_length*2-1):
                    if type(grid[i][j-1]) == type(task_group[0]):
                        if grid[i][j-1] in following_task:
                            for item in following_task[grid[i][j-1]]:
                                grid[i][j].append(('right', item) )
            
            # place the up and down turns from other lines
            for i in range(grid_width):
                for j in range(grid_length*2-1):
                    if type(grid[i][j-1]) == list:
                        if type(grid[i][j]) == list:
                            for k in grid[i][j-1]:
                                if k[0] == 'right':
                                    if in_column(grid , i , k[1], j) == 'up':
                                        grid[i][j].append(('right up', k[1]) )
                                    if in_column(grid , i , k[1], j) == 'down':
                                        grid[i][j].append(('right down', k[1]) )
            # follow up
            for i in range(grid_width-1):
                for j in range(grid_length*2-1):
                    if type(grid[i+1][j]) == list:
                        if type(grid[i][j]) == list:
                            for k in grid[i+1][j]:
                                if k[0] == 'right up' or k[0] == 'up':
                                    grid[i][j].append(('up', k[1]) )

            # place the up and down turns from tasks
            for i in range(grid_width-1):
                for j in range(grid_length*2-1):
                    if type(grid[i][j-1]) == type(task_group[0]):
                        if grid[i][j-1] in following_task:
                            if type(grid[i][j+1]) == type(task_group[0]):
                                if len(following_task[grid[i][j-1]]) >= 2:
                                       for item in following_task[grid[i][j-1]]:
                                           if item not in grid[i]:
                                               if which_row(grid, i, item) == 'up':
                                                   grid[i][j].append(('right up', item) )
                                               if which_row(grid, i, item) == 'down':
                                                   grid[i][j].append(('right down', item) )
                                               
            # after going down either flatten or continue down
            for i in range(1,grid_width):
                for j in range(grid_length*2-1):
                    if type(grid[i-1][j]) == list:
                        if type(grid[i][j]) == list:
                            for k in grid[i-1][j]:
                                if k[0] == 'down' or k[0] == 'right down':
                                    if k[1] in grid[i]:
                                        grid[i][j].append(('down right', k[1]) )
                                    else:
                                        grid[i][j].append(('down', k[1]) )
            # continue right
            for i in range(grid_width):
                for j in range(1,grid_length*2-1):
                    if type(grid[i][j-1]) == list:
                        if type(grid[i][j]) == list:
                            for k in grid[i][j-1]:
                                if k[0] == 'right' or k[0] == 'down right':
                                    if k[1] in grid[i]:
                                        grid[i][j].append(('right', k[1]) )

            # if nothing, leave blank
            for i in range(grid_width):
                for j in range(grid_length*2-1):
                    if grid[i][j] == []:
                        grid[i][j] = None
            return grid
                                                           
            
        shown_grid = find_arrows(shown_grid)
        
        # used to put the items in the grid
        for i in range(grid_width):
            for j in range(grid_length*2-1):
                if type(shown_grid[i][j]) == type(task_group[0]): # if that spot is a task
                    task_layout.add_widget(add_task_view(shown_grid[i][j], color_map[shown_grid[i][j].id], task_group,\
                                                           task_combo, task_successors, size_hint = (1.8,1))) # adding a task screen
                elif shown_grid[i][j] == None:
                    task_layout.add_widget(empty_cell()) # adding a blank cell to help align others
                else: # add the arrows
                    layout = FloatLayout()
                    for k in shown_grid[i][j]:
                        if k[0] == 'right':
                            arrows = add_arrows_right()
                        if k[0] == 'up':
                            arrows = add_arrows_down()
                        if k[0] == 'right up':
                            arrows = add_arrows_right_up()
                        if k[0] == 'right down':
                            arrows = add_arrows_right_down()
                        if k[0] == 'down':
                            arrows = add_arrows_down()
                        if k[0] == 'down right':
                            arrows = add_arrows_down_right()
                        arrows.size_hint = (1, 1)
                        arrows.pos_hint ={'x':0, 'y':0}
                        layout.add_widget(arrows)
                    task_layout.add_widget(layout)
                

        # the inroduction to each sim
        def intro_popup_content(task_group, task_combo):
            # the text of the info block
            data = [] # the text of the popup
            data.append("About this Simulation")
            data.append("You have " + str(task_combo.number_periods) + ", " + str(task_combo.length_period/60) + " hour " +str(task_combo.length_period%60) +  " minute long periods")
            data.append("Your bills are $"+ str(task_combo.period_cost) + " each period")
            data.append("The limitations are:")
            for limit in task_combo.limitations:
                data.append("Sales of "+ str(limit.startState[4]) + " are limited by sales of " + str(task_combo.limitations[limit].startState[4]) )
            data.append("Information on each task") 
            for task in task_group:
                data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
                data.append("Task: " + str(task.task_name))
                data.append("Done by robot " + str(task.id))
                data.append("Inputs " + str(task.startState[1]) + " at a time")
                data.append("Set up takes  " + clock_label(task.startState[2]))
                data.append("Processing takes " + clock_label(task.startState[3]))
                data.append("Outputs " + str(task.startState[5]) + " at a time")

                if task.input_price != [0]* len(task.input_price):
                    if len(task.input_price) == 1:
                        data.append("Each inputs cost $" + str(task.input_price[0]))
                    else:            
                        data.append("Each inputs cost " + str(task.input_price) + "dollars respectively")
                if task.output_price != 0:
                    data.append("Each output prices sells for $" + str(task.output_price))

            list_adapter = ListAdapter(data=data,
                                       cls=ListItemLabel,
                                       selection_mode='single',
                                       allow_empty_selection=False)
            # the scrolable list
            list_view = ListView(adapter=list_adapter, size_hint=(1, 1))
            return list_view

        start_content = intro_popup_content(task_group, task_combo)
        
        welcome_popup = Popup(title='Welcome', content=start_content, size_hint=(.7, .7)) # control the content and the size
        welcome_popup.open()
            
                
        current_time = 0 # start the clock at 0
        time_lbl = Label(text=str(current_time), color = [0,0,0,0], size_hint = (.001,1 )) # counting the timesteps, not shown
        clock_lbl = Label(text = clock_label(current_time), bold = True, color = [0,1,0,1], size_hint = (1.5,1)) # showing the clock
        money_lbl = Label(text=str(task_combo.cash), bold = True, color = [0,1,0,1], size_hint = (.5,1))
        slid = Slider(min=0, max=50, value=0, step = 1, size_hint = (.75, 1)) # adding the slider to control the speed

        def end_period_block(task_combo):
            layout = BoxLayout(orientation='vertical')
            data = [] # text
            data.append("End of Period")
            data.append("Period bills: " + str(task_combo.period_cost))
            data.append("Time: " + clock_label(int(time_lbl.text)))
            data.append("Current cash: "+ str(task_combo.cash))
            data.append("remember you only have " + str(task_combo.number_periods) + " periods")
            list_adapter = ListAdapter(data=data,
                                       cls=ListItemLabel,
                                       selection_mode='single',
                                       allow_empty_selection=False)
            # the scrolable list
            list_adapter = ListAdapter(data=data,
                                       cls=ListItemLabel,
                                       selection_mode='single',
                                       allow_empty_selection=False)
            list_view = ListView(adapter=list_adapter, size_hint=(1, .85))
            layout.add_widget(list_view)
            
            return layout
        
        

        end_period_content = end_period_block(task_combo)
        end_period_popup = Popup(title='period done', content=end_period_content, size_hint=(.4, .4)) # control the content and the size

        # what happens at the end of a period
        def end_period(task_combo):
            setattr(slid, 'value', 0) # set the speed to 0
            clock.unschedule(pressed_step) # stop step from running
            task_combo.cash -= task_combo.period_cost # take the period cost
            if task_combo.cash < 0: # if lose
                end_game("couldn't pay bills")
                return False
            else: # else show the end_period popup
                setattr(end_period_popup, 'content', end_period_block(task_combo))
                end_period_popup.open()

        # what happens to move foward one step
        # called at the rate of the speed slider
        def pressed_step(instance):
            current_time = int(time_lbl.text) # get the current time
            if task_combo.cash < 0: # if lose
                end_game("couldn't pay bills")
                return False
            if current_time >= task_combo.time_limit: # if time limit
                setattr(clock_lbl, 'text', "out of time") # updating the clock
                end_game("out of time")
                return False
            current_time +=1 # updating the clock
            setattr(time_lbl, 'text', str(current_time)) # updating the time label
            setattr(clock_lbl, 'text', clock_label(current_time)) # updating the clock
            end_period_popup.dismiss()
            if current_time % (task_combo.length_period) == 0 and current_time != 0:
                end_period(task_combo)
            # the backend calculates the next values
            task_combo.getNextValues(task_combo.startState)
            
            
            
        def stats_block(task_group, task_combo):
            # the text of the info block
            data = []
            data.append("Information")
            if task_combo.time_limit < 1440:
                hours = task_combo.time_limit /60
                minutes = task_combo.time_limit%60
                data.append("Time limit: " + str(hours) + " hours " + str(minutes) + " minutes")
            else:
                days = task_combo.time_limit /(60*24)
                hours = (task_combo.time_limit - (days*24*60) ) / (60)
                minutes = task_combo.time_limit % (60)
                data.append("Time limit: " + str(days) + " days "+ str(hours) + " hours " + str(minutes) + " minutes")
            data.append("Period cost: "+ str(task_combo.period_cost))
            data.append("Limitations")
            for limit in task_combo.limitations:
                data.append("sales of "+ str(limit.startState[4]) + " is limited by sales of " + str(task_combo.limitations[limit].startState[4]) )
            data.append("Information on each task") 
            for i in range(len(task_group)):
                stats = task_group[i].startState[12]
                if task_group[i].startState[12][0][4] == 0:
                    data.append("Task: " + task_group[i].task_name)
                    data.append("It has not run yet")
                    data.append("Input queue length: "+  str([float(int(term*100))/100 for term in stats[2]]) + " items")
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
                    
                else:
                    data.append("Task: " + task_group[i].task_name)  
                    data.append("Time on: " + str(int(float(100*stats[0][0])/stats[0][4])) +  "%")
                    data.append("Time setting up: " + str(int(float(100*stats[0][1])/stats[0][4])) +  "%")
                    data.append("Time making something: " + str(int(float(100*stats[0][2])/stats[0][4])) +  "%")
                    data.append("Time starved: " + str(int(float(100*stats[0][3])/stats[0][4])) +  "%")
                    data.append("Items proccessed: " +  str(stats[1]))
                    data.append("Input queue length: " +  str([float(int(term*100))/100 for term in stats[2]]))
                    if task_combo.sell_amounts[task_group[i]] != 0:
                        data.append("Items sold: " + str(task_combo.sell_amounts[task_group[i]]))
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
                    

            list_adapter = ListAdapter(data=data,
                                       cls=ListItemLabel,
                                       selection_mode='single',
                                       allow_empty_selection=False)
            # the scrolable list
            list_view = ListView(adapter=list_adapter, size_hint=(1, 1))
            return list_view
        
        def end_game_block(task_group, task_combo):
            layout = BoxLayout(orientation='vertical')
            data = [] # the text
            data.append("Information")
            data.append("End Time: " + clock_label(int(time_lbl.text)))
            data.append("Final cash: "+ str(task_combo.cash))
            data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
            data.append("Information on each task")
            data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
            for i in range(len(task_group)):
                stats = task_group[i].startState[12]
                if task_group[i].startState[12][0][4] == 0:
                    data.append("Task: " + task_group[i].task_name)
                    data.append("It has not run yet")
                    data.append("Input queue length: "+  str([float(int(term*100))/100 for term in stats[2]]) + " items")
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
                    
                else:
                    data.append("Task: " + task_group[i].task_name)  
                    data.append("Time on: " + str(int(float(100*stats[0][0])/stats[0][4])) +  "%")
                    data.append("Time setting up: " + str(int(float(100*stats[0][1])/stats[0][4])) +  "%")
                    data.append("Time making something: " + str(int(float(100*stats[0][2])/stats[0][4])) +  "%")
                    data.append("Time starved: " + str(int(float(100*stats[0][3])/stats[0][4])) +  "%")
                    data.append("Items proccessed: " +  str(stats[1]))
                    data.append("Input queue length: " +  str([float(int(term*100))/100 for term in stats[2]]))
                    if task_combo.sell_amounts[task_group[i]] != 0:
                        data.append("Items sold: " + str(task_combo.sell_amounts[task_group[i]]))
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --")
                    

            list_adapter = ListAdapter(data=data,
                                       cls=ListItemLabel,
                                       selection_mode='single',
                                       allow_empty_selection=False)
            # the scrolable list
            list_view = ListView(adapter=list_adapter, size_hint=(1, .85))
            layout.add_widget(list_view)
            # the button options
            btn_layout = BoxLayout(size_hint=(1, .15))
            reset_btn = Button(text = "reset") # the reset button
            reset_btn.bind(on_press=reset) # making the reset button call the reset function
            btn_layout.add_widget(reset_btn)
            save_btn = Button(text = "save") # the save button
            save_btn.bind(on_press=save) # making the save button call the save function
            btn_layout.add_widget(save_btn)
            layout.add_widget(btn_layout)
            return layout

        # how to reset
        def reset(instance):
            current_time = 0 # updating the clock
            setattr(time_lbl, 'text', str(current_time)) # updating the time label
            setattr(clock_lbl, 'text', clock_label(current_time)) # updating the clock
            setattr(slid, 'value', 0)
            task_combo.reset
            task_combo.cash = copy.deepcopy(task_combo.save_money)
            for task in task_group:
                task.reset()
            pop_up_end_game.dismiss() 
            self.clear_widgets() # clear
            self.add_widget(start_screen()) # back to start

        # save to file
        def save(instance):
            save_file = open("save_state.txt", "w")
            data = [] # text saved
            data.append("Information \n")
            data.append("End Time: " + clock_label(int(time_lbl.text)) + " \n")
            data.append("Final cash: "+ str(task_combo.cash) + " \n")
            data.append("--  --  --  --  --  --  --  --  --  --  --  --  -- \n")
            data.append("Information on each task"+ " \n")
            data.append("--  --  --  --  --  --  --  --  --  --  --  --  -- \n")
            for i in range(len(task_group)):
                stats = task_group[i].startState[12]
                if task_group[i].startState[12][0][4] == 0:
                    data.append("Task: " + task_group[i].task_name+ " \n")
                    data.append("It has not run yet"+ " \n")
                    data.append("Input queue length: "+  str([float(int(term*100))/100 for term in stats[2]]) + " items"+ " \n")
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  -- \n")
                else:
                    data.append("Task: " + task_group[i].task_name + " \n")  
                    data.append("Time on: " + str(int(float(100*stats[0][0])/stats[0][4])) +  "%"+ " \n")
                    data.append("Time setting up: " + str(int(float(100*stats[0][1])/stats[0][4])) +  "%"+ " \n")
                    data.append("Time making something: " + str(int(float(100*stats[0][2])/stats[0][4])) +  "%"+ " \n")
                    data.append("Time starved: " + str(int(float(100*stats[0][3])/stats[0][4])) +  "%"+ " \n")
                    data.append("Items proccessed: " +  str(stats[1])+ " \n")
                    data.append("Input queue length: " +  str([float(int(term*100))/100 for term in stats[2]])+ " \n")
                    if task_combo.sell_amounts[task_group[i]] != 0:
                        data.append("Items sold: " + str(task_combo.sell_amounts[task_group[i]])+ " \n")
                    data.append("--  --  --  --  --  --  --  --  --  --  --  --  -- \n")
            for line in data:
                save_file.write(line)
                print line
            save_file.close
            
        end_game_content = end_game_block(task_group, task_combo)
        pop_up_end_game = Popup(title='Game Over', content=end_game_content, size_hint=(.7, .7), auto_dismiss=False)
        # what happens when you lose
        def end_game(reason):
            clock.unschedule(pressed_step)
            setattr(slid, 'value', 0)
            if reason == "out of time":
                setattr(pop_up_end_game, 'content', end_game_block(task_group, task_combo))
                pop_up_end_game.open()
                pass
            if reason == "couldn't pay bills":
                setattr(pop_up_end_game, 'content', end_game_block(task_group, task_combo))
                pop_up_end_game.open()
            if reason == "quit":
                setattr(pop_up_end_game, 'content', end_game_block(task_group, task_combo))
                pop_up_end_game.auto_dismiss=True # if you quit, you can change your mind
                pop_up_end_game.open()
                
        def quit_game(instance):
            reason = "quit"
            end_game(reason)
            
        

            
        def update(instance):
            if int(time_lbl.text) == "out of time":
                end_game("out of time")
                return False
            setattr(money_lbl, 'text', str(task_combo.cash))
            for item1 in task_layout.children:
                if type(item1)== add_task_view:
                    task = item1.task
                    # set the progress bar and background
                    if task.startState[8][0]: 
                        setattr(item1.progress_bar.pb, 'max',  task.startState[2])
                        setattr(item1.progress_bar.pb, 'value', task.startState[9][0])
                        item1.remove_widget(item1.progress_bar_back)
                        item1.progress_bar_back = yellow_cell()
                        item1.progress_bar_back.size_hint=(1, .05)
                        item1.progress_bar_back.pos_hint={'x':0, 'y':.95}
                        item1.add_widget(item1.progress_bar_back)
                        item1.remove_widget(item1.progress_bar)
                        item1.add_widget(item1.progress_bar)
                    else:
                        setattr(item1.progress_bar.pb, 'max',  task.startState[3])
                        setattr(item1.progress_bar.pb, 'value', task.startState[9][0])
                        item1.remove_widget(item1.progress_bar_back)
                        item1.progress_bar_back = green_cell()
                        item1.progress_bar_back.size_hint=(1, .05)
                        item1.progress_bar_back.pos_hint={'x':0, 'y':.95}
                        item1.add_widget(item1.progress_bar_back)
                        item1.remove_widget(item1.progress_bar)
                        item1.add_widget(item1.progress_bar)
                    setattr(item1.input_labels.inp_lbl, 'text',  str(task.startState[6]))
                    if task.startState[10][0]:
                        setattr(item1.on_block.on_off_btn, 'text', 'Turn on')
                        setattr(item1.image_gif.image, 'source' , 'robot.png')
                    else:
                        setattr(item1.on_block.on_off_btn, 'text', 'Turn off')
                        setattr(item1.image_gif.image, 'source' , 'robot_gif.gif')
                        setattr(item1.image_gif.image, 'anim_delay' , .08)
                    setattr(item1.output_labels.out_lbl, 'text',  str(task.startState[7]))


        update_clock = Clock
        update_clock.schedule_interval(update, .001) # how often to update the gui

        
        
        def OnSpeedSliderValueChange(instance,value): # what happens when the slider is changed
            speed_lbl.text = "speed: " + str(value) # change the label above it to show the speed
            if value == 0:
                clock.unschedule(pressed_step) # if the speed is on 0 the steps stops
            else:
                clock.unschedule(pressed_step) # stop the old clock
                clock.schedule_interval(pressed_step, 1/value) # restart a new clock at the new speed

        def popup_reload(instance): # info popup
            setattr(popup_info, 'content', stats_block(task_group, task_combo))
            popup_info.open()

        
        
        # creating the control layout
        stats_content = stats_block(task_group, task_combo)
        popup_info = Popup(title='Stats', content=stats_content, size_hint=(.4, .4))
        stats_btn = Button(text = "Info", size_hint = (.5, 1))
        stats_btn.bind(on_release=popup_reload)
        
        slid.bind(value=OnSpeedSliderValueChange) # making the slider call the changing speed function
        speed_lbl = Label(text = " Speed: " + str(getattr(slid, 'value')), size_hint = (.5,1)) # the speed label               
        quit_btn = Button(text = "Quit", size_hint = (.5, 1)) # the reset button
        quit_btn.bind(on_press=quit_game) # making the reset button call the reset function
        

        
        controls_layout.add_widget(quit_btn) # adding the reset button # doesn't work yet
        controls_layout.add_widget(stats_btn) # adding the stats button # doesn't work yet
        controls_layout.add_widget(Label(text = "Time: ", bold = True, color = [0,1,0,1], size_hint = (.5,1)))
        controls_layout.add_widget(clock_lbl) # showing the clock
        controls_layout.add_widget(Label(text = "Cash: ", bold = True, color = [0,1,0,1], size_hint = (.5,1)))
        controls_layout.add_widget(money_lbl) # ading the time label, shows how many time steps have passed
        controls_layout.add_widget(slid) # adding the slider
        controls_layout.add_widget(speed_lbl) # adding the speed label
        controls_layout.add_widget(time_lbl) # keeping track of the time
        
        
        
        input_node = Label(text = 'inputs', size_hint = (.1,1))
        output_node = Label(text = 'outputs', size_hint = (.1,1))
        #top_bar_layout.add_widget(input_node)
        top_bar_layout.add_widget(controls_layout)
        #top_bar_layout.add_widget(output_node)

        # add the two layouts to the full screen
        self.add_widget(top_bar_layout)
        self.add_widget(task_layout)

        with self.canvas.before:
            Color(.2, 0, 0, 1)  # black background so it is not see through
            self.rect = Rectangle(size=self.size, pos=self.pos)
        # size will stay the same as the full widget
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value): # make sure it always fills the whole space 
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        

class start_screen(BoxLayout):
    def __init__(self, **kwargs):
        super(start_screen, self).__init__(**kwargs)
        def run_sim_1(instance):
            # which task group to use
            task_group = rl.OPT_G
            # make the task combo
            task_combo = rl.OPT_C
            # the successors dictionairy
            task_successors = sim.make_dict(task_group) # the dictionairy that shows where ech task exports to
            following_task = {} # the dictionairy that only shows the task and not the index of the next tasks
            for task in task_successors:
                if type(task_successors[task][0]) != tuple:
                    following_task[task] = [task_successors[task][0]]
                else:
                    following_task[task] = [term[0] for term in task_successors[task]]
            # the task tree and demensions 
            (task_grid, grid_width, grid_length) = sim.make_grid(task_group)
            start_popup.dismiss()
            self.add_widget(game(task_group, task_combo, task_successors, following_task, task_grid, grid_width, grid_length))
        def run_sim_2(instance):
            # which task group to use
            task_group = rl.MG1
            # make the task combo
            task_combo = rl.MC1
            # the successors dictionairy
            task_successors = sim.make_dict(task_group) # the dictionairy that shows where ech task exports to
            following_task = {} # the dictionairy that only shows the task and not the index of the next tasks
            for task in task_successors:
                if type(task_successors[task][0]) != tuple:
                    following_task[task] = [task_successors[task][0]]
                else:
                    following_task[task] = [term[0] for term in task_successors[task]]
            # the task tree and demensions 
            (task_grid, grid_width, grid_length) = sim.make_grid(task_group)
            start_popup.dismiss()
            self.add_widget(game(task_group, task_combo, task_successors, following_task, task_grid, grid_width, grid_length))
        def run_sim_3(instance):
            # which task group to use
            task_group = rl.AG
            # make the task combo
            task_combo = rl.AC
            # the successors dictionairy
            task_successors = sim.make_dict(task_group) # the dictionairy that shows where ech task exports to
            following_task = {} # the dictionairy that only shows the task and not the index of the next tasks
            for task in task_successors:
                if type(task_successors[task][0]) != tuple:
                    following_task[task] = [task_successors[task][0]]
                else:
                    following_task[task] = [term[0] for term in task_successors[task]]
            # the task tree and demensions 
            (task_grid, grid_width, grid_length) = sim.make_grid(task_group)
            start_popup.dismiss()
            self.add_widget(game(task_group, task_combo, task_successors, following_task, task_grid, grid_width, grid_length))
        def run_self_sim(instance):
            # which task group to use
            task_group = rl.tg
            # make the task combo
            task_combo = rl.tc
            # the successors dictionairy
            task_successors = sim.make_dict(task_group) # the dictionairy that shows where ech task exports to
            following_task = {} # the dictionairy that only shows the task and not the index of the next tasks
            for task in task_successors:
                if type(task_successors[task][0]) != tuple:
                    following_task[task] = [task_successors[task][0]]
                else:
                    following_task[task] = [term[0] for term in task_successors[task]]
            # the task tree and demensions 
            (task_grid, grid_width, grid_length) = sim.make_grid(task_group)
            start_popup.dismiss()
            self.add_widget(game(task_group, task_combo, task_successors, following_task, task_grid, grid_width, grid_length))        
        btn_layout = BoxLayout(orientation = 'vertical')
        btn_pre = BoxLayout()
        btn_1 = Button(text = 'Sim 1')
        btn_1.bind(on_release = run_sim_1)
        btn_2 = Button(text = 'Sim 2')
        btn_2.bind(on_release = run_sim_2)
        btn_3 = Button(text = 'Sim 3')
        btn_3.bind(on_release = run_sim_3)
        btn_pre.add_widget(btn_1)
        btn_pre.add_widget(btn_2)
        btn_pre.add_widget(btn_3)
        btn_self = Button(text = 'Use your own sim')
        btn_self.bind(on_release = run_self_sim)
        btn_layout.add_widget(btn_pre)
        btn_layout.add_widget(btn_self)
        btn_layout.add_widget(Label(text = "Copyright (c) <2014> \n <Brian Wheatman, Andre Calmon, Stephen Graves>"))
        
        start_content = btn_layout
        
        start_popup = Popup(title='Start', content=start_content, size_hint=(.7, .7), auto_dismiss=False)
        start_popup.open()
    
########################################################################
class Sim(App):
    
    #----------------------------------------------------------------------
    def build(self): # when its built load the start screen
        return start_screen()

#----------------------------------------------------------------------
app = Sim()
app.run() # run the app
