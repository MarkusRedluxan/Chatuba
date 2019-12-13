#! /usr/bin/python3

import os
import socket


help_msg = {
	'exit': ['', 'Close the app.'],
	'help': ['[cmd]', 'Show how to use a command.'],
	'list': ['[items]', 'List users(users) or messages(msgs).'],
	'send': ['[message]', 'Send a message.'],
	'clear': ['', 'Clear all lines.']
}

print('Welcome to Chat!\n')

name = input('Your name[Unknown]: ')

if not name:
	name = 'Unknown'

server = {}

server['ip'] = input('Server IP[localhost]: ')

if not server['ip']:
	server['ip'] = 'localhost'

try:
	server['port'] = int(input('Server PORT[6666]: '))
except ValueError:
	server['port'] = 6666

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server['ip'], server['port']))

print()
print('# Connecting... ', end='')

client.send(str.encode('join:' + name))
server['name'] = client.recv(2048).decode()

print('OK!\n')

while True:
	cmd = input('%s@%s: ' % (name, server['name'])).strip().split(' ')
	cmd[0] = cmd[0].lower()

	print()

	if not cmd[0]:
		os.system('cls' if os.name == 'nt' else 'clear')
		client.send(str.encode('list:msgs'))
		reply = client.recv(2048).decode()
		print(reply)

	elif cmd[0] == 'exit':
		break

	elif cmd[0] == 'help':
		if len(cmd) == 1:
			for msg in help_msg:
				print('%s %s: %s' % (msg, help_msg[msg][0], help_msg[msg][1]))

			print()

		else:
			try:
				print('%s %s: %s\n' % (cmd[1], help_msg[cmd[1]][0], help_msg[cmd[1]][1]))
			except KeyError:
				print('# Unknown command!\n')

	elif cmd[0] == 'list':
		if len(cmd) == 1:
			print('# What do you want to list?')
			print('Tip: Use \'help list\'.\n')

		else:
			client.send(str.encode('list:' + cmd[1].lower()))
			reply = client.recv(2048).decode()
			print(reply)

	elif cmd[0] == 'send' or cmd[0] == '-':
		if len(cmd) == 1:
			print('# You cannot send a empty message!')
			print('Tip: Use \'help send\'.\n')

		else:
			client.send(str.encode('add:' + ' '.join(cmd[1:])))
			reply = client.recv(2048).decode()

	elif cmd[0] == 'clear' or cmd[0] == 'cls':
		os.system('cls' if os.name == 'nt' else 'clear')

	else:
		print('# Unknown command!\n')

client.close()
