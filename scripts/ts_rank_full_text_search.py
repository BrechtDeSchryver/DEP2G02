from datetime import datetime
from connectie import get_database

N_afstand = 10
DOCS = ['ts_jaarrekening','ts_website']
LANGUAGES = ['dutch','english']
kmo_id_start = ''#Voor als je wilt beginnen vanaf een specifieke kmo als je dit niet nodig hebt zet op ''

pg_engine = get_database()

#hulpfunctie wordt niet gebruikt in de mainfunctie
def get_rank_word_in_document(kmo_id,type_docu,word):
    type_docu = 'ts_' + type_docu
    query = f'SELECT ts_rank({type_docu},queri) as rank FROM raw_data,to_tsquery(\'dutch\',%s) queri WHERE "ondernemingsNummer" = %s and queri @@ {type_docu};'
    args = (word,kmo_id)
    res = pg_engine.execute(query,args).all()
    if not len(res) == 0:
        return res[0][0]
    return 0

def get_kmos_met_data():
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE jaarrekening is not NULL OR website is not NULL or duurzaamheidsrapport is not NULL;')
    kmos = [kmo_id[0] for kmo_id in res]

    return kmos

#hulpfunctie dat bepaald of keyword dicht bij de words liggen per kmo. De threshold voor als de dicht liggen wordt bepaald door N_afstand
def is_keyword_close_to_words(keyword,words,type_docu,kmo_id):
    query = f'SELECT \"ondernemingsNummer\" FROM raw_data WHERE \"ondernemingsNummer\" = %s AND {type_docu} @@ to_tsquery(\'dutch\',\''
    for word in words:
        for i in range(1,N_afstand+1):
            # keyword <1> word | word <1> keyword | keyword <2> word | ...
            query += f'{keyword} <{i}> {word} | {word} <{i}> {keyword} | '

    query = query[:-3]
    query += '\');'
    res = pg_engine.execute(query,(kmo_id)).all()
    return False if len(res)==0 else True

#geeft query terug met alle keywords om ze te gaan zoeken en checkt of keyword dicht bij andere woorden zit indien er ()haakjes inzitten
def get_query_keywords(keywords,kmo_id,type_docu):
    keywords_to_delete = []
    for i in range(len(keywords)):
        keyword = keywords[i]
        #Als extra conditie dan is er een ( in keyword
        if '(' in keyword:
            words_str = keyword[keyword.index('('):keyword.index(')')]
            words = words_str.replace('(','').replace(')','').replace('/',',').split(',')
            words = [word.strip().replace(' ',' <1> ') for word in words]
            if is_keyword_close_to_words(keywords[i][0:keyword.index('(')].strip().replace(' ',' <1> '),words,type_docu,kmo_id):
                keywords[i] = keywords[i][0:keyword.index('(')].strip() 
            else: 
                keywords_to_delete.append(keyword)

    [keywords.remove(keyword) for keyword in keywords_to_delete]
    words = [keyword.replace(' ',' <1> ') for keyword in keywords]
    return ' | '.join(words)# neemt elk woord per subdomain in 1 query en neemt het gemiddelde van hun scores per subdomain
    


#return dict van domain van subdomains van keywords
#example : {'Social' : {'subdomain' : [keyword1,keyword2],'subdomain2': [...]}, 'Goverance' : {...}, 'Environment' : {...}}
def get_all_keywords_by_domains():
    dict_keywords = {}
    raw_keywords = pg_engine.execute('SELECT * FROM durability_keyword').all()
    for data in raw_keywords:
        subdomain = data[2].strip()
        keyword = data[1].strip()
        if subdomain in dict_keywords.keys():
            dict_keywords[subdomain].append(keyword)
        else:
            dict_keywords[subdomain] = [keyword]

    raw_domains = pg_engine.execute('SELECT * FROM durability_term').all()
    dict_domains = {}
    for data in raw_domains:
        subdomain = data[0].strip()
        domain = data[2].strip()
        if not domain=='testcat':# test waarde in db
            if (domain in dict_domains.keys()):
                dict_domains[domain][subdomain] = dict_keywords[subdomain]
            else:
                dict_domains[domain] = {subdomain : dict_keywords[subdomain]}

    return dict_domains

#Laatste ID van tabel subdomain_score
def get_laatste_id_subdomain_score():
    res = pg_engine.execute('SELECT * FROM subdomain_score ORDER BY "ID" desc fetch first 1 rows only').all()
    if len(res) == 0:
        return 0
    return res[0][0]

def insert_subdomain_score(kmo_id,score,subdomain,id=None):
    #   score table
    # ID = eigen ID geen relatie
    # score = double score
    # subdomain
    # ondernemingsNummer
    if not id:
        id = get_laatste_id_subdomain_score()
        id+=1
    pg_engine.execute('INSERT INTO subdomain_score VALUES(%s,%s,%s,%s)',(id,score,subdomain,kmo_id))
          
def delete_scores_kmo_id_start():
    pg_engine.execute('DELETE FROM subdomain_score WHERE \"ondernemingsNummer\" = %s',(kmo_id_start))

def main():
    #Neem enkel de KMO's die een website of jaarrekening of duurzaamheidsrapport hebben en filter ze met de globale variable kmo_id_start om niet altijd opnieuw te beginnen
    kmos_met_data = get_kmos_met_data()
    if not kmo_id_start == '':
        kmos_met_data = kmos_met_data[kmos_met_data.index(kmo_id_start):]

    #delete kolommen in subdomain_score van kmo_id_start zodat geen dubbele kolommen
    delete_scores_kmo_id_start()
    
    teller=0
    id = get_laatste_id_subdomain_score()+1# ID van de tabel subdomain_score
    print(f'START ID {id}')
    print(f'{len(kmos_met_data)} KMO\'s te gaan')
    #Loop over elke kmo en dan over elke subdomein en bepaal subdomainscore.
    for kmo_id in kmos_met_data:
        start = datetime.now()
        print(f'KMO({kmo_id}) bezig : {round(teller/len(kmos_met_data),4)*100}%')
        keywords = get_all_keywords_by_domains()
        for domain in keywords.keys():
            for subdomain in keywords[domain].keys():
                #subdomain score is de optelling van de scores van de 3 documenten
                score = 0
                for type_docu in DOCS:
                    score_lang = 0
                    for lang in LANGUAGES: # berekent score voor elke taal in LANGUAGES en neemt het hoogste
                        query = f'SELECT ts_rank({type_docu},queri) as rank FROM raw_data,to_tsquery(%s,%s) queri WHERE "ondernemingsNummer" = %s and queri @@ {type_docu};'
                        words = get_query_keywords(keywords[domain][subdomain],kmo_id,type_docu)
                        args = (lang,words,kmo_id)
                        res=pg_engine.execute(query,args).all()
                        if not len(res) == 0:
                            if score_lang < float(res[0][0]):
                                if not score_lang == 0: print(f'Tis int engels {kmo_id}')
                                score_lang = float(res[0][0])
                    score += score_lang
                print(f'{subdomain} : {score} : ID {id}') if not score == 0 else None
                insert_subdomain_score(kmo_id,score,subdomain,id)
                id+=1

        end = datetime.now()
        print(f'{round(((len(kmos_met_data)-teller)*(end-start).total_seconds())/3600,2)} hours left')
        teller+=1
    
    print('Klaar let\'s go')

main()