

from sys import maxint
from random import randint

# For Scan and Look Algorithms
def calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos):
	memory_state.append(chosen_cylinder)
	difference = abs(int(chosen_cylinder) - curr_head_pos)
	return difference



def c_scan_or_c_look(curr_head_pos, num_cylinders, disk_queue, next_larger_pos, direction, algo):
	total_head_movements = 0 # To keep track of the total number of read/write head movements
	memory_state = [] # To keep track of the order in which cylinders are visited
	memory_state.append(curr_head_pos)
	if(direction == 0): # Inward direction
		start_idx = next_larger_pos - 1
		for i in range(next_larger_pos):
			chosen_cylinder = disk_queue[start_idx]
			start_idx = start_idx -1
			memory_state.append(chosen_cylinder)
			difference = abs(int(chosen_cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(chosen_cylinder)
		if(algo == 3):
			chosen_cylinder = 0
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
			chosen_cylinder = num_cylinders - 1
			memory_state.append(chosen_cylinder)
			curr_head_pos = int(chosen_cylinder)
		if(algo == 5):
			curr_head_pos = disk_queue[-1]
		for i, cylinder in reversed(list(enumerate(disk_queue[next_larger_pos:]))):
			memory_state.append(cylinder)
			difference = abs(int(cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(cylinder)
	else: # Outward direction
		for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
			memory_state.append(cylinder)
			difference = abs(int(cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(cylinder)
		if(algo == 3):
			chosen_cylinder = num_cylinders - 1
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
			chosen_cylinder = 0
			memory_state.append(chosen_cylinder)
			curr_head_pos = int(chosen_cylinder)
		if(algo == 5):
			curr_head_pos = disk_queue[0]
		for i, cylinder in enumerate(disk_queue[0:next_larger_pos]):
			chosen_cylinder = cylinder
			memory_state.append(chosen_cylinder)
			difference = abs(int(chosen_cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(chosen_cylinder)
			
	status = (memory_state, total_head_movements);
	return status



def scan_or_look(curr_head_pos, num_cylinders, disk_queue, next_larger_pos, direction, algo):
	total_head_movements = 0 # To keep track of the total number of read/write head movements
	memory_state = [] # To keep track of the order in which cylinders are visited
	memory_state.append(curr_head_pos)
	if(direction == 0): # Inward direction
		start_idx = next_larger_pos - 1
		for i in range(next_larger_pos):
			chosen_cylinder = disk_queue[start_idx]
			start_idx = start_idx -1
			memory_state.append(chosen_cylinder)
			difference = abs(int(chosen_cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(chosen_cylinder)
		if(algo == 2):
			chosen_cylinder = 0
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
		for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
			memory_state.append(cylinder)
			difference = abs(int(cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(cylinder)
		if(algo == 2):
			chosen_cylinder = num_cylinders - 1
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
	else: # Outward direction
		for i, cylinder in enumerate(disk_queue[next_larger_pos:]):
			memory_state.append(cylinder)
			difference = abs(int(cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(cylinder)
		if(algo == 2):
			chosen_cylinder = num_cylinders - 1
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
		start_idx = next_larger_pos - 1
		for i in range(next_larger_pos):
			chosen_cylinder = disk_queue[start_idx]
			start_idx = start_idx -1
			memory_state.append(chosen_cylinder)
			difference = abs(int(chosen_cylinder) - curr_head_pos)
			total_head_movements += difference
			curr_head_pos = int(chosen_cylinder)
		if(algo == 2):
			chosen_cylinder = 0
			total_head_movements += calc_end_cylinder_moves(chosen_cylinder, memory_state, curr_head_pos)
			curr_head_pos = int(chosen_cylinder)
	status = (memory_state, total_head_movements);
	return status


def shortest_seek_time_first(curr_head_pos, disk_queue):
	total_head_movements = 0 # To keep track of the total number of read/write head movements
	memory_state = [] # To keep track of the order in which cylinders are visited
	memory_state.append(str(curr_head_pos))

	# To find the next cylinder with shortest seek time till the disk queue is empty
	while len(disk_queue) > 0:
		min_seek = maxint # To track the cylinder with minimum seek time from current head position
		min_idx = -1
		for idx, cylinder in enumerate(disk_queue):
			if abs(int(cylinder) - curr_head_pos) < min_seek:
				min_seek = abs(int(cylinder) - curr_head_pos)
				min_idx = idx
			elif abs(int(cylinder) - curr_head_pos) == min_seek:
				min_seek = abs(int(cylinder) - curr_head_pos) 
				min_idx = randint(idx, min_idx)
		chosen_cylinder = disk_queue[min_idx]
		memory_state.append(chosen_cylinder)
		difference = abs(int(chosen_cylinder) - curr_head_pos)
		total_head_movements += difference
		curr_head_pos = int(chosen_cylinder)
		del disk_queue[min_idx]

	status = (memory_state, total_head_movements);
	return status

def first_come_first_serve(curr_head_pos, disk_queue):
	total_head_movements = 0 # To keep track of the total number of read/write head movements
	memory_state = [] # To keep track of the order in which cylinders are visited
	memory_state.append(str(curr_head_pos))
	for cylinder in disk_queue:
		memory_state.append(cylinder)
		difference = abs(int(cylinder) - curr_head_pos)
		total_head_movements += difference
		curr_head_pos = int(cylinder)

	status = (memory_state, total_head_movements);
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
		secondary_storage_memory, total_head_movements = first_come_first_serve(curr_head_pos, disk_queue)
	elif data['algo'] == 1:
		secondary_storage_memory, total_head_movements = shortest_seek_time_first(curr_head_pos, disk_queue)
	else:
		
		larger = curr_head_pos # To find the next largest cylinder to current head position
	
		new_disk_queue=list(map(int, disk_queue))
		disk_queue = sorted(new_disk_queue)
		for idx, cylinder in enumerate(disk_queue):
			if(int(cylinder) > curr_head_pos):
				larger = idx 
				break
		if data['algo'] == 2 or data['algo'] == 4:
			secondary_storage_memory, total_head_movements = scan_or_look(curr_head_pos, num_cylinders, disk_queue, larger, direction, data['algo'])
		elif data['algo'] == 3 or data['algo'] == 5:
			secondary_storage_memory, total_head_movements = c_scan_or_c_look(curr_head_pos, num_cylinders, disk_queue, larger, direction, data['algo'])
	secondary_storage_chart['memory_state'] = secondary_storage_memory
	secondary_storage_chart['total_head_moves'] = total_head_movements
	print str(secondary_storage_chart)
	return secondary_storage_chart