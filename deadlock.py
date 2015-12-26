import copy

# Deadlock Avoidance
def check_request(available, maximum, allocation, request, process, n, m):
    need = [[10 for x in range(m)] for x in range(n)]
    for i in range(n):
        for j in range(m):
            need[i][j] = maximum[i][j] - allocation[i][j]
    for j in range(m):
        if request[j] > need[process][j]:
            return False, "Error: P"+str(process+1)+" requesting more resources than it needs."
    for j in range(m):
        if request[j] > available[j]:
            return False, "Wait: P"+str(process+1)+" requesting more resources than currently available."
    return True, "Request Granted."

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
        return True, schedule
    else:
        return False, schedule


def dispatchable(need, work, m):
    for i in range(m):
        if (need[i] > work[i]):
            return False
    return True

# Deadlock Detection
def detect(available, allocation, request, n, m):
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
        return True, schedule
    else:
        return False, schedule
