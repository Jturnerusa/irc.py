import socket, ssl, re

class Message:

	def __init__(self, raw):
		self.raw = raw
		if self.raw.count(":") == 2:
			self.prefix, self.suffix = self.raw.split(":")[1], self.raw.split(":")[-1]
		if self.raw.count(":") == 1:
			self.prefix, self.suffix = self.raw.split(":")[0], self.raw.split(":")[-1]
		try:
			self.type = re.findall("([A-Z]+)", self.prefix)[0]
		except:
			self.type = None
		try:
			self.sender = re.findall("([a-zA-Z0-9]+)!", self.prefix)[0]
			self.ident = re.findall("!~([a-zA-Z0-9]+)@", self.prefix)[0]
			self.mask = re.findall("@([a-zA-Z0-9]+) ", self.prefix)[0]
		except:
			self.sender, self.ident, self.mask = None, None, None

class Irc:

	def __init__(self, address, port, ssl):
		self.socket = socket.socket()
		self.connect(address, port, ssl)
		self.alive = True
		self.buffer = ""

	def __iter__(self):
		while True:
			try:
				self.buffer += self.socket.recv(1024).decode()
			except:
				self.alive = False
				return
			while "\r\n" in self.buffer:
				length = self.buffer.index("\r\n")
				data = self.buffer[:length]
				self.buffer = self.buffer[length + 2:]
				message = handle_message(data)
				yield message

	def connect(self, host, port, ssl_enabled):
			if ssl_enabled:
				context = ssl.create_default_context()
				self.socket = context.wrap_socket(self.socket, server_hostname=host)
			self.socket.connect((host, port))

	def send_message(self, message):
		data = bytes(f"{message}\r\n", "UTF-8")
		self.send_messageall(data)

	def nick(self, nick):
		self.send_message("NICK {0}")

	def password(self, password):
		self.send_message("PASS {0}")

	def user(self, user):
		self.send_message("USER {0} {0} {0} :{0}")

	def ping(self, host):
		self.send_message("PING :{0}")

	def pong(self, server):
		self.send_message("PONG :{0}")

	def join_channel(self, channel):
		self.send_message("JOIN {0}")

	def part(self, channel):
		self.send_message("PART {0}")

	def privmsg(self, channel, message):
		self.send_message("PRIVMSG {0} :{1}")

	def notice(self, channel, message):
		self.send_message("NOTICE {0} :{1}")

	def kick(self, channel, nick, reason=None):

		if reason is not None:
			self.send_message("KICK {0} {1} :{2}")
		else:
			self.send_message("KICK {0} {1}")

	def names(self, channel):
		self.send_message("NAMES {0}")

	def topic(self, channel, topic):
		self.send_message("TOPIC {0} :{1}")

	def ban(self, channel, target):
		self.send_message("MODE {0} +b {1}")

	def unban(self, channel, target):
		self.send_message("MODE {0} -b {1}")

	def quiet(self, channel, target):
		self.send_message("MODE {0} +q {1}")

	def unquiet(self, channel, target):
		self.send_message("MODE {0} -q {1}")

	def who(self, target):
		self.send_message("WHO {0}")

	def me(self, channel, message):
		self.send_message("PRIVMSG {0} :\001ACTION {1}\001")

assert Message("PING :123").prefix == "PING "
assert Message("PING :123").suffix == "123"
assert Message("PING :123").type == "PING"
assert Message(":sender!~ident@mask NICK :newnick").prefix == "sender!~ident@mask NICK "
assert Message(":sender!~ident@mask NICK :newnick").suffix == "newnick"
assert Message(":sender!~ident@mask NICK :newnick").type == "NICK"
assert Message(":sender!~ident@mask NICK :newnick").sender == "sender"
assert Message(":sender!~ident@mask NICK :newnick").ident == "ident"
assert Message(":sender!~ident@mask NICK :newnick").mask == "mask"