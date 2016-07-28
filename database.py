import sqlite3
import os
from db_types import *


class Database:

	def __init__(self):
		self.create_db_dir()
		db_path = os.path.join(self.db_dir, 'database')		
		self.database = sqlite3.connect(db_path)
		self.database.row_factory = self.dict_factory

	def create_db_dir(self):
		root = os.path.dirname(os.path.realpath(__file__))
		self.db_dir = os.path.join(root, 'db')
		if not os.path.isdir(self.db_dir):
			os.mkdir(self.db_dir)

	def get_cursor(self):
		return self.database.cursor()

	def dict_factory(self, cursor, row):
	    results_dict = {}
	    for index, column in enumerate(cursor.description):
	        results_dict[column[0]] = row[index]
	    return results_dict

	def execute_sql(self, sql):
		cursor = self.get_cursor()
		try:
			cursor.execute(sql)
			self.database.commit()
		except Exception as e:
			pass

	@staticmethod
	def get_model_name(model):
		return model.__class__.__name__.lower()

	@staticmethod
	def get_class_name(c):
		return c.__name__.lower()

	def build_tables(self, models):
		for Model in models:
			model = Model()
			model.validate()
			table = self.get_class_name(Model)
			# table = Model.__name__.lower()
			sql = 'CREATE TABLE IF NOT EXISTS {} ('.format(table)
			for k, v in model.__dict__.items():
				values = v.__dict__
				if isinstance(v, ForeignKeyType):
					relation = values.get('relation')
					if relation:
						relation_name = self.get_class_name(relation)
						cols = '{}_id {} '.format(relation_name, v.type)
				else:
					cols = '{} {} '.format(k, v.type)
				if values.get('primary_key'):
					cols += 'PRIMARY KEY '
				if values.get('unique'):
					cols += 'UNIQUE '
				if not values.get('allow_null'):
					cols += 'NOT NULL'
				cols += ','
				sql += cols
			sql = '{})'.format(sql.rstrip(','))
			print sql
			# self.execute_sql(sql)

	def insert(self, model):
		table = self.get_model_name(model)
		sql = 'INSERT INTO {} '.format(table)
		keys = ''
		values = ''
		for k, v in model.__dict__.items():
			if v.__dict__.get('auto_increment'):
				continue
			keys += '{},'.format(k)
			val = '"{}",' if v.type == 'TEXT' else '{},'
			values += val.format(v.value)
		keys = keys.rstrip(',')
		values = values.rstrip(',')
		sql += '({}) VALUES ({})'.format(keys, values)
		self.execute_sql(sql)

	def query(self, model, id=None, where=None, operator='AND', join=None, order_asc=None, order_desc=None):
		table = self.get_model_name(model)
		sql = 'SELECT * FROM {} '.format(table)
		if id:
			sql += 'WHERE id={}'.format(id)
		elif where:
			sql += 'WHERE '
			for k, v in where.items():
				if type(v) is list:
					for li in v:
						sql += self.add_where_clause(k, li)
						sql += 'OR'
					sql = sql.rstrip('OR')
				sql += self.add_where(k, v)
				sql += operator
			sql = sql.rstrip(operator)
		if join:
			sql += self.add_join()
		if order_asc:
			sql += self.add_order(order_asc, 'ASC')
		elif order_desc:
			sql += self.add_order(order_desc, 'DESC')
		print sql
		cursor = self.get_cursor()
		cursor.execute(sql)
		results = cursor.fetchall()
		return results

	@staticmethod	
	def add_where(k, v):
		if type(v) is str:
			return ' {}="{}" '.format(k, v)
		else:
			return ' {}={} '.format(k, v)

	@staticmethod
	def add_order(column, order):
		if type(column) is list:
			column = ','.join(column)
		return 'ORDER BY {} {} '.format(column, order)

	@staticmethod
	def add_join():
		return ''