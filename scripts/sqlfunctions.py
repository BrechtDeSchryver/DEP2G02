from connectie import get_database


def insert_kmo(kmo, pg_conn=None):
    # kmo[0]=ondernemingsnummer
    # kmo[1]=naam
    # kmo[2]=adres
    # kmo[3]=email
    # kmo[4]=telefoon
    # kmo[5]=website
    # kmo[6]=nbbID
    # kmo[7]=nacebelCode
    ondernemingsnummer = kmo[0]
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO kmo VALUES (%s, %s, %s, %s, %s, %s,%s);', kmo)
    pg_conn.execute(
        'INSERT INTO raw_data("ondernemingsNummer") VALUES (%s);', ondernemingsnummer)
    if connaanwezig == False:
        pg_conn.close()


def select_kmos(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute('SELECT * FROM kmo')
    if connaanwezig == False:
        pg_conn.close()
    return result.all()


def select_ondernemingsnummers(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute('SELECT "ondernemingsNummer" FROM kmo')
    if connaanwezig == False:
        pg_conn.close()
    return result.all()


def select_naam_ondernemingsnummer_kmos(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute('SELECT "ondernemingsNummer", name FROM kmo')
    if connaanwezig == False:
        pg_conn.close()
    return result.all()


def select_kmo(ondernemingsnummer, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        'SELECT * FROM kmo WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    if connaanwezig == False:
        pg_conn.close()
    return result.first()


def select_postcodes(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        'SELECT "ondernemingsNummer", zipcode FROM adress')
    if connaanwezig == False:
        pg_conn.close()
    return result.fetchall()


def select_raw_data(ondernemingsnummer, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        'SELECT * FROM raw_data WHERE "ondernemingsNummer" = %s;', ondernemingsnummer)
    if connaanwezig == False:
        pg_conn.close()
    return result.first()


def select_raw_datas(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute('SELECT * FROM raw_data')
    if connaanwezig == False:
        pg_conn.close()
    return result.all()


def select_bedrijven_zonder_site(pg_conn=None):
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        '''select * from kmo right join raw_data r on kmo."ondernemingsNummer" = r."ondernemingsNummer" where r.website is null or r.website = '';''')
    if connaanwezig == False:
        pg_conn.close()
    return result.all()


def insertRawPDF(ondernemingsnummer, pdftext, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;',
                    (pdftext, ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()


def insert_capital_city(ondernemingsnummer, capital_city, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE adress SET capital_city=%s WHERE "ondernemingsNummer" = %s;',
                    (capital_city, ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()


def insertRawWebsite(ondernemingsnummer, websitetext, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    pg_conn = get_database()
    # insert functie
    pg_conn.execute('UPDATE raw_data SET website=%s WHERE "ondernemingsNummer" = %s;',
                    (websitetext, ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()

def get_stedelijkheidsklasse(postcode, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        'SELECT stedelijkheidsklasse FROM municipality WHERE zipcode = %s;', postcode)
    if connaanwezig == False:
        pg_conn.close()
    return result.first()[0]
def insertRawDuurzaamheidsrapport(ondernemingsnummer, duurzaamheidsrapporttext, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE raw_data SET jaarrekening=%s WHERE "ondernemingsNummer" = %s;',
                    (duurzaamheidsrapporttext, ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()


def inertNBBID(ondernemingsnummer, nbbID, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'UPDATE kmo SET "nbbID"=%s WHERE "ondernemingsNummer" = %s;', (nbbID, ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()


def getRawPDF(ondernemingsnummer, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    result = pg_conn.execute(
        'select jaarrekening from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()
    return result.first()


def getRawWebsite(ondernemingsnummer, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    result = pg_conn.execute(
        'select website from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()
    return result.first()


def getRawDuurzaamheidsrapport(ondernemingsnummer, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    result = pg_conn.execute(
        'select duurzaamheidsrapport from raw_data where "ondernemingsNummer"= %s;', (ondernemingsnummer))
    if connaanwezig == False:
        pg_conn.close()
    return result.first()


def get_datapunten_voor_model(pg_conn=None):
    pg_conn = get_database()
    result = pg_conn.execute("""
        select rd."ondernemingsNummer",f.turnover as omzet, f.beursgenoteerd, km."nacebelCode" as sector, e.total as total_employees,  
        CASE WHEN rd.website = '' or rd.website is null THEN 0 ELSE 1 END AS site_aanwezig, \
        case when rd.jaarrekening = '' or rd.jaarrekening is null then 0 else 1 end as pdf_aanwezig,m.stedelijkheidsklasse ,km.score as total_score \
        from raw_data rd  \
        join adress a on a."ondernemingsNummer"=rd."ondernemingsNummer" \
        join municipality m ON m.zipcode = a.zipcode \
        join finance f on rd."ondernemingsNummer"=f."ondernemingsNummer" \
        join employees e on f."ondernemingsNummer"=e."ondernemingsNummer" \
        join kmo km on km."ondernemingsNummer" = e."ondernemingsNummer"; \
                             """).fetchall()
    pg_conn.close()
    return result
    
# returnt 0 als het niet voorkomt, 1 als het op website voorkomt, 2 als het op duurzaamheidsrapport voorkomt en 3 als het op beide voorkomt
def get_score_for_word(ondernemingsnummer, word, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # search functie
    result_website = pg_conn.execute(
        'select ondernemingsnummer from raw_data where "ondernemingsNummer"= %s and "ts_website" @@ to_tsquery("dutch",%s);', (ondernemingsnummer, word)).first()
    result_duurzaamheidsrapport = pg_conn.execute(
        'select ondernemingsnummer from raw_data where "ondernemingsNummer"= %s and "ts_duurzaamheidsrapport" @@ to_tsquery("dutch",%s);', (ondernemingsnummer, word)).first()

    score = 0
    if len(result_website) > 0:
        if len(result_duurzaamheidsrapport) > 0:
            score = 3
        else:
            score = 1
    else:
        if len(result_duurzaamheidsrapport) > 0:
            score = 2

    if connaanwezig == False:
        pg_conn.close()
    return score


def insert_kmo_durabilityitem(ondernemingsnummer, keyword, context):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO kmo_durability_item(ondernemingsnummer,durability_keyword,context) VALUES (%s,%s,%s);',
                    (ondernemingsnummer, keyword, context))
    if connaanwezig == False:
        pg_conn.close()


def insert_municipality(postcode, gemeente, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'INSERT INTO municipality(zipcode,name) VALUES (%s,%s);', (postcode, gemeente))
    if connaanwezig == False:
        pg_conn.close()


def insert_adress(ondernemingsnummer, straat, zipcode, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO adress VALUES (%s,%s,%s);',
                    (ondernemingsnummer, straat, zipcode))
    if connaanwezig == False:
        pg_conn.close()


def insert_personeel(ondernemingsnummer, personeel, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO employees VALUES (%s,%s);',
                    (ondernemingsnummer, personeel))
    if connaanwezig == False:
        pg_conn.close()


def insert_sector(naam, nacebel, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO sector VALUES (%s,%s);', (naam, nacebel))
    if connaanwezig == False:
        pg_conn.close()


def insert_stedelijkheidsklasse(stedelijkheidsklasse, zipcode, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE municipality set stedelijkheidsklasse=%s WHERE zipcode = %s;',
                    (stedelijkheidsklasse, zipcode))
    if connaanwezig == False:
        pg_conn.close()


def insert_kmo_sector(i, ondernemingsnummer, sector, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO kmo_sector VALUES (%s,%s,%s);',
                    (i, ondernemingsnummer, sector))
    if connaanwezig == False:
        pg_conn.close()


def insert_website_kmo(odn, website, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'UPDATE kmo set website=%s where "ondernemingsNummer"=%s;', (website, odn))
    if connaanwezig == False:
        pg_conn.close()


def insert_beursgenoteerd(odn, beursgenoteerd, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO finance values (%s,0,0,0,%s)',
                    (odn, beursgenoteerd))
    if connaanwezig == False:
        pg_conn.close()
# script woordenlijst aanmaken
# select statements


def get_durability_category(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    results = pg_conn.execute('select name from durability_category;')
    if connaanwezig == False:
        pg_conn.close()
    return results.all()


def get_durability_terms_fromcategory(category, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    results = pg_conn.execute(
        'select name from durability_term where durability_category=%s;', (category))
    if connaanwezig == False:
        pg_conn.close()
    return results.all()


def get_durability_keyword_fromterm(term, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    result = pg_conn.execute(
        'select name from durability_keyword where durability_term=%s;', (term))
    if connaanwezig == False:
        pg_conn.close()
    return result.all()
# insert statements


def insert_durability_category(name, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('INSERT INTO durability_category VALUES (%s);', (name))
    if connaanwezig == False:
        pg_conn.close()


def insert_durability_term(name, category, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'INSERT INTO durability_term(durability_category,description,name) VALUES (%s,\'?\',%s);', (category, name))
    if connaanwezig == False:
        pg_conn.close()


def insert_durability_keyword(term, name, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'INSERT INTO durability_keyword(durability_term,name) VALUES (%s,%s);', (term, name))
    if connaanwezig == False:
        pg_conn.close()
# detele statements


def delete_durability_keyword_and_hits(name, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # delete functie
    pg_conn.execute(
        'DELETE FROM kmo_durability_item Where kmo_durability_item."ID"=(SELECT "ID" from durability_keyword WHERE name=%s)', (name))
    pg_conn.execute('DELETE FROM durability_keyword WHERE name=%s;', (name))
    if connaanwezig == False:
        pg_conn.close()
# flush statement


def flush_woordenlijst(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute(
        'TRUNCATE population_score,score,durability_category, durability_term, durability_keyword, kmo_durability_item;')
    if connaanwezig == False:
        pg_conn.close()
# end


def insert_balanstotaal(odn, balanstotaal, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE finance set total_assets=%s where "ondernemingsNummer"=%s;',
                    (balanstotaal, odn))
    if connaanwezig == False:
        pg_conn.close()


def insert_omzet(odn, omzet, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE finance set turnover=%s where "ondernemingsNummer"=%s;',
                    (omzet, odn))
    if connaanwezig == False:
        pg_conn.close()


def insert_bevolkingsdichtheid(name, bev, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE municipality set "bevolkingsdichtheidPermm2"=%s where "name"=%s;',
                    (bev, name))
    if connaanwezig == False:
        pg_conn.close()


def select_passwordhashes(pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # select functie
    results = pg_conn.execute('select "passwordHash" from credentials;')
    if connaanwezig == False:
        pg_conn.close()
    return results.all()


def insert_lat_long(postcode, lat, long, pg_conn=None):
    # connect met de databank
    if pg_conn is None:
        pg_conn = get_database()
        connaanwezig = False
    else:
        connaanwezig = True
    # insert functie
    pg_conn.execute('UPDATE municipality set "lat"=%s, "long"=%s where "zipcode"=%s;',
                    (lat, long, postcode))
    if connaanwezig == False:
        pg_conn.close()
