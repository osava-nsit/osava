from operator import itemgetter
from copy import deepcopy

#to check if external fragmentation is present 
def check_external_frag(memory_allocated, process_size, total_size):
    flag = 0 #variable to check if external fragmentation is present
    free_space = 0
    for i, pair in enumerate(memory_allocated):    
        process_name1,start1,end1 = pair
        if(i == len(memory_allocated)-1):
            free_space += total_size - end1
            break
        process_name2,start2,end2 = memory_allocated[i+1]
        free_space += start2-end1
    if free_space >= process_size:
        flag = 1 #external fragmentation present
        return flag 
    else:
        return flag


def add_termination_event(event_list, process_id, curr_time, burst_time, process_size):
    pair = (process_id,0,curr_time+burst_time,burst_time,process_size);
    event_list.append(pair)
    new_list = sorted(event_list,key=lambda x: (x[2],x[1]))
    return new_list

def add_to_memory_firstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    external_frag = 0
    if(arrival_time>curr_time):
        curr_time = arrival_time
    i = 0
    flag = 0
    if not memory_allocated:
        if(process_size < total_size):
            start = 0
            end = process_size
            new_pair1 = (process_id,start, end);
            memory_allocated.append(new_pair1)
            event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        else:
            new_pair1 = (process_id,process_size,burst_time);
            wait_queue.append(new_pair1)
            external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['processes_waiting'] = deepcopy(wait_queue)
        temp_memory['external_fragmentation'] = external_frag
        return temp_memory
        # find free memory block 
    for pair in memory_allocated:    
            process_name1,start1,end1 = pair
            #only last pair left to check
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
            #if memory available, allocate it
            if(start2-end1 >= process_size):
                start = end1
                end = end1 + process_size
                new_pair1 = (process_id,start,end);
                memory_allocated.insert(i+1,new_pair1)
                flag = 1 #processes has been alloted a memory block
                #sorted(memory_allocated,key=itemgetter(1))
                break
    #process has not been allocated any memory block
    if(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
    #process has been allocated memory
    else:
        #appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
    temp_memory['memory_state'] = deepcopy(memory_allocated)    
    temp_memory['external_fragmentation'] = external_frag
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory

def remove_from_memory_firstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    if(end_time > curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        if not memory_allocated:
                if(size < total_size):
                    start = 0
                    end = size 
                    new_pair1 = (process_name,start, end);
                    memory_allocated.append(new_pair1)
                    # add event of termination
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                    # delete process from wait queue
                    del wait_queue[i]
                temp_memory['memory_state'] = deepcopy(memory_allocated)
                temp_memory['processes_waiting'] = deepcopy(wait_queue)        
                continue 

        for j, mem_pair in enumerate(memory_allocated):
            # find free memory block 
                process_name1,start1,end1 = mem_pair
            #only last pair left to check
                if(j == len(memory_allocated)-1):
                    if(total_size-end1 >= size):
                        start = end1
                        end = end1 + size
                        new_pair1 = (process_name,start,end);
                        memory_allocated.append(new_pair1)
                        temp_memory['memory_state'] = deepcopy(memory_allocated)
                        #delete process from wait queue
                        del wait_queue[i]
                        #add termination event
                        event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                    break
                process_name2,start2,end2 = memory_allocated[j+1]
                j = j+1
            #if memory available, allocate it
                if(start2-end1 >= process_size):
                    start = end1
                    end = end1 + size
                    new_pair1 = (process_name,start,end);
                    memory_allocated.insert(j+1,new_pair1)
                    #delete process from wait queue
                    del wait_queue[i]
                    #sorted(memory_allocated,key=itemgetter(1))
                    temp_memory['memory_state'] = deepcopy(memory_allocated)
                    #add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                    break
    temp_memory['processes_waiting'] = deepcopy(wait_queue)      
    return temp_memory

def first_fit(data):
    processes = sorted(data, key=itemgetter('arrival'))
    total_size = processes[0]['mem_size']
    curr_time = 0
    memory_chart = []
    memory_allocated = []
    wait_queue = []
    event_list = []
    for process in processes:
        #total_size=process['mem_size']
        process_id = process['name']
        arrival_bit = 1 #time field indiactes arrival time
        arrival_time = process['arrival']
        burst_time = process['burst']
        process_size = process['size']
        pair = (process_id,arrival_bit,arrival_time,burst_time,process_size);
        event_list.append(pair)
    for event in event_list:
        process_id,arrival_bit,arrival_time,burst_time,process_size = event
        if(arrival_bit == 1):
            #new process has arrived
            temp_memory = add_to_memory_firstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            # print "-------------------"
            # print "Added to memory: " + str(temp_memory)
            event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            temp_memory['event'] = event1
            memory_chart.append(temp_memory)
            # print "\nMemory chart after addition: " + str(memory_chart)
            # print "-------------------"
        else:
            #process has completed its execution
            #here arrival time=curr_time+burst_time set by add_to_memory function
            end_time = arrival_time
            temp_memory = remove_from_memory_firstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            # print "-------------------"
            # print "Removed from memory: " + str(temp_memory)
            event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            temp_memory['event'] = event1
            temp_memory['external_fragmentation'] = 0
            memory_chart.append(temp_memory)
            # print "\nMemory chart after removal: " + str(memory_chart)
            # print "-------------------"
    return memory_chart

#Worst Fit Agorithm
def add_to_memory_worstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    external_frag = 0
    if(arrival_time > curr_time):
        curr_time = arrival_time
    i = 0
    flag = 0
    if not memory_allocated:
        if(process_size < total_size):
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
        return temp_memory
        # find free memory block
    max_space = 0
    max_ind = -1 
    for pair in memory_allocated:    
            process_name1,start1,end1 = pair
            #only last pair left to check
            if(i == len(memory_allocated)-1):
                if(total_size-end1 >= process_size):
                    start = end1
                    end = end1+process_size
                    new_pair1 = (process_id,start,end);
                    memory_allocated.append(new_pair1)
                    flag = 1
                break
            process_name2,start2,end2 = memory_allocated[i+1]
            i = i+1
            #if memory available, find largest slot of unallocated memory
            if(start2-end1 >= process_size):
                if(max_space < start2-end1):
                    max_space = start2-end1
                    max_ind = i-1
    #a worst fit slot is available      
    if(flag == 0 and max_ind != -1):
        flag = 1 
        # allocate worst fit slot to process
        start = memory_allocated[max_ind][2]
        end = memory_allocated[max_ind][2]+process_size
        new_pair1 = (process_id,start,end);
        memory_allocated.insert(max_ind+1,new_pair1)
    #process is allocated no memory slot
    elif(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag
        temp_memory['memory_state'] = deepcopy(memory_allocated)
    #process has been allocated a worst fit memory slot
    if flag == 1:
        #appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['external_fragmentation'] = 0
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory
            

def remove_from_memory_worstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    if(end_time>curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        #remove process from main memory
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        if not memory_allocated:
                if(size < total_size):
                    start = 0
                    end = size 
                    new_pair1 = (process_name,start, end);
                    memory_allocated.append(new_pair1)
                    #delete process from wait queue
                    del wait_queue[i]
                     #add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                temp_memory['memory_state'] = deepcopy(memory_allocated)
                temp_memory['processes_waiting'] = deepcopy(wait_queue)        
                continue 
        max_ind = -1
        max_space = 0
        for j, mem_pair in enumerate(memory_allocated):
            # find free worst fit memory block 
                process_name1,start1,end1 = mem_pair
            #only last pair left to check
                if(j == len(memory_allocated)-1):
                    if(total_size-end1 >= size):
                        start = end1
                        end = end1+size
                        new_pair1 = (process_name,start,end);
                        memory_allocated.append(new_pair1)
                        temp_memory['memory_state'] = deepcopy(memory_allocated)
                        #add termination event
                        event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                        #delete process from wait queue
                        del wait_queue[i]
                    break
                process_name2,start2,end2 = memory_allocated[j+1]
                j = j+1
            #if memory available, allocate it
                if(start2-end1 >= process_size):
                    if(max_space <= start2-end1):
                        max_space = start2-end1
                        max_ind = j-1
        # a worst fit memory slot is available for a waiting process
        if(max_ind != -1):
            #delete process from wait queue
            del wait_queue[i]
            #allocate the worst fit memory slot to the process
            start = memory_allocated[max_ind][2]
            end = memory_allocated[max_ind][2]+size
            new_pair1 = (process_name,start,end);
            memory_allocated.insert(max_ind+1,new_pair1)
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            #add termination event
            event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
    temp_memory['processes_waiting'] = deepcopy(wait_queue)        
    return temp_memory

def worst_fit(data):
    processes = sorted(data, key=itemgetter('arrival'))
    total_size = processes[0]['mem_size']
    curr_time = 0
    memory_chart = []
    memory_allocated = []
    wait_queue = []
    event_list = []
    for process in processes:
        #total_size=process['mem_size']
        process_id = process['name']
        arrival_bit = 1 #time field indicates arrival time
        arrival_time = process['arrival']
        burst_time = process['burst']
        process_size = process['size']
        pair = (process_id,arrival_bit,arrival_time,burst_time,process_size);
        event_list.append(pair)
    for event in event_list:
        process_id,arrival_bit,arrival_time,burst_time,process_size=event
        if(arrival_bit == 1):
            #new process has arrived

            temp_memory = add_to_memory_worstfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            temp_memory['event'] = event1
            memory_chart.append(temp_memory)
        else:
            #process has completed its execution
            #here arrival time=curr_time+burst_time set by add_to_memory function
            end_time = arrival_time
            temp_memory = remove_from_memory_worstfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            temp_memory['event'] = event1
            temp_memory['external_fragmentation'] = 0
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
        if(process_size < total_size):
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
        temp_memory['memory_state']=deepcopy(memory_allocated)
        temp_memory['processes_waiting']=deepcopy(wait_queue)
        return temp_memory
        # find free memory block 
    min_space = total_size+1
    min_ind = -1
    for pair in memory_allocated:    
            process_name1,start1,end1=pair
            
            #only last pair left to check
            if(i == len(memory_allocated)-1):
                if(total_size-end1 >= process_size):
                    start = end1
                    end = end1+process_size
                    new_pair1 = (process_id,start,end)
                    memory_allocated.append(new_pair1)
                    flag=1
                break
            process_name2,start2,end2 = memory_allocated[i+1]
            i = i+1
            #if memory available, find smallest slot of unallocated memory
            if(start2-end1 >= process_size):
                if(min_space > start2-end1):
                    min_space = start2-end1
                    min_ind = i-1
    #a best fit slot is available      
    if(flag == 0 and min_ind != -1):
        flag = 1 
        # allocate best fit slot to process
        start = memory_allocated[min_ind][2]
        end = memory_allocated[min_ind][2]+process_size
        new_pair1 = (process_id,start,end);
        memory_allocated.insert(min_ind+1,new_pair1)
    #process is allocated no memory slot
    elif(flag == 0):
        new_pair1 = (process_id,process_size,burst_time);
        wait_queue.append(new_pair1)
        external_frag = check_external_frag(memory_allocated, process_size, total_size)
        temp_memory['external_fragmentation'] = external_frag
        temp_memory['memory_state'] = deepcopy(memory_allocated)
    #process has been allocated a worst fit memory slot
    if flag == 1:
        #appending process with termination time in event list
        event_list = add_termination_event(event_list, process_id, curr_time, burst_time, process_size)
        temp_memory['memory_state'] = deepcopy(memory_allocated)
        temp_memory['external_fragmentation'] = 0
    temp_memory['processes_waiting'] = deepcopy(wait_queue)
    return temp_memory

def remove_from_memory_bestfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue):
    temp_memory = {}
    if(end_time > curr_time):
        curr_time = end_time
    for i,pair in enumerate(memory_allocated):
        process_name,start,end = pair
        if(process_name == process_id):
            del memory_allocated[i]
            temp_memory['memory_state'] = deepcopy(memory_allocated)
    for i,pair in enumerate(wait_queue):
        process_name,size,burst_time = pair
        if not memory_allocated:
                if(size < total_size):
                    start = 0
                    end = size 
                    new_pair1 = (process_name,start, end)
                    memory_allocated.append(new_pair1)
                    #delete process from wait queue
                    del wait_queue[i]
                    #add termination event
                    event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                temp_memory['memory_state']=deepcopy(memory_allocated)    
                temp_memory['processes_waiting']=deepcopy(wait_queue)        
                continue 
        min_ind = -1
        min_space = total_size+1
        for j, mem_pair in enumerate(memory_allocated):
            # find free best fit memory block 
                process_name1,start1,end1 = mem_pair
            #only last pair left to check
                if(j == len(memory_allocated)-1):
                    if(total_size-end1 >= size):
                        start = end1
                        end = end1+size
                        new_pair1 = (process_name,start,end)
                        memory_allocated.append(new_pair1)
                        temp_memory['memory_state']=deepcopy(memory_allocated)
                        #add termination event
                        event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
                        #delete process from wait queue
                        del wait_queue[i]
                    break
                process_name2,start2,end2=memory_allocated[j+1]
                j=j+1
            #if memory available, allocate it
                if(start2-end1 >= process_size):
                      if(min_space >= start2-end1):
                        min_space = start2-end1
                        min_ind = j-1
        # a best fit memory slot is available for a waiting process
        if(min_ind != -1):
            #delete process from wait queue
            del wait_queue[i]
            #allocate the worst fit memory slot to the process
            start = memory_allocated[min_ind][2]
            end = memory_allocated[min_ind][2]+size
            new_pair1 = (process_name,start,end);
            memory_allocated.insert(min_ind+1,new_pair1)
            temp_memory['memory_state'] = deepcopy(memory_allocated)
            #add termination event
            event_list = add_termination_event(event_list, process_name, curr_time, burst_time, process_size)
    temp_memory['processes_waiting'] = deepcopy(wait_queue)        
    return temp_memory 

          
def best_fit(data):
    processes = sorted(data, key=itemgetter('arrival'))
    total_size = processes[0]['mem_size']
    memory_chart = []
    curr_time = 0
    memory_allocated=[]
    wait_queue=[]
    event_list=[]
    for process in processes:
        process_id=process['name']
        arrival_bit=1 #time field indiactes arrival time
        arrival_time=process['arrival']
        burst_time=process['burst']
        process_size=process['size']
        pair=(process_id,arrival_bit,arrival_time,burst_time,process_size)
        event_list.append(pair)
    for event in event_list:
        process_id,arrival_bit,arrival_time,burst_time,process_size=event
        if(arrival_bit==1):
            #new process has arrived
            temp_memory=add_to_memory_bestfit(event_list,process_id,arrival_time,burst_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            event1=(process_id,arrival_bit,arrival_time,burst_time,process_size)
            temp_memory['event']=event1
            memory_chart.append(temp_memory)
        else:
            #process has completed its execution
            #here arrival time=curr_time+burst_time set by add_to_memory function
            end_time=arrival_time
            temp_memory=remove_from_memory_bestfit(event_list,process_id,end_time,process_size,total_size,curr_time,memory_allocated,wait_queue)
            event1 = (process_id,arrival_bit,arrival_time,burst_time,process_size);
            temp_memory['event'] = event1
            temp_memory['external_fragmentation'] = 0
            memory_chart.append(temp_memory)
    return memory_chart
        
