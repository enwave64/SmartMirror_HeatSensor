#client.py

### Programmers: Elliott Watson, Michelle Jagelid

############################################################################
# This program is a client application that uses Python3's socket library.
############################################################################

import socket, sys, errno, time

HOST = '169.254.100.247' #should be changed as necessary
PORT = 50007 #any non-priveleged port; should be matched with server
values = []

def main():
	flag = 'v'

	variables = ""

	#This with statement wraps the socket object according to context management
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.settimeout(20.0)
		try:
			s.connect((HOST, PORT))
			#s.sendall(flag.encode('ascii'))
			#s.sendall(message.encode('ascii'))
		except socket.timeout:
			print("Sorry, server.py is currently unavailable")
			sys.exit(1)
		except socket.error as e:
			#handles the case where the sever.py counterpart is not running
			if e.errno == errno.ECONNREFUSED:
				print("Sorry, server.py is ECONNREFUSED")
				sys.exit(1)
			else:
				raise
		while True:
                        s.sendall(flag.encode('ascii'))           # send "ready" message             
                        data = s.recv(256, socket.MSG_WAITALL)    # receive data from server
                        global values
                        values = str(data, "utf-8").split("\r\n") # format data to ['temp', 'cels', 'hum'..]
                        time.sleep(5)
		s.close()
		
def getValues():
        global values
        return values
	
if __name__ == "__main__":
	main()
