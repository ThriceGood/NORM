from db_types import IntegerType, TextType, ForeignKeyType, CharType
from model_parent import Model, query

class Car(Model):

	def __init__(self, make=None, model=None, year=None, engine=None):
		# self.id = IntegerType(value=None, primary_key=True)
		self.id = IntegerType(primary_key=True)
		self.make = TextType(value=make)
		self.model = TextType(value=model)
		self.year = IntegerType(value=year)
		self.engine = IntegerType(value=engine)


class Sack(Model):

	def __init__(self, name=None, item=None):
		self.id = IntegerType(primary_key=True)
		self.name = TextType(value=name)

class Item(Model):

	def __init__(self, name=None, weight=None, sack=None):
		self.sack = ForeignKeyType(value=sack, relation=Sack)
		self.id = IntegerType(primary_key=True)
		self.name = CharType(value=name, size=20)
		self.weight = IntegerType(value=weight)


def initialize_models():
	# Model.initialize_models([Car])
	Model.initialize_models([Sack, Item])