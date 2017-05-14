import sqlite3


def create_db_table(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS glucose_val(InternalTime TEXT, GlucoseVal INT, DisplayTime TEXT)")
    conn.commit()
    conn.close
