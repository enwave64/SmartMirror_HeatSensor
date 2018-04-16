#client.py

### Programmer: Elliott Watson; enwave@hotmail.com, enwatson@sdsu.edu

### Program: Assignment # 1: Network Socket Programming

### Programming Language: Python 3

### OS1: Linux Mint Mate x64, BASH shell, ifconfig
### OS2: Windows 10, Cygwin with Python3 installed, Powershell for ipconfig

### Professor: Dr. Wei Wang
### Course: CS 576: Networks and Distributed Systems, Spring 2018

############################################################################
# This program is a client application that uses Python3's socket library.
# It connects to a server application, sens a message no more than
# 265 characters, as well as a flag message indicating whether the message
# is to be encoded or decoded. These messages are passed as command line args
# of the form: python3 client.py encode\decode 'actual message'
############################################################################

import socket, sys, errno, time

HOST = '169.254.100.247' #should be changed as necessary
PORT = 50007 #any non-priveleged port; should be matched with server

def main():
	flag = 'v' 
	
	#all remaining words in the command line arguments get joined together as the message
	message = "string2"

	variables = ""
	y = 0

	#256 character limit on the message
	if len(message) > 256:
		print("ERROR: Please run again with a message of 256 characters or less")
		sys.exit(1)

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
                        s.sendall(flag.encode('ascii'))
                        variables = ""
                        values = ""
                        #for x in range(0,19):
                                # send to server, we're ready
                                

                                
                        data = s.recv(256, socket.MSG_WAITALL)
                        print("length data", len(data))
                        variables = variables + str(data, "utf-8")
                        #variables = str(data, "utf-8")
                        #print(repr(data.decode('ascii')))
                        print()
                        print("variables: ", variables)
                        values = variables.split("\r\n") # list in format ['temp', 'cels', 'hum'..]
                        print("values: ", values)
                        
                        if len(values) >= 4:
                                table = {'temp_f': values[0], 'temp_c': values[1], 'humidity': values[2], 'heat_index_f': values[3]}
                                for k, v in table.items():
                                        print(k, ": ", v)
                        #y = y+1
                        time.sleep(5)
		s.close()
		
	print('Recieved a(n)', flag, ':', repr(data.decode('ascii')))
        # while True:
	
if __name__ == "__main__":
	main()
