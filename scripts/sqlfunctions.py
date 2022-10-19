from connectie import get_database

def insert_kmo(kmo,pg_conn=None):
    #kmo[0]=ondernemingsnummer
    #kmo[1]=naam
    #kmo[2]=adres
    #kmo[3]=email
    #kmo[4]=telefoon
    #kmo[5]=website
    #kmo[6]=nbbID
    #kmo[7]=nacebelCode
    ondernemingsnummer = kmo[0]
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    pg_conn.execute('INSERT INTO kmo VALUES (%s, %s, %s, %s, %s, %s,%s);', kmo)
    pg_conn.execute('INSERT INTO raw_data("ondernemingsNummer") VALUES (%s);', ondernemingsnummer)
    if connaanwezig==False:
        pg_conn.close()

def select_kmos(pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #select functie
    result = pg_conn.execute('SELECT * FROM kmo')
    if connaanwezig==False:
        pg_conn.close()
    return result.all()

def select_kmo(ondernemingsnummer,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #select functie
    result = pg_conn.execute('SELECT * FROM kmo WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    if connaanwezig==False:
        pg_conn.close()
    return result.first()

def select_raw_data(ondernemingsnummer,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #select functie
    result = pg_conn.execute('SELECT * FROM raw_data WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    if connaanwezig==False:
        pg_conn.close()
    return result.first()

def select_raw_datas(pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #select functie
    result = pg_conn.execute('SELECT * FROM raw_data')
    if connaanwezig==False:
        pg_conn.close()
    return result.all()

def insertRawPDF(ondernemingsnummer, pdftext,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;', (pdftext, ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()

def insertRawWebsite(ondernemingsnummer, websitetext,pg_conn=None):
    #connect met de databank   
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    pg_conn = get_database()
    #insert functie
    pg_conn.execute('UPDATE raw_data SET website=%s WHERE "ondernemingsNummer" = %s;', (websitetext, ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()

def insertRawDuurzaamheidsrapport(ondernemingsnummer, duurzaamheidsrapporttext,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;', (duurzaamheidsrapporttext, ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()
