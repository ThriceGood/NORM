from db_types import IntegerType, TextType
from model_parent import Model, query, initialize_models


class Child(Model):

	def __init__(self, name=None, nationality=None, age=None):
		self.id = IntegerType(value=None, primary_key=True, auto_increment=True)
		self.name = TextType(value=name, unique=True)
		self.nationality = TextType(value=nationality)
		self.age = IntegerType(value=age)


class Car(Model):

	def __init__(self, make=None, model=None, year=None, engine=None):
		self.id = IntegerType(value=None, primary_key=True, auto_increment=True)
		self.make = TextType(value=make)
		self.model = TextType(value=model)
		self.year = IntegerType(value=year)
		self.engine = IntegerType(value=engine)


initialize_models([Car, Child])