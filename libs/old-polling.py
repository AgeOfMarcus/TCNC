import time

stoppoll = False

def polling_loop(api,handler,wait=1):
	while True:
		if stoppoll:
			break
		time.sleep(wait)
		for dm in api.direct_messages(tweet_mode='extended'):
			handler.handle(dm.id)

class DMHandler(object):
	def __init__(self, db):
		self.db = db
		self.cursor = db.cursor()
		self.queue = []
	def handle(self, id):
		chk = self.cursor.execute("SELECT ID FROM ignore WHERE ID='%s'" % id).fetchall()
		if not len(chk) == 0:
			return None
		else:
			self.queue.append(id)
			return None

# Due to sqlite3 not playing nice with threads (for good reasons), this will remain un-used
