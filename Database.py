import sqlite3
import os
from sqlalchemy import create_engine

def create_db_table(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS glucose_val(InternalTime TEXT, GlucoseVal INT, DisplayTime TEXT)")
    conn.commit()
    conn.close


def insert_to_database(data):
    db = input('Enter path to DB: ')
    if not os.path.isfile(db):
        create_db_table(db)

    engine = create_engine('sqlite:///%s' % db)
    data.to_sql('glucose_val', con=engine, if_exists='append')