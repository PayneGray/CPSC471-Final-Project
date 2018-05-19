# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys

if len(sys.argv)<2:
	print "Not enough."
# Server address
serverAddr = "localhost"

# Server port
serverPort = int(sys.argv[1])

# Create a TCP socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
connSock.connect((serverAddr, serverPort))


# Keep sending until all is sent
while True:
	
	isay = raw_input("ftp> ")

	if isay=="quit":
		connSock.send(isay)
		print "time to go"
		break
	else:
		connSock.send(isay)

# Close the socket and the file
connSock.close()
 	


