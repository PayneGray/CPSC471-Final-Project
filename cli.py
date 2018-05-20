from socket import *
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
    #recieve port num from server
    port_num = control_connection.recv(5)
    print "Server sent temp port", port_num+". Connecting now..."
    temp_socket = socket(AF_INET, SOCK_STREAM)
    temp_socket.connect((server_name, int(port_num)))
    print 'Opened a temp connection with server', (server_name, port_num)
    #DO THE SENDING FILE PART HERE
    #step 1: make sure the file exists

    temp_socket.close()

  #NOTE: Send command after or before  opening data connection?

  # OPEN DATA CONNECTION #

  # DO FUNCTION #

  # CLOSE DATA CONNECTION #

# CLOSE CONTROL CONNECTION #
control_connection.close()
print 'Control connection with', (server_name, server_port), 'closed'
