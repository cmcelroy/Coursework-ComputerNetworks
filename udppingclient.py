###########################################################################
###
###	   Name: Chris McElroy
###	  Class: CSC450
###    Date: 10-13-2020
###	Summary: A UDP client that pings a server and displays the RTT and reports 
###			 timeouts, and diplays min max and average.
###
###	 Python 2.7
###
###########################################################################




#imports
import sys
import random, datetime, time
from socket import *

#create UDP Socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

server_ip = sys.argv[1]
server_port = int(sys.argv[2])
numPings = sys.argv[3]

#RTT List in order to calculate max, min and avg
RTTList = []

#counter to know how many requested time out
counter = 0

#find the Avg 
def avg(list):
	sum = 0
	for x in list:
		sum += x

	return str(sum/len(list)*1.0)

#find the Max 
def max(list):
	max = list[0]
	for x in list[1:]:
		if x > max:
			max = x

	return str(max)

#find the Min 
def min(list):
	min = list[0]
	for x in list[1:]:
		if x < min:
			min = x

	return str(min)

#find the Percentange
def perc(num, whole):
	return (float(num)/float(whole))*100

print('Pinging %s' % (server_ip))

for seq_num in range(1,int(numPings)+1):

	#time packet is being sent in hours, minutes, seconds, year
	senttime = time.strftime("%H:%M:%S:%Y", time.localtime())

	#initial time packet is send; Used for RTT
	intime = time.time()

	RTT = (time.time() - intime)
	timertt = RTT*1000000
	
	#message being sent
	message = 'Reply from %s : Ping %d %s : time=%.3s TTL=1' % (server_ip, seq_num, senttime, timertt)

	#sendmessage to Server
	clientSocket.sendto(message, (server_ip, server_port))

	#set timeout to 1 second
	clientSocket.settimeout(1)

	try:
		#receive message
		modifiedMessage, serverAddress = clientSocket.recvfrom(server_port)
		
		#print the Modified Message
		print(modifiedMessage)

		#calculate RTT Time
		RTT = (time.time() - intime)
		RTT = RTT*10000
		RTTList.insert(seq_num, RTT)

	except timeout:
		print('Request timed out.')
		counter += 1

print('Ping statistics for %s' % (server_ip))
print("     Segments: Sent: {}, Received: {}, Lost: {}%" .format(seq_num, counter+1, perc(counter, numPings)))

print('Approximate round trip time in ms:')
print('     Minimum = %.3s, Maximum RTT: %.3s, Average = %.3s' % (min(RTTList), max(RTTList), avg(RTTList)))


clientSocket.close()
