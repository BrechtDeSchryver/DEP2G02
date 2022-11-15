from connectie import get_database
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
    if len(result_website) == 1:
        if len(result_duurzaamheidsrapport) == 1:
            score =  3
        else:
            score = 1
    else:
        if len(result_duurzaamheidsrapport) == 1:
            score = 2

    if connaanwezig==False:
        pg_conn.close()
    return score

    

get_score_for_word()