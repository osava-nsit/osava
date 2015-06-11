from operator import itemgetter
import Queue

def fcfs(data):
	schedule = sorted(data, key=itemgetter('arrival'))
	# curr_time = 0
	# wait_time = 0
	# turn_time = 0
	# for process in schedule:
	# 	if process['arrival'] > curr_time:
	# 		curr_time = process['arrival']
	return schedule

def round_robin(data,max_quanta):
	time_present = 0
	count = 0
	q = Queue.Queue(maxsize=0)
	for process in data:
		q.put(process)
		count += 1
	
	process_chart = []
	active_process = []
	while True:
		chart_details = {}
		temp_process = q.get()
			
		if temp_process['burst'] > 0 and temp_process['arrival'] <= time_present:
			#print str(temp_process['name']) + " " + str(temp_process['burst']) + " " + str(time_present)
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
	return process_chart

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


list_process_round_robin = list()
list_process_shortest_job_non_prempted = list()
list_process_shortest_job_prempted = list()

# Test case for round robin
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

process = {}
process['name'] = 1
process['burst'] = 7
process['arrival'] = 0
list_process_shortest_job_non_prempted += [process]
process = {}
process['name'] = 2
process['burst'] = 10
process['arrival'] = 0
list_process_shortest_job_non_prempted += [process]
process = {}
process['name'] = 3
process['burst'] = 5
process['arrival'] = 0
list_process_shortest_job_non_prempted += [process]
process = {}
process['name'] = 4
process['burst'] = 7
process['arrival'] = 0
list_process_shortest_job_non_prempted += [process]


process = {}
process['name'] = 1
process['burst'] = 7
process['arrival'] = 0
list_process_shortest_job_prempted += [process]
process = {}
process['name'] = 2
process['burst'] = 4
process['arrival'] = 4
list_process_shortest_job_prempted += [process]
process = {}
process['name'] = 3
process['burst'] = 5
process['arrival'] = 1
list_process_shortest_job_prempted += [process]
process = {}
process['name'] = 4
process['burst'] = 2
process['arrival'] = 5
list_process_shortest_job_prempted += [process]
#val = shortest_job_non_prempted(list_process_shortest_job_non_prempted)
val = shortest_job_prempted(list_process_shortest_job_prempted)
#val = round_robin(list_process_round_robin,4)
for x in val:
	print str(x['name'])+ " "+str(x['start']) + " " + str(x['end'])
