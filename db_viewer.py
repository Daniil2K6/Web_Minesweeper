import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'db.sqlite3'

def print_table(table_name):
    con = sqlite3.connect(DB_PATH)
    cursor = con.execute(f'SELECT * FROM {table_name}')
    columns = [description[0] for description in cursor.description]
    print(f'Таблица: {table_name}')
    print('| ' + ' | '.join(columns) + ' |')
    print('|' + '---|'*len(columns))
    rows = cursor.fetchall()
    for row in rows:
        print('| ' + ' | '.join(str(x) for x in row) + ' |')
    con.close()

def print_all_tables():
    con = sqlite3.connect(DB_PATH)
    cursor = con.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print('Таблицы:', tables)
    for table in tables:
        print_table(table)
    con.close()

if __name__ == '__main__':
    print_all_tables()
