from socket import *
import sys
import os

def temp_connect(command, file):
  #recieve port num from server
  port_num = control_connection.recv(5)
  print "Server sent temp port", port_num+". Connecting now..."
  temp_socket = socket(AF_INET, SOCK_STREAM)
  temp_socket.connect((server_name, int(port_num)))
  
  print 'Opened a temp connection with server', (server_name, port_num)
  if command=="put":
    #send over file size
    numBytes = get_file_size(file)
    temp_socket.send(str(numBytes))
    print numBytes
    #sending file
    putFile(temp_socket, file)
  print "Closed temp socket"
  temp_socket.close()


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


# ================== CHECK VALID FUNCTION ARGS ================= #

if len(sys.argv) < 3:
  print "USAGE python cli.py ", sys.argv[0], " <server machine> <server port>"
  sys.exit()

server_name = sys.argv[1]
try:
  server_port = int(sys.argv[2])
except:
  print "Error: please enter a valid server port number"
  sys.exit()

# ==========  OPEN CONTROL CONNECTION WITH SERVER ============= #

try:
  control_connection = socket(AF_INET, SOCK_STREAM)
  control_connection.connect((server_name, server_port))
except Exception as e:
  print "Could not connect to the specified server"
  print "Error: ", e
  sys.exit()
print 'Opened a control connection with server', (server_name, server_port)

# ===== SEND COMMAND AND OPEN DATA CONNECTION WITH SERVER ==== #

command = ""

while command != "quit":

  #Get command from user
  command = raw_input('ftp> ')

  #Send length of command (as a 3-character string)
  command_len_str = str( len(command) ).zfill(3)

  print 'Sending length of the command:', command_len_str
  bytes_sent = 0
  while bytes_sent != 3:
    bytes_sent += control_connection.send( command_len_str[bytes_sent:] )
  
  #Length of command has been sent
  print 'Length of command sent!'


  #Send command
  print 'Sending command:', command
  bytes_sent = 0
  while bytes_sent != len(command):
    bytes_sent += control_connection.send( command[bytes_sent:] ) 
  
  #Command has been sent
  print 'Command sent!'


  #SEND FILE TO SERVER
  if command.split(" ")[0]=="put":
    temp_connect("put",command.split(" ")[1])
    break
  elif command.split(" ")[0]=="get":
    pass
    #PREPARE TO RECIEVE
  elif command == "lss":
    os.system("ls")
  else:
    print "invalid command"




# CLOSE CONTROL CONNECTION #
control_connection.close()
print 'Control connection with', (server_name, server_port), 'closed'
