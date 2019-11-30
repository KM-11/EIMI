import dotenv
from pathlib import Path
import re
import ipaddress
import sqlite3
from datetime import date
from termcolor import colored
import json


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


def jaccard_index(a, b):
    if a != None and b != None:

        return float(len(set(a).intersection(b))) / len(set(a).union(b)) * 100
    else:
        return 0


def get_num_func_cc(func_dict_cc):
    func_cc_count = {}
    if func_dict_cc is not None:
        for i in func_dict_cc:
            try:
                func_cc_count[func_dict_cc[i]] += 1
            except:
                func_cc_count[func_dict_cc[i]] = 1
        return func_cc_count
    return None


def structural_similarity(a, b):
    sample_a = get_num_func_cc(a)
    sample_b = get_num_func_cc(b)

    distance = []
    if sample_a is not None and sample_b is not None:
        for i in sample_a:
            if i in sample_b:
                distance.append(min(sample_a[i], sample_b[i]) / max(sample_a[i], sample_b[i]))

        for i in sample_b:
            if i not in sample_a:
                distance.append(0)

        return (functools.reduce(lambda a, b: a + b, distance) / len(distance)) * 100
    return 0


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


def get_data_bbdd(field, hash, table, mode):
    try:
        # Connection
        sqliteConnection = sqlite3.connect('../db.sqlite3')
        cursor = sqliteConnection.cursor()

        result = []

        # Execute query
        cursor.execute('SELECT ' + field + ' FROM ' + table + ' WHERE hash = "' + hash + '";')
        print('SELECT ' + field + ' FROM ' + table + ' WHERE hash = "' + hash + '";')

        # Parse
        sample_data = cursor.fetchall()

        for i in sample_data:
            a = json.loads(i[0])
            data = dict()
            data['name'] = a['hash']
            data['opcodes_func'] = a['static_anal']['opcodes_func']
            result.append(data)

        # Commit changes and close the connection
        sqliteConnection.commit()
        sqliteConnection.close()
        print(result)
        return result
    except sqlite3.Error as error:
        print(colored("[X] Failed to insert data into sqlite table: " + str(error).lower(), 'red'))

# get_data_bbdd('static_anal', '47e8f92ae8f428300b630ed62599203a', 'web_muestra', 'n_grams')
