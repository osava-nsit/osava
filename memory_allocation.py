from operator import itemgetter

def first_fit(data):
	processes = sorted(data, key=itemgetter('arrival'))
	process_chart = []
	curr_time = 0
	# TODO: Maintain memory state too
	for process in processes:
		if process['arrival'] > curr_time:
			curr_time = process['arrival']
		chart_details = {}
		chart_details['name'] = process['name']
		chart_details['start'] = curr_time
		chart_details['end'] = process['termination']
		process_chart += chart_details