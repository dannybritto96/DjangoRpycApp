import os, binascii
import sys
import socket
operation = sys.argv[1]
parameters = sys.argv[2:]
temp = binascii.b2a_hex(os.urandom(5))
machine_name = socket.gethostname()
def_operation = ['ping','update']
filename = None
def exec_remove(pyfile):
	os.system("python "+pyfile)
	os.remove(pyfile)
def ping_fn(f,p):
	if (len(p) == 1 and '.' in p[0]):
		fh = open(f,"w+")
		fh.write("import os\n")
		fh.write("os.system('ping"+" "+str(parameters[0])+" -c 5')")
		fh.close()
		exec_remove(f)
	else:
		raise ValueError("Check Parameters")
def update_fn():
	print("Will require sudo privileges")
	os.system('apt update -y')
	
if operation in def_operation:
	filename = machine_name+operation+temp+".py"
	if operation == 'ping':
		ping_fn(filename,parameters)
	if operation == 'update':
		if len(parameters) == 0:
			update_fn()
		else:
			raise ValueError
else:
	raise TypeError("Invalid Operation")

		
		 
