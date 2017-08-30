class Stack:
	def __init__(self):
		self.content = []

	def push(self, e):
		self.content.append(e)

	def pop(self):
		return self.content.pop(-1)

	def __str__(self):
		return str(self.content)

class Queue:
	def __init__(self):
		self.content = []

	def enqueue(self, e):
		self.content.append(e)

	def dequeue(self):
		return self.content.pop(0)

	def __str__(self):
		return str(self.content)

