import sqlite3
import pandas as pd

from itertools import chain


def make_table(table_name, col_types, db_name=':memory:'):
    """
    Create a new table in a database using column names and types supplied.
    """
    columns = []
    for col_name, col_type in col_types:
        col_str = f'{col_name} {col_type}'
        columns.append(col_str)
    columns = ', '.join(columns)
    query = f'''create table {table_name} ({columns})'''

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with conn:
        c.execute(query)


def append_csv_to_table(table_name, csv_path, db_name=':memory:'):
    """
    Append the data from a csv file to a table in the database.
    """
    conn = sqlite3.connect(db_name)

    with conn:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)


def get_tables_list(db_name=':memory:'):
    """
    Return a list of all the tables in a database.
    """
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    with conn:
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        result = list(chain.from_iterable(c.fetchall()))
        return result