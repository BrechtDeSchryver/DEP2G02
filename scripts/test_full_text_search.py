from datetime import datetime
from connectie import get_database

N_afstand = 10 # bij extra conditie afstand van keyword tot words

kmo_id_start = ''#Voor als je wilt beginnen vanaf een specifieke kmo als je dit niet nodig hebt zet op ''

#De variable laatste_id dat je ook kan aanpassen staat in de main functie. 

pg_engine = get_database()

def fill_kmo_durability_item(keywords,kmos,laatste_id_found_term):
    print(f'{len(kmos)} kmo\'s te overlopen met {len(keywords)} keywords')
    keywords_found = 0
    teller=1
    id_kmo_durability_table=laatste_id_found_term+1

    keywords_ids = get_keywords_ids()
    for kmo_id in kmos:
        start = datetime.now()
        print(f'KMO({kmo_id}) bezig : {round(teller/len(kmos),4)*100}% : {keywords_found} keywords found')

        # keywords = clean_up_keywords(keywords)
        print(keywords)

    #     for keyword in keywords:
    #         keyword = keyword.strip()
    #         extra_conditie = False
    #         words = get_words_keyword_condition(keyword)
    #         if not len(words) == 0:
    #             keyword = keyword[0:keyword.index('(')].strip()
    #             extra_conditie = True
    #         keyword_id = keywords_ids[keyword]
    #         keyword = keyword.replace(' ',' <1> ')
            
    #         if get_rank_word_in_document(kmo_id,'jaarrekening',keyword):
    #             if extra_conditie:
    #                 if is_keyword_close_to_words(kmo_id,'jaarrekening',keyword,words):
    #                     print(f'Keyword {keyword} bij {words} is in jaarrekening : ID_found_term {id_kmo_durability_table}')
    #                     context = get_context(kmo_id,keyword,"jaarrekening")
    #                     insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                     id_kmo_durability_table+=1
    #                     keywords_found += 1
    #                     continue
    #             else:
    #                 print(f'Keyword {keyword} is in jaarrekening : ID_found_term {id_kmo_durability_table}')
    #                 context = get_context(kmo_id,keyword,"jaarrekening")
    #                 insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                 id_kmo_durability_table+=1
    #                 keywords_found += 1
    #                 continue
    #         if get_rank_word_in_document(kmo_id,'website',keyword):
    #             if extra_conditie:
    #                 if is_keyword_close_to_words(kmo_id,'website',keyword,words):
    #                     print(f'Keyword {keyword} bij {words} is in website : ID_found_term {id_kmo_durability_table}')
    #                     context = get_context(kmo_id,keyword,"website")
    #                     insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                     id_kmo_durability_table+=1
    #                     keywords_found += 1
    #                     continue
    #             else:
    #                 print(f'Keyword {keyword} is in website : ID_found_term {id_kmo_durability_table}')
    #                 context = get_context(kmo_id,keyword,"website")
    #                 insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                 id_kmo_durability_table+=1
    #                 keywords_found += 1
    #                 continue
    #         if get_rank_word_in_document(kmo_id,'duurzaamheidsrapport',keyword):
    #             if extra_conditie:
    #                 if is_keyword_close_to_words(kmo_id,'duurzaamheidsrapport',keyword,words):
    #                     print(f'Keyword {keyword} bij {words} is in duurzaamheidsrapport : ID_found_term {id_kmo_durability_table}')
    #                     context = get_context(kmo_id,keyword,"duurzaamheidsrapport")
    #                     insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                     id_kmo_durability_table+=1
    #                     keywords_found += 1
    #                     continue
    #             else:
    #                 print(f'Keyword {keyword} is in duurzaamheidsrapport : ID_found_term {id_kmo_durability_table}')
    #                 context = get_context(kmo_id,keyword,"duurzaamheidsrapport")
    #                 insert_found_keyword(id_kmo_durability_table,kmo_id,keyword_id,context)
    #                 id_kmo_durability_table+=1
    #                 keywords_found += 1
    #                 continue

    #     end = datetime.now()
    #     print(f'{round(((len(kmos)-teller)*(end-start).total_seconds())/3600,2)} hours left')
    #     teller+=1

    # print('Klaar let\'sgo')
    # print(f'Keywords found={keywords_found} van de {len(kmos)*len(keywords)}')

def get_rank_word_in_document(kmo_id,type_docu,word):
    type_docu = 'ts_' + type_docu
    query = f'SELECT ts_rank({type_docu},queri) as rank FROM raw_data,to_tsquery(\'dutch\',%s) queri WHERE "ondernemingsNummer" = %s and queri @@ {type_docu};'
    args = (word,kmo_id)
    res = pg_engine.execute(query,args).all()
    if not len(res) == 0:
        return res[0][0]
    return 0

def get_rank_words_in_document(kmo_id,type_docu,keywords):
    pass

def is_keyword_close_to_words(kmo_id,type_docu,keyword,words):
    if len(words) == 0:
        return True
    type_docu = 'ts_' + type_docu
    query = get_query_keyword_close_to_words(keyword,words,type_docu)
    args = (kmo_id)
    print
    res = pg_engine.execute(query,args)
    return not len(res.all()) == 0

def get_query_keyword_close_to_words(keyword,words,type_docu):
    query = f'SELECT \"ondernemingsNummer\" FROM raw_data WHERE \"ondernemingsNummer\" = %s AND {type_docu} @@ to_tsquery(\'dutch\',\''
    for word in words:
        for i in range(1,N_afstand+1):
            query += f'{keyword} <{i}> {word} | {word} <{i}> {keyword} | '
    
    query = query[:-3]
    query += '\');'
    return query

def get_words_keyword_condition(keyword):
    words = []
    if '(' in keyword:
        first = keyword.index('(')+1
        last = keyword.index(')')
        words = keyword[first:last]
        words = words.replace('/',',').split(',')
        words = [word.strip() for word in words]
        words = [word.replace(' ',' <1> ') for word in words]

    return words

# keyword moet stam zijn van woord
#TODO: get de context
def get_context(kmo_id,keyword,type_docu):
    # tsvector = pg_engine.execute(f'SELECT ts_{type_docu} FROM raw_data WHERE \"ondernemingsNummer\" = %s;',(kmo_id)).all()[0][0].split(' ')
    # word_indexs = [item for item in tsvector if keyword in item][0].split(':')[1].split(',')
    # word_index = min([int(index) for index in word_indexs])#returned alleen de eerste index van het keyword. Verwijderd laatste '[0]' om alle indexes te krijgen

    # word_index = int(word_index)-1
    # document = pg_engine.execute(f'SELECT {type_docu} FROM raw_data WHERE \"ondernemingsNummer\" = %s;',(kmo_id)).all()[0][0].strip().split(" ")
    # document = [word for word in document if not word == '']
    return ''
    

def insert_found_keyword(id,ondernemingsNr,keyword_id,context):
    pg_engine.execute('INSERT INTO kmo_durability_item VALUES (%s,%s,%s,%s)',(id,ondernemingsNr,keyword_id,context))

def get_keywords_ids():
    res = pg_engine.execute('SELECT * FROM durability_keyword;').all()
    keywords_ids = {}
    for item in res:
        keyword = item[1].strip()
        if '(' in keyword:
            keyword = keyword[0:keyword.index('(')].strip()
        keywords_ids[keyword] = item[0]

    return keywords_ids

def get_laatste_id_kmo_durability_term():
    res = pg_engine.execute('SELECT * FROM kmo_durability_item ORDER BY "ID" desc fetch first 1 rows only').all()
    if not len(res) == 0:
        return res[0][0]
    return 0

def delete_keywords_found_kmo(kmo_id):
    pg_engine.execute('DELETE FROM kmo_durability_item WHERE "ondernemingsNummer" = %s',(kmo_id))


def get_kmos_met_data():
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE jaarrekening is not NULL OR website is not NULL or duurzaamheidsrapport is not NULL;')
    kmos = [kmo_id[0] for kmo_id in res]

    return kmos
        

def get_all_keywords():
    res = pg_engine.execute('SELECT * FROM durability_keyword')
    # 0: id
    # 1: durability_keyword.name
    # 2: durability_keyword.subdomain
    keywords = []
    for row in res.all():
        keyword = row[1]
        keywords.append(keyword)
    
    return keywords

#return dict van domain van subdomains van keywords
#example : {'Social' : {'subdomain' : [..],'subdomain2': [..]}}
def get_all_keywords_by_domains():
    dict_keywords = {}
    raw_keywords = pg_engine.execute('SELECT * FROM durability_keyword').all()
    for data in raw_keywords:
        subdomain = data[2][:(len(data[2]) if data[2].find('(')==-1 else data[2].find('('))].strip()
        keyword = data[1][:(len(data[1]) if data[1].find('(')==-1 else data[1].find('('))].strip()
        if subdomain in dict_keywords.keys():
            dict_keywords[subdomain].append(keyword)
        else:
            dict_keywords[subdomain] = [keyword]

    raw_domains = pg_engine.execute('SELECT * FROM durability_term').all()
    dict_domains = {}
    for data in raw_domains:
        subdomain = data[0][:(len(data[0]) if data[0].find('(')==-1 else data[0].find('('))].strip()
        domain = data[2].strip()
        if domain in dict_domains.keys():
            dict_domains[domain][subdomain] = dict_keywords[subdomain]
        else:
            dict_domains[domain] = {subdomain : dict_keywords[subdomain]}

    return dict_domains
        


#alleen voor testing gebruikt ipv main
def test():
    query = 'SELECT ts_rank(ts_jaarrekening,queri) as rank FROM raw_data,to_tsquery(\'dutch\',%s) queri WHERE "ondernemingsNummer" = %s and queri @@ ts_jaarrekening;'
    kmo_id = '0464184293'
    queri = ''
    keywords = get_all_keywords_by_domains()
    for domain in keywords.keys():
        for subdomain in keywords[domain].keys():
            words = keywords[domain][subdomain]
            iets = '|'.join(words).replace(' ',' <1> ')
            print(iets)
        
        args = (queri,kmo_id)
            

def main():
    kmos_met_data = get_kmos_met_data()
    if not kmo_id_start == '':
        kmos_met_data = kmos_met_data[kmos_met_data.index(kmo_id_start):]
        delete_keywords_found_kmo(kmo_id_start)
    keywords = get_all_keywords()

    laatste_id = 0#Voor in de kmo_durability_term table zijn primary key. Indien 0 wordt het zelf gezocht wat het laatste id was.

    if laatste_id == 0:
        laatste_id = get_laatste_id_kmo_durability_term()
    fill_kmo_durability_item(keywords,kmos_met_data,laatste_id)

test()