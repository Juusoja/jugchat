import sys
import socket
import select

class Room:
	
	def __init__(self, given_name, given_password):
		self.name = given_name
		self.password = given_password
		self.messages = []
		self.users = []
	
	def save_message(self, message):
		if message != None:
			self.messages.append(message)
			return 1
		else:
			return 0

	def get_messages(self):
		return self.messages

	def get_password(self):
		return self.password

	def set_password(self, password):
		self.password = password
		return 1

	def get_name(self):
		return self.name

	def set_name(name):
		self.name = name
		return 1