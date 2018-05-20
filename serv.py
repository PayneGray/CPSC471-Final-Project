from socket import *
import sys


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
  while command != "quit":		#NOTE: I plan on implementing a quit function instead of doing it this way...
    
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

    #Command has been received
    print 'Received command', command
  
    # OPEN DATA CONNECTION #
    
    # DO FUNCTION #

    #CLOSE DATA CONNECTION #   


  #Client has closed the connection
  # CLOSE CONTROL CONNECTION #
  control_connection.close()
  print 'Closed connection with client', client_address
  


