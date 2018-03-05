import copy

# Bad input case(s):
# 0. 0 < num_resources 
# 1. 0 < num_processes 
# 2. 0 <= available 
# 3. 0 <= maximum 
# 4. 0 <= request 
# 5. 0 <= request_process_number <= num_processes 
# 6. 0 <= allocation 

# Bad input handling and error message for the user
default_message = "Press back button to go back to the input form."

def get_error_message(error_number, process_id, resource_type):
    ERROR = {}
    if error_number == -1:
        ERROR['error_message'] = " "
        ERROR['error_number'] = -1
    elif error_number == 0:
        ERROR['error_message'] = "Please enter valid number of resources."  + default_message
        ERROR['error_number'] = 0
    elif error_number == 1:
        ERROR['error_message'] = "Please enter valid number of processes." + default_message
        ERROR['error_number'] = 1
    elif error_number == 2:
        ERROR['error_message'] = "Please enter valid number of available resources of resource type " + str(resource_type) + ".\n" + default_message
        ERROR['error_number'] = 2
    elif error_number == 3:
        ERROR['error_message'] = "Please enter valid number of maximum resources of resource type " + str(resource_type) + " for process P" + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 3
    elif error_number == 4:
        ERROR['error_message'] = "Please enter a valid request for resource type " + str(resource_type) + "." + default_message
        ERROR['error_number'] = 4
    elif error_number == 5:
        ERROR['error_message'] = "Process number exceeds number of processes in the system.\nPlease enter request for a valid process.\n" + default_message
        ERROR['error_number'] = 5
    elif error_number == 6:
        ERROR['error_message'] = "Please enter valid number of allocated resources of resource type " + str(resource_type) + " for process P" + str(process_id) + ".\n" + default_message
        ERROR['error_number'] = 6
    return ERROR

# Bad input checking function for deadlock avoidance
def check_for_bad_input_avoidance(available, maximum, allocation, request, process, num_processes, num_resources):
    error = 0 # Boolean to check bad input 
    error_status = {} # Dictionary to store error number and error message
    if int(num_resources) <= 0:
        error_status = get_error_message(0, -1, -1)
        error =1
    elif int(num_processes) <= 0:
        error_status = get_error_message(1, -1, -1)
        error = 1
    elif int(process) > num_processes or int(process) < 0:
        error_status = get_error_message(5, -1, -1)
        error = 1
    if error == 0:
        for j in range(num_resources):
            if int(available[j]) < 0:
                error_status = get_error_message(2, -1, chr(ord('A')+j))
                error = 1
                break
            if int(request[j]) < 0:
                error_status = get_error_message(4, -1, chr(ord('A')+j))
                error = 1
                break
        if error == 0:
            for i in range(num_processes):
                for j in range(num_resources):
                    if int(maximum[i][j]) < 0:
                        error_status = get_error_message(3, i+1, chr(ord('A')+j))
                        error = 1
                        break
                    if int(allocation[i][j]) < 0:
                        error_status = get_error_message(6, i+1, chr(ord('A')+j))
                        error = 1
                        break
    # No bad input
    if error == 0:
        error_status = get_error_message(-1, -1, -1)
    status = (error, error_status);
    return status

# Bad input checking function for deadlock detection
def check_for_bad_input_detection(available, allocation, request, num_processes, num_resources):
    error = 0 # Boolean to check bad input 
    error_status = {} # Dictionary to store error number and error message
    if int(num_resources) <= 0:
        error_status = get_error_message(0, -1, -1)
        error =1
    elif int(num_processes) <= 0:
        error_status = get_error_message(1, -1, -1)
        error = 1
    if error == 0:
        for j in range(num_resources):
            if int(available[j]) < 0:
                error_status = get_error_message(2, -1, chr(ord('A')+j))
                error = 1
                break
        if error == 0:
            for i in range(num_processes):
                for j in range(num_resources):
                    if int(allocation[i][j]) < 0:
                        error_status = get_error_message(6, i+1, chr(ord('A')+j))
                        error = 1
                        break
                    if int(request[i][j]) < 0:
                        error_status = get_error_message(4, -1, chr(ord('A')+j))
                        error = 1
                        break
    # No bad input
    if error == 0:
        error_status = get_error_message(-1, -1, -1)
    status = (error, error_status);
    return status

# Deadlock Avoidance
def check_request(available, maximum, allocation, request, process, n, m):
    # For bad input handling
    error, error_status = check_for_bad_input_avoidance(available, maximum, allocation, request, process, n, m)
    if(error):
        return -1, -1, error_status
    else:
        need = [[10 for x in range(m)] for x in range(n)]
        for i in range(n):
            for j in range(m):
                need[i][j] = maximum[i][j] - allocation[i][j]
        for j in range(m):
            if request[j] > need[process][j]:
                return False, "Error: P"+str(process+1)+" requesting more resources than it needs.", error_status
        for j in range(m):
            if request[j] > available[j]:
                return False, "Wait: P"+str(process+1)+" requesting more resources than currently available.", error_status
        return True, "Request Granted.", error_status

def is_safe(available, maximum, allocation, n, m):
    # Initialize work and finish vectors, and need matrix
    work = copy.deepcopy(available)
    finish = [False] * n
    need = [[10 for x in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            need[i][j] = maximum[i][j] - allocation[i][j]
    num_left = n
    schedule = list()
    # print "Need: "+str(need)
    while num_left > 0:
        i = 0
        while i < n and (finish[i] or not dispatchable(need[i], work, m)):
            # print "Process "+str(i)+" not dispatchable. Trying process "+str(i+1)
            i += 1
        if i == n:
            # print "No process dispatched"
            break
        for j in range(m):
            work[j] += allocation[i][j]
        finish[i] = True
        schedule.append(i)
        num_left -= 1

    if num_left == 0:
        return True, schedule, need
    else:
        return False, schedule, need


def dispatchable(need, work, m):
    for i in range(m):
        if (need[i] > work[i]):
            return False
    return True


# Deadlock Detection
def detect(available, allocation, request, n, m):
    # For bad input handling
    error, error_status = check_for_bad_input_detection(available, allocation, request, n, m)
    if(error):
        return -1, -1, error_status
    else:
        work = copy.deepcopy(available)
        finish = [False] * n
        num_left = n
        schedule = list()
        while num_left > 0:
            i = 0
            while i < n and (finish[i] or not dispatchable(request[i], work, m)):
                i += 1
            if i == n:
                break
            for j in range(m):
                work[j] += allocation[i][j]
            finish[i] = True
            schedule.append(i)
            num_left -= 1

        if num_left == 0:
            return True, schedule, error_status
        else:
            return False, schedule, error_status
