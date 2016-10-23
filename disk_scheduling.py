


def first_come_first_serve(curr_head_pos, num_cylinders, disk_queue):
	total_head_movements = 0 # To keep track of the total number of read/write head movements
	memory_state = [] # To keep track of the order in which cylinders are visited
	memory_state.append(str(curr_head_pos))
	for cylinder in disk_queue:
		memory_state.append(cylinder)
		difference = abs(int(cylinder) - curr_head_pos)
		total_head_movements += difference
		curr_head_pos = int(cylinder)

	status = (memory_state,total_head_movements);
	return status


# Main function to call algo chosen by the user
def disk_scheduling(data):
	curr_head_pos = int(data['curr_pos'])
	num_cylinders = int(data['total_cylinders'])
	disk_queue = data['disk_queue']
	# For Scan, C-Scan, Look and C-Look algorithms
	if data['algo'] != 0 and data['algo'] != 1:
		direction = data['direction']
	# To store secondary memory chart and total number of head movements 
	secondary_storage_chart = {}

	if data['algo'] == 0:
		secondary_storage_memory, total_head_movements = first_come_first_serve(curr_head_pos, num_cylinders, disk_queue)
	elif data['algo'] == 1:
		secondary_storage_memory, total_head_movements = shortest_seek_time_first(curr_head_pos, num_cylinders, disk_queue)
	elif data['algo'] == 2:
		secondary_storage_memory, total_head_movements = scan(curr_head_pos, num_cylinders, disk_queue)
	elif data['algo'] == 3:
		secondary_storage_memory, total_head_movements = c_scan(curr_head_pos, num_cylinders, disk_queue)
	elif data['algo'] == 4:
		secondary_storage_memory, total_head_movements = look(curr_head_pos, num_cylinders, disk_queue)
	elif data['algo'] == 5:
		secondary_storage_memory, total_head_movements = c_look(curr_head_pos, num_cylinders, disk_queue)
	secondary_storage_chart['memory_state'] = secondary_storage_memory
	secondary_storage_chart['total_head_moves'] = total_head_movements
	print str(secondary_storage_chart)
	return secondary_storage_chart