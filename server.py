#! /usr/bin/python3

import os
import readline
import socket

from _thread import *


name = ''
port = 0
done = False
server = None
users = {}
messages = []

def login():
	global name, port

	print('Welcome to Chatuba(SERVER)!\n')

	name = input('Name[ChatServer]: ').strip()
	name = name if name else 'ChatServer'

	try:
		port = int(input('Port[6666]: '))
	except ValueError:
		port = 6666

def setup():
	global server

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind(('', port))
	server.listen()
	
	print()

	if os.name == 'nt':
		os.system('ipconfig | find "IPv4"') 

	else:
		os.system('echo IP: $(hostname -I)')
	
	print('\n# Running...', end='\n\n')

def session(conn, addr):
	global messages

	while True:
		try:
			data = conn.recv(2048)
			reply = data.decode('utf-8')

			if not data:
				conn.send(str.encode('exit'))
				break

			cmd, arg = reply.split(':')

			if cmd == 'join':
				users[addr] = arg
				reply = name

			elif cmd == 'list':
				reply = ''

				if arg == 'usr':
					for user in users:
						reply += '[%s]: %s' % (user[0], users[user]) + '\n'

				elif arg == 'msg':
					if len(messages) == 0:
						reply = '...\n'

					else:
						for message in messages:
							reply += '[%s]: %s' % message + '\n'

			elif cmd == 'add':
				messages.append((users[addr], arg))
				reply = 'sucess'

			conn.sendall(str.encode(reply))
		except:
			break

	conn.close()
	users.pop(addr)
	print('# %s: unconnected.' % addr[0])

def check():
	global server, done

	try:
		conn, addr = server.accept()
		print('# %s: connected.' % addr[0])

		start_new_thread(session, (conn, addr))
	except KeyboardInterrupt:
		done = True

def main():
	global done, server

	try:
		login()
	except:
		exit()

	setup()
	
	while not done:
		check()			
	
	print('\n# Server finished!')
	server.close()

if __name__ == '__main__':
	main()
