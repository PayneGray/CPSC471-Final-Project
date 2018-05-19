import socket
import commands

'''
get_file_size (might want a shorter name)
takes a file name
returns the size of the data to be sent over tcp
including file size + file name + delimiter character
'''
def get_file_size (file_name):
    file = open(file_name, "r")
    file_data = file.read(65536)
    if file_data:
        file_size = len(file_data)
    file.close()
    return (file_size + len(file_name) + 1)

'''
putFile Client side version
Takes: socket to ephemeral port, name of file to send
returns: number of bytes sent
'''
def putFile(socket, file_name):
    bytes_sent = 0
    file = open(file_name, "r")
    # The file data
    file_data = None
    # Keep sending until all is sent
    while True:
        
        # Read 65536 bytes of data
        file_data = file.read(65536)
        file_data = file_name + bytes(0x1f) + file_data #prepend the file name to the file data with a delimiter of 0x1f which is the ascii code for unit separator 
        # Make sure we did not hit EOF
        if file_data:
            # Get the size of the data read
            # and convert it to string
            file_size = len(file_data)
                        
            # Send the data!
            while file_size > bytes_sent:
                bytes_sent += socket.send(file_data[bytes_sent:])
        # The file has been read. We are done
        else:
            break
    file.close()
    return bytes_sent

'''
takes a socket to receive on, and the number of bytes to receive
returns the number of bytes received
the bytes received will be in the form of:
file_name + 1 byte delimiter + file_data
This function creates a file using file_name and then writes file_data into it
'''
def getFile(sock, numBytes):
    

    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    # Keep receiving till all is received
    while len(recvBuff) < numBytes:
        
        # Attempt to receive bytes
        tmpBuff =  sock.recv(numBytes)
        
        # The other side has closed the socket
        if not tmpBuff:
            break
        
        # Add the received bytes to the buffer
        recvBuff += tmpBuff
    file_size = len(recvBuff)
    i = recvBuff.find(bytes(0x1f))
    file_name = recvBuff[0:i]
    i += 1
    file_data = recvBuff[i:]
    file = open(file_name, "w")
    file.write(file_data)
    file.close()
    return file_size

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to port 0
server_socket.bind(('',0))

# Retreive the ephemeral port number
print "I chose ephemeral port: ", server_socket.getsockname()[1]

# Start listening on the socket
server_socket.listen(1)

while True:
	  
  	# OPEN CONTROL CONNECTION WITH CLIENT #
  	print "Server now listening for connection requests..."

  	# Accept connections

  	clientSock, addr = server_socket.accept()
  	print 'Opened a control connection with client', addr
  

	while True:
		file_name = ""
		buff = clientSock.recv(100)
		print "client> ",buff

		if buff == "quit":
			break
		elif buff[0:4]=="get ":
			file_name = buff[4:]
			print "get "+file_name
		elif buff[0:4]=="put ":
			file_name = buff[4:]
			print "put "+file_name
		elif buff == "ls":
			# Run ls command, get output, and print it
			for line in commands.getstatusoutput(buff):
				print "client> ",line
				clientSock.send(str(line))
		elif buff == "lls":
			print "list client stuff"
		else:
			print "Command not recognized."


	break
server_socket.close()

#get <file name> (downloads file <file name> from the server)
#put <filename> (uploads file <file name> to the server)
#ls (lists files on the server)
#lls (lists files on the client)
#quit (disconnects from the server and exits)