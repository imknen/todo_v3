from .data_db_login import NAME, PASSWD, BASE
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import re

def createDB():
    print('Create DB:')
    try:
        con = psycopg2.connect(database='postgres',
                               port='5432',
                               host='localhost',
                               user=NAME,
                               password=PASSWD)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()

        cur.execute(f'CREATE DATABASE {BASE}')
        print(f'База данных {BASE} успешно создана\n')

    except psycopg2.ProgrammingError as e:
        print(f'Base {BASE} already exists\n')
    finally:
        cur.close()
        con.close()


class Connection:

    def __init__(self):
        try:
            self.conn = psycopg2.connect(database=BASE,
                                         port='5432',
                                         host='localhost',
                                         user=NAME,
                                         password=PASSWD)
            self.cursor = self.conn.cursor()

        except psycopg2.ProgrammingError as e:
            print("Connection error", error)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()


def getVersionDB():
    conn = Connection()
    cur = conn.cursor
    try:
        cur.execute('''
                    SELECT fversion FROM db_version
                    ORDER BY fdate DESC LIMIT 1
                    ''')
    except psycopg2.ProgrammingError as e:
        return ['0', '0']

    rows = cur.fetchall()

    return (rows[0][0].split('.'))


def getInfo():
    file_names = os.listdir('base/migrations')
    files_migragion = list(filter(lambda x: re.fullmatch(r'\w+.sql', x),
                           file_names))
    ret = {'up': [], 'down': []}
    for name in files_migragion:
        ret[name.split('_')[0]].append(name)

    ret['up'].sort()
    ret['down'].sort(reverse=True)
    ret['version'] = getVersionDB()

    return ret


def loadQuery(name: str):
    with open(f'base/migrations/{name}') as query:
        return query.read()


def print_version_DB(action='current'):
    print(f"{action} version DB {'.'.join(getVersionDB())}")


def Execute(file_query: str, action: str):
    conn = Connection()
    cur = conn.cursor
    cur.execute(loadQuery(file_query))
    conn.commit()
    print(f'\tmigration_file:\t{file_query}')
    print_version_DB(f'\t{action}')


def updateDB():

    print('Update DB:')
    print_version_DB()
    info = getInfo()

    last_update = f"up_{info['version'][0]}_{info['version'][1]}.sql"
    list_up_migrations = info['up']
    list_for_update = list(filter(lambda x: x > last_update,
                                  list_up_migrations))

    if not list_for_update:
        print('no updates found')
    else:
        for file_name in list_for_update:
            Execute(file_name, 'base update to')


def clearDB():
    print('Deleting DB:')
    print_version_DB()
    info = getInfo()
    list_down_migration = info['down']
    current_downgrade = f"down_{info['version'][1]}_{info['version'][0]}.sql"
    list_for_downgrade = list(filter(lambda x: x <= current_downgrade,
                                     list_down_migration))
    if not list_for_downgrade:
        print('database is already on the first change')
    else:
        for file_name in list_for_downgrade:
            Execute(file_name, 'base downgrade to')
