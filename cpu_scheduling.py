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


# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, process_id, queue_number=-1):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Queue assigned to process " + str(process_id) + " does not exist. Please assign a valid queue to the process." + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = "Please enter a valid CPU burst time for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = "Time quantum entered is invalid. Please enter a valid time quantum.\n" + default_message
        ERROR['error_number'] = 2
    elif error_number == 3:
        ERROR['error_message'] = "Please enter a valid priority for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 3
    elif error_number == 4:
        ERROR['error_message'] = "Please enter a valid arrival time for process " + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 4
    elif error_number == 5:
        ERROR['error_message'] = "Please enter a valid dispatch latency.\n" + default_message
        ERROR['error_number'] = 5
    elif error_number == 6:
        ERROR['error_message'] = "Time quantum entered for queue " + str(queue_number) + " is invalid. Please enter a valid time quantum.\n" + default_message
        ERROR['error_number'] = 6
    return ERROR

# Values for algo : FCFS = 1, SJF Premptive/Non-premptive = 2, Priority Premptive/Non-premptive = 3, Round Robin = 4, Multilevel Queue = 5, Multilevel Feedback Queue = 6
def check_for_bad_input(data, dispatch_latency, priority, quantum, algo, num_queues, quantum_queue, algo_queue):
    error = 0 # Boolean to check bad input 
    error_status = {} # Dictionary to store error number and error message
    processes = sorted(data, key=itemgetter('arrival'))
    if int(dispatch_latency) < 0:
        error_status = get_error_message(5, -1, -1)
        error = 1
    elif algo == 3 and priority < 0:
        error_status = get_error_message(3, -1, -1)
        error = 1
    elif algo == 4 and quantum <= 0:
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
        for i in range(quantum_queue):
            if quantum_queue[i] <= 0 and algo_queue == 1:
                error_status = get_error_message(6, -1, i+1)
                error = 1
                break
    if(error == 0):
        error_status = get_error_message(-1, -1, -1)
    status = (error, error_status);
    return status


def fcfs(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, 1, -1, -1, -1)
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

            # Add dispatch latency
            if (dispatch_latency > 0):
                dl_cpu = dict()
                dl_cpu['name'] = 'DL'
                dl_cpu['start'] = chart_details['end']
                dl_cpu['end'] = chart_details['end'] + dispatch_latency
                process_chart += [dl_cpu]
                curr_time += dispatch_latency

        stats = {}
        stats['sum_time'] = sum_time
        stats['wait_time'] = float(wait_time)/len(processes)
        stats['resp_time'] = float(resp_time)/len(processes)
        stats['turn_time'] = float(turn_time)/len(processes)
        stats['throughput'] = len(processes)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
        return process_chart, stats, details_process, error_status

def round_robin(data, max_quanta = 4, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, max_quanta, 4, -1, -1, -1)
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
        stats['throughput'] = len(details_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
            
        return process_chart, stats, process_details, error_status

def shortest_job_non_prempted(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, 2, -1, -1, -1)
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
        stats['throughput'] = len(data_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status
    
def shortest_job_prempted(data, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, 2, -1, -1, -1)
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
        stats['throughput'] = len(details_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def priority_non_preemptive(data, increment_after_time = 4, upper_limit_priority = 0, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, upper_limit_priority, -1, 3, -1, -1, -1)
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
        stats['throughput'] = len(data_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
        
        return process_chart, stats, process_details, error_status
    
def priority_preemptive(data, increment_after_time = 4, upper_limit_priority = 0, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, upper_limit_priority, -1, 3, -1, -1, -1)
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
        stats['throughput'] = len(details_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status

def multilevel(data, num_queues, algo_queue, quantum_queue, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, 5, num_queues, quantum_queue, algo_queue)
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
            if algo_queue[i] == 0:
                queue_cpu_schedule[i], queue_stats[i], queue_details[i], queue_error_status[i] = fcfs(queue_data[i], dispatch_latency)
            elif algo_queue[i] == 1:
                queue_cpu_schedule[i], queue_stats[i], queue_details[i], queue_error_status[i] = round_robin(queue_data[i], quantum_queue[i], dispatch_latency)
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
        priority_cpu_scheduling, priority_stats, priority_details, priority_error_status = priority_preemptive(priority_data, maxsize, dispatch_latency)
        curr_time = 0
        for chart_details in priority_cpu_scheduling:
            if chart_details['name'] == 'Idle':
                process_chart.append(deepcopy(chart_details))
            else:
                for process in priority_data:
                    if process['name'] == chart_details['name']:
                        while True:
                            temp_process = {}
                            temp_process = queue_cpu_schedule[process['priority']][index[process['priority']]].copy()
                            exp_process = {}
                            exp_process = queue_cpu_schedule[process['priority']][index[process['priority']]]
                            temp_process['start'] = curr_time  
                            if temp_process['name'] == 'Idle':
                                index[process['priority']] += 1
                                continue
                            for details in details_process:
                                if details['name'] == temp_process['name']: 
                                    if details['flag'] == 0:
                                        details['start'] = curr_time
                                        details['flag'] = 1
                            if (temp_process['end'] - exp_process['start'] + curr_time) < chart_details['end']:
                                process_chart.append(deepcopy(temp_process))
                                index[process['priority']] += 1 
                                curr_time += temp_process['end'] - exp_process['start']
                                for details in details_process:
                                    if details['name'] == temp_process['name']:
                                        if details['flag'] == 1:
                                            details['end'] = curr_time
                                continue
                            elif temp_process['end'] - exp_process['start'] + curr_time == chart_details['end']:
                                temp_process['end'] = chart_details['end']
                                process_chart.append(deepcopy(temp_process))
                                index[process['priority']] += 1
                                for details in details_process:
                                    if details['name'] == temp_process['name']:
                                        if details['flag'] == 1:
                                            details['end'] = chart_details['end']
                                break
                            else:
                                temp_process['end'] = chart_details['end']
                                process_chart.append(deepcopy(temp_process))
                                queue_cpu_schedule[process['priority']][index[process['priority']]]['start'] += chart_details['end'] - curr_time
                                for details in details_process:
                                    if details['name'] == temp_process['name']:
                                        if details['flag'] == 1:
                                            details['end'] = chart_details['end']
                                break
                        break
            curr_time = chart_details['end']
        
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
        stats['throughput'] = len(details_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time

        return process_chart, stats, process_details, error_status
    
def multilevel_feedback(data, num_queues, quantum_queue, dispatch_latency = 0):
    # For bad input handling
    error, error_status = check_for_bad_input(data, dispatch_latency, -1, -1, 6, num_queues, quantum_queue, -1)
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
            for data in details_process:
                if data['name'] == process['name'] and data['flag'] == 0:
                    data['start'] = time_present
                    data['flag'] = 1
            chart_details['name'] = process['name']
            chart_details['start'] = time_present
            chart_details['end'] = time_present + process['burst']
            chart_details['next_queue'] = 0
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
                    process_chart += [idle_cpu]
            elif len(process_chart) == 0 and chart_details['start'] > 0:
                idle_cpu = dict()
                idle_cpu['name'] = 'Idle'
                idle_cpu['start'] = 0
                idle_cpu['end'] = chart_details['start']
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
        stats['throughput'] = len(details_process)*1000/float(curr_time)
        stats['cpu_utilization'] = float(sum_time)*100/curr_time
            
        return process_chart, stats, process_details, error_status