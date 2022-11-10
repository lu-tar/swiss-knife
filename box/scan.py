import threading
from queue import Queue
import time
import socket
import datetime

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()

#target = input("ip: ")
#test
target = '51.75.30.1'


ip = socket.gethostbyname(target)

start_time = time.time()
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print('port', port)
        con.close()
    except:
        pass
    end_time = time.time()

# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()


# Create the queue and threader
q = Queue()

# how many threads are we going to allow for
for x in range(30):
    t = threading.Thread(target=threader)

    # classifying as a daemon, so they will die when the main dies
    t.daemon = True

    # begins, must come after daemon definition
    t.start()

start = time.time()

# 100 jobs assigned.
for worker in range(1, 100):
    q.put(worker)

# wait until the thread terminates.
q.join()
end_time = time.time()
duration = end_time-start_time

print(duration)

with open("log.txt", "a") as log:
    log.write(str(datetime.datetime.now()) + "Scan of "+target+" completed in " + str(duration) +"\n")
