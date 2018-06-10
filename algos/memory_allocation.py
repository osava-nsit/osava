'''
This file contains the implementation of Memory Allocation strategies
'''

from operator import itemgetter
from copy import deepcopy
from common import OSAVAException

# Bad input case(s):
# 0. 1 <= total_size 
# 1. 1 <= process_size 
# 2. 1 <= arrival_time 
# 3. 1 <= burst_time


# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, process_id):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Please enter a valid size of main memory.\n" + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = "Please enter a valid size of process " + str(process_id) + ".\n " + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = "Arrival time for process " + str(process_id) + " is invalid. Please enter a valid arrival time.\n" + default_message
        ERROR['error_number'] = 2
    elif error_number == 3:
        ERROR['error_message'] = "CPU-I/O burst time for process " + str(process_id) + " is invalid. Please enter a valid arrival time.\n" + default_message
        ERROR['error_number'] = 3
    return ERROR

def check_for_bad_input(data):
    error_status = {} # Dictionary to store error number and error message
    processes = sorted(data, key=itemgetter('arrival'))
    total_size = processes[0]['mem_size']
    if int(total_size) <= 0:
        error_status = get_error_message(0, -1)
        raise OSAVAException(error_status)
    else:
        for process in processes:
            #total_size=process['mem_size']
            process_id = process['name']
            arrival_time = process['arrival']
            if int(arrival_time) < 0:
                error_status = get_error_message(2, process_id)
                raise OSAVAException(error_status)
            burst_time = process['burst']
            if int(burst_time) <= 0:
                error_status = get_error_message(3, process_id)
                raise OSAVAException(error_status)
            process_size = process['size']
            if int(process_size) <= 0:
                error_status = get_error_message(1, process_id)
                raise OSAVAException(error_status)

    # No bad input
    error_status = get_error_message(-1, -1)
    return error_status

# To construct output in case of bad input             
def construct_output(error_status, event, memory_state, processes_waiting, wait_to_memory, external_fragmentation):
    temp_memory = {}
    temp_memory['event'] = event
    temp_memory['memory_state'] = memory_state
    temp_memory['processes_waiting'] =  processes_waiting
    temp_memory['wait_to_memory'] =wait_to_memory
    temp_memory['external_fragmentation'] = external_fragmentation
    temp_memory['error_status'] = error_status
    return temp_memory

# To check if external fragmentation is present 
def check_external_frag(memory_allocated, process_size, total_size):
    flag = 0 # Variable to check if external fragmentation is present
    free_space = 0
    for i, pair in enumerate(memory_allocated):    
        process_name1,start1,end1 = pair
        if(i == len(memory_allocated)-1):
            free_space += total_size - end1
            break
        process_name2,start2,end2 = memory_allocated[i+1]
        free_space += start2-end1
    if free_space >= process_size:
        flag = 1 # External fragmentation present
        return flag 
    else:
        return flag

def add_termination_event(event_list, process_id, curr_time, burst_time, process_size):
    pair = (process_id,0,curr_time+burst_time,burst_time,process_size);
    event_list.append(pair)
    # print "add_termination_event - before sorting: " + str(event_list)
    # new_list = sorted(event_list,key=lambda x: (x[2],x[1]))
    new_list = sorted(event_list, key=itemgetter(1))
    new_list = sorted(new_list, key=itemgetter(2))
    # print "add_termination_event - after sorting: " + str(new_list)
    return new_list

def add_to_memory_firstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    external_frag = 0
    if(arrival_time>curr_time):
        curr_time = arrival_time
    i = 0
    flag = 0
    if not memory_allocated:
        if(process_size <= total_size):
            start = 0
            end = process_size
            new_pair1 = (process_id, start, end);
            memory_allocated.append(new_pair1)
            # print "\nAdding termination event for " + str(process_id)
            event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
            # print "Event list after adding termination event: "
            # print str(event_list) + "\n"
        else:
            new_pair1 = (process_id,process_size,burst_time);
            wait_queue.append(new_pair1)
            external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['processes_waiting'] = deepcopy(wait_queue)
        temp_memory['external_fragmentation'] = external_frag
        return temp_memory, event_list
        # Find free memory block 
    for pair in memory_allocated:
            process_name1,start1,end1 = pair
            # Only last pair left to check
            if(i == len(memory_allocated)-1):
                if(total_size-end1 >= process_size):
                    start = end1
                    end = end1 + process_size
                    new_pair1 = (process_id,start,end);
                    memory_allocated.append(new_pair1)
                    flag = 1
                break
            process_name2,start2,end2 = memory_allocated[i+1]
            i = i+1
            # If memory available, allocate it
            if(start2-end1 >= process_size):
                start = end1
                end = end1 + process_size
                new_pair1 = (process_id,start,end);
                memory_allocated.insert(i+1,new_pair1)
                flag = 1 #processes has been alloted a memory block
                #sorted(memory_allocated,key=itemgetter(1))
                break
    # Process has not been allocated any memory block
    if(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
    # Process has been allocated memory
    else:
        # Appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
    temp_memory['memory_state'] = deepcopy(memory_allocated)    
    temp_memory['external_fragmentation'] = external_frag
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory, event_list

def remove_from_memory_firstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    wait_to_memory = []

    # Remove process from memory_allocated list
    if(end_time > curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)


    # print "\nChecking wait queue...."
    # Check if a process in wait_queue can now be allocated memory
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        # print "Trying to allocate memory to " + str(process_name) + " picked from wait queue"
        # print "Checking memroy_allocated list: " + str(memory_allocated)
        if not memory_allocated:
            # print "Empty memory"
            if(size <= total_size):
                # print "size < total_size = True\n"
                start = 0
                end = size 
                new_pair1 = (process_name,start, end);
                wait_to_memory.append(process_name)
                memory_allocated.append(new_pair1)
                # Add event of termination
                event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                # Delete process from wait queue
                del wait_queue[i]

            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['processes_waiting'] = deepcopy(wait_queue)        
            continue

        for j, mem_pair in enumerate(memory_allocated):
            # Find free memory block 
            process_name1,start1,end1 = mem_pair
            # Only last pair left to check
            if(j == len(memory_allocated)-1):
                if(total_size-end1 >= size):
                    start = end1
                    end = end1 + size
                    new_pair1 = (process_name,start,end);
                    wait_to_memory.append(process_name)
                    memory_allocated.append(new_pair1)
                    temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                    temp_memory['memory_state'] = deepcopy(memory_allocated)
                    # Delete process from wait queue
                    del wait_queue[i]
                    # Add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                break
            process_name2,start2,end2 = memory_allocated[j+1]
            j = j+1

            # If memory available, allocate it
            if(start2-end1 >= process_size):
                start = end1
                end = end1 + size
                new_pair1 = (process_name,start,end);
                wait_to_memory.append(process_name)
                memory_allocated.insert(j+1,new_pair1)
                # Delete process from wait queue
                del wait_queue[i]
                #sorted(memory_allocated,key=itemgetter(1))
                temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                temp_memory['memory_state'] = deepcopy(memory_allocated)
                # Add termination event
                event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                break

    temp_memory['processes_waiting'] = deepcopy(wait_queue)      
    return temp_memory, event_list


def first_fit(data):
    # To store memory states and wait queue state after arrival of each process
    memory_chart = [] 
    # For bad input handling
    try:
    	error_status = check_for_bad_input(data)
        processes = sorted(data, key=itemgetter('arrival'))
        total_size = processes[0]['mem_size']
        curr_time = 0
        memory_allocated = []
        wait_queue = []
        event_list = []
        wait_to_memory = [] # Processes added from wait queue to memory
        for process in processes:
            #total_size=process['mem_size']
            process_id = process['name']
            arrival_bit = 1 # Time field indiactes arrival time
            arrival_time = process['arrival']
            burst_time = process['burst']
            process_size = process['size']
            pair = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            event_list.append(pair)

        #for idx in range(len(event_list)):
        while (len(event_list) > 0):
            event = event_list[0]
            process_id,arrival_bit,arrival_time,burst_time,process_size = event
            if(arrival_bit == 1):
                #new process has arrived
                temp_memory, event_list = add_to_memory_firstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                # print "-------------------"
                # print "Added to memory: " + str(temp_memory)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
                temp_memory['event'] = event1
                temp_memory['wait_to_memory'] = wait_to_memory
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
                # print "\nMemory chart after addition: " + str(memory_chart)
                # print "-------------------"
            else:
                # Process has completed its execution
                # Here arrival time=curr_time+burst_time set by add_to_memory function
                end_time = arrival_time
                temp_memory, event_list = remove_from_memory_firstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                # print "-------------------"
                # print "Removed from memory: " + str(temp_memory)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
                temp_memory['event'] = event1
                temp_memory['external_fragmentation'] = 0
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
                # print "\nMemory chart after removal: " + str(memory_chart)
                # print "----------
            del event_list[0]
        return memory_chart
    except OSAVAException as ex:
	    temp_memory = {}
	    temp_memory = construct_output(ex.error_status, -1, -1, -1, -1, -1)
	    memory_chart.append(temp_memory)
	    return memory_chart

# Worst Fit Agorithm
def add_to_memory_worstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    external_frag = 0
    if(arrival_time > curr_time):
        curr_time = arrival_time
    i = 0
    flag = 0
    if not memory_allocated:
        if(process_size <= total_size):
            start = 0
            end = process_size
            new_pair1 = (process_id,start, end);
            memory_allocated.append(new_pair1)
            event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        else:
            new_pair1 = (process_id,process_size,burst_time);
            wait_queue.append(new_pair1)   
            external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag  
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['processes_waiting'] = deepcopy(wait_queue)
        return temp_memory, event_list
        
    # Find free memory block
    max_space = 0
    max_ind = -1 
    for pair in memory_allocated:    
            process_name1,start1,end1 = pair
            # Only last pair left to check
            if(i == len(memory_allocated)-1):
                if(total_size-end1 >= process_size):
                    start = end1
                    end = end1 + process_size
                    new_pair1 = (process_id,start,end);
                    memory_allocated.append(new_pair1)
                    flag = 1
                break
            process_name2,start2,end2 = memory_allocated[i+1]
            i = i+1
            # If memory available, find largest slot of unallocated memory
            if(start2-end1 >= process_size):
                if(max_space < start2-end1):
                    max_space = start2-end1
                    max_ind = i-1
    # A worst fit slot is available      
    if(flag == 0 and max_ind != -1):
        flag = 1 
        # Allocate worst fit slot to process
        start = memory_allocated[max_ind][2]
        end = memory_allocated[max_ind][2]+process_size
        new_pair1 = (process_id,start,end);
        memory_allocated.insert(max_ind+1,new_pair1)
    # Process is allocated no memory slot
    elif(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag
        temp_memory['memory_state'] = deepcopy(memory_allocated)
    # Process has been allocated a worst fit memory slot
    if flag == 1:
        # Appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['external_fragmentation'] = 0
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory, event_list
            

def remove_from_memory_worstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    wait_to_memory = []
    if(end_time > curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        # Remove process from main memory
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        if not memory_allocated:
                if(size <= total_size):
                    start = 0
                    end = size 
                    new_pair1 = (process_name,start, end);
                    wait_to_memory.append(process_name)
                    memory_allocated.append(new_pair1)
                    # Delete process from wait queue
                    del wait_queue[i]
                     # Add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                temp_memory['memory_state'] = deepcopy(memory_allocated)
                temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                temp_memory['processes_waiting'] = deepcopy(wait_queue)        
                continue 
        max_ind = -1
        max_space = 0
        for j, mem_pair in enumerate(memory_allocated):
            # Find free worst fit memory block 
                process_name1,start1,end1 = mem_pair
            # Only last pair left to check
                if(j == len(memory_allocated)-1):
                    if(total_size-end1 >= size):
                        start = end1
                        end = end1+size
                        new_pair1 = (process_name,start,end);
                        wait_to_memory.append(process_name)
                        memory_allocated.append(new_pair1)
                        temp_memory['memory_state'] = deepcopy(memory_allocated)
                        temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                        # Add termination event
                        event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                        # Delete process from wait queue
                        del wait_queue[i]
                    break
                process_name2,start2,end2 = memory_allocated[j+1]
                j = j+1
            # If memory available, allocate it
                if(start2-end1 >= process_size):
                    if(max_space <= start2-end1):
                        max_space = start2-end1
                        max_ind = j-1
        # A worst fit memory slot is available for a waiting process
        if(max_ind != -1):
            # Delete process from wait queue
            del wait_queue[i]
            # Allocate the worst fit memory slot to the process
            start = memory_allocated[max_ind][2]
            end = memory_allocated[max_ind][2]+size
            new_pair1 = (process_name,start,end);
            wait_to_memory.append(process_name)
            memory_allocated.insert(max_ind+1,new_pair1)
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
            # Add termination event
            event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
    temp_memory['processes_waiting'] = deepcopy(wait_queue)        
    return temp_memory, event_list

def worst_fit(data):
    # To store memory states and wait queue state after arrival of each process
    memory_chart = [] 
    # For bad input handling
    try:
    	error_status = check_for_bad_input(data)
        processes = sorted(data, key=itemgetter('arrival'))
        total_size = processes[0]['mem_size']
        curr_time = 0
        memory_allocated = []
        wait_queue = []
        event_list = []
        wait_to_memory = []
        for process in processes:
            # Total_size=process['mem_size']
            process_id = process['name']
            arrival_bit = 1 # Time field indicates arrival time
            arrival_time = process['arrival']
            burst_time = process['burst']
            process_size = process['size']
            pair = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            event_list.append(pair)
        while (len(event_list) > 0):
            event = event_list[0]
            process_id, arrival_bit, arrival_time, burst_time, process_size = event
            if(arrival_bit == 1):
                # New process has arrived
                temp_memory, event_list = add_to_memory_worstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
                temp_memory['event'] = event1
                temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
            else:
                # Process has completed its execution
                # Here arrival time=curr_time+burst_time set by add_to_memory function
                end_time = arrival_time
                temp_memory, event_list = remove_from_memory_worstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
                temp_memory['event'] = event1
                temp_memory['external_fragmentation'] = 0
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
            del event_list[0]
        return memory_chart
    except OSAVAException as ex:
	temp_memory = {}
        temp_memory = construct_output(ex.error_status, -1, -1, -1, -1, -1)
        memory_chart.append(temp_memory)
        return memory_chart

def add_to_memory_bestfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    external_frag = 0
    if(arrival_time > curr_time):
        curr_time = arrival_time
    i = 0
    flag = 0
    if not memory_allocated:
        if(process_size <= total_size):
            start = 0
            end = process_size
            new_pair1 = (process_id,start, end)
            memory_allocated.append(new_pair1)
            event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        else:
            new_pair1 = (process_id,process_size,burst_time)
            wait_queue.append(new_pair1)  
            external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag   
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['processes_waiting'] = deepcopy(wait_queue)
        return temp_memory, event_list
        # Find free memory block 
    min_space = total_size + 1
    min_ind = -1
    for pair in memory_allocated:    
            process_name1,start1,end1 = pair
            # Only last pair left to check
            if(i == len(memory_allocated)-1):
                if(total_size-end1 >= process_size):
                    start = end1
                    end = end1 + process_size
                    new_pair1 = (process_id,start,end)
                    memory_allocated.append(new_pair1)
                    flag=1
                break
            process_name2,start2,end2 = memory_allocated[i+1]
            i = i+1
            # If memory available, find smallest slot of unallocated memory
            if(start2-end1 >= process_size):
                if(min_space > start2-end1):
                    min_space = start2-end1
                    min_ind = i-1
    # A best fit slot is available      
    if(flag == 0 and min_ind != -1):
        flag = 1 
        # Allocate best fit slot to process
        start = memory_allocated[min_ind][2]
        end = memory_allocated[min_ind][2]+process_size
        new_pair1 = (process_id,start,end);
        memory_allocated.insert(min_ind+1,new_pair1)
    # Process is allocated no memory slot
    elif(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag
        temp_memory['memory_state'] = deepcopy(memory_allocated)
    # Process has been allocated a worst fit memory slot
    if flag == 1:
        # Appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['external_fragmentation'] = 0
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory,event_list

def remove_from_memory_bestfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    wait_to_memory = []
    if(end_time > curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        if not memory_allocated:
                if(size <= total_size):
                    start = 0
                    end = size 
                    new_pair1 = (process_name,start, end)
                    wait_to_memory.append(process_name)
                    memory_allocated.append(new_pair1)
                    # Delete process from wait queue
                    del wait_queue[i]
                    # Add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                temp_memory['memory_state']=deepcopy(memory_allocated)
                temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)    
                temp_memory['processes_waiting']=deepcopy(wait_queue)        
                continue 
        min_ind = -1
        min_space = total_size+1
        for j, mem_pair in enumerate(memory_allocated):
            # Find free best fit memory block 
                process_name1,start1,end1 = mem_pair
            # Only last pair left to check
                if(j == len(memory_allocated)-1):
                    if(total_size-end1 >= size):
                        start = end1
                        end = end1+size
                        new_pair1 = (process_name,start,end)
                        wait_to_memory.append(process_name)
                        memory_allocated.append(new_pair1)
                        temp_memory['memory_state']=deepcopy(memory_allocated)
                        temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                        # Add termination event
                        event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                        # Delete process from wait queue
                        del wait_queue[i]
                    break
                process_name2,start2,end2=memory_allocated[j+1]
                j=j+1
            # If memory available, allocate it
                if(start2-end1 >= process_size):
                      if(min_space >= start2-end1):
                        min_space = start2-end1
                        min_ind = j-1
        # A best fit memory slot is available for a waiting process
        if(min_ind != -1):
            # Delete process from wait queue
            del wait_queue[i]
            # Allocate the worst fit memory slot to the process
            start = memory_allocated[min_ind][2]
            end = memory_allocated[min_ind][2]+size
            new_pair1 = (process_name,start,end);
            wait_to_memory.append(process_name)
            memory_allocated.insert(min_ind+1,new_pair1)
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
            # Add termination event
            event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
    temp_memory['processes_waiting'] = deepcopy(wait_queue)        
    return temp_memory, event_list

          
def best_fit(data):
    # To store memory states and wait queue state after arrival of each process
    memory_chart = [] 
    # For bad input handling
    try:
    	error_status = check_for_bad_input(data)
        curr_time = 0
        memory_allocated = []
        wait_queue = []
        event_list = []
        wait_to_memory = []
        # Input data
        processes = sorted(data, key=itemgetter('arrival'))
        total_size = processes[0]['mem_size']
        for process in processes:
            process_id = process['name']
            arrival_bit = 1 # Time field indicates arrival time
            arrival_time = process['arrival']
            burst_time = process['burst']
            process_size = process['size']
            pair = (process_id,arrival_bit,arrival_time,burst_time,process_size)
            event_list.append(pair)
        while (len(event_list) > 0):
            event = event_list[0]
            process_id,arrival_bit,arrival_time,burst_time,process_size=event
            if(arrival_bit == 1):
                # New process has arrived
                temp_memory, event_list = add_to_memory_bestfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size)
                temp_memory['event'] = event1
                temp_memory['wait_to_memory'] = deepcopy(wait_to_memory)
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
            else:
                # Process has completed its execution
                # Here arrival time=curr_time+burst_time set by add_to_memory function
                end_time = arrival_time
                temp_memory, event_list = remove_from_memory_bestfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
                event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
                temp_memory['event'] = event1
                temp_memory['external_fragmentation'] = 0
                temp_memory['error_status'] = error_status
                memory_chart.append(temp_memory)
            del event_list[0]
        return memory_chart
    except OSAVAException as ex:
	temp_memory = {}
        temp_memory = construct_output(ex.error_status, -1, -1, -1, -1, -1)
        memory_chart.append(temp_memory)
        return memory_chart
    
