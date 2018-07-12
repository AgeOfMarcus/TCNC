import tweepy, time
from tweepy import OAuthHandler

queue = []

# Ignore funcs
def ignore():
	try:
		with open("ignore.txt","r") as f:
			ids = f.read().split("\n")
			idlist = []
			for i in ids:
				if not i == '':
					idlist.append(i)
		return idlist
	except:
		with open("ignore.txt","w") as f: pass
		return []
def add_ignore(id):
	if not id in ignore():
		with open("ignore.txt","a") as f:
			f.write(str(id) + "\n")


def check_dms(api, agent_user, wait=1):
	while True:
		for dm in api.direct_messages(tweet_mode='extended'):
			if dm.sender_screen_name == agent_user:
				id = dm.id
				if not id in ignore():
					if not id in queue:
						queue.append(id)
		time.sleep(wait)

def sort_queue(handle_func):
	for id in queue:
		message = api.get_direct_message(ID, tweet_mode='extended', full_text=True)
		handle_func(message)
		queue.remove(id)
		add_ignore(id)


