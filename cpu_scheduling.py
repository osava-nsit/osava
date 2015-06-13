from operator import itemgetter
import Queue

def fcfs(data):
    processes = sorted(data, key=itemgetter('arrival'))
    process_chart = []
    curr_time = 0
    wait_time = 0
    turn_time = 0
    sum_time = 0
    for process in processes:
        chart_details = {}
        if (process['arrival'] > curr_time):
            curr_time = process['arrival']

        chart_details['name'] = process['name']
        chart_details['start'] = curr_time
        chart_details['end'] = curr_time + process['burst']

        wait_time += (curr_time - process['arrival'])
        curr_time += process['burst']
        turn_time += (curr_time - process['arrival'])
        sum_time += process['burst']

        process_chart += [chart_details]

    stats = {}
    stats['sum_time'] = sum_time
    stats['wait_time'] = float(wait_time)/len(processes)
    stats['turn_time'] = float(turn_time)/len(processes)
    stats['throughput'] = len(processes)*1000/float(curr_time)
    stats['cpu_utilization'] = float(sum_time)*100/curr_time

    return process_chart, stats 

def round_robin(data,max_quanta=20):
	time_present = 0
    	wait_time = 0
    	turn_time = 0
    	sum_time = 0
	count = 0
	
	details_process = []

	q = Queue.Queue(maxsize=0)
	for process in data:
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
		
	process_chart = []
	active_process = []
	var_count = 0
	while True:
		chart_details = {}
		temp_process = q.get()
			
		if temp_process['burst'] > 0 and temp_process['arrival'] <= time_present:
			#print str(temp_process['name']) + " " + str(temp_process['burst']) + " " + str(time_present)
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
				active_process.append(temp_process)
			else:
				if temp_process in active_process:
					for data in details_process:
						if data['name'] == temp_process['name']:
							data['end'] = time_present
					active_process.remove(temp_process)
					count -= 1
			
			time_present += quanta
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
					time_present += quanta
					var_count = 0
			q.put(temp_process)
			
		if q.empty():
			break
	for data in details_process:
    		wait_time += ((data['start'] - data['arrival']) + (data['end'] - (data['start'] + data['burst'])))
    		turn_time += (data['end'] - data['arrival'])
    		sum_time += data['burst']
	
	curr_time = time_present
	print curr_time
	stats = {}
	stats['sum_time'] = sum_time
	stats['wait_time'] = float(wait_time)/len(details_process)
	stats['turn_time'] = float(turn_time)/len(details_process)
	stats['throughput'] = len(details_process)*1000/float(curr_time)
	stats['cpu_utilization'] = float(sum_time)*100/curr_time
		
	return process_chart,stats

def shortest_job_non_prempted(data):
	all_processes = sorted(data, key=itemgetter('burst'))
	time_present = 0
	var = 0
	process_chart = []
	while True:
		for process in all_processes:
			chart_details = {}	
			if process['burst'] > 0 and process['arrival'] <= time_present:
				chart_details['name'] = process['name']
				chart_details['start'] = time_present
				time_present += process['burst']
				chart_details['end'] = time_present
				process['burst'] = 0
				all_processes.remove(process)
				if len(process_chart) > 0:
					temp_dict = process_chart[-1]
					if temp_dict['name'] == chart_details['name']:
						chart_details['start'] = temp_dict['start']
						del process_chart[-1]	
				process_chart += [chart_details]
				var = 0
			else:
				var += 1
				if var == len(all_processes):
					time_present += 1
					var = 0

		if len(all_processes) == 0:	
			break
	return process_chart
	
def shortest_job_prempted(data):
	all_processes = sorted(data, key=itemgetter('burst'))
	time_present = 0
	var = 0
	process_chart = []
	while True:	
		for process in all_processes:
			chart_details = {}
			if process['burst'] > 0 and process['arrival'] <= time_present:
				chart_details['name'] = process['name']
				chart_details['start'] = time_present
				time_present += 1
				chart_details['end'] = time_present
				process['burst'] -= 1
				if process['burst'] == 0:
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
					time_present += 1
					var = 0
		if len(all_processes) == 0:	
			break
		all_processes = sorted(all_processes, key=itemgetter('burst'))

	return process_chart


###### Test code ######

list_process_round_robin = list()
# list_process_shortest_job_non_prempted = list()
# list_process_shortest_job_prempted = list()

# # Test case for round robin
process = {}
process['name'] = 1
process['burst'] = 7
process['arrival'] = 0
list_process_round_robin += [process]
process = {}
process['name'] = 2
process['burst'] = 10
process['arrival'] = 9
list_process_round_robin += [process]
process = {}
process['name'] = 3
process['burst'] = 5
process['arrival'] = 11
list_process_round_robin += [process]
process = {}
process['name'] = 4
process['burst'] = 7
process['arrival'] = 12
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
xyz,x = round_robin(list_process_round_robin,4)
print str(x['cpu_utilization'])+ " "+str(x['wait_time'])+ " "+str(x['sum_time']) + " " + str(x['throughput'])
