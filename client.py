#! /usr/bin/python3

import readline
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
	
	print()

	try:
		print('%s: %s' % (cmd[0], funcs[cmd[0]].__doc__))
	except:
		for cmd in funcs.keys():
			print('%s: %s' % (cmd, funcs[cmd].__doc__))
	
	print()

def lst(what):
	'''List users[usr] or messages[msg] in the server.'''
	global client

	what = ' '.join(what)

	if what == 'msg' or what == 'usr':
		what = 'list:' + what
		client.send(str.encode(what))
		reply = client.recv(2048).decode()
		print('\n%s' % reply)
	
	else:
		print('\n# %s: not exist.', what, end='\n\n')

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

	print('# Welcome to Chatuba!', end='\n\n')
	
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

	print('\n# Connecting... ', end='')

	client.send(str.encode('join:' + name))
	server['name'] = client.recv(2048).decode()
	prompt = '%s@%s: ' % (name, server['name'])

	print('OK!', end='\n\n')

def parse(cmds):
	cmds = cmds.split(';')
	
	for cmd in cmds:
		if not cmd.strip():
			cmds.remove(cmd)
	
	return cmds

def check():
	global funcs

	try:
		cmds = input(prompt)
	except:
		cmds = 'exit'

	for cmd in parse(cmds):
		try:
			cmd = cmd.split()

			if cmd[0][0] == '!':
				cmd[0] = cmds[0].replace('!', '', 1)
				os.system(' '.join(cmd))
			
			else:
				funcs[cmd[0]](cmd[1:])
		except KeyError:
			print('\n# %s: not found.' % cmd[0], end='\n\n')

def main():
	global done
	
	try:
		login()
	except:
		exit()

	setup()
	
	while not done:
		check()

if __name__ == '__main__':
	main()

