import sqlite3
import os


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

	def build_tables(self, models):
		for Model in models:
			model = Model()
			model.validate()
			sql = 'CREATE TABLE IF NOT EXISTS {} ('.format(model.__class__.__name__.lower())
			for k, v in model.__dict__.items():
				values = v.__dict__
				cols = '{} {} '.format(k, v.type)
				auto_increment = values.get('auto_increment')
				if auto_increment:
					# cols += 'AUTO INCREMENT '
					pass
				primary_key = values.get('primary_key')
				if primary_key:
					cols += 'PRIMARY KEY '
				unique = values.get('unique')
				if unique:
					cols += 'UNIQUE '
				allow_null = values.get('allow_null')
				if not allow_null:
					cols += 'NOT NULL'
				cols += ','
				sql += cols
			sql = '{})'.format(sql.rstrip(','))
			cursor = self.get_cursor()
			cursor.execute(sql)
			self.database.commit()

	def insert(self, model):
		sql = 'INSERT INTO {} '.format(model.__class__.__name__)
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
		cursor = self.get_cursor()
		cursor.execute(sql)
		self.database.commit()

	def query(self, model, id=None, query=None, operator=None):
		table = model.__name__.lower()
		sql = 'SELECT * FROM {} '.format(table)
		if id:
			sql += 'WHERE id={}'.format(id)
		elif query:
			sql += 'WHERE '
			if not operator:
				operator = 'AND'
			for k, v in query.items():
				if type(v) is list:
					for li in v:
						sql += self.add_where_clause(k, li)
						sql += 'OR'
					sql = sql.rstrip('OR')
				sql += self.add_where_clause(k, v)
				sql += operator
			sql = sql.rstrip(operator)
		cursor = self.get_cursor()
		cursor.execute(sql)
		results = cursor.fetchall()
		return results

	@staticmethod	
	def add_where_clause(k, v):
		if type(v) is str:
			return ' {}="{}" '.format(k, v)
		else:
			return ' {}={} '.format(k, v)

