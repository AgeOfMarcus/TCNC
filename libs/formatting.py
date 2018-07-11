import base64

# The base message format
base = {
	'cliid':'XXXXXXXXX',
	'type':'XXXXXX',
	'data':'XXXXXXXXXXXXXXX',
}

# Message types
types = [
	'cmdreq', # A request for a command
	'error', # A client error
	'result', # Result of a command (from cmdreq)
]

# Data strunctures
cmdreq = {} # Just blank
error = {
	'time':'XXXXXX', # Time that the error occured
	'errormsg':'XXXXXXXXXXXX', # The actual error message
}
result = {
	'cmdid':'XXXXXXXXX', # The command ID
	'result':'XXXXXXXXXXXX', # The result of the command
	'time':{
		'recv':'XXXXXX', # Time that message was recieved
		'sent':'XXXXXX', # Time that response was sent
	} # Timestamps

# Encoding and decoding functions (thanks, random guy on StackOverflow)
def encode(clear,key):
	enc = []
	for i in range(len(clear)):
		key_c = key[i % len(key)]
		enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
		enc.append(enc_c)
	return base64.urlsafe_b64encode("".join(enc).encode()).decode()
def decode(enc,key):
	dec = []
	enc = base64.urlsafe_b64decode(enc).decode()
	for i in range(len(enc)):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
		dec.append(dec_c)
	return "".join(dec)
