# *************************************************************
# This program illustrates how to generate an emphemeral port
# *************************************************************
import socket
import commands

# Create a socket
welcomeSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to port 0
welcomeSocket.bind(('',0))

# Retreive the ephemeral port number
print "I chose ephemeral port: ", welcomeSocket.getsockname()[1]

# Start listening on the socket
welcomeSocket.listen(1)

while True:
	
	print "Waiting for connections..."
	
	# Accept connections
	clientSock, addr = welcomeSocket.accept()
	
	print "Accepted connection from client: ", addr

	while True:
		buff = clientSock.recv(100)

		

		print "client> ",buff



		if buff == "quit":
			break
		else:
			# Run ls command, get output, and print it
			for line in commands.getstatusoutput(buff):
				print "client> ",line


	break
welcomeSocket.close()

#get <file name> (downloads file <file name> from the server)
#put <filename> (uploads file <file name> to the server)
#ls (lists files on the server)
#lls (lists files on the client)
#quit (disconnects from the server and exits)