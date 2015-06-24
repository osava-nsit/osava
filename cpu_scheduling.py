from operator import itemgetter
import Queue

def fcfs(data):
    processes = sorted(data, key=itemgetter('arrival'))
    process_chart = []
    curr_time = 0
    wait_time = 0
    turn_time = 0
    sum_time = 0
    details_process = dict()
    for process in processes:
        temp_process['name'] = process['name']
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
        temp['resp_time'] = process['arrival'] - process['start']
        turn_time += temp_process['turn_time']
        sum_time += process['burst']
        details_process += [temp_process]

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
    stats['turn_time'] = float(turn_time)/len(processes)
    stats['throughput'] = len(processes)*1000/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/curr_time

    return process_chart,stats,details_process

def round_robin(data,max_quanta=4):
	all_processes = sorted(data, key=itemgetter('arrival'))
	time_present = 0
	wait_time = 0
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
		temp_val['wait_time'] = 0
		temp_val['turn_time'] = 0
		temp_val['resp_time'] = 0
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

	for data in details_process:
		data['resp_time'] = data['start'] - data['arrival']
		data['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
		data['turn_time'] = (data['end'] - data['arrival'])
		wait_time += data['wait_time']
		turn_time += data['turn_time']
		sum_time += data['burst']

	curr_time = time_present
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(details_process)
	stats['turn_time'] = float(turn_time)/len(details_process)
	stats['throughput'] = len(details_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
		
	return process_chart,stats,details_process

def shortest_job_non_prempted(data):
	all_processes = sorted(data, key=itemgetter('burst'))
	time_present = 0 
	var = 0
        wait_time = 0 
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
				details_process['wait_time'] = 0
				details_process['turn_time'] = 0
				details_process['resp_time'] = 0
				chart_details['start'] = time_present
				time_present += process['burst']
				chart_details['end'] = time_present
				details_process['end'] = time_present
				process['burst'] = 0
				completed_processes.append(process)
				"""
				if len(process_chart) > 0:
					temp_dict = process_chart[-1]
					if temp_dict['name'] == chart_details['name']:
						chart_details['start'] = temp_dict['start']
						del process_chart[-1]	
				"""
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

	for data in data_process:
		data['resp_time'] = data['start'] - data['arrival']
		data['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
		data['turn_time'] = (data['end'] - data['arrival'])
		wait_time += data['wait_time']
		turn_time += data['turn_time']
		sum_time += data['burst']

	curr_time = time_present
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(data_process)
	stats['turn_time'] = float(turn_time)/len(data_process)
	stats['throughput'] = len(data_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
	
	return process_chart,stats,data_process
	
def shortest_job_prempted(data):
	all_processes = sorted(data, key=itemgetter('burst'))
	time_present = 0
        wait_time = 0 
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
		temp_val['wait_time'] = 0
		temp_val['resp_time'] = 0
		temp_val['turn_time'] = 0
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
	
	for data in details_process:
		data['resp_time'] = data['start'] - data['arrival']
		data['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
		data['turn_time'] = (data['end'] - data['arrival'])
		wait_time += data['wait_time']
		turn_time += data['turn_time']
		sum_time += data['burst']


	curr_time = time_present
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(details_process)
	stats['turn_time'] = float(turn_time)/len(details_process)
	stats['throughput'] = len(details_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
	
	return process_chart,stats,details_process

def priority_non_preemptive(data, increment_after_time = 4, upper_limit_priority = 0):
	all_processes = sorted(data, key=itemgetter('priority'))
	time_present = 0 
	var = 0
        wait_time = 0 
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
				details_process['resp_time'] = 0
				details_process['turn_time'] = 0
				details_process['wait_time'] = 0
				chart_details['start'] = time_present
				time_present += process['burst']
				chart_details['end'] = time_present
				details_process['end'] = time_present
				for val_process in all_processes:
					if 'wait_time' not in val_process:
						val_process['wait_time'] = 0
					if val_process['arrival'] < time_present and val_process['name'] != process['name'] and val_process['burst'] > 0:
						val_process['wait_time'] += val_process['burst']
						val_process['priority']	 -= (val_process['wait_time'] / increment_after_time)
						val_process['wait_time'] = val_process['wait_time'] % increment_after_time
						if val_process['priority'] < upper_limit_priority:
							val_process['priority'] = upper_limit_priority
				process['burst'] = 0
	
				completed_processes.append(process)
				"""
				if len(process_chart) > 0:
					temp_dict = process_chart[-1]
					if temp_dict['name'] == chart_details['name']:
						chart_details['start'] = temp_dict['start']
						del process_chart[-1]	
				"""
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

	for data in data_process:
		data['resp_time'] = data['start'] - data['arrival']
		data['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
		data['turn_time'] = (data['end'] - data['arrival'])
		wait_time += data['wait_time']
		turn_time += data['turn_time']
		sum_time += data['burst']

	curr_time = time_present
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(data_process)
	stats['turn_time'] = float(turn_time)/len(data_process)
	stats['throughput'] = len(data_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
	
	return process_chart,stats,data_process
	
def priority_preemptive(data, increment_after_time = 4, upper_limit_priority = 0):
	all_processes = sorted(data, key=itemgetter('priority'))
	time_present = 0
        wait_time = 0 
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
		temp_val['turn_time'] = 0
		temp_val['wait_time'] = 0
		temp_val['resp_time'] = 0
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
						val_process['priority']	 -= (val_process['wait_time'] / increment_after_time)
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
	
	for data in details_process:
		data['resp_time'] = data['start'] - data['arrival']
		data['wait_time'] = (data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst']))
		data['turn_time'] = (data['end'] - data['arrival'])
		wait_time += data['wait_time']
		turn_time += data['turn_time']
		sum_time += data['burst']


	curr_time = time_present
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(details_process)
	stats['turn_time'] = float(turn_time)/len(details_process)
	stats['throughput'] = len(details_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
	
	return process_chart,stats,details_process
###### Test code ######

list_process_round_robin = list()
# list_process_shortest_job_non_prempted = list()
# list_process_shortest_job_prempted = list()

# # Test case for round robin

process = {}
process['name'] = 1
process['burst'] = 5
process['arrival'] = 0
process['priority'] = 1
process['wait_time'] = 0
list_process_round_robin += [process]
process = {}
process['name'] = 2
process['burst'] = 9
process['arrival'] = 0
process['priority'] = 2
process['wait_time'] = 0
list_process_round_robin += [process]
process = {}
process['name'] = 3
process['burst'] = 4
process['arrival'] = 0
process['priority'] = 3 
process['wait_time'] = 0
list_process_round_robin += [process]
process = {}
process['name'] = 4
process['burst'] = 7
process['arrival'] = 0
process['priority'] = 4
process['wait_time'] = 0
list_process_round_robin += [process]
process = {}
process['name'] = 5
process['burst'] = 3
process['arrival'] = 0
process['priority'] = 5
process['wait_time'] = 0
list_process_round_robin += [process]


# process = {}
# process['name'] = 1
# process['burst'] = 7
# process['arrival'] = 0
# list_process_shortest_job_non_prempted += [process]
# process = {}
# process['name'] = 2
# process['burst'] = 10
# process['arrival'] = 0
# list_process_shortest_job_non_prempted += [process]
# process = {}
# process['name'] = 3
# process['burst'] = 5
# process['arrival'] = 0
# list_process_shortest_job_non_prempted += [process]
# process = {}
# process['name'] = 4
# process['burst'] = 7
# process['arrival'] = 0
# list_process_shortest_job_non_prempted += [process]


# process = {}
# process['name'] = 1
# process['burst'] = 7
# process['arrival'] = 0
# list_process_shortest_job_prempted += [process]
# process = {}
# process['name'] = 2
# process['burst'] = 4
# process['arrival'] = 4
# list_process_shortest_job_prempted += [process]
# process = {}
# process['name'] = 3
# process['burst'] = 5
# process['arrival'] = 1
# list_process_shortest_job_prempted += [process]
# process = {}
# process['name'] = 4
# process['burst'] = 2
# process['arrival'] = 5
# list_process_shortest_job_prempted += [process]
# #val = shortest_job_non_prempted(list_process_shortest_job_non_prempted)
# val = shortest_job_prempted(list_process_shortest_job_prempted)
#xyz,p,xxx= priority_preemptive(list_process_round_robin)
#for p in xxx:
#	print str(p['name']) + " " +str(p['turn_time']) + " " + str(p['wait_time']) + " " + str(p['resp_time'])
