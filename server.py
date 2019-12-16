#! /usr/bin/python3

import os
import readline
import socket

from _thread import *


name, port = '', 0
users = {}
messages = []

def init():
	global name, port

	print('Welcome to Chatuba(SERVER)!\n')

	name = input('Name[ChatServer]: ')

	if not name:
		name = 'ChatServer'

	try:
		port = int(input('Port[6666]: '))
	except ValueError:
		port = 6666

def work(conn, addr):
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
						reply += '[%s]: %s' % (user, users[user]) + '\n'

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
	print('#', addr, 'unconnected;')

init()
print()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', port))
server.listen()

os.system('ipconfig | find "IPv4"' if os.name == 'nt' else 'echo IP: $(hostname -I)')
print()
print('# Running...')

while True:
	try:
		conn, addr = server.accept()
		print('#', addr, 'connected;')

		start_new_thread(work, (conn, addr))
	except KeyboardInterrupt:
		break

server.close()
