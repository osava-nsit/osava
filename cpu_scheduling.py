from sys import maxsize
from operator import itemgetter
import Queue
from copy import deepcopy
# Bad input case(s):
# 0. 1 <= queue assigned <= num_queues
# 1. 0 < burst_time 
# 2. 0 < quantum 
# 3. 0 < priority 
# 4. 0 <= arrival_time 
# 5. 0 <= dispatch_latency 
# 6. 0 < quantum_queue
# 7. 1 <= aging

# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, process_id, queue_number=-1):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Queue assigned to process " + str(process_id) + " does not exist. Please assign a valid queue to the process.\n" + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = "Please enter a valid CPU burst time for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = "Time quantum entered is invalid. Please enter a valid value for time quantum.\n" + default_message
        ERROR['error_number'] = 2
    elif error_number == 3:
        ERROR['error_message'] = "Please enter a valid priority for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 3
    elif error_number == 4:
        ERROR['error_message'] = "Please enter a valid arrival time for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 4
    elif error_number == 5:
        ERROR['error_message'] = "Please enter a valid value for dispatch latency.\n" + default_message
        ERROR['error_number'] = 5
    elif error_number == 6:
        ERROR['error_message'] = "Time quantum entered for queue " + str(queue_number) + " is invalid. Please enter a valid value for time quantum.\n" + default_message
        ERROR['error_number'] = 6
    elif error_number == 7:
        ERROR['error_message'] = "Please enter a valid value for aging.\n" + default_message
        ERROR['error_number'] = 7
    return ERROR

# Values for algo : FCFS = 1, SJF Premptive/Non-premptive = 2, Priority Premptive/Non-premptive = 3, Round Robin = 4, Multilevel Queue = 5, Multilevel Feedback Queue = 6
def check_for_bad_input(data, dispatch_latency, priority, aging, quantum, algo, num_queues, quantum_queue, algo_queue):
    error = 0 # Boolean to check bad input 
    error_status = {} # Dictionary to store error number and error message
    processes = sorted(data, key=itemgetter('arrival'))
    if int(dispatch_latency) < 0:
        error_status = get_error_message(5, -1, -1)
        error = 1
    elif algo == 3 and int(priority) < 0:
        error_status = get_error_message(3, -1, -1)
        error = 1
    elif algo == 3 and int(aging) <= 0:
        error_status = get_error_message(7, -1, -1)
        error = 1
    elif algo == 4 and int(quantum) <= 0:
        error_status = get_error_message(2, -1, -1)
        error = 1
    else:
        for process in processes:
            #total_size=process['mem_size']
            process_id = process['name']
            arrival_time = process['arrival']
            if int(arrival_time) < 0:
                error_status = get_error_message(4, process_id, -1)
                error = 1
                break
            burst_time = process['burst']
            if int(burst_time) <= 0:
                error_status = get_error_message(1, process_id, -1)
                error = 1
                break
            if algo == 5:
                if process['queue_assigned'] <= 0 or process['queue_assigned'] > num_queues:
                    error_status = get_error_message(0, process_id, -1)
                    error = 1
                    break
    if error == 0 and algo == 5:
        for i in range(len(quantum_queue)):
            if quantum_queue[i] <= 0 and algo_queue == 1:
                error_status = get_error_message(6, -1, i+1)
                error = 1
                break
    if(error == 0):
        error_status = get_error_message(-1, -1, -1)
    status = (error, error_status);
    return status

def create_dl_process(dispatch_latency, curr_time):
    dl_cpu = dict()
    dl_cpu['name'] = 'DL'
    dl_cpu['start'] = curr_time
    dl_cpu['end'] = curr_time + dispatch_latency
    return dl_cpu

def fcfs(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 1, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        processes = sorted(data, key=itemgetter('arrival'))
        process_chart = []
        curr_time = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0
        sum_time = 0
        details_process = {}
        for process in processes:
            temp_process = {}
            temp_process['arrival'] = process['arrival']
            temp_process['burst'] = process['burst']
            chart_details = {}

            if (process['arrival'] > curr_time):
                curr_time = process['arrival']

            # Add dispatch latency
            if (dispatch_latency > 0):
                dl_cpu = create_dl_process(dispatch_latency, curr_time)
                process_chart += [dl_cpu]
                curr_time += dispatch_latency

            chart_details['name'] = process['name']
            chart_details['start'] = curr_time
            chart_details['end'] = curr_time + process['burst']

            temp_process['wait_time'] = curr_time - process['arrival']
            wait_time += temp_process['wait_time']
            curr_time += process['burst']
            temp_process['turn_time'] = curr_time - process['arrival']
            temp_process['resp_time'] = chart_details['start'] - process['arrival']
            turn_time += temp_process['turn_time']
            resp_time += temp_process['resp_time']
            sum_time += process['burst']
            details_process[process['name']] = temp_process

            # Add Idle process if required
            if len(process_chart) > 0:
                if process_chart[-1]['end'] != chart_details['start']:
                    idle_cpu = dict()
                    idle_cpu['name'] = 'Idle'
                    idle_cpu['start'] = process_chart[-1]['end']
                    idle_cpu['end'] = chart_details['start']
                    process_chart += [idle_cpu]
            elif len(process_chart) == 0 and chart_details['start'] > 0:
                idle_cpu = dict()
                idle_cpu['name'] = 'Idle'
                idle_cpu['start'] = 0
                idle_cpu['end'] = chart_details['start']
                process_chart += [idle_cpu]

            process_chart += [chart_details]

        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(processes)
        stats['resp_time'] = float(resp_time)/len(processes)
        stats['turn_time'] = float(turn_time)/len(processes)
        stats['throughput'] = len(processes)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
        return process_chart, stats, details_process, error_status

def round_robin(data, quantum=4, dispatch_latency=0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, quantum, 4, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status

    all_processes = sorted(data, key=itemgetter('arrival'))
    curr_time = 0
    total_wait_time = 0
    total_resp_time = 0
    total_turn_time = 0
    sum_time = 0

    # The list of process objects in the gantt chart
    process_chart = []

    # Process wise details
    details_process = {}
    for process in all_processes:
        details_process[process['name']] = {}
        details_process[process['name']]['arrival'] = process['arrival']
        details_process[process['name']]['burst'] = process['burst']
        details_process[process['name']]['wait_time'] = 0
        details_process[process['name']]['turn_time'] = 0
        details_process[process['name']]['resp_time'] = 0

    process_queue = []
    add_processes_to_queue(all_processes, process_queue)

    robin_idx = 0
    prev_robin_idx = -1
    last_process_name = ''

    while process_queue:
        process = process_queue[robin_idx]

        if curr_time < process['arrival']:
            # Add idle process
            idle_cpu = dict()
            idle_cpu['name'] = 'Idle'
            idle_cpu['start'] = curr_time
            idle_cpu['end'] = process['arrival']
            process_chart += [idle_cpu]

            curr_time = process['arrival']

        # Add dispatch latency
        # if dispatch_latency > 0 and (robin_idx != prev_robin_idx or force_dispatch_flag):
        if dispatch_latency > 0 and last_process_name != process['name']:
            dl_cpu = create_dl_process(dispatch_latency, curr_time)
            process_chart += [dl_cpu]
            curr_time += dispatch_latency

        if (process['burst'] - process['time_given']) > quantum:
            time_added = quantum
            process['time_given'] += quantum
        else:
            time_added = process['burst'] - process['time_given']
            process['time_given'] = process['burst']

        if process['last_time'] == 0:
            process['start_time'] = curr_time
            process['resp_time'] = curr_time - process['arrival']
            process['wait_time'] += curr_time - process['arrival']
        else:
            process['wait_time'] += curr_time - process['last_time']

        # Add process segment to gantt chart
        chart_details = {}
        chart_details['name'] = process['name']
        chart_details['start'] = curr_time
        chart_details['end'] = curr_time+time_added
        process_chart += [chart_details]
        last_process_name = chart_details['name']

        curr_time += time_added
        process['last_time'] = curr_time

        if process['time_given'] == process['burst']: # Process has finished execution
            process['turn_time'] = curr_time - process['arrival']

            details_process[process['name']]['wait_time'] = process['wait_time']
            details_process[process['name']]['turn_time'] = process['turn_time']
            details_process[process['name']]['resp_time'] = process['resp_time']

            total_wait_time += process['wait_time']
            total_turn_time += process['turn_time']
            total_resp_time += process['resp_time']
            sum_time += process['burst']

            process_queue.remove(process)

            force_dispatch_flag = True
            if robin_idx >= len(process_queue):
                robin_idx = 0
        else:
            prev_robin_idx = robin_idx
            robin_idx = rr_get_next_process(robin_idx, curr_time, process_queue)
            force_dispatch_flag = False

    stats = {}
    stats['sum_time'] = sum_time
    stats['wait_time'] = float(total_wait_time)/len(all_processes)
    stats['resp_time'] = float(total_resp_time)/len(all_processes)
    stats['turn_time'] = float(total_turn_time)/len(all_processes)
    stats['throughput'] = len(all_processes)/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/float(curr_time)

    return process_chart, stats, details_process, error_status

# Returns the index of the next process to be scheduled
def rr_get_next_process(robin_idx, curr_time, process_queue):
    next_idx = (robin_idx+1)%len(process_queue)
    if process_queue[next_idx]['arrival'] <= curr_time:
        return next_idx
    else:
        return robin_idx

def add_processes_to_queue(processes, queue):
    for orig_process in processes:
        process = deepcopy(orig_process)
        process['time_given'] = 0
        process['last_time'] = 0
        process['wait_time'] = 0
        process['turn_time'] = 0
        process['resp_time'] = 0
        queue.append(process)

def round_robin_old(data, max_quanta = 4, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, max_quanta, 4, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        all_processes = sorted(data, key=itemgetter('arrival'))
        time_present = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0
        sum_time = 0
        count = 0
        details_process = []
        q = Queue.Queue(maxsize=0)
        for process in all_processes:
            q.put(process)
            count += 1
            temp_val = {}
            temp_val['name'] = process['name']
            temp_val['arrival'] = process['arrival']
            temp_val['burst'] = process['burst']
            temp_val['flag'] = 0
            temp_val['start'] = -1
            temp_val['end'] = -1
            details_process += [temp_val]
            del temp_val

        process_chart = []
        active_process = []
        var_count = 0
        while True:
            chart_details = {}
            temp_process = q.get()
                
            if temp_process['burst'] > 0 and temp_process['arrival'] <= time_present:
                for data in details_process:
                    if data['name'] == temp_process['name'] and data['flag'] == 0:
                        data['start'] = time_present
                        data['flag'] = 1

                quanta = max_quanta
                var_count = 0
                chart_details['name'] = temp_process['name']
                chart_details['start'] = time_present

                if temp_process['burst'] >= max_quanta:
                    temp_process['burst'] -= max_quanta
                else:
                    quanta = temp_process['burst']
                    temp_process['burst'] = 0

                if temp_process['burst'] > 0:
                    q.put(temp_process)
                    time_present += quanta
                    active_process.append(temp_process)
                else:
                    time_present += quanta
                    for data in details_process:
                        if data['name'] == temp_process['name'] and data['flag'] == 1:
                            data['end'] = time_present

                    if temp_process in active_process:
                        active_process.remove(temp_process)
                        count -= 1
                
                chart_details['end'] = time_present
                if len(process_chart) > 0:
                    temp_dict = process_chart[-1] 
                    if temp_dict['name'] == chart_details['name']:
                        chart_details['start'] = temp_dict['start']
                        del process_chart[-1]
                
                process_chart += [chart_details]
                    
            else:
                if len(active_process) > 0:
                    var_count = 0
                    quanta = 0
                else:
                    quanta = 1
                
                if quanta == 1:
                    var_count += 1
                    if var_count == count:
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                chart_details = process_chart[-1]
                                time_present += quanta
                                chart_details['end'] = time_present
                                del process_chart[-1]   
                                process_chart += [chart_details]
                            else:
                                chart_details = {}
                                chart_details['name'] = 'Idle'
                                chart_details['start'] = time_present
                                time_present += quanta  
                                chart_details['end'] = time_present
                                process_chart += [chart_details]
                                del chart_details
                        elif len(process_chart) == 0:
                            chart_details = {}
                            chart_details['name'] = 'Idle'
                            chart_details['start'] = 0
                            time_present += quanta  
                            chart_details['end'] = time_present
                            process_chart += [chart_details]
                            del chart_details
                        var_count = 0
                q.put(temp_process)
                
            if q.empty():
                break

        process_details = dict()
        for data in details_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(details_process)
        stats['resp_time'] = float(resp_time)/len(details_process)
        stats['turn_time'] = float(turn_time)/len(details_process)
        stats['throughput'] = len(details_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
            
        return process_chart, stats, process_details, error_status

def shortest_job_non_prempted(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 2, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        all_processes = sorted(data, key=itemgetter('burst'))
        time_present = 0
        var = 0
        wait_time = 0
        turn_time = 0
        resp_time = 0
        sum_time = 0
        completed_processes = list()
        process_chart = list()
        data_process = list()
        
        while True:
            for process in all_processes:
                chart_details = {}
                if process['burst'] > 0 and process['arrival'] <= time_present:
                    # Add dispatch latency
                    if dispatch_latency > 0:
                        dl_cpu = create_dl_process(dispatch_latency, time_present)
                        process_chart += [dl_cpu]
                        time_present += dispatch_latency

                    details_process = {}
                    chart_details['name'] = process['name']
                    details_process['name'] = process['name']
                    details_process['burst'] = process['burst']
                    details_process['arrival'] = process['arrival']
                    details_process['start'] = time_present
                    chart_details['start'] = time_present
                    time_present += process['burst']
                    chart_details['end'] = time_present
                    details_process['end'] = time_present
                    process['burst'] = 0
                    completed_processes.append(process)
                    process_chart += [chart_details]
                    var = 0
                    data_process += [details_process]
                    break
                else:
                    var += 1
                    if var == len(all_processes):
                        var = 0
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                idle_cpu = process_chart[-1]
                                time_present += 1
                                idle_cpu['end'] = time_present
                                del process_chart[-1]
                                process_chart += [idle_cpu]
                            else:
                                idle_cpu = dict()
                                idle_cpu['name'] = 'Idle'
                                idle_cpu['start'] = time_present
                                time_present += 1
                                idle_cpu['end'] = time_present
                                process_chart += [idle_cpu]
                        elif len(process_chart) == 0:
                            idle_cpu = dict()
                            idle_cpu['name'] = 'Idle'
                            idle_cpu['start'] = 0
                            time_present += 1
                            idle_cpu['end'] = time_present
                            process_chart += [idle_cpu]

            if len(all_processes) == len(completed_processes):
                break

        process_details = dict()
        for data in data_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(data_process)
        stats['resp_time'] = float(resp_time)/len(data_process)
        stats['turn_time'] = float(turn_time)/len(data_process)
        stats['throughput'] = len(data_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def shortest_job_prempted(data, dispatch_latency=0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 2, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status

    all_processes = sorted(data, key=itemgetter('arrival'))
    curr_time = 0
    total_wait_time = 0
    total_resp_time = 0
    total_turn_time = 0
    sum_time = 0

    # The list of process objects in the gantt chart
    process_chart = []

    # Process wise details
    details_process = {}
    for process in all_processes:
        details_process[process['name']] = {}
        details_process[process['name']]['arrival'] = process['arrival']
        details_process[process['name']]['burst'] = process['burst']
        details_process[process['name']]['wait_time'] = 0
        details_process[process['name']]['turn_time'] = 0
        details_process[process['name']]['resp_time'] = 0

    process_queue = []
    add_processes_to_queue(all_processes, process_queue)

    curr_process_idx = 0
    last_process_name = ''

    while process_queue:
        if curr_time < process_queue[0]['arrival']:
            # Add idle process
            idle_cpu = dict()
            idle_cpu['name'] = 'Idle'
            idle_cpu['start'] = curr_time
            idle_cpu['end'] = process_queue[0]['arrival']
            process_chart += [idle_cpu]

            curr_time = process_queue[0]['arrival']

        curr_process_idx = get_shortest(curr_time, process_queue)
        process = process_queue[curr_process_idx]

        dispatch_latency_added = False
        # Add dispatch latency
        if dispatch_latency > 0 and last_process_name != process['name']:
            dl_cpu = create_dl_process(dispatch_latency, curr_time)
            process_chart += [dl_cpu]
            curr_time += dispatch_latency
            dispatch_latency_added = True

        if dispatch_latency_added:
            next_arrival_time = get_next_arrival_time(curr_time-dispatch_latency, process_queue)
        else:
            next_arrival_time = get_next_arrival_time(curr_time, process_queue)

        while next_arrival_time != -1 and get_shortest(next_arrival_time, process_queue) == curr_process_idx:
            next_arrival_time = get_next_arrival_time(next_arrival_time, process_queue)

        # No other shorter process to preempt current process
        if next_arrival_time == -1:
            time_added = process['burst'] - process['time_given']
        elif next_arrival_time > curr_time + process['burst'] - process['time_given']:
            time_added = process['burst'] - process['time_given']
        else:
            time_added = next_arrival_time - curr_time

        # To handle cases with odd behaviour due to dispatch_latency
        # That is, by the time a process is dispatched, a new process arrives with shorter remaining burst
        if time_added < 0:
            time_added = 0

        process['time_given'] += time_added

        if process['last_time'] == 0:
            process['start_time'] = curr_time
            process['resp_time'] = curr_time - process['arrival']
            process['wait_time'] += curr_time - process['arrival']
        else:
            process['wait_time'] += curr_time - process['last_time']

        # Add process segment to gantt chart
        chart_details = {}
        chart_details['name'] = process['name']
        chart_details['start'] = curr_time
        chart_details['end'] = curr_time+time_added
        process_chart += [chart_details]
        last_process_name = chart_details['name']

        curr_time += time_added
        process['last_time'] = curr_time

        if process['time_given'] == process['burst']: # Process has finished execution
            process['turn_time'] = curr_time - process['arrival']

            details_process[process['name']]['wait_time'] = process['wait_time']
            details_process[process['name']]['turn_time'] = process['turn_time']
            details_process[process['name']]['resp_time'] = process['resp_time']

            total_wait_time += process['wait_time']
            total_turn_time += process['turn_time']
            total_resp_time += process['resp_time']
            sum_time += process['burst']

            process_queue.remove(process)

    stats = {}
    stats['sum_time'] = sum_time
    stats['wait_time'] = float(total_wait_time)/len(all_processes)
    stats['resp_time'] = float(total_resp_time)/len(all_processes)
    stats['turn_time'] = float(total_turn_time)/len(all_processes)
    stats['throughput'] = len(all_processes)/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/float(curr_time)

    return process_chart, stats, details_process, error_status

def get_shortest(curr_time, process_queue):
    shortest_burst = -1
    shortest_idx = -1

    for idx, process in enumerate(process_queue):
        if process['arrival'] <= curr_time and process['time_given'] != process['burst']:
            if shortest_burst == -1 or (process['burst'] - process['time_given'] < shortest_burst):
                shortest_burst = process['burst'] - process['time_given']
                shortest_idx = idx

    return shortest_idx

def get_next_arrival_time(curr_time, process_queue):
    for process in process_queue:
        if process['arrival'] <= curr_time:
            continue
        if process['time_given'] != process['burst']:
            return process['arrival']

    return -1

def shortest_job_prempted_old(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 2, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        all_processes = sorted(data, key=itemgetter('burst'))
        time_present = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0 
        sum_time = 0
        var = 0
        process_chart = []
        details_process = list()
        for process in all_processes:
            temp_val = {}
            temp_val['name'] = process['name']
            temp_val['arrival'] = process['arrival']
            temp_val['burst'] = process['burst']
            temp_val['flag'] = 0
            temp_val['start'] = -1
            temp_val['end'] = -1
            details_process += [temp_val]
            del temp_val

        while True:
            for process in all_processes:
                chart_details = {}
                if process['burst'] > 0 and process['arrival'] <= time_present:
                    for data in details_process:
                        if data['name'] == process['name'] and data['flag'] == 0:
                            data['start'] = time_present
                            data['flag'] = 1

                    chart_details['name'] = process['name']
                    chart_details['start'] = time_present
                    time_present += 1
                    chart_details['end'] = time_present
                    process['burst'] -= 1
                    if process['burst'] == 0:
                        for data in details_process:
                            if data['name'] == process['name'] and data['flag'] == 1:
                                data['end'] = time_present

                        all_processes.remove(process)
                    if len(process_chart) > 0:
                        temp_dict = process_chart[-1]
                        if temp_dict['name'] == chart_details['name']:
                            chart_details['start'] = temp_dict['start']
                            del process_chart[-1]
                    process_chart += [chart_details]
                    var = 0
                    break
                else:
                    var += 1
                    if var == len(all_processes):
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                idle_cpu = process_chart[-1]
                                time_present += 1
                                idle_cpu['end'] = time_present
                                del process_chart[-1]
                                process_chart += [idle_cpu]
                            else:
                                idle_cpu = dict()
                                idle_cpu['name'] = 'Idle'
                                idle_cpu['start'] = time_present
                                time_present += 1
                                idle_cpu['end'] = time_present
                                process_chart += [idle_cpu]
                        elif len(process_chart) == 0:
                            idle_cpu = dict()
                            idle_cpu['name'] = 'Idle'
                            idle_cpu['start'] = 0
                            time_present += 1
                            idle_cpu['end'] = time_present
                            process_chart += [idle_cpu]

                        var = 0
            if len(all_processes) == 0:
                break

            all_processes = sorted(all_processes, key=itemgetter('burst'))

        process_details = dict()
        for data in details_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(details_process)
        stats['resp_time'] = float(resp_time)/len(details_process)
        stats['turn_time'] = float(turn_time)/len(details_process)
        stats['throughput'] = len(details_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def priority_non_preemptive(data, increment_after_time = 4, upper_limit_priority = 0, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, upper_limit_priority, increment_after_time, -1, 3, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        all_processes = sorted(data, key=itemgetter('priority'))
        time_present = 0 
        var = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0 
        sum_time = 0
        completed_processes = list()
        process_chart = list()
        data_process = list()
        while True:
            for process in all_processes:
                chart_details = {}  
                if process['burst'] > 0 and process['arrival'] <= time_present:
                    # Add dispatch latency
                    if dispatch_latency > 0:
                        dl_cpu = create_dl_process(dispatch_latency, time_present)
                        process_chart += [dl_cpu]
                        time_present += dispatch_latency

                    details_process = {}
                    chart_details['name'] = process['name']
                    details_process['name'] = process['name']
                    details_process['burst'] = process['burst']
                    details_process['arrival'] = process['arrival']
                    details_process['start'] = time_present
                    chart_details['start'] = time_present
                    time_present += process['burst']
                    chart_details['end'] = time_present
                    details_process['end'] = time_present
                    for val_process in all_processes:
                        if 'wait_time' not in val_process:
                            val_process['wait_time'] = 0
                        if val_process['arrival'] < time_present and val_process['name'] != process['name'] and val_process['burst'] > 0:
                            val_process['wait_time'] += val_process['burst']
                            val_process['priority']  -= (val_process['wait_time'] / increment_after_time)
                            val_process['wait_time'] = val_process['wait_time'] % increment_after_time
                            if val_process['priority'] < upper_limit_priority:
                                val_process['priority'] = upper_limit_priority
                            process['burst'] = 0
        
                    completed_processes.append(process)
                    process_chart += [chart_details]
                    var = 0
                    data_process += [details_process]
                    break
                else:
                    var += 1
                    if var == len(all_processes):
                        var = 0
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                idle_cpu = process_chart[-1]
                                time_present += 1
                                idle_cpu['end'] = time_present
                                del process_chart[-1]
                                process_chart += [idle_cpu]
                            else:
                                idle_cpu = dict()
                                idle_cpu['name'] = 'Idle'
                                idle_cpu['start'] = time_present
                                time_present += 1
                                idle_cpu['end'] = time_present
                                process_chart += [idle_cpu]
                        elif len(process_chart) == 0:
                            idle_cpu = dict()
                            idle_cpu['name'] = 'Idle'
                            idle_cpu['start'] = 0
                            time_present += 1
                            idle_cpu['end'] = time_present
                            process_chart += [idle_cpu]

            if len(all_processes) == len(completed_processes):  
                break
            all_processes = sorted(all_processes, key=itemgetter('priority'))

        process_details = dict()
        for data in data_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(data_process)
        stats['resp_time'] = float(resp_time)/len(data_process)
        stats['turn_time'] = float(turn_time)/len(data_process)
        stats['throughput'] = len(data_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
        
        return process_chart, stats, process_details, error_status

def priority_preemptive(data, increment_after_time=4, upper_limit_priority=0, dispatch_latency=0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, upper_limit_priority, increment_after_time, -1, 3, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status

    all_processes = sorted(data, key=itemgetter('arrival'))
    curr_time = 0
    total_wait_time = 0
    total_resp_time = 0
    total_turn_time = 0
    sum_time = 0

    # The list of process objects in the gantt chart
    process_chart = []

    # Process wise details
    details_process = {}
    for process in all_processes:
        details_process[process['name']] = {}
        details_process[process['name']]['arrival'] = process['arrival']
        details_process[process['name']]['burst'] = process['burst']
        details_process[process['name']]['wait_time'] = 0
        details_process[process['name']]['turn_time'] = 0
        details_process[process['name']]['resp_time'] = 0

    # To handle aging
    aging_wait_time = {}
    for process in all_processes:
        aging_wait_time[process['name']] = 0

    # Enforce priority limit
    for process in all_processes:
        if process['priority'] < upper_limit_priority:
            process['priority'] = upper_limit_priority

    process_queue = []
    add_processes_to_queue(all_processes, process_queue)

    curr_process_idx = 0
    last_process_name = ''

    while process_queue:
        if curr_time < process_queue[0]['arrival']:
            # Add idle process
            idle_cpu = dict()
            idle_cpu['name'] = 'Idle'
            idle_cpu['start'] = curr_time
            idle_cpu['end'] = process_queue[0]['arrival']
            process_chart += [idle_cpu]

            curr_time = process_queue[0]['arrival']

        curr_process_idx = get_most_priority(curr_time, process_queue)
        process = process_queue[curr_process_idx]

        dispatch_latency_added = False
        # Add dispatch latency
        if dispatch_latency > 0 and last_process_name != process['name']:
            dl_cpu = create_dl_process(dispatch_latency, curr_time)
            process_chart += [dl_cpu]
            curr_time += dispatch_latency
            dispatch_latency_added = True

        if dispatch_latency_added:
            next_arrival_time = get_next_arrival_time(curr_time-dispatch_latency, process_queue)
        else:
            next_arrival_time = get_next_arrival_time(curr_time, process_queue)

        while next_arrival_time != -1 and get_most_priority(next_arrival_time, process_queue) == curr_process_idx:
            next_arrival_time = get_next_arrival_time(next_arrival_time, process_queue)

        # No other high priority process to preempt current process
        if next_arrival_time == -1:
            time_added = process['burst'] - process['time_given']
        elif next_arrival_time > curr_time + process['burst'] - process['time_given']:
            time_added = process['burst'] - process['time_given']
        else:
            time_added = next_arrival_time - curr_time

        # To handle cases with odd behaviour due to dispatch_latency
        # That is, by the time a process is dispatched, a new process arrives with shorter remaining burst
        if time_added < 0:
            time_added = 0

        # Handle aging
        # Find candidates which might preempt current process before curr_time + time_added
        aging_disrupt_idx, aging_disrupt_time = get_aging_process(curr_process_idx, curr_time, time_added, increment_after_time, process_queue, aging_wait_time)

        # Found a candidate
        if aging_disrupt_idx != -1:
            # To prevent time_given from exceeding burst_time
            if aging_disrupt_time < time_added:
                time_added = aging_disrupt_time

        process['time_given'] += time_added

        # print "aging_disrupt_idx: {}, aging_disrupt_time: {}".format(aging_disrupt_idx, aging_disrupt_time)
        # print "time_added: {}, {}['time_given']: {}".format(time_added, process['name'], process['time_given'])

        if process['last_time'] == 0:
            process['start_time'] = curr_time
            process['resp_time'] = curr_time - process['arrival']
            process['wait_time'] += curr_time - process['arrival']
        else:
            process['wait_time'] += curr_time - process['last_time']

        # Add process segment to gantt chart
        chart_details = {}
        chart_details['name'] = process['name']
        chart_details['start'] = curr_time
        chart_details['end'] = curr_time+time_added
        process_chart += [chart_details]
        last_process_name = chart_details['name']

        curr_time += time_added
        process['last_time'] = curr_time

        if process['time_given'] == process['burst']: # Process has finished execution
            process['turn_time'] = curr_time - process['arrival']

            details_process[process['name']]['wait_time'] = process['wait_time']
            details_process[process['name']]['turn_time'] = process['turn_time']
            details_process[process['name']]['resp_time'] = process['resp_time']

            total_wait_time += process['wait_time']
            total_turn_time += process['turn_time']
            total_resp_time += process['resp_time']
            sum_time += process['burst']

            process_queue.remove(process)

    stats = {}
    stats['sum_time'] = sum_time
    stats['wait_time'] = float(total_wait_time)/len(all_processes)
    stats['resp_time'] = float(total_resp_time)/len(all_processes)
    stats['turn_time'] = float(total_turn_time)/len(all_processes)
    stats['throughput'] = len(all_processes)/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/float(curr_time)

    return process_chart, stats, details_process, error_status

def get_most_priority(curr_time, process_queue):
    shortest_priority = -1
    shortest_idx = -1

    for idx, process in enumerate(process_queue):
        if process['arrival'] <= curr_time and process['time_given'] != process['burst']:
            if shortest_priority == -1 or process['priority'] < shortest_priority:
                shortest_priority = process['priority']
                shortest_idx = idx

    return shortest_idx

def get_aging_process(curr_process_idx, curr_time, time_added, increment_after_time, process_queue, aging_wait_time):
    aging_disrupt_idx = -1
    aging_disrupt_time = -1

    if process_queue[curr_process_idx]['priority'] == 0:
        return aging_disrupt_idx, aging_disrupt_time

    for idx, process in enumerate(process_queue):
        if idx == curr_process_idx:
            continue
        if process['arrival'] >= curr_time + time_added:
            continue

        wait_time = curr_time + time_added - process['arrival']
        aging_wait_time[process['name']] += wait_time

        # Time needed to get this process's priority higher than currently executing process
        time_needed = (process['priority'] - (process_queue[curr_process_idx]['priority'] - 1)) * increment_after_time

        if aging_wait_time[process['name']] >= time_needed:
            aging_disrupt_idx = idx
            aging_disrupt_time = time_needed

            aging_wait_time[process['name']] -= time_needed
            process['priority'] -= time_needed/increment_after_time

            return aging_disrupt_idx, aging_disrupt_time
        else:
            process['priority'] -= aging_wait_time[process['name']]/increment_after_time
            aging_wait_time[process['name']] %= increment_after_time

    return aging_disrupt_idx, aging_disrupt_time

def priority_preemptive_old(data, increment_after_time = 4, upper_limit_priority = 0, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, upper_limit_priority, increment_after_time, -1, 3, -1, -1, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        all_processes = sorted(data, key=itemgetter('priority'))
        time_present = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0 
        sum_time = 0
        var = 0
        process_chart = list()
        details_process = list()

        for process in all_processes:
            temp_val = {}
            temp_val['name'] = process['name']
            temp_val['arrival'] = process['arrival']
            temp_val['burst'] = process['burst']
            temp_val['flag'] = 0
            temp_val['start'] = -1
            temp_val['end'] = -1
            details_process += [temp_val]
            del temp_val

        while True:
            for process in all_processes:
                chart_details = {}
                if process['burst'] > 0 and process['arrival'] <= time_present:
                    for data in details_process:
                        if data['name'] == process['name'] and data['flag'] == 0:
                            data['start'] = time_present
                            data['flag'] = 1

                    chart_details['name'] = process['name']
                    chart_details['start'] = time_present
                    time_present += 1
                    chart_details['end'] = time_present
                    process['burst'] -= 1
                    for val_process in all_processes:
                        if 'wait_time' not in val_process:
                            val_process['wait_time'] = 0
                        if val_process['arrival'] < time_present and val_process['name'] != process['name'] and val_process['burst'] > 0:
                            val_process['wait_time'] += 1
                            val_process['priority']  -= (val_process['wait_time'] / increment_after_time)
                            val_process['wait_time'] = val_process['wait_time'] % increment_after_time
                            if val_process['priority'] < upper_limit_priority:
                                val_process['priority'] = upper_limit_priority

                    if process['burst'] == 0:
                        for data in details_process:
                            if data['name'] == process['name'] and data['flag'] == 1:
                                data['end'] = time_present

                        all_processes.remove(process)

                    if len(process_chart) > 0:
                        temp_dict = process_chart[-1]
                        if temp_dict['name'] == chart_details['name']:
                            chart_details['start'] = temp_dict['start']
                            del process_chart[-1]
                    process_chart += [chart_details]
                    var = 0
                    break
                else:
                    var += 1
                    if var == len(all_processes):
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                idle_cpu = process_chart[-1]
                                time_present += 1
                                idle_cpu['end'] = time_present
                                del process_chart[-1]
                                process_chart += [idle_cpu]
                            else:
                                idle_cpu = dict()
                                idle_cpu['name'] = 'Idle'
                                idle_cpu['start'] = time_present
                                time_present += 1
                                idle_cpu['end'] = time_present
                                process_chart += [idle_cpu]
                        elif len(process_chart) == 0:
                            idle_cpu = dict()
                            idle_cpu['name'] = 'Idle'
                            idle_cpu['start'] = 0
                            time_present += 1
                            idle_cpu['end'] = time_present
                            process_chart += [idle_cpu]

                        var = 0
            if len(all_processes) == 0:
                break

            all_processes = sorted(all_processes, key=itemgetter('priority'))

        process_details = dict()
        for data in details_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(details_process)
        stats['resp_time'] = float(resp_time)/len(details_process)
        stats['turn_time'] = float(turn_time)/len(details_process)
        stats['throughput'] = len(details_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def multilevel(data, num_queues, algo_queue, quantum_queue, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 5, num_queues, quantum_queue, algo_queue)
    if(error):
        return -1, -1, -1, error_status
    else:
        queue_data = [[] for i in range(num_queues)]
        all_processes = data
        queue_cpu_schedule = [list() for i in range(num_queues)]
        queue_stats = [{} for i in range(num_queues)]
        queue_details = [{} for i in range(num_queues)]
        queue_error_status = [{} for i in range(num_queues)]
        priority_cpu_scheduling = []
        priority_error_status = {}
        priority_stats = {}
        priority_details = {}
        priority_process = {}
        priority_data = []
        process_chart = list()
        details_process = []
        index = [0]*num_queues
        flag = False
        wait_time = 0
        resp_time = 0
        turn_time = 0 
        sum_time = 0
        idx = 0
        # For assignment of processes to their respective queues
        for process in all_processes:
            queue_data[process['queue_assigned']-1].append(process)
            temp_val = {}
            temp_val['name'] = process['name']
            temp_val['arrival'] = process['arrival']
            temp_val['burst'] = process['burst']
            temp_val['flag'] = 0
            temp_val['start'] = -1
            temp_val['end'] = -1
            details_process += [temp_val]
            del temp_val
        # Calling fcfs or round robin cpu scheduling algorithm on every queue
        for i in range(num_queues):
            if algo_queue[i] == 0 and len(queue_data[i])>0:
                queue_cpu_schedule[i], queue_stats[i], queue_details[i], queue_error_status[i] = fcfs(queue_data[i], 0)
            elif algo_queue[i] == 1 and len(queue_data[i])>0:
                queue_cpu_schedule[i], queue_stats[i], queue_details[i], queue_error_status[i] = round_robin(queue_data[i], quantum_queue[i], 0)
        for i in range(num_queues):
            for index_queue ,process in enumerate(queue_cpu_schedule[i]):
                if flag == False and process['name'] != 'Idle':
                    priority_process['name'] = process['name']
                    priority_process['arrival'] = process['start']
                    priority_process['priority'] = i
                    flag = True
                elif flag == True and process['name'] == 'Idle':
                    priority_process['burst'] = queue_cpu_schedule[i][index_queue-1]['end'] - priority_process['arrival']
                    flag = False
                    priority_data.insert(idx, deepcopy(priority_process))
                    idx = idx+1
                if process['name'] == queue_cpu_schedule[i][-1]['name'] and flag == True:
                    priority_process['burst'] = process['end'] - priority_process['arrival']
                    flag = False
                    priority_data.insert(idx, deepcopy(priority_process))
                    idx = idx+1
        priority_cpu_scheduling, priority_stats, priority_details, priority_error_status = priority_preemptive(priority_data, maxsize, 0)
        curr_time = 0
        for chart_details in priority_cpu_scheduling:
            interval = chart_details['end'] - chart_details['start']
            if chart_details['name'] == 'Idle':
                diff = curr_time - chart_details['start']
                if diff > 0 and diff < interval:
                    temp_process = {}
                    temp_process['name'] = chart_details['name']
                    temp_process['start'] = curr_time
                    temp_process['end'] = chart_details['end']
                    process_chart.append(deepcopy(temp_process))
                    curr_time += interval - diff
                elif diff > 0 and diff >= interval:
                    continue
                else:
                    process_chart.append(deepcopy(chart_details))
                    curr_time += interval
            else:
                for process in priority_data:
                    if process['name'] == chart_details['name']:
                        while True:
                            temp_process = {}
                            temp_process = deepcopy(queue_cpu_schedule[process['priority']][index[process['priority']]])
                            exp_process = {}
                            exp_process = queue_cpu_schedule[process['priority']][index[process['priority']]]

                            if temp_process['name'] == 'Idle':
                                index[process['priority']] += 1
                                continue

                            # Add dispatch latency
                            if (dispatch_latency > 0):
                                if len(process_chart) == 0 or (len(process_chart) > 0 and temp_process['name'] != process_chart[-1]['name']):
                                    dl_cpu = dict()
                                    dl_cpu['name'] = 'DL'
                                    dl_cpu['start'] = curr_time
                                    dl_cpu['end'] = curr_time + dispatch_latency
                                    process_chart += [dl_cpu]
                                    curr_time += dispatch_latency
                            temp_process['start'] = curr_time  
                            for details in details_process:
                                if details['name'] == temp_process['name']: 
                                    if details['flag'] == 0:
                                        details['start'] = curr_time
                                        details['flag'] = 1
                            if (exp_process['end'] - exp_process['start']) <= interval:
                                curr_time += exp_process['end'] - exp_process['start']
                                temp_process['end'] = curr_time
                                index[process['priority']] += 1 
                                for details in details_process:
                                    if details['name'] == temp_process['name']:
                                        if details['flag'] == 1:
                                            details['end'] = curr_time
                                process_chart.append(deepcopy(temp_process))
                                if (exp_process['end'] - exp_process['start']) < interval:
                                    interval -= exp_process['end'] - exp_process['start']
                                    continue
                                else:
                                    interval -= exp_process['end'] - exp_process['start']
                                    break
                            else:
                                curr_time += interval
                                temp_process['end'] = curr_time
                                queue_cpu_schedule[process['priority']][index[process['priority']]]['start'] += interval
                                process_chart.append(deepcopy(temp_process))
                                interval = 0
                                for details in details_process:
                                    if details['name'] == temp_process['name']:
                                        if details['flag'] == 1:
                                            details['end'] = curr_time
                                break
                        break
                                                   
        process_details = dict()
        for data in details_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(details_process)
        stats['resp_time'] = float(resp_time)/len(details_process)
        stats['turn_time'] = float(turn_time)/len(details_process)
        stats['throughput'] = len(details_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def add_processes_to_list_multilevel_feedback(processes):
    process_list = []
    for orig_process in processes:
        process = deepcopy(orig_process)
        process['time_given'] = 0
        process['last_time'] = 0
        process['wait_time'] = 0
        process['turn_time'] = 0
        process['resp_time'] = 0
        process['queue_num'] = 0
        process_list.append(process)

    return process_list

def get_highest_queue(curr_time, process_queue):
    shortest_queue = -1
    shortest_idx = -1

    for idx, process in enumerate(process_queue):
        if process['arrival'] <= curr_time and process['time_given'] != process['burst']:
            if shortest_queue == -1 or process['queue_num'] < shortest_queue:
                shortest_queue = process['queue_num']
                shortest_idx = idx

    return shortest_idx

def multilevel_feedback(data, num_queues, queue_quantum, dispatch_latency=0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 6, num_queues, queue_quantum, -1)
    if(error):
        return -1, -1, -1, error_status

    all_processes = sorted(data, key=itemgetter('arrival'))
    curr_time = 0
    total_wait_time = 0
    total_resp_time = 0
    total_turn_time = 0
    sum_time = 0

    # The list of process objects in the gantt chart
    process_chart = []

    # Process wise details
    details_process = {}
    for process in all_processes:
        details_process[process['name']] = {}
        details_process[process['name']]['arrival'] = process['arrival']
        details_process[process['name']]['burst'] = process['burst']
        details_process[process['name']]['wait_time'] = 0
        details_process[process['name']]['turn_time'] = 0
        details_process[process['name']]['resp_time'] = 0

    process_queue = add_processes_to_list_multilevel_feedback(all_processes)

    robin_idx = 0
    last_process_name = ''

    while process_queue:
        # Not expected to happen, added for safety
        if robin_idx < 0:
            robin_idx = 0

        process = process_queue[robin_idx]

        if curr_time < process['arrival']:
            # Add idle process
            idle_cpu = dict()
            idle_cpu['name'] = 'Idle'
            idle_cpu['start'] = curr_time
            idle_cpu['end'] = process['arrival']
            process_chart += [idle_cpu]

            curr_time = process['arrival']

        dispatch_latency_added = False
        # Add dispatch latency
        if dispatch_latency > 0 and last_process_name != process['name']:
            dl_cpu = create_dl_process(dispatch_latency, curr_time)
            process_chart += [dl_cpu]
            curr_time += dispatch_latency
            dispatch_latency_added = True

        if dispatch_latency_added:
            next_arrival_time = get_next_arrival_time(curr_time-dispatch_latency, process_queue)
        else:
            next_arrival_time = get_next_arrival_time(curr_time, process_queue)

        while next_arrival_time != -1 and get_highest_queue(next_arrival_time, process_queue) == robin_idx:
            next_arrival_time = get_next_arrival_time(next_arrival_time, process_queue)

        # No other process to preempt current process
        if next_arrival_time == -1:
            time_added = process['burst'] - process['time_given']
        elif next_arrival_time > curr_time + process['burst'] - process['time_given']:
            time_added = process['burst'] - process['time_given']
        # Preemption
        else:
            time_added = next_arrival_time - curr_time

        # Adjust for queue time quantum
        if process['queue_num'] == len(queue_quantum):
            # Pseudo infinite quantum to simulate FCFS
            # TODO: Better implementation
            quantum = 1000000000000000000
        else:
            quantum = queue_quantum[process['queue_num']]
        if time_added > quantum:
            time_added = quantum

        # To handle cases with odd behaviour due to dispatch_latency
        # That is, by the time a process is dispatched, a new process arrives with shorter remaining burst
        if time_added < 0:
            time_added = 0

        process['time_given'] += time_added

        if process['last_time'] == 0:
            process['start_time'] = curr_time
            process['resp_time'] = curr_time - process['arrival']
            process['wait_time'] += curr_time - process['arrival']
        else:
            process['wait_time'] += curr_time - process['last_time']

        # Add process segment to gantt chart
        chart_details = {}
        chart_details['name'] = process['name']
        chart_details['start'] = curr_time
        chart_details['end'] = curr_time + time_added
        chart_details['queue_name'] = process['queue_num'] + 1
        if process['time_given'] == process['burst']:
            # Next queue == 0 marks process completion
            chart_details['next_queue'] = 0
        else:
            chart_details['next_queue'] = process['queue_num'] + 1

        process_chart += [chart_details]
        last_process_name = chart_details['name']

        prev_queue_num = process['queue_num']
        # If the process wasn't picked from the last (fcfs) queue
        if process['queue_num'] < len(queue_quantum):
            process['queue_num'] += 1
            # print "Moving process {} to Q{}".format(process['name'], process['queue_num']+1)

        curr_time += time_added
        process['last_time'] = curr_time

        if process['time_given'] == process['burst']: # Process has finished execution
            process['turn_time'] = curr_time - process['arrival']

            details_process[process['name']]['wait_time'] = process['wait_time']
            details_process[process['name']]['turn_time'] = process['turn_time']
            details_process[process['name']]['resp_time'] = process['resp_time']

            total_wait_time += process['wait_time']
            total_turn_time += process['turn_time']
            total_resp_time += process['resp_time']
            sum_time += process['burst']

            process_queue.remove(process)

            force_dispatch_flag = True
            # Happens when last idx process was completed and removed from process_queue
            if robin_idx >= len(process_queue):
                robin_idx = len(process_queue) - 1

            if len(process_queue) > 0:
                robin_idx = mf_get_next_process(robin_idx, curr_time, process_queue, prev_queue_num, queue_quantum)
        else:
            robin_idx = mf_get_next_process(robin_idx, curr_time, process_queue, prev_queue_num, queue_quantum)
            force_dispatch_flag = False

    stats = {}
    stats['sum_time'] = sum_time
    stats['wait_time'] = float(total_wait_time)/len(all_processes)
    stats['resp_time'] = float(total_resp_time)/len(all_processes)
    stats['turn_time'] = float(total_turn_time)/len(all_processes)
    stats['throughput'] = len(all_processes)/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/float(curr_time)

    return process_chart, stats, details_process, error_status

# Returns the index of the next process to be scheduled
# If no process is found to be scheduled, we've reached the last queue, hence directly apply FCFS
def mf_get_next_process(robin_idx, curr_time, process_queue, prev_queue_num, queue_quantum):
    next_idx = (robin_idx + 1) % len(process_queue)

    # Try to find a process with same queue number
    same_idx = -1
    while next_idx != robin_idx:
        if process_queue[next_idx]['arrival'] > curr_time or process_queue[next_idx]['queue_num'] > prev_queue_num:
            next_idx = (next_idx + 1) % len(process_queue)
            continue

        # Found a higher priority process (can only happen in case a new process enters the first queue
        # while the previous process executed)
        if process_queue[next_idx]['queue_num'] < prev_queue_num:
            return next_idx

        # Found a same priority process
        if same_idx == -1 and process_queue[next_idx]['queue_num'] == prev_queue_num:
            same_idx = next_idx

        next_idx = (next_idx + 1) % len(process_queue)

    # Found process in same queue
    if same_idx != -1:
        return same_idx
    else:
        highest_queue_idx = get_highest_queue(curr_time, process_queue)
        if process_queue[highest_queue_idx]['queue_num'] == len(queue_quantum):
            # FCFS: Start with process that arrived first
            # print "Calling get_min_arrival_process at curr_time: {} for prev_queue_num: {}".format(curr_time, prev_queue_num)
            return get_min_arrival_process(process_queue)
        else:
            return highest_queue_idx

def get_min_arrival_process(process_queue):
    min_arrival_time = -1
    min_arrival_idx = -1

    for idx,process in enumerate(process_queue):
        if min_arrival_time == -1 or process['arrival'] < min_arrival_time:
            min_arrival_time = process['arrival']
            min_arrival_idx = idx

    return min_arrival_idx

def multilevel_feedback_old(data, num_queues, quantum_queue, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, -1, 6, num_queues, quantum_queue, -1)
    if(error):
        return -1, -1, -1, error_status
    else:
        queue_data = [[] for i in range(num_queues)]
        all_processes = sorted(data, key=itemgetter('arrival'))
        time_present = 0
        wait_time = 0
        resp_time = 0
        turn_time = 0
        sum_time = 0
        details_process = []
        process_chart = []
        for process in all_processes:
            queue_data[0].append(process)
            temp_val = {}
            temp_val['name'] = process['name']
            temp_val['arrival'] = process['arrival']
            temp_val['burst'] = process['burst']
            temp_val['flag'] = 0
            temp_val['start'] = -1
            temp_val['end'] = -1
            details_process += [temp_val]
            del temp_val
        for i in range(num_queues-1):
            for process in queue_data[i]:
                successful = False
                while not successful:
                    chart_details = {}

                    if process['burst'] > 0 and process['arrival'] <= time_present:
                        successful = True
                        chart_details['queue_name'] = i+1
                        # Add dispatch latency
                        if (dispatch_latency > 0):
                            if len(process_chart) == 0 or (len(process_chart) > 0 and process['name'] != process_chart[-1]['name']):
                                dl_cpu = dict()
                                dl_cpu['name'] = 'DL'
                                dl_cpu['start'] = time_present
                                dl_cpu['end'] = time_present + dispatch_latency
                                dl_cpu['queue_name'] = 0
                                process_chart += [dl_cpu]
                                time_present += dispatch_latency
                        for data in details_process:
                            if data['name'] == process['name'] and data['flag'] == 0:
                                data['start'] = time_present
                                data['flag'] = 1
                        chart_details['name'] = process['name']
                        chart_details['start'] = time_present
                        quanta = quantum_queue[i]

                        if process['burst'] >= quantum_queue[i]:
                            process['burst'] -= quantum_queue[i]
                        else:
                            quanta = process['burst']
                            process['burst'] = 0

                        if process['burst'] > 0:
                            queue_data[i+1].append(process)
                            chart_details['next_queue'] = i+1
                            time_present += quanta
                            
                        else:
                            time_present += quanta
                            chart_details['next_queue'] = 0
                            for data in details_process:
                                if data['name'] == process['name'] and data['flag'] == 1:
                                    data['end'] = time_present
                           
                        chart_details['end'] = time_present
                        if len(process_chart) > 0:
                            temp_dict = process_chart[-1]
                            if temp_dict['name'] == chart_details['name']:
                                chart_details['start'] = temp_dict['start']
                                del process_chart[-1]
                        
                        process_chart += [chart_details]
                    else:  
                        chart_details['queue_name'] = 0          
                        if len(process_chart) > 0:
                            if process_chart[-1]['name'] == 'Idle':
                                chart_details = process_chart[-1]
                                time_present += 1
                                chart_details['end'] = time_present
                                chart_details['next_queue'] = 0
                                del process_chart[-1]   
                                process_chart += [chart_details]
                            else:
                                chart_details = {}
                                chart_details['name'] = 'Idle'
                                chart_details['start'] = time_present
                                chart_details['next_queue'] = 0
                                time_present += 1 
                                chart_details['end'] = time_present
                                process_chart += [chart_details]
                                del chart_details
                        elif len(process_chart) == 0:
                            chart_details = {}
                            chart_details['name'] = 'Idle'
                            chart_details['start'] = 0
                            chart_details['next_queue'] = 0
                            time_present += 1  
                            chart_details['end'] = time_present
                            process_chart += [chart_details]
                            del chart_details
                        var_count = 0

        for process in queue_data[num_queues-1]:
            chart_details = {}
            if (process['arrival'] > time_present):
                time_present = process['arrival']
            # Add dispatch latency
            if (dispatch_latency > 0):
                if len(process_chart) == 0 or (len(process_chart) > 0 and process['name'] != process_chart[-1]['name']):
                    dl_cpu = dict()
                    dl_cpu['name'] = 'DL'
                    dl_cpu['start'] = time_present
                    dl_cpu['end'] = time_present + dispatch_latency
                    dl_cpu['queue_name'] = 0
                    process_chart += [dl_cpu]
                    time_present += dispatch_latency
            for data in details_process:
                if data['name'] == process['name'] and data['flag'] == 0:
                    data['start'] = time_present
                    data['flag'] = 1
            chart_details['name'] = process['name']
            chart_details['start'] = time_present
            chart_details['end'] = time_present + process['burst']
            chart_details['next_queue'] = 0
            chart_details['queue_name'] = num_queues
            time_present = time_present + process['burst']
            for data in details_process:
                if data['name'] == process['name'] and data['flag'] == 1:
                    data['end'] = time_present 
            if len(process_chart) > 0:
                if process_chart[-1]['end'] != chart_details['start']:
                    idle_cpu = dict()
                    idle_cpu['name'] = 'Idle'
                    idle_cpu['start'] = process_chart[-1]['end']
                    idle_cpu['end'] = chart_details['start']
                    idle_cpu['queue_name'] = 0
                    process_chart += [idle_cpu]
            elif len(process_chart) == 0 and chart_details['start'] > 0:
                idle_cpu = dict()
                idle_cpu['name'] = 'Idle'
                idle_cpu['start'] = 0
                idle_cpu['end'] = chart_details['start']
                idle_cpu['queue_name'] = 0
                process_chart += [idle_cpu]

            process_chart += [chart_details]


        process_details = dict()
        for data in details_process:
            process_details[data['name']] = dict()
            process_details[data['name']]['resp_time'] = data['start'] - data['arrival']
            process_details[data['name']]['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
            process_details[data['name']]['turn_time'] = (data['end'] - data['arrival'])
            wait_time += process_details[data['name']]['wait_time']
            resp_time += process_details[data['name']]['resp_time']
            turn_time += process_details[data['name']]['turn_time']
            sum_time += data['burst']

        curr_time = time_present
        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(details_process)
        stats['resp_time'] = float(resp_time)/len(details_process)
        stats['turn_time'] = float(turn_time)/len(details_process)
        stats['throughput'] = len(details_process)/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
            
        return process_chart, stats, process_details, error_status
