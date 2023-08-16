###########################################################################
###
###	   Name: Chris McElroy
###	  Class: CSC450
###    Date: 10-13-2020
###	Summary: A UDP server that responds to client queries.
###
###	 Python 2.7
###
###########################################################################
 
import random
from socket import *

HOST = ''
PORT = 12000

# create a UDP socket 
serverSocket = socket(AF_INET, SOCK_DGRAM)
# assign IP address and port number to socket 
serverSocket.bind((HOST, PORT))

print('The server is ready to receive...\n')

while True:
	# generate random number in the range of 0 to 10
	rand = random.randint(0, 10)
	# receive the client packet along with the address it is coming from 
	message, address = serverSocket.recvfrom(12000)
	# If rand is less is than 4, we consider the packet lost and do not respond 
	if rand < 4:
		continue
    # otherwise, the server responds
	serverSocket.sendto(message, address)
