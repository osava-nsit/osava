from copy import deepcopy
from sys import maxint
from random import randint

# Bad input case(s):
# 0. 1 <= Frame number
# 1. 0 < Page number
# 2. 0 <= modify_bit <= 1

# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, page_num_or_modify_bit_pos):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Please enter valid number of frames.\n" + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = "Page number at " + str(page_num_or_modify_bit_pos) + " position in reference string is invalid. Please enter a valid page number.\n" + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = "Modify bit at position " + str(page_num_or_modify_bit_pos) + " in modify bit string is invalid. Please enter a valid modify bit ( 0 or 1 ).\n" + default_message
        ERROR['error_number'] = 2
    return ERROR

def check_for_bad_input(data):
    error = 0 # Boolean to check if bad input entered
    error_status = {} # Dictionary to store error number and error message
    frames_number = data['num_frames']
    page_numbers = data['ref_str']
    if frames_number <= 0:
        error_status = get_error_message(0, -1)
        error = 1
    else:
        for idx,page_number in enumerate(page_numbers):
            if int(page_number) < 0:
                print "Error detected"
                error_status = get_error_message(1, idx+1)
                error = 1
                break
    if(error == 1):
        status = (error, error_status);
        print "Error detected"
        return status
    else:
        if data['algo'] == 4:
            modify_bit_string = data['modify_bits'] 
            for idx,modify_bit in enumerate(modify_bit_string):
                if int(modify_bit) != 0 and int(modify_bit) != 1:
                    error_status = get_error_message(2, idx+1)
                    error = 1
                    break
        if(error == 0):
            error_status = get_error_message(-1, -1) # No error in input data
            error = 0
        status = (error, error_status);
        return status

# Utility function to check if referenced page is already in memory
def page_in_memory(page_number, memory_frames):
    for frame_number, page_n in enumerate(memory_frames):
        # If page is already in memory, return frame_number and set in_memory bit
        if page_n == page_number:
            status = (frame_number, 1);
            return status
    # If page is not already in memory 
    status = (-1, 0);
    return status

# Funtion to find and replace a page using fifo algorithm 
def find_and_replace_page_fifo(page_number, memory_frames, last_replaced_frame):
    last_replaced_frame = (last_replaced_frame + 1) % len(memory_frames)
    memory_frames[last_replaced_frame] = page_number
    status = (last_replaced_frame, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using optimal algorithm 
def find_and_replace_page_optimal(page_number, memory_frames, reference_string, pos_ref_str):
    # To keep track of page number with farthest future reference
    frame_to_be_replaced = -1
    flag = 0 # To check if an empty frame is available
    
    future_reference_pos = [] # To keep track of each page's farthest future reference
    for frame_number, page in enumerate(memory_frames):
        last_reference_pos = -1
        for idx, page_n in enumerate(reference_string[pos_ref_str:]):
             # Empty frame is available
            if page == -1:
                frame_to_be_replaced = frame_number
                flag = 1
                break
            elif page == page_n:
                last_reference_pos = idx
                break
        if flag == 1:
            break
        elif last_reference_pos == -1 :
            last_reference_pos = maxint 
        pair =(frame_number, page, last_reference_pos);
        future_reference_pos.append(pair)

     
    if flag == 0:
        # To find page with farthest reference in future
        max_pos = -1
        for pair in future_reference_pos:
            frame_number, page, last_reference_pos = pair
            if max_pos < last_reference_pos:
                max_pos = last_reference_pos
                frame_to_be_replaced = frame_number
            elif max_pos == last_reference_pos:
                max_pos = last_reference_pos
                frame_to_be_replaced =randint(frame_to_be_replaced,frame_number)

    memory_frames[frame_to_be_replaced] = page_number
    status = (frame_to_be_replaced, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using lru algorithm 
def find_and_replace_page_lru(page_number, memory_frames, reference_string, pos_ref_str):
    # To keep track of page number with nearest past reference
    frame_to_be_replaced = -1
    flag = 0 # To check if an empty frame is available
    
    past_reference_pos = [] # To keep track of each page's farthest past reference
    for frame_number, page in enumerate(memory_frames):
        last_reference_pos = -1
        for idx, page_n in enumerate(reference_string[0:pos_ref_str+1]):
             # Empty frame is available
            if page == -1:
                frame_to_be_replaced = frame_number
                flag = 1
                break
            elif page == page_n:
                last_reference_pos = idx
        if flag == 1:
            break
        pair =(frame_number, page, last_reference_pos);
        past_reference_pos.append(pair)

    
    if flag == 0:
        # To find page with farthest reference in past
        min_pos = maxint
        for pair in past_reference_pos:
            frame_number, page, last_reference_pos = pair
            if min_pos > last_reference_pos:
                min_pos = last_reference_pos
                frame_to_be_replaced = frame_number
            elif min_pos == last_reference_pos:
                min_pos = last_reference_pos
                frame_to_be_replaced =randint(frame_to_be_replaced,frame_number)
    memory_frames[frame_to_be_replaced] = page_number
    status = (frame_to_be_replaced, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using second chance algorithm 
def find_and_replace_page_second_chance(page_number, memory_frames, last_replaced_frame, reference_bit):

    flag = False # to find a frame that is to be replaced
    while(flag==False):
        last_replaced_frame = (last_replaced_frame + 1) % len(memory_frames)
        if reference_bit[last_replaced_frame] == 1:
            reference_bit[last_replaced_frame] = 0
            continue
        memory_frames[last_replaced_frame] = page_number
        flag = True
    status = (last_replaced_frame, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using enhanced second chance algorithm 
def find_and_replace_page_enhanced_second_chance(page_number, memory_frames, last_replaced_frame, reference_bit, modify_bit,pos,modify_bit_string):
    last_replaced_frame = (last_replaced_frame + 1) % len(reference_bit)
    flag = False # to find a frame that is to be replaced
    while (flag==False):
        # If an empty frame is available in memory
        for idx in range(len(reference_bit)):
            frame_number = (last_replaced_frame + idx) % len(reference_bit)
            if memory_frames[frame_number] == -1:
                last_replaced_frame = frame_number
                flag = True
                break
        if flag == True:
            break
        # Select frame to be replaced if reference bit and modify bit are both 0
        for idx in range(len(reference_bit)):
            frame_number = (last_replaced_frame + idx) % len(reference_bit )
            if reference_bit[frame_number] == 0 and modify_bit[frame_number] == 0:
                last_replaced_frame = frame_number
                flag = True
                break
        if flag == True:
            break
        # Select frame to be replaced if reference bit is 0 and modify bit is 1
        for idx in range(len(reference_bit)):
            frame_number = (last_replaced_frame + idx) % len(reference_bit )
            if reference_bit[frame_number] == 0 and modify_bit[frame_number] == 1:
                last_replaced_frame = frame_number
                flag = True
                break
        if flag == True:
            break
        # Select frame to be replaced if reference bit is 1 and modify bit is 0
        for idx in range(len(reference_bit)):
            frame_number = (last_replaced_frame + idx) % len(reference_bit )
            if reference_bit[frame_number] == 1 and modify_bit[frame_number] == 0:
                last_replaced_frame = frame_number
                flag = True
                break
        if flag == True:
            break
        # Select frame to be replaced if reference bit and modify bit are both 1
        for idx in range(len(reference_bit)):
            frame_number = (last_replaced_frame + idx) % len(reference_bit )
            if reference_bit[frame_number] == 1 and modify_bit[frame_number] == 1:
                last_replaced_frame = frame_number
                flag = True
                break

    if modify_bit_string[pos] == 1:
        reference_bit[last_replaced_frame] = 1
        modify_bit[last_replaced_frame] = 0
    else:
        reference_bit[last_replaced_frame] = 0
        modify_bit[last_replaced_frame] = 1  

    memory_frames[last_replaced_frame] = page_number
    status = (last_replaced_frame, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using lfu algorithm 
def find_and_replace_page_least_frequently_used(page_number, memory_frames, reference_string, pos_ref_str):
    # To keep track of page number with minimum reference in past
    frame_to_be_replaced = -1
    flag = 0 # To check if an empty frame is available
    
    freq_reference_pos = [] # To keep track of each page's number of references
    for frame_number, page in enumerate(memory_frames):
        num_reference_pos = 0
        for idx, page_n in enumerate(reference_string[0:pos_ref_str+1]):
            # Empty frame is available
            if page == -1:
                frame_to_be_replaced = frame_number
                flag = 1
                break
            elif page == page_n:
                num_reference_pos += 1
        if flag == 1:
            break
        pair =(frame_number, page, num_reference_pos);
        freq_reference_pos.append(pair)

     
    if flag == 0:
        # To find page with minimum reference in past
        min_pos = maxint
        for pair in freq_reference_pos:
            frame_number, page, num_reference_pos = pair
            if min_pos > num_reference_pos:
                min_pos = num_reference_pos
                frame_to_be_replaced = frame_number
            elif min_pos == num_reference_pos:
                min_pos = num_reference_pos
                frame_to_be_replaced =randint(frame_to_be_replaced,frame_number)

    memory_frames[frame_to_be_replaced] = page_number
    status = (frame_to_be_replaced, deepcopy(memory_frames));
    return status

# Funtion to find and replace a page using mfu algorithm 
def find_and_replace_page_most_frequently_used(page_number, memory_frames, reference_string, pos_ref_str):
    # To keep track of page number with maximum reference in past
    frame_to_be_replaced = -1
    flag = 0 # To check if an empty frame is available
    
    freq_reference_pos = [] # To keep track of each page's number of references
    for frame_number, page in enumerate(memory_frames):
        num_reference_pos = 0
        for idx, page_n in enumerate(reference_string[0:pos_ref_str+1]):
             # Empty frame is available
            if page == -1:
                frame_to_be_replaced = frame_number
                flag = 1
                break
            elif page == page_n:
                num_reference_pos += 1
        if flag == 1:
            break
        pair =(frame_number, page, num_reference_pos);
        freq_reference_pos.append(pair)

     
    if flag == 0:
        # To find page with maximum reference in past
        max_pos = -1
        for pair in freq_reference_pos:
            frame_number, page, num_reference_pos = pair
            if max_pos < num_reference_pos:
                max_pos = num_reference_pos
                frame_to_be_replaced = frame_number
            elif max_pos == num_reference_pos:
                max_pos = num_reference_pos
                frame_to_be_replaced =randint(frame_to_be_replaced,frame_number)

    memory_frames[frame_to_be_replaced] = page_number
    status = (frame_to_be_replaced, deepcopy(memory_frames));
    return status

def construct_output(error_status, page_number, frame_number, memory_frames, page_fault, page_fault_count):
    temp_memory = {}
    temp_memory['page_number'] = page_number
    temp_memory['frame_number'] = frame_number 
    temp_memory['memory_frames'] = memory_frames
    temp_memory['page_fault'] = page_fault
    temp_memory['page_fault_count'] = page_fault_count
    temp_memory['error_status'] = error_status
    return temp_memory

# Main function to call algo chosen by the user
def page_replacement(data):
    # To store the state of main memory(which is divided into frames) after each page arrives
    memory_chart = [] 
    # For bad input handling
    error, error_status = check_for_bad_input(data)
    if(error):
        temp_memory = {}
        temp_memory = construct_output(error_status, -1, -1, -1, -1, -1)
        memory_chart.append(temp_memory)
        return memory_chart
    else:
        frames_number = data['num_frames']
        page_numbers = data['ref_str']
        memory_frames = []
        page_fault_count = 0
        if data['algo'] == 3 or data['algo'] == 4:
            reference_bit = []
        if data['algo'] == 4:
            modify_bit_string = data['modify_bits'] 
            modify_bit = []

        # variable for FIFO, Second Chance and Enhanced Second Chance Algorithmn
        last_replaced_frame = -1 # to track which page was allocated memory first

        # Intialising all frames to empty 
        for i in range(frames_number):
            memory_frames.append(-1)
            if data['algo'] == 3 or data['algo'] == 4:
                reference_bit.append(0)
            if data['algo'] == 4:
                modify_bit.append(0)

        for pos, page_number in enumerate(page_numbers):
            temp_memory = {}
            frame_number, in_memory = page_in_memory(page_number, memory_frames) 
            if in_memory:
                temp_memory = construct_output(error_status, page_number, frame_number+1, deepcopy(memory_frames), 0, page_fault_count)
                memory_chart.append(temp_memory)
                if data['algo'] == 3:
                    reference_bit[frame_number] = 1
                if data['algo'] == 4:
                    if modify_bit_string[pos] == 1:
                        reference_bit[frame_number] = 1
                    else:
                        modify_bit[frame_number] = 1
            else:
                temp_memory['page_number'] = page_number
                if data['algo'] == 0:
                    allocated_frame, new_memory_frames = find_and_replace_page_fifo(page_number, memory_frames, last_replaced_frame)
                    last_replaced_frame = allocated_frame 
                elif data['algo'] == 1:
                    allocated_frame, new_memory_frames = find_and_replace_page_optimal(page_number, memory_frames, page_numbers, pos)
                elif data['algo'] == 2:
                    allocated_frame, new_memory_frames = find_and_replace_page_lru(page_number, memory_frames, page_numbers, pos)
                elif data['algo'] == 3:
                    allocated_frame, new_memory_frames = find_and_replace_page_second_chance(page_number, memory_frames, last_replaced_frame, reference_bit)
                    last_replaced_frame = allocated_frame
                elif data['algo'] == 4:
                    allocated_frame, new_memory_frames = find_and_replace_page_enhanced_second_chance(page_number, memory_frames, last_replaced_frame, reference_bit, modify_bit,pos,modify_bit_string)
                    last_replaced_frame = allocated_frame
                elif data['algo'] == 5:
                    allocated_frame, new_memory_frames = find_and_replace_page_least_frequently_used(page_number, memory_frames, page_numbers, pos)
                elif data['algo'] == 6:
                    allocated_frame, new_memory_frames = find_and_replace_page_most_frequently_used(page_number, memory_frames, page_numbers, pos)
                temp_memory = construct_output( error_status, page_number, allocated_frame+1, new_memory_frames, 1, page_fault_count)
                page_fault_count += 1
                memory_chart.append(temp_memory)
        return memory_chart
