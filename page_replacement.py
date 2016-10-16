from copy import deepcopy

# Utility function to check if referenced page is already in memory
def page_in_memory(page_number, memory_frames):
    for frame_number, page_n in enumerate(memory_frames):
        # If page is already in memory, return frame_number and set in_memory bit
        if page_n == page_number:
            status = (frame_number+1, 1);
            return status
    # If page is not already in memory 
    status = (-1, 0);
    return status

# Funtion to find and replace a page using fifo algorithm 
def find_and_replace_page_fifo(page_number, memory_frames, last_replaced_frame):
    last_replaced_frame = (last_replaced_frame + 1) % len(memory_frames)
    memory_frames[last_replaced_frame-1] = page_number
    status = (last_replaced_frame, deepcopy(memory_frames));
    return status

# First in first out algorithm
def fifo(data):
    memory_chart = []
    frames_number = data[0]['num_frames']
    page_numbers = data[0]['ref_str']
    print str(page_numbers)
    memory_frames = []
    page_fault_count = 0
    last_replaced_frame = 0 # to track which page was allocated memory first 
    # intialising all frames to empty 
    for i in range(frames_number):
        memory_frames.append(-1)
    
    for page_number in page_numbers:
        temp_memory = {}
        frame_number, in_memory = page_in_memory(page_number, memory_frames) 
        if in_memory:
            temp_memory['page_number'] = page_number
            temp_memory['frame_number'] = frame_number
            temp_memory['memory_frames'] = deepcopy(memory_frames)
            temp_memory['page_fault'] = 0
            temp_memory['page_fault_count'] = page_fault_count
            print str(temp_memory) + '\n'
            memory_chart.append(temp_memory)
        else:
            temp_memory['page_number'] = page_number
            allocated_frame, new_memory_frames = find_and_replace_page_fifo(page_number, memory_frames, last_replaced_frame)
            last_replaced_frame = allocated_frame
            temp_memory['frame_number'] = allocated_frame
            temp_memory['memory_frames'] = new_memory_frames
            temp_memory['page_fault'] = 1
            page_fault_count += 1
            temp_memory['page_fault_count'] = page_fault_count
            print str(temp_memory) + '\n'
            memory_chart.append(temp_memory)
    return memory_chart
