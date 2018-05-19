import socket
import os
import sys

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
	command = raw_input("ftp> ")

	if command=="quit":
		connSock.send(command)
		print "time to go"
		break
	else:
		connSock.send(command)

# Close the socket and the file
connSock.close()
 	


