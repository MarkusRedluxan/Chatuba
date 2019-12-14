#! /usr/bin/python3

import os
import socket


done = False
name = ''
server = {}
prompt = '> '
client = None

# User functions:
# These functions are called when the user (client) types a command.
# All the commands are keys in 'funcs dictionary'.. It is a bit stange,
# because some commands like Python lang functions. So, using 'funcs
# dictionary' is possible find and call the functions.

def close(nothing):
	'''Exit the server and close the app.'''
	global done, client
	
	done = True
	client.close()

def man(cmd):
	'''Show how to use a command.'''
	global funcs
	
	if not cmd:
		for cmd in funcs.keys():
			print('%s: %s' % (cmd, funcs[cmd].__doc__))

def lst(what):
	'''List users[usr] or messages[msg] in the server.'''
	global client

	what = 'list:' + ' '.join(what)
	client.send(str.encode(what))
	reply = client.recv(2048).decode()
	print(reply)

def send(what):
	'''Send a text message to the server.'''
	global client

	what = 'add:' + ' '.join(what)
	client.send(str.encode(what))
	reply = client.recv(2048).decode()

# In this dict all references to the user functions are stored.
funcs = {
	'exit': close,
	'help': man,
	'list': lst,
	'send': send
}

# Internal functions:
# These functions are used during an app session.
# It means these make something like get user date, connect the server,
# etc. The bulk of these are called in 'main function'.

def login():
	global name, server

	print('Welcome to Chatuba!\n')
	
	txt = input('Your name[Unknown]: ')
	name = txt if txt else 'Unknown'

	txt = input('Server IP[localhost]: ')
	server['ip'] = txt if txt else 'localhost'

	try:
		server['port'] = int(input('Server PORT[6666]: '))
	except ValueError:
		server['port'] = 6666

def setup():
	global client, server, prompt

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((server['ip'], server['port']))

	print()
	print('# Connecting... ', end='')

	client.send(str.encode('join:' + name))
	server['name'] = client.recv(2048).decode()
	prompt = '%s@%s: ' % (name, server['name'])

	print('OK!\n')

def check():
	global funcs

	cmds = input(prompt)
	
	if cmds.strip()[0] == '!':
		os.system(cmds.replace('!', '', 1))
		return None
	
	cmds = cmds.rsplit(';')

	for cmd in cmds:
		try:
			cmd = cmd.rsplit(' ')
			funcs[cmd[0]](cmd[1:])
		except KeyError:
			print('%s: not find \'-\'' % cmd[0])

def main():
	global done
	
	login()
	setup()
	
	while not done:
		check()

if __name__ == '__main__':
	main()

