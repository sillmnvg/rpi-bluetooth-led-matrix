# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *
import subprocess
import psutil

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print "Waiting for connection on RFCOMM channel %d" % port

client_sock, client_info = server_sock.accept()
print "Accepted connection from ", client_info
data_str = ""
matrix_flag = False
matrix_output_pid = ""

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
	if (ord(data) != 13):
		data_str += data
	elif (ord(data) == 13):
		print data_str
		args = ["sudo","python","runtext.py","-t",data_str]
		if matrix_flag:
			p_old = psutil.Process(matrix_output_pid)
			p_old.terminate() #or p_old.kill()
		p = subprocess.Popen(args, shell=False)
		matrix_flag = True
		matrix_output_pid = p.pid
		data_str = ""
	#print "DEBUG DATA: recieved [%s]" % data
	#print data_str
except IOError:
    pass

print "disconnected"

client_sock.close()
server_sock.close()
print "all done"
