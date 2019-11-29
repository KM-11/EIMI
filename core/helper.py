import dotenv
from pathlib import Path
import re
import ipaddress
import sqlite3
from datetime import date

def load_env_file():
    env_path = Path('..') / '.env'
    dotenv.load_dotenv(dotenv_path=env_path)

def is_ip_valid(ip):
	try:
		ipaddress.ip_address(ip)
		return True
	except:
		return False

def find_ip_address(data):
	pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
	matches = re.findall(pattern,data)
	return list(filter(lambda x: is_ip_valid(x),list(matches)))

def add_to_muestra(tupla_args): #la tupla de be ser saneada antes de entrar a la función
	#("d1aklfianfn", "nombre", analdin, None, None, "architecture", analst, today)
	try:
		sqliteConnection = sqlite3.connect('db.sqlite3')
		cursor = sqliteConnection.cursor()
		print("Successfully Connected to SQLite")
		cursor.execute('insert into web_muestra values (?,?,?,?,?,?,?,?)',tupla_args)

		# count = cursor.execute(sqlite_insert_query)
		sqliteConnection.commit()
	except sqlite3.Error as error:
		print("Failed to insert data into sqlite table", error)
