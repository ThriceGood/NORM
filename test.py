import sqlite3


db = sqlite3.connect(':memory:')
cursor = db.cursor()

sql = "CREATE TABLE person (id INTEGER PRIMARY KEY, name CHAR(20), wallet_id INTEGER)"
cursor.execute(sql)
db.commit()
sql = "CREATE TABLE wallet (id INTEGER PRIMARY KEY, cash INTEGER)"
cursor.execute(sql)
db.commit()

sql = "INSERT INTO person (name, wallet_id) VALUES ('Jonathan', 1)"
cursor.execute(sql)
db.commit()
sql = "INSERT INTO wallet (cash) VALUES (1000000)"
cursor.execute(sql)
db.commit()

sql = "SELECT * FROM person JOIN wallet ON person.wallet_id == wallet.id"
cursor.execute(sql)
print cursor.fetchall()
#sql = "SELECT * FROM wallet"
#cursor.execute(sql)
#print cursor.fetchall()

db.close()
