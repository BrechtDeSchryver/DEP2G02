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
def inertNBBID(ondernemingsnummer, nbbID,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    pg_conn.execute('UPDATE kmo SET "nbbID"=%s WHERE "ondernemingsNummer" = %s;', (nbbID, ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()
def getRawPDF(ondernemingsnummer,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    result=pg_conn.execute('select jaarrekening from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()
    return result.first()
def getRawWebsite(ondernemingsnummer,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    result=pg_conn.execute('select website from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()
    return result.first()
def getRawDuurzaamheidsrapport(ondernemingsnummer,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #insert functie
    result=pg_conn.execute('select duurzaamheidsrapport from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig==False:
        pg_conn.close()
    return result.first()
#returnt 0 als het niet voorkomt, 1 als het op website voorkomt, 2 als het op duurzaamheidsrapport voorkomt en 3 als het op beide voorkomt
def get_score_for_word(ondernemingsnummer,word,pg_conn=None):
    #connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig=False
    else:
        connaanwezig=True
    #search functie
    result_website=pg_conn.execute('select ondernemingsnummer from raw_data where "ondernemingsNummer"= %s and "ts_website" @@ to_tsquery("dutch",%s);', (ondernemingsnummer,word)).first()
    result_duurzaamheidsrapport=pg_conn.execute('select ondernemingsnummer from raw_data where "ondernemingsNummer"= %s and "ts_duurzaamheidsrapport" @@ to_tsquery("dutch",%s);', (ondernemingsnummer,word)).first()
    
    score = 0
    if len(result_website) > 0:
        if len(result_duurzaamheidsrapport) > 0:
            score =  3
        else:
            score = 1
    else:
        if len(result_duurzaamheidsrapport) > 0:
            score = 2

    if connaanwezig==False:
        pg_conn.close()
    return score
