from sqlalchemy import create_engine
from connectie import get_database

def insert_kmo(kmo):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #insert functie
    pg_conn.execute('INSERT INTO kmo VALUES (%s, %s, %s, %s, %s, %s);', kmo)
    pg_conn.close()
def select_kmos():
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #select functie
    result = pg_conn.execute('SELECT * FROM kmo')
    pg_conn.close()
    return result.all()
