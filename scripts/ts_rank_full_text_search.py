from datetime import datetime
from connectie import get_database
import json

# VOOR UITVOER VAN SCRIPT MOETEN BEIDE PADEN HIERONDER BESCHREVEN BESTAAN
# ANDERS VOER VOLGENDE SCRIPT IN DEZE VOLGORDE UIT: vertaal_keywords.py -> detect_lang.py

#tekst bestand met dictionary van keywords vertaalt naar engels
# path_txt_keywords_eng = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\keywords_eng.txt'# vertaalde keywords van nederlands naar engels -> Eerst vertaal_keywords.py uitvoeren
# path_kmos_nl_en = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\kmos_lang.txt'# Alle kmo_ids in het nederlands en engels -> Voer detect_lang.py uit
N_afstand = 10
DOCS = ['ts_website','ts_jaarrekening']
LANGUAGES = ['dutch','english']

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

# Geeft alle kmo_ids in een lijst terug die een jaarrekening of website of duurzaamheidsrapport hebben
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

#Returnt true als kmo alleen een website of alleen een jaarrekening heeft
def kmo_is_lonely(kmo_id,type_docu,lang,kmos_met_data):
    type_docu = type_docu.replace('ts_','').replace('_eng','')
    if type_docu == 'website':
        if kmo_id in kmos_met_data['jaarrekening']['dutch']:
            return False
        elif kmo_id in kmos_met_data['jaarrekening']['english']:
            return False
    elif type_docu == 'jaarrekening':
        if kmo_id in kmos_met_data['website']['dutch']:
            return False
        elif kmo_id in kmos_met_data['website']['english']:
            return False

    return True

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
    score*=1000# voor mooiheid
    pg_engine.execute('INSERT INTO subdomain_score VALUES(%s,%s,%s,%s)',(id,score,subdomain,kmo_id))

def main(path_txt_keywords_eng,path_kmos_nl_en):
    #nederlanse keywords in dict vorm met subdomain en domain
    keywords = get_all_keywords_by_domains()
    
    #engelse keywords (worden opgeslagen in tekstbestand voor performantie anders altijd 30+ min wachten voor vertaling)
    with open(path_txt_keywords_eng,'r') as f:
        data = f.read()
    keywords_eng = json.loads(data)

    #Neem enkel de KMO's die een nederlandse of engelse website hebben vanuit tekstbestand
    with open(path_kmos_nl_en) as f:
        data = f.read()
    kmos_met_data = json.loads(data)
    count_kmo_ids = len(kmos_met_data['jaarrekening']['english'])+len(kmos_met_data['website']['english'])+len(kmos_met_data['jaarrekening']['dutch'])+len(kmos_met_data['website']['dutch'])
    teller=0
    id = get_laatste_id_subdomain_score()+1# ID van de tabel subdomain_score
    som_score_kmos = {}
    print(f'START ID {id}')
    print(f"{count_kmo_ids} KMO\'s te gaan")
    
    for type_docu in DOCS:
        for lang in LANGUAGES:
            if lang == 'english':# In het engels andere ts_vector document in databank gebruiken en engelse keywords gebruiken
                type_docu+='_eng'
            print(f'START {lang} : {type_docu}')
            #Loop over elke kmo van specifieke language en specifieke document(website,jaarrekening) en dan over elke subdomein en bepaal subdomainscore.
            for kmo_id in kmos_met_data[type_docu.replace('ts_','').replace('_eng','')][lang]:
                start = datetime.now()
                lonely_kmo = kmo_is_lonely(kmo_id,type_docu,lang,kmos_met_data)
                print(f'KMO({kmo_id}) bezig : {round(teller/count_kmo_ids,4)*100}%')
                for domain in keywords.keys():
                    for subdomain in keywords[domain].keys():
                        #subdomain score is de optelling van de scores van de 2 documenten
                        score = 0
                        words = keywords_eng[domain][subdomain] if lang == 'english' else keywords[domain][subdomain]
                        query = f'SELECT ts_rank({type_docu},queri) as rank FROM raw_data,to_tsquery(%s,%s) queri WHERE "ondernemingsNummer" = %s and queri @@ {type_docu};'
                        words_query = get_query_keywords(words,kmo_id,type_docu)
                        args = (lang,words_query,kmo_id)
                        res=pg_engine.execute(query,args).all()
                        if len(res) > 0:
                            score = float(res[0][0])

                        
                        trash = kmo_id+subdomain
                        if trash in som_score_kmos.keys() or lonely_kmo:
                            if lonely_kmo:
                                insert_subdomain_score(kmo_id,score,subdomain,id)
                            else:
                                insert_subdomain_score(kmo_id,score+som_score_kmos[trash],subdomain,id)
                            if not score == 0: print(f'{subdomain} : {score} : ID {id}')
                        else:
                            som_score_kmos[trash] = score 
                        id+=1
                teller+=1
                end = datetime.now()
                print(f'{round(((count_kmo_ids-teller)*(end-start).total_seconds())/3600,2)} hours left')
    
    print('Klaar let\'s go')

# main(r'C:\Users\manuv\Documents\School\test\DEP2G02\data\keywords_eng.txt',r'C:\Users\manuv\Documents\School\test\DEP2G02\data\kmo_langs.txt')