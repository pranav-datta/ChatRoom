import socket
import threading
import sys 
import select
import datetime
import argparse

#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

parser = argparse.ArgumentParser(description='Client for connecting to chatroom')
parser.add_argument('-join', action='store_true')
parser.add_argument('-host')
parser.add_argument('-port')
parser.add_argument('-username')
parser.add_argument('-passcode')

args = parser.parse_args()

displayName = args.username
password = args.passcode
ip = args.host
port = int(args.port)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((ip, port))

def receive():
	while True:
		try:
			message = clientSocket.recv(2048).decode('ascii')
			if message == "nickname":
				clientSocket.send(displayName.encode('ascii'))
				print("Connected to " + ip + " on port " + str(port))
				sys.stdout.flush()
			elif message == "password":
				clientSocket.send(password.encode('ascii'))
			elif message == "Incorrect passcode":
				print("Incorrect passcode")
				sys.stdout.flush() 
			else:
				print(message)
				sys.stdout.flush() 
		except:
			clientSocket.close()
			break
def write():
	while True:
		msg = input("")
		if (msg == ":)"):
			msg = "[feeling happy]"
		if (msg == ":("):
			msg = "[feeling sad]"
		if (msg == ":mytime"):
			date = datetime.datetime.now()
			msg = date.strftime("%a %b %d %H:%M:%S %Y")
		if (msg == ":+1hr"):
			date = datetime.datetime.now()
			date = date + datetime.timedelta(hours = 1)
			msg = date.strftime("%a %b %d %H:%M:%S %Y")
		message = displayName + ": " + msg
		if (msg == ":Exit"):
			clientSocket.send(msg.encode('ascii'))
			break
		clientSocket.send(message.encode('ascii'))
	clientSocket.close()
		
		

receive_thread = threading.Thread(target = receive)
receive_thread.start()

write_thread = threading.Thread(target = write)
write_thread.start()


if __name__ == "__main__":
	pass