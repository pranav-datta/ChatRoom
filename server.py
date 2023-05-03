import socket
import threading
import sys 
import argparse


#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

parser = argparse.ArgumentParser(description='Chatroom server')
parser.add_argument('-start', action='store_true')
parser.add_argument('-port')
parser.add_argument('-passcode')

args = parser.parse_args()

passcode = args.passcode
ip = '127.0.0.1'
port = int(args.port)

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind((ip, port))

serverSocket.listen()

clients = []
displayNames = []

def clientThread(connection):

	while True:
		try:
			message = connection.recv(2048)
			if message.decode('ascii') == ":Exit":
				exitChat(connection)
				break
			broadcast(message, connection)
			print(message.decode('ascii'))
			sys.stdout.flush()
		except:
			remove(connection)
			break

def exitChat(connection):
	index = clients.index(connection)
	displayName = displayNames[index]
	message = displayName + " left the chatroom"
	print(message)
	sys.stdout.flush()
	remove(connection)
	broadcast(message.encode('ascii'), connection)

def broadcast(message, connection):
	for client in clients:
		if client != connection:
			client.send(message)

def remove(connection):
	if connection in clients:
		index = clients.index(connection)
		clients.remove(connection)
		displayName = displayNames[index]
		displayNames.remove(displayName)

def createClient():
	while True:

		connection, address = serverSocket.accept()
	
		connection.send("password".encode('ascii'))
	
		password = connection.recv(2048).decode('ascii')
	
		if (password != passcode):
			incorrect_passcode = "Incorrect passcode"
			connection.send(incorrect_passcode.encode('ascii'))
	 
		else:

			connection.send("nickname".encode('ascii'))

			displayName = connection.recv(2048).decode('ascii')
			displayNames.append(displayName)
			clients.append(connection)

			print(displayName + " joined the chatroom")
			sys.stdout.flush()

			join_message = displayName + " joined the chatroom"
			broadcast(join_message.encode('ascii'), connection)


			thread = threading.Thread(target=clientThread, args=(connection,))

			thread.start()
		
print("Server started on port " + str(port) + ". Accepting connections")
sys.stdout.flush()
createClient()


if __name__ == "__main__":
	pass