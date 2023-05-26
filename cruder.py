import os

class User:
	def __init__(self, id, name, password):
		self.id = id
		self.name = name
		self.password = password

class Board:
	def __init__(self, id, name, creator, users, columns, date):
		self.id = id
		self.name = name
		self.creator = creator
		self.users = users
		self.columns = columns
		self.date = date

class Column:
	def __init__(self, id, title, cards):
		self.id = id
		self.title = title
		self.cards = cards

class Card:
	def __init__(self, id, title, description, priority, column, thumbnail):
		self.id = id
		self.title = title
		self.description = description
		self.priority = priority
		self.column = column
		self.thumbnail = thumbnail

class FileHandler:
	def __init__(self, file_name, entity_class):
		self.file_name = file_name
		self.entity_class = entity_class

	def read_entities(self):
		if not os.path.exists(self.file_name):
			return []

		entities = []
		with open(self.file_name, 'r') as f:
			for line in f.readlines():
				fields = line.strip().split('|')
				entity = self.entity_class(*[int(fields[0])] + fields[1:])
				entities.append(entity)
		return entities

	def write_entities(self, entities):
		with open(self.file_name, 'w') as f:
			for entity in entities:
				f.write('|'.join([str(getattr(entity, attr)) for attr in vars(entity)]) + '\n')

class CRUDOperations:
	def __init__(self, file_handler):
		self.file_handler = file_handler

	def create(self, *args):
		entities = self.file_handler.read_entities()
		entity_id = len(entities) + 1
		entity = self.file_handler.entity_class(entity_id, *args)
		entities.append(entity)
		self.file_handler.write_entities(entities)
		return entity

	def read(self, entity_id):
		entities = self.file_handler.read_entities()
		for entity in entities:
			if entity.id == entity_id:
				return entity
		return None

	def update(self, entity_id, **kwargs):
		entities = self.file_handler.read_entities()
		for entity in entities:
			if entity.id == entity_id:
				for attr, value in kwargs.items():
					if value is not None:
						setattr(entity, attr, value)
				self.file_handler.write_entities(entities)
				return entity
		return None

	def delete(self, entity_id):
		entities = self.file_handler.read_entities()
		for entity in entities:
			if entity.id == entity_id:
				entities.remove(entity)
				self.file_handler.write_entities(entities)
				return True
		return False

	def find_by_name_and_password(self, name, password):
		entities = self.file_handler.read_entities()
		for entity in entities:
			if entity.name == name and entity.password == password:
				return entity
		return None

def PersonId(name, password):
		user = user_crud.find_by_name_and_password(name, password)
		if user is not None:
				return user.id
		else:
				return "No"

user_crud = CRUDOperations(FileHandler('users.txt', User))
board_crud = CRUDOperations(FileHandler('boards.txt', Board))
column_crud = CRUDOperations(FileHandler('columns.txt', Column))
card_crud = CRUDOperations(FileHandler('cards.txt', Card))

user = user_crud.create("Vitya", "wasd")

# board = board_crud.create("thefirst", "vitya", ["Alex", "Natcha"], ["001", "002"], "19.05")
# board_crud.update(board.id, columns=["001"])
# print(len(board.columns))

# card = card_crud.create("ha", "wa", 1, "1", "1.jpg")
# column = column_crud.create("Shtosh", card.id)

print(PersonId("Vitya", "wasd"))