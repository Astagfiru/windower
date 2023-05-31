import os
import ast

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

	def find_by_name(self, name):
		entities = self.file_handler.read_entities()
		for entity in entities:
			if entity.name == name:
				return entity
		return None

def PersonId(name, password):
	user = user_crud.find_by_name_and_password(name, password)
	if user is not None:
		return user.id
	else:
		return "No"

def BoardId(name):
	board = board_crud.find_by_name(name)
	if board is not None:
		return board.id
	else:
		return "No"

def ColumnId(name): # Добавил
	column = column_crud.find_by_name(name)
	if column is not None:
		return column.id
	else:
		return "No"

def CardId(name):
	cards = card_crud.file_handler.read_entities()
	for card in cards:
		if card.title == name:
			return card.id

	return "No"

def Reader(object_type, object_id):
	if object_type == "User":
		return user_crud.read(object_id)
	elif object_type == "Board":
		return board_crud.read(object_id)
	elif object_type == "Column":
		return column_crud.read(object_id)
	elif object_type == "Card":
		return card_crud.read(object_id)
	else:
		return None

def IsAppropriate(username):
	users = user_crud.file_handler.read_entities()
	for user in users:
		if user.name == username:
			return False
	return True

def GetUserBoards(username):
	user_boards = []
	boards = board_crud.file_handler.read_entities()
	for board in boards:
		if username in board.creator:
			user_boards.append(board)
	return user_boards

def GetUserAsAddedBoards(username):
	user_boards = []
	boards = board_crud.file_handler.read_entities()
	for board in boards:
		if username in board.users:
			user_boards.append(board)
	return user_boards

def delete_board_by_creator_and_name(user_nickname, board_name):
	boards = board_crud.file_handler.read_entities()
	for board in boards:
		if board.creator == user_nickname and board.name == board_name:
			board_crud.delete(board.id)
			return True
	return False

def delete_column_by_anybody(board_name, column_name): # Добавил
	boards = board_crud.file_handler.read_entities()
	for board in boards:
		if board.name == board_name:
			for column in board.columns:
				if column.title == column_name:
					column_Id = ColumnId(column_name)
					board_crud.delete(column_Id)
					column_crud.delete(column_Id)
					return True
	return False

def checkifyouanauthor(user_nickname, board_name):
	boards = board_crud.file_handler.read_entities()
	for board in boards:
		if board.creator == user_nickname and board.name == board_name:
			return True
	return False

def get_all_users_except(UserNicknames):
	boards = board_crud.file_handler.read_entities()
	result = []
	for board in boards:
		b = board.users
		b_arr = ast.literal_eval(b)
		for i in range(len(b_arr)):
			if b_arr[i] not in UserNicknames:
				result.append(board)
	return result

def get_all_user_nicknames():
	users = user_crud.file_handler.read_entities()
	result = []
	for user in users:
		result.append(user.name)
	return result

# user_info = Reader("User", 1)
# print(user_info.name)


user_crud = CRUDOperations(FileHandler('users.txt', User))
board_crud = CRUDOperations(FileHandler('boards.txt', Board))
column_crud = CRUDOperations(FileHandler('columns.txt', Column))
card_crud = CRUDOperations(FileHandler('cards.txt', Card))

# user = user_crud.create("Vitya", "wasd")

# board = board_crud.create("thefirst", "vitya", ["Alex", "Natcha"], ["001", "002"], "19.05")
# board_crud.update(board.id, columns=["001"])
# print(len(board.columns))

# card = card_crud.create("ha", "wa", 1, "1", "1.jpg")
# column = column_crud.create("Shtosh", card.id)

# print(PersonId("Vitya", "wasd"))