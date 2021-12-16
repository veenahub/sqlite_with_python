import sqlite3

database = 'musicdatabase.db'

def run(query, values = {}):
 #creating database
  conn = sqlite3.connect(database)
  cursor = conn.cursor()
  results = cursor.execute(query, values)
  conn.commit()
  conn.close()
  return results.lastrowid

def get(query, values = {}):
  conn = sqlite3.connect(database)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute(query, values) 
  results = cursor.fetchall()
  conn.close()
  return results



