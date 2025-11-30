class Message:
	def __init__(self, role, content):
		self.role = role
		self.content = content


class Chat:
	def __init__(self, *messages: tuple[Message]):
		self.messages = [
			{
				'role': message.role,
				'content': message.content,
			}
			for message in messages
		]

	def add(self, message: Message):
		self.messages.append({
			'role': message.role,
			'content': message.content,
		})