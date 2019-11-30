import dotenv
from pathlib import Path
import re
import ipaddress
import sqlite3
from datetime import date
from termcolor import colored


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
    matches = re.findall(pattern, data)
    return list(filter(lambda x: is_ip_valid(x), list(matches)))


def store_static_fields(tuple_args):
    try:
        # Connection
        sqliteConnection = sqlite3.connect('../db.sqlite3')
        cursor = sqliteConnection.cursor()

        # Execute query
        cursor.execute('INSERT INTO web_muestra VALUES (?, ?, ?, ?, ?, ?, ?, ?)', tuple_args)

        # Commit changes and close the connection
        sqliteConnection.commit()
        sqliteConnection.close()
    except sqlite3.Error as error:
        print(colored("[X] Failed to insert data into sqlite table: " + str(error).lower(), 'red'))
