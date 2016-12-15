from sys import maxint
from random import randint

# Bad input case(s):
# 0. 1 <= total cylinders
# 1. Each cylinder number < total number of cylinders
# 2. 0 <= cylinder number
# Internal error(s):
# 3. 0 <= curr_head < total cylinders

# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, cylinder_number):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Please enter valid total number of cylinders.\n" + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = str(cylinder_number) + " cylinder entered in disk queue exceeds the total number of cylinders entered. Please enter a valid cylinder number.\n" + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = str(cylinder_number) +  " cylinder is invalid. Please enter a valid cylinder number.\n" + default_message
        ERROR['error_number'] = 2
    elif error_number == 3:
        ERROR['error_message'] = "Please enter a valid current head position.\n" + default_message
        ERROR['error_number'] = 3
    return ERROR

def check_for_bad_input(data):
    error = 0 # Boolean to check bad input 
    error_status = {} # Dictionary to store error number and error message
    curr_head_pos = int(data['curr_pos'])
    num_cylinders = int(data['total_cylinders'])
    disk_queue = data['disk_queue']
    if  num_cylinders <= 0:
        error_status = get_error_message(0,-1)
        error = 1 
    elif curr_head_pos <= 0 or curr_head_pos >= num_cylinders:
        error_status = get_error_message(3,-1)
        error = 1
    else:
        for cylinder in disk_queue:
            if int(cylinder) > num_cylinders - 1:
                error_status = get_error_message(1, int(cylinder))
                error = 1
                break
            if int(cylinder) < 0:
                error_status = get_error_message(2,int(cylinder))
                error = 1
                break
        if(error == 0):
            error_status = get_error_message(-1, -1) # No error in input data
            error = 0
    status = (error, error_status);
    return status


# For Scan and Look Algorithms
def calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos):
    memory_state.append(chosen_cylinder)
    difference = abs(int(chosen_cylinder) - curr_head_pos)
    return difference

def c_scan_or_c_look(curr_head_pos, num_cylinders, disk_queue, next_larger_pos, direction, algo):
    total_head_movements = 0 # To keep track of the total number of read/write head movements
    memory_state = [] # To keep track of the order in which cylinders are visited
    memory_state.append(curr_head_pos)

    if(direction == 0): # Inward direction
        start_idx = next_larger_pos - 1
        for i in range(next_larger_pos):
            chosen_cylinder = disk_queue[start_idx]
            start_idx = start_idx -1
            memory_state.append(chosen_cylinder)
            difference = abs(int(chosen_cylinder) - curr_head_pos)
            total_head_movements += difference
        curr_head_pos = int(chosen_cylinder)
        if(algo == 3):
            chosen_cylinder = 0
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)
            chosen_cylinder = num_cylinders - 1
            memory_state.append(chosen_cylinder)
            curr_head_pos = int(chosen_cylinder)
        if(algo == 5):
            curr_head_pos = disk_queue[-1]
        for i, cylinder in reversed(list(enumerate(disk_queue[next_larger_pos:]))):
            memory_state.append(cylinder)
            difference = abs(int(cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(cylinder)
    else: # Outward direction
        for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
            memory_state.append(cylinder)
            difference = abs(int(cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(cylinder)
        if(algo == 3):
            chosen_cylinder = num_cylinders - 1
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)
            chosen_cylinder = 0
            memory_state.append(chosen_cylinder)
            curr_head_pos = int(chosen_cylinder)
        if(algo == 5):
            curr_head_pos = disk_queue[0]
        for i, cylinder in enumerate(disk_queue[0:next_larger_pos]):
            chosen_cylinder = cylinder
            memory_state.append(chosen_cylinder)
            difference = abs(int(chosen_cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(chosen_cylinder)

    status = (memory_state, total_head_movements);
    return status

def scan_or_look(curr_head_pos, num_cylinders, disk_queue, next_larger_pos, direction, algo):
    total_head_movements = 0 # To keep track of the total number of read/write head movements
    memory_state = [] # To keep track of the order in which cylinders are visited
    memory_state.append(curr_head_pos)

    if(direction == 0): # Inward direction
        start_idx = next_larger_pos - 1
        for i in range(next_larger_pos):
            chosen_cylinder = disk_queue[start_idx]
            start_idx = start_idx -1
            memory_state.append(chosen_cylinder)
            difference = abs(int(chosen_cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(chosen_cylinder)
        if(algo == 2):
            chosen_cylinder = 0
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)
        for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
            memory_state.append(cylinder)
            difference = abs(int(cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(cylinder)
        if(algo == 2):
            chosen_cylinder = num_cylinders - 1
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)
    else: # Outward direction
        for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
            memory_state.append(cylinder)
            difference = abs(int(cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(cylinder)
        if(algo == 2):
            chosen_cylinder = num_cylinders - 1
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)
        start_idx = next_larger_pos - 1
        for i in range(next_larger_pos):
            chosen_cylinder = disk_queue[start_idx]
            start_idx = start_idx -1
            memory_state.append(chosen_cylinder)
            difference = abs(int(chosen_cylinder) - curr_head_pos)
            total_head_movements += difference
            curr_head_pos = int(chosen_cylinder)
        if(algo == 2):
            chosen_cylinder = 0
            total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
            curr_head_pos = int(chosen_cylinder)

    status = (memory_state, total_head_movements);
    return status

def shortest_seek_time_first(curr_head_pos, disk_queue):
    total_head_movements = 0 # To keep track of the total number of read/write head movements
    memory_state = [] # To keep track of the order in which cylinders are visited
    memory_state.append(str(curr_head_pos))

    # To find the next cylinder with shortest seek time till the disk queue is empty
    while len(disk_queue) > 0:
        min_seek = maxint # To track the cylinder with minimum seek time from current head position
        min_idx = -1
        for idx, cylinder in enumerate(disk_queue):
            # Bad input handling 
            if int(cylinder) > num_cylinders - 1:
                error_number = 1
                error_status = get_error_message(error_number, int(cylinder))
                break
            if abs(int(cylinder) - curr_head_pos) < min_seek:
                min_seek = abs(int(cylinder) - curr_head_pos)
                min_idx = idx
            elif abs(int(cylinder) - curr_head_pos) == min_seek:
                min_seek = abs(int(cylinder) - curr_head_pos) 
                min_idx = randint(idx, min_idx)
        if error_number != -1:
            break
        chosen_cylinder = disk_queue[min_idx]
        memory_state.append(chosen_cylinder)
        difference = abs(int(chosen_cylinder) - curr_head_pos)
        total_head_movements += difference
        curr_head_pos = int(chosen_cylinder)
        del disk_queue[min_idx]

    status = (memory_state, total_head_movements);
    return status

def first_come_first_serve(curr_head_pos, disk_queue):
    total_head_movements = 0 # To keep track of the total number of read/write head movements
    memory_state = [] # To keep track of the order in which cylinders are visited
    memory_state.append(str(curr_head_pos))

    for cylinder in disk_queue:
        memory_state.append(cylinder)
        difference = abs(int(cylinder) - curr_head_pos)
        total_head_movements += difference
        curr_head_pos = int(cylinder)

    status = (memory_state, total_head_movements);
    return status

# Returning the output as a dictionary
def construct_output(error_status, secondary_storage_memory, total_head_movements):
    # To store secondary memory chart and total number of head movements 
    secondary_storage_chart = {}
    secondary_storage_chart['memory_state'] = secondary_storage_memory
    secondary_storage_chart['total_head_moves'] = total_head_movements
    secondary_storage_chart['error_status'] = error_status
    print str(secondary_storage_chart)
    return secondary_storage_chart

# Main function to call algo chosen by the user
def disk_scheduling(data):
    # To store secondary memory chart and total number of head movements 
    secondary_storage_chart = {}
    # For bad input handling
    error, error_status = check_for_bad_input(data)
    if(error):
        secondary_storage_chart = construct_output(error_status, -1, -1)
        return secondary_storage_chart
    else:
        curr_head_pos = int(data['curr_pos'])
        num_cylinders = int(data['total_cylinders'])
        disk_queue = data['disk_queue']
        # For Scan, C-Scan, Look and C-Look algorithms
        if data['algo'] != 0 and data['algo'] != 1:
            direction = data['direction']

        if data['algo'] == 0:
            secondary_storage_memory, total_head_movements = first_come_first_serve(curr_head_pos, disk_queue)
        elif data['algo'] == 1:
            secondary_storage_memory, total_head_movements = shortest_seek_time_first(curr_head_pos, disk_queue)
        else:
            larger = curr_head_pos # To find the next largest cylinder to current head position
            new_disk_queue=list(map(int, disk_queue))
            disk_queue = sorted(new_disk_queue)
            for idx, cylinder in enumerate(disk_queue):
                if(int(cylinder) > curr_head_pos):
                    larger = idx 
                    break
            if data['algo'] == 2 or data['algo'] == 4:
                secondary_storage_memory, total_head_movements = scan_or_look(curr_head_pos, num_cylinders, disk_queue, larger, direction, data['algo'])
            elif data['algo'] == 3 or data['algo'] == 5:
                secondary_storage_memory, total_head_movements = c_scan_or_c_look(curr_head_pos, num_cylinders, disk_queue, larger, direction, data['algo'])
        secondary_storage_chart = construct_output(error_status, secondary_storage_memory, total_head_movements)
        return secondary_storage_chart