from sqlalchemy import create_engine
from connectie import get_database

def insert_kmo(kmo):
    #connect met de databank
    ondernemingsnummer = kmo[0]
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #insert functie
    pg_conn.execute('INSERT INTO kmo VALUES (%s, %s, %s, %s, %s, %s);', kmo)
    pg_conn.execute('INSERT INTO raw_data("ondernemingsNummer") VALUES (%s);', ondernemingsnummer)
    pg_conn.close()

def select_kmos():
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #select functie
    result = pg_conn.execute('SELECT * FROM kmo')
    pg_conn.close()
    return result.all()

def select_kmo(ondernemingsnummer):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #select functie
    result = pg_conn.execute('SELECT * FROM kmo WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    pg_conn.close()
    return result.first()

def select_raw_data(ondernemingsnummer):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #select functie
    result = pg_conn.execute('SELECT * FROM raw_data WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    pg_conn.close()
    return result.first()

def select_raw_datas():
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #select functie
    result = pg_conn.execute('SELECT * FROM raw_data')
    pg_conn.close()
    return result.all()

def insertRawPDF(ondernemingsnummer, pdftext):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;', (pdftext, ondernemingsnummer))
    pg_conn.close()
def insertRawWebsite(ondernemingsnummer, websitetext):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #insert functie
    pg_conn.execute('UPDATE raw_data SET website=%s WHERE "ondernemingsNummer" = %s;', (websitetext, ondernemingsnummer))
    pg_conn.close()

def insertRawDuurzaamheidsrapport(ondernemingsnummer, duurzaamheidsrapporttext):
    #connect met de databank
    pg_engine = get_database()
    pg_conn = pg_engine.connect()
    #insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;', (duurzaamheidsrapporttext, ondernemingsnummer))
    pg_conn.close()