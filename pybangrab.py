import optparse
from socket import *
import subprocess
import os

FILE_PATH = "/root/Music/banner_file_" + str(os.getpid())
def banner(targetHost, targetPort):
	try:
		#print("RUNNING") for debugging purpose
		connsocket = socket(AF_INET, SOCK_STREAM)
		#socket.setdefaulttimeout(3)
		#print("RUNNING1")
		#connsocket.connect((targetHost, targetPort))
		#connsocket.send('Hi therern')
		#results = connsocket.recv(100)
		#print '' + str(results)
		#if results == None :
		connsocket.connect((targetHost, targetPort))

		#print("RUNNING2")
		data = "GET / HTTP/1.1\r\nhost:" +  str(targetHost) + "\r\nConnection: close\r\n\r\n"
		connsocket.send(data.encode('UTF_8'))			 #Data must be encoded in UTF_8 For python3
		recv_ban = connsocket.recv(10000)
		#connsocket.close()                                        #GET / HTTP/1.1\r\nhost: ip\r\nConnection: close\r\n\r\n")
		#print("RUNNING3")
		with open(FILE_PATH, 'w') as f:
			print(recv_ban, file=f)
			f.close()
		if 'HTTP' in open(FILE_PATH).read():
			cmd = 'cat ' + FILE_PATH + "|awk -F'Server: ' '{print $2}'|sed 's/[\]//g'|awk -F'rn' '{print $1}'"
			#return subprocess.getoutput("cat /home/xyz/Music/banner_file |awk -F'Server: ' '{print $2}'|awk -F'r' '{print $1}'")
			return subprocess.getoutput(cmd)
			#return cmd_out
			#s = subprocess.Popen(["echo $banner"])
		else:
			cmd = 'cat ' + FILE_PATH + '|sed  "s/' + "[b']//g" + '"' + "|sed 's/[\]//g'|awk -F'rn' '{print $1}'"  #|' + "sed s'/" + ".....$//'"

			return subprocess.getoutput(cmd)
			#return cmd_out
		#print("Running4")
		connsocket.close()
	except OSError:
		#print(error)
		return " "

'''def main():
	options = {}
	parser = optparse.OptionParser('usage %prog -H <target host> -P <target port>')
	parser.add_option('-H', '--host', dest='target_host', type='string', help='specify target host')
	parser.add_option('-P', '--port', dest='target_port', type='int', help='specify target port')

	(options, args) = parser.parse_args()
	target_host = options.target_host
	target_port = options.target_port

	if(target_host == None) | (target_port == None):
		print(parser.usage)
		exit(0)

	banner(target_host, target_port)

if __name__ == '__main__':
    main()
'''
