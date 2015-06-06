from operator import itemgetter

def fcfs(data):
	schedule = sorted(data, key=itemgetter('arrival'))
	# curr_time = 0
	# wait_time = 0
	# turn_time = 0
	# for process in schedule:
	# 	if process['arrival'] > curr_time:
	# 		curr_time = process['arrival']
	return schedule