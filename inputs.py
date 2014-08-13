# // Copyright (c) <2014> <Brian Wheatman>
import simulator as sim
import os
Task = sim.Task
TaskCombo = sim.TaskCombo
make_grid = sim.make_grid
# to read the text document define a factory
def read_input(doc):
    group = [] # the group of tasks
    text = open(doc, 'r') # open the document to read
    
    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'How many different tasks do you have? (an integer)\n': # the line I am looking for
            break
    number_of_tasks = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form
    
    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'How much money to start with? (an integer)\n': # the line I am looking for
            break
    money = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form
    
    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'What is the period length? (an integer number of time steps)\n': # the line I am looking for
            break
    length_period = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'How many periods are there? (an integer)\n': # the line I am looking for
            break
    number_periods = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'What is the period cost? (an integer)\n': # the line I am looking for
            break
    period_cost = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

    for j in range(number_of_tasks): # for each task
        for i in range(10): # finding the task name
            line = text.readline()
            if line == 'Task name?\n': # the line I am looking for
                break
        task_name = text.readline().replace('-', '').replace('\n', '').replace(' ', '') # converting it to the right form

        for i in range(10): # which robot
            line = text.readline()
            if line == 'What robot will be completing the task?\n': # the line I am looking for
                break
        robot_id = text.readline().replace('-', '').replace('\n', '').replace(' ', '') # converting it to the right form

        for i in range(10): # what inputs
            line = text.readline()
            if line == 'What inputs are used? (the name of each input seperated by commas)\n': # the line I am looking for
                break
        inputs = text.readline().replace('-', '').replace('\n', '').replace(' ', '').split(',') # converting it to the right form

        for i in range(10): # how many of the inputs
            line = text.readline()
            if line == 'How many of each input is nessasary to make one round of outputs? (integers, same order as above, seperated by commas)\n':  # the line I am looking for
                break
        number_inputs = [int(term) for term in text.readline().replace('-', '').replace('\n', '').replace(' ', '').split(',')] # converting it to the right form
        
        for i in range(10): # set up times
            line = text.readline()
            if line == 'The number of time steps it taks to set up? (an integer)\n': # the line I am looking for
                break
        set_up = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

        for i in range(10): # processing times
            line = text.readline()
            if line == 'The number of time steps to process one set of inputs? (an integer)\n': # the line I am looking for
                break
        processing = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

        for i in range(10): # output
            line = text.readline()
            if line == 'What the output is?\n': # the line I am looking for
                break
        output = text.readline().replace('-', '').replace('\n', '').replace(' ', '') # converting it to the right form

        for i in range(10): # outputs a round
            line = text.readline()
            if line == 'How many outputs are made each round? (an integer)\n': # the line I am looking for
                break
        outputs_a_round = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

        for i in range(10): # input queue
            line = text.readline()
            if line == 'How many of each item starts in the input queue? (integers seperated by commas)\n': # the line I am looking for
                break
        queue = [int(term) for term in text.readline().replace('-', '').replace('\n', '').replace(' ', '').split(',')] # converting it to the right form

        for i in range(10): # input price
            line = text.readline()
            if line == "How much does it cost to buy an input? (integers seperated by commas, 0 if it can't be bought)\n": # the line I am looking for
                break
        input_price = [int(term) for term in text.readline().replace('-', '').replace('\n', '').replace(' ', '').split(',')] # converting it to the right form

        for i in range(10): # output price
            line = text.readline()
            if line == "How much can you sell an output for? (an integer, 0 if it can't be sold)\n": # the line I am looking for
                break
        output_price = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form

        task_name = Task(inputs, number_inputs, set_up, processing,output,\
                          outputs_a_round, queue, [0], [True], [0], [True], [False],\
                          [[0,0,0,0,0],0,0], robot_id, input_price, output_price, str(task_name) )
        group.append(task_name)
    limitations = {}
    for i in range(10): # looking through a couple of lines to find the right one
        line = text.readline()
        if line == 'How many limitations are there? (A limitation is a rule that says one output can only sell an amount up to the amount sold of another output)\n':
            break
    num_limits = int(text.readline().replace('-', '').replace('\n', '').replace(' ', '')) # converting it to the right form
    
    skip = text.readline()
    
    for j in range(num_limits):
        line = [int(term)-1 for term in text.readline().replace('-', '').replace('\n', '').replace(' ', '').split(',')]
        limitations[group[line[0]]]=group[line[1]]

    return (group, limitations, money, period_cost, length_period, number_periods)
# declaring the groups and factories
(group, limitations, money, period_cost, length_period, number_periods) = read_input(str(os.getcwd()) + '\input_group.txt')
tg = group
tc = TaskCombo(tg, limitations, money, period_cost, length_period, number_periods)

(group, limitations, money, period_cost, length_period, number_periods) = read_input(str(os.getcwd()) + '\sim1.txt')
OPT_G = group
OPT_C = TaskCombo(OPT_G, limitations, money, period_cost, length_period, number_periods)

(group, limitations, money, period_cost, length_period, number_periods) = read_input(str(os.getcwd()) + '\sim2.txt')
MG1 = group
MC1 = TaskCombo(MG1, limitations, money, period_cost, length_period, number_periods)

(group, limitations, money, period_cost, length_period, number_periods) = read_input(str(os.getcwd()) + '\sim3.txt')
AG = group
AC = TaskCombo(AG, limitations, money, period_cost, length_period, number_periods)

