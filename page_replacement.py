from copy import deepcopy
import sys
from random import randint

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
            last_reference_pos = sys.maxint 
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
        min_pos = sys.maxint
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
        min_pos = sys.maxint
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


# Main function to call algo chosen by the user
def page_replacement(data):
    memory_chart = []
    frames_number = data['num_frames']
    page_numbers = data['ref_str']
    memory_frames = []
    page_fault_count = 0
    reference_bit = []

     # variable for FIFO Algorithmn
    last_replaced_frame = -1 # to track which page was allocated memory first

    # Intialising all frames to empty 
    for i in range(frames_number):
        memory_frames.append(-1)
        reference_bit.append(0)

    for pos, page_number in enumerate(page_numbers):
        temp_memory = {}
        frame_number, in_memory = page_in_memory(page_number, memory_frames) 
        if in_memory:
            temp_memory['page_number'] = page_number
            temp_memory['frame_number'] = frame_number + 1 # To start frame numbers from 1 instead of 0 
            temp_memory['memory_frames'] = deepcopy(memory_frames)
            temp_memory['page_fault'] = 0
            temp_memory['page_fault_count'] = page_fault_count
            memory_chart.append(temp_memory)
            if data['algo'] == 3:
                reference_bit[frame_number] = 1
                print reference_bit
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
                allocated_frame, new_memory_frames = find_and_replace_page_enhanced_second_chance(page_number, memory_frames)
            elif data['algo'] == 5:
                allocated_frame, new_memory_frames = find_and_replace_page_least_frequently_used(page_number, memory_frames, page_numbers, pos)
            elif data['algo'] == 6:
                allocated_frame, new_memory_frames = find_and_replace_page_most_frequently_used(page_number, memory_frames, page_numbers, pos)
            temp_memory['frame_number'] = allocated_frame + 1 # To start frame numbers from 1 instead of 0 
            temp_memory['memory_frames'] = new_memory_frames
            temp_memory['page_fault'] = 1
            page_fault_count += 1
            temp_memory['page_fault_count'] = page_fault_count
            print reference_bit
            memory_chart.append(temp_memory)
    return memory_chart
