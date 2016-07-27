from db_types import TypeParent
from database import Database 

db = Database()
query =	db.query
initialize_models = db.build_tables(models)

class Model:

	def __init__(self):
		pass

	def validate(self):
		for k, v in self.__dict__.items():
			if not isinstance(v, TypeParent):
				raise ValueError('{} is not a valid object type: {}'.format(k, type(v)))

	def insert(self):
		db.insert(self)


