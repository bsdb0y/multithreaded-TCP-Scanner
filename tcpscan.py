import threading
from queue import Queue
import time
import socket
import sys
import subprocess
import pybangrab #for banner grabbing
import time

# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.

'''if len(sys.argv) != 3:
	sys.exit('Usage: %s <Target> <FromIP> <ToIP>' % sys.argv[0])

'''
print_lock = threading.Lock()



target = sys.argv[1]
fromip = sys.argv[2]
toip = sys.argv[3]

def getServiceName(port, proto):
    """ Check and Get service name from port and proto string combination using socket.getservbyport

    @param port string or id
    @param protocol string
    @return Service name if port and protocol are valid, else None
    """

    try:
        name = socket.getservbyport(int(port), proto)
    except:
        return None
    return name


def portscan(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(0.5)

	try:
		con = s.connect((target,port))
		with print_lock:
			#print('port',port)
			#print(target)
			servname = getServiceName(port,'tcp')
			#print(servname)
			result = pybangrab.banner(target,port)
			#print("result:")
			#print(result)
			#print("{:1d} {:6s} {:10s}".format(port,servname,result))

			if len(str(port)) != 3 :
				print("\t",port ," ","\t",servname," ","\t\t",result)
			else:
				print("\t",port," ","\t\t",servname," ","\t\t",result)

			#print(str(result))
		s.close()
	#banner(target,port)

	except:
		pass






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
for x in range(40):
	t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
	t.daemon = True

     # begins, must come after daemon definition
	t.start()


start = time.time()

# 100 jobs assigned.

for worker in range(int(fromip),int(toip)):
	q.put(worker)

# wait until the thread terminates.
q.join()


print(('Entire job took:',time.time() - start))
