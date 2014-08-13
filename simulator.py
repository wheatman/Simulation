# // Copyright (c) <2014> <Brian Wheatman>

from collections import Counter
import random
import copy

# the basic task
class Task():
    def __init__(self, set_inputs, inputs_to_output, set_up_time, processing_time,\
                 output, output_a_round, items_waiting , items_done, in_set_up, counter , on_off , broken, stats, robot_id, \
                 price_input, price_output, task_name = ""):
        # each task will store
        # # what the task can take (list of strings)
        # # how many inputs it takes a round (list of ints)
        # # set up time (float)
        # # processing time for each (float)
        # # what the robot outputs (string)
        # # how many outputs made in a round (int)
        # # items waiting to be processed on [list of ints]
        # # items already processed (list of int)
        # # whether or not the robot is currently in a setup phase (Boolean)
        # # a counter (list of int)
        # # whether or not the task is in use (boolean)
        # # whether or not the task is broken (boolean)
        # # stats about the task (list)
        # # # [[time on, time setting up, time producing, idle time, total time], number of exports, [average length of queues]]
        stats[2] = [0]*len(set_inputs)
        self.startState=[set_inputs, inputs_to_output, set_up_time, processing_time,\
                 output, output_a_round, items_waiting, items_done, in_set_up, counter, on_off, broken, stats]
        self.id = robot_id
        self.save_startState = copy.deepcopy(self.startState)
        self.input_price = price_input
        self.output_price = price_output
        self.task_name= task_name
        self.push = False
        self.number_push = 1 # for now push all
        """
        state[0] = input list
        state[1] = inputs to outputs
        state[2] = set up times
        state[3] = processing times
        state[4] = output
        state[5] = outputs a timestep
        state[6] = items in queue
        state[7] = finished items
        state[8] = if in set up
        state[9] = counter
        state[10] = if it is on or off, true is off false is on
        state[11] = if broken
        state[12] = stats
        state[12][0] = time information
        state[12][0][0] = time on
        state[12][0][1] = time seting up 
        state[12][0][2] = time making something
        state[12][0][3] = time starved
        state[12][0][4] = total time
        state[12][1] = total number of outputs
        state[12][2] = average length of queue
        """
        

    def __repr__(self):
        # the task will tell about itself when you print it
        state = self.startState
        a0 = self.task_name # + "\n"
        a1 = "this task is done by robot " + str(self.id) + "\n"
        a = "This task takes input " + str(state[0]) + "\n"
        b = "It takes " + str(state[1]) + " inputs each round.\n"
        c = "This task takes " + str(state[2]) + " minutes to set up.\n"
        d = "This task takes " + str(state[3]) + " minutes to process each item.\n"
        e = "This task outputs " + state[4] + "\n"
        f = "It makes " + str(state[5]) + " outputs each round.\n"
        g = "This task has " + str(state[6]) + " items waiting.\n"
        h = "This task has " + str(state[7]) + " items finished.\n"
        if state[8][0]:
            i = "This task is currently in the setup phase.\n"
        else:
            i = "This task is not currently in the setup phase.\n"
        if state[10][0]:
            j = "This task is currently off.\n"
        else:
            j = "This task is currently on.\n"
        if state[11][0]:
            k = "This task is currently broken.\n"
        else:
            k = "This task is not currently broken.\n"
        l = "counter is at " + str(state[9][0]) + ".\n"
        m = "this task has been running for " + str(state[12][0][0]) + " minutes\n"
        n = "this task has exported  " + str(state[12][1]) + " items\n"
        return a0# +a1+a#+b+c+d+e+f+g+h+i+j+k+l+m+n # how much to show to make it easier to display
    
    # to change what the task takes as input
    def set_input(self,input_list):
        self.startState[0] = input_list
        
    # to change the set up times
    def set_set_up_time(self, set_up_time):
        self.startState[2] = set_up_time
        
    # to change the processing times
    def set_processing_time(self, processing_time):
        self.startState[3] = processing_time
        
    # to change what the output is
    def set_output(self, output):
        self.startState[4] = output
        
    # to add items to the group that will be processed
    def add_items_to_queue(self,index_of_item, number_of_items_to_add):
        self.startState[6][index_of_item] += number_of_items_to_add

    # to edit the queue as a whole
    def set_queue(self, queue):
        self.startState[6] = queue

    # removes an item from the cue and return true if it is able to remove an item
    def remove_items(self, items_to_remove):
        if self.startState[7][0] >= items_to_remove: # if there are enough items to remove
            self.startState[7][0] -= items_to_remove # remove the item
            return True
        
    #set how many items have been finished
    def set_finished_items(self, finished):
        self.startState[7] = finished

    # take out of or put into set up
    def set_mode(self, mode):
        self.startState[8][0] = mode

    # set the counter
    def set_counter(self, counter):
        self.startState[9] = counter

    
    # it is posiple to add the ability to break and fix robots, but this is not currently in use
    # checking if the task can be fixed
    def fix(self):
        if random.random()<=1: # probability of being able to fix it
            self.startState[11][0] = False

    # checking if the task broke
    def damage(self):
        if random.random()<=1:# probability of it breaking
            self.startState[11][0] = True

    # set the stats
    def set_stats(self, stats):
        self.startState[12] = stats

    # turn the task on or off
    def on_off(self):
        if self.startState[10][0] == False: # if it is on
            self.startState[10][0] = True # turn it off
            self.startState[8][0] = True # make it need set up
            self.startState[9][0] = 0 # set the counter to 0
        else:
            self.startState[10][0] = False # turn it on
            self.startState[8][0] = True # make it need set up
            self.startState[9][0] = 0 # set the counter to 0

    # reset the task back to its starting values
    def reset(self):
        self.startState = copy.deepcopy(self.save_startState) 

    # weather or not the task auto pushes
    def push_switch(self):
        if self.push:
            self.push = False
        else:
            self.push = True

    # how many push at a time
    def set_push_number(self, number):
        self.number_push = number
    
          
            
    # to get the next value for the state machine   
    def getNextValues(self, state):
        #giving the variables names so they are easier to use
        [set_inputs, inputs_to_output, set_up_time, processing_times,\
                 output, output_a_round, items_waiting, items_done, in_set_up, counter, on_off, broken, stats] = state
        len_items_waiting = len(items_waiting) # to avoid looping
        #check if the task can be used
        if broken[0]:
            pass 
        elif on_off[0]:
            pass
        elif in_set_up[0]: # if it is in set up
            if counter[0] >= set_up_time: # if time passed is equal to set up time
                in_set_up[0] = False # take it out of set up mode
                counter[0] = 0 # and reset the counter
        else: # if it is not in setup mode
            if counter[0] >= processing_times: # if enough time has passed that an item has been made
                # check if I could use an if any construction here
                dummy = 0 #dummy variable
                for i in range(len_items_waiting): # check enumerate
                    if items_waiting[i] < inputs_to_output[i]: # and if there are still enough items waiting to be made
                        dummy += 1
                if dummy == 0:
                    for i in range(len_items_waiting):
                        items_waiting[i] -= inputs_to_output[i] # remove items from the items waiting
                    items_done[0] += output_a_round # add items to the items done
                    stats[1] += output_a_round #keep track of how many outputs have been done total
                    counter[0] = 0 # reset the counter
        a = "This task has " + str(state[6]) + " items waiting.  "
        b = "This task has " + str(state[7]) + " items finished.  "
        output = a+b
        stats[0][4] += 1 # total time
        if in_set_up[0]:
            if not on_off[0]:
                counter[0] += 1 # always increase the counter if it is setting up and on
        if not in_set_up[0]:
            dummy2 = 0 # dummy variable
            for i in range(len_items_waiting):
                if items_waiting[i] < inputs_to_output[i]: # and if there are still enough items waiting to be made
                    dummy2 += 1
            if dummy2 == 0:
                counter[0] += 1 # only increase the counter if there are items that the robot could be processing
                stats[0][2] += 1 # time making something
        if not broken[0] and not on_off[0]: 
            stats[0][0] += 1 # keep track of the total number of time steps
            if in_set_up[0]:
                stats[0][1] +=1 # time in set up
        stats[0][3] = stats[0][0] - stats[0][1] - stats[0][2] # time starved
        for i in range(len(stats[2])):
            if stats[0][4] == 0: # total time
                stats[2][i] = 0 # average length of queue
            else:
                stats[2][i] = (float(stats[2][i]*(stats[0][4]-1)+items_waiting[i]))/stats[0][4] # average length of queue
        state = [set_inputs, inputs_to_output, set_up_time, processing_times,\
                 output, output_a_round, items_waiting, items_done, in_set_up, counter, on_off, broken, stats]
        return (state, output)
    
# to have a group of tasks connected in a push way
class TaskCombo():
    def __init__(self,task_group, limitations = {}, money = 0,\
                 period_cost = 0, length_period= 2400, number_periods = 2 ):
        self.task_successors = make_dict(task_group) #create dictionaries that keep track of flow
        stats = [0]
        self.startState = [task_group, stats] # the task list and stats
        self.save_startState = copy.deepcopy(self.startState) # to be able to reset
        self.cash = money 
        self.save_money = copy.deepcopy(self.cash)
        self.limitations = limitations # of the form lim[T1] = T2, meaning T1 cant sell more than T2
        self.time_limit = length_period*number_periods # time to the end of the game
        self.period_cost = period_cost # how much the bills are per period
        self.length_period = length_period # how long each period is
        self.number_periods = number_periods # how many periods there are
        
        self.push_direction = {} # what direction is everythng currently pushing
        for task in self.task_successors: # for each task that has something to push to
            if self.task_successors[task][0] in task_group: # if it can only push to one task
                self.push_direction[task] = self.task_successors[task]
            else: # if it has multiple options
                self.push_direction[task] = self.task_successors[task][0]# give it the first option
        self.sell_amounts = {} # how much has each task sold
        for task in task_group:
            self.sell_amounts[task] = 0
        
        
    def __repr__(self):
        # when printed, print out the information for each task and the total time
        state = self.startState
        string = ""
        for i in range(len(state[0])):
            string = string + "task " + str(i+1) + " \n" +state[0][i].__repr__() + " \n"
        string2 = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX the total time passed is " + str(state[1][0]) + " XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
        return string + string2
    
    def update_clock(self, time):
        self.startState[1][0] = time

    # to push
    def push_action(self, task, number, target): # task = what task is pushing; number is how many to push; target is where they are going
        if task.startState[7][0] >= number: # if there is more than the number to push 
            task.remove_items(number) # remove that number
            target[0].add_items_to_queue(target[1], number) # and add to the target
        elif task.startState[7][0] >= 1: # if there is less than the number to push
            target[0].add_items_to_queue(target[1], task.startState[7][0]) # add all of them to the queue
            task.remove_items(task.startState[7][0]) # and remove them from the task
    
    # change where a task will push
    def change_push_direction(self, task):
        for i in range(len(self.task_successors[task])):
            if self.push_direction[task] == self.task_successors[task][i]:
                self.push_direction[task] = self.task_successors[task][(i+1)%len(self.task_successors[task])] # cycle through all of the options
                break
            
    # to reset
    def reset(self):
        self.startState = copy.deepcopy(self.save_startState)
        self.cash = copy.deepcopy(self.save_money) 

    def add_money(self, amount):
        self.cash += amount

    def lose_money(self, amount):
        self.cash -= amount

    # chck if there are any splits
    def check_for_splits(self, task_group):
        for task in task_group:
            if self.task_successors[bot][0] not in task_group:
                return True
        return False
        
    
    
    def getNextValues(self, state):
        task_path = self.task_successors #the dictionary that deals with flow
        list_of_tasks = state[0] #what tasks are in this system
        output_list = [0]*len(list_of_tasks) #declaring the output list
        new_state_of_task = [0]*len(list_of_tasks[0].startState) # declaring the list that will be the next state
        len_list_of_tasks = len(list_of_tasks) #to avoid looping
        # adding and removing items accordingly to push them through the system
        for i in range(len_list_of_tasks): # for each task
            if list_of_tasks[i] in task_path: # if it is not an end
                [successor, index_of_input] = task_path[list_of_tasks[i]]
                if list_of_tasks[i].push: # if the task is on auto push
                    self.push_action(list_of_tasks[i], 100000000, self.push_direction[list_of_tasks[i]]) # push all
                        
        # resetting the tasks with the changes the last pass through had on them
        for i in range(len_list_of_tasks):
            (new_state_of_task,output_list[i])=list_of_tasks[i].getNextValues(list_of_tasks[i].startState) # getting the new values for each task
            list_of_tasks[i].set_queue(new_state_of_task[6]) # set the value
            list_of_tasks[i].set_finished_items(new_state_of_task[7]) # set the value
            list_of_tasks[i].set_counter(new_state_of_task[9]) # set the value
            list_of_tasks[i].set_stats(new_state_of_task[12]) # set the value
            list_of_tasks[i].set_mode(new_state_of_task[8][0]) # set the value
        # the next state
        time = state[1][0]+1
        stats = [time]
        self.update_clock(time)
        new_state_plus_stats = [list_of_tasks, stats]
        return (new_state_plus_stats, output_list)
        

# create a dictionary to keep track of how the items flow through the factory
def make_dict(task_group):
    task_successors = {} #declare the empty dict
    len_task_group = len(task_group) # to avoid looping
    for i in range(len_task_group): # check each one
        for j in range(len_task_group): # against every other one           
            if task_group[i].startState[4] in task_group[j].startState[0]: #if the output of one is in the input of another
                number_inputs = len(task_group[j].startState[0]) # to avoid looping
                for k in range(number_inputs): # check every input
                    if task_group[i].startState[4] == task_group[j].startState[0][k]: # if the output of one is the input of the next
                        successor = task_group[j]
                        index_of_input = k
                        # each task is the key to which robot it passes on to and which slot its output goes into
                        if task_group[i] in task_successors:
                            task_successors[task_group[i]] = (task_successors[task_group[i]], (successor, index_of_input))
                        else:
                            task_successors[task_group[i]] = (successor, index_of_input)
    return task_successors


    
# make the grid to display
def make_grid(task_group):
    task_group_edit = task_group[:] # an editable group of tasks
    task_successors = make_dict(task_group) # make the dictionairy
    following_task = {} # a dictionairy that doesn't include the index of the input
    for task in task_successors:
        if type(task_successors[task][0]) != tuple:
            following_task[task] = [task_successors[task][0]]
        else:
            following_task[task] = [term[0] for term in task_successors[task]]
    ends = []
    starts = []
    not_starts = [] # to help find starts
    for task in task_group:
        if task in following_task:
            for item in following_task[task]:
                if item not in not_starts:
                    not_starts.append(item) # if something pushes to it it is not a start
        else:
            ends.append(task) # if it pushes to nothing it is an end
            
    starts = task_group[:]
    for item in not_starts:
        starts.remove(item) 
        
    # to find all the path from one start to one ends
    def find_all_paths(graph, start, end, path=[]): 
        path = path + [start] # the path is the current path + the next start
        if start == end: # if the start is the end , the path has been found
            return [path]
        if not graph.has_key(start): # if the start has no successors there is not path
            return []
        paths = [] # all of the paths
        for node in graph[start]: # for all of the successors of the start
            if node not in path: # if that node is not already in the path
                newpaths = find_all_paths(graph, node, end, path) # strart again using that node
                for newpath in newpaths:
                    paths.append(newpath) # append all of the new paths
        return paths

    paths = []
    for start in starts: # for every start
        for end in ends: # and every end
            if find_all_paths(following_task, start, end) != []: # if there is a path
                paths.append(find_all_paths(following_task, start, end)) # append all of the paths
    task_grid = [] # the grid of the tasks
    for path in paths:
        for item in path:
            task_grid.append(item) # append all of the paths found
    grid_width = len(task_grid) # start guess for the length
    grid_length = 0
    # find the true length by finding the longest path
    for row in task_grid:
        if len(row) > grid_length:
            grid_length = len(row) 
    # make all the rows the same lenth
    for row in task_grid:
        if len(row) != grid_length:
            for dif in range(grid_length-len(row)):
                row.insert(0,None)  
    # if the task has already been placed, only show the first one            
    for i in range(grid_width):
        for j in range(grid_length):
            if task_grid[i][j] in task_group_edit:
                task_group_edit.remove(task_grid[i][j])
            else:
                task_grid[i][j] = None
    
    task_grid = [row for row in task_grid if row != [None]*grid_length] # removing empty rows from the task grid
    grid_width = len(task_grid) 
    grid_length = len(task_grid[0])
    return (task_grid, grid_width, grid_length)


# to test the simulation without the gui
# allows you to have it run for n steps
def test(a, n = 50):
    state = a.startState
    for i in range(n):
        (state, output) = a.getNextValues(state)
        #print output
        print a
