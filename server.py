from socket import *
import sys
import os


# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

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
  
  return recvBuff


# CHECK VALID FUNCTION ARGS #
if len(sys.argv) < 2:
  print "USAGE python ", sys.argv[0], " <PORT NUMBER>"
  sys.exit()

try:
  port = int(sys.argv[1])
except:
  print "Error: please enter a valid port number"
  sys.exit()

# CREATE SERVER SOCKET #

server_socket = socket(AF_INET, SOCK_STREAM)
try:
  server_socket.bind(('', port))
except Exception as e:
  print "Could not bind the server socket to the specified port number"
  print "Error: ", e
  sys.exit()
  
server_socket.listen(100)

while 1:
  
  # OPEN CONTROL CONNECTION WITH CLIENT #
  print "Server now listening for connection requests..."

  
  control_connection, client_address = server_socket.accept()
  print 'Opened a control connection with client', client_address
  
  command = ""

  # LISTEN FOR A NEW COMMAND #
  while True:
    #Reset command buffer
    command = ""

    #Get the length of the command
    print 'Waiting for length of command...'
    command_len_str = ""
    while len(command_len_str) != 3:
      command_len_buffer = control_connection.recv(3)
      if not command_len_buffer:
        print 'Connection closed unexpectedly when waiting for length of command'
        break
      command_len_str += command_len_buffer

    #Length of command has been received  
    command_len = int(command_len_str)
    print 'Received length of command:', command_len_str

    #Get command
    print 'Waiting for command...'
    while len(command) != command_len:
      command_buffer = control_connection.recv(command_len)
      if not command_buffer:
        print 'Connection closed unexpectedly when waiting for command'
        break
      command += command_buffer
    print 'Received command', command

    if command=="quit":
      break
    elif command.split(" ")[0]=="put":
      # Create a socket
      temp_socket = socket(AF_INET, SOCK_STREAM)
      # Bind the socket to port 0
      temp_socket.bind(('',0))
      # Retreive the ephemeral port number
      print "I chose ephemeral port: ", temp_socket.getsockname()[1]
      #send port num
      control_connection.send(str(temp_socket.getsockname()[1]))
      # wait for the client to connect to it
      print "Waiting for the client to connect to temp port..."
      temp_socket.listen(1)

      control_connection_t, client_address_t = temp_socket.accept()
      print "client connected to temp port"





      ## DO THE RECIEVING FILE PART HERE


      temp_socket.close()

    elif command=="ls":
      os.system("ls")
      #send this stuff to client
    else:
      #Command has been received
      print "Command invalid."
    
    # OPEN DATA CONNECTION #
    
    # DO FUNCTION #

    #CLOSE DATA CONNECTION #   


  #Client has closed the connection
  # CLOSE CONTROL CONNECTION #
  control_connection.close()
  print 'Closed connection with client', client_address
  server_socket.close()  
  sys.exit()

