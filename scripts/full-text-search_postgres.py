from sqlalchemy import create_engine
from datetime import datetime

N_afstand = 10 # bij extra conditie afstand van keyword tot words

kmo_id_start = ''#Voor als je wilt beginnen vanaf een specifieke kmo als je dit niet nodig hebt zet op ''

pg_engine = create_engine('postgresql://pyuser:dikkeberta@vichogent.be:40035/dep')

def fill_kmo_durability_item(keywords,kmos):
    print(f'{len(kmos)} kmo\'s te overlopen met {len(keywords)} keywords')
    keywords_found = 0
    teller=1
    for kmo_id in kmos:
        start = datetime.now()
        print(f'KMO({kmo_id}) bezig : {round(teller/len(kmos),4)*100}% : {keywords_found} keywords found')

        for keyword in keywords:
            keyword = keyword.strip()
            extra_conditie = False
            words = get_words_keyword_condition(keyword)
            if not len(words) == 0:
                keyword = keyword[0:keyword.index('(')-1]
                extra_conditie = True
            keyword = keyword.replace(' ',' <1> ')
            
            if is_word_in_document(kmo_id,'jaarrekening',keyword):
                if extra_conditie:
                    if is_keyword_close_to_words(kmo_id,'jaarrekening',keyword,words):
                        print(f'Keyword {keyword} bij {words} is in jaarrekening van kmo {kmo_id}')
                        context = get_context(kmo_id,keyword,"jaarrekening")
                        insert_found_keyword(kmo_id,keyword,context)
                        keywords_found += 1
                        continue
                else:
                    print(f'Keyword {keyword} is in jaarrekening van kmo {kmo_id}')
                    context = get_context(kmo_id,keyword,"jaarrekening")
                    insert_found_keyword(kmo_id,keyword,context)
                    keywords_found += 1
                    continue
            if is_word_in_document(kmo_id,'website',keyword):
                if extra_conditie:
                    if is_keyword_close_to_words(kmo_id,'website',keyword,words):
                        print(f'Keyword {keyword} bij {words} is in website van kmo {kmo_id}')
                        context = get_context(kmo_id,keyword,"website")
                        insert_found_keyword(kmo_id,keyword,context)
                        keywords_found += 1
                        continue
                else:
                    print(f'Keyword {keyword} is in website van kmo {kmo_id}')
                    context = get_context(kmo_id,keyword,"website")
                    insert_found_keyword(kmo_id,keyword,context)
                    keywords_found += 1
                    continue
            if is_word_in_document(kmo_id,'duurzaamheidsrapport',keyword):
                if extra_conditie:
                    if is_keyword_close_to_words(kmo_id,'duurzaamheidsrapport',keyword,words):
                        print(f'Keyword {keyword} bij {words} is in duurzaamheidsrapport van kmo {kmo_id}')
                        context = get_context(kmo_id,keyword,"duurzaamheidsrapport")
                        insert_found_keyword(kmo_id,keyword,context)
                        keywords_found += 1
                        continue
                else:
                    print(f'Keyword {keyword} is in duurzaamheidsrapport van kmo {kmo_id}')
                    context = get_context(kmo_id,keyword,"duurzaamheidsrapport")
                    insert_found_keyword(kmo_id,keyword,context)
                    keywords_found += 1
                    continue

        end = datetime.now()
        print(f'{round(((len(kmos)-teller)*(end-start).total_seconds())/3600,2)} hours left')
        teller+=1

    print('Klaar let\'sgo')
    print(f'Keywords found={keywords_found} van de {len(kmos)*len(keywords)}')

def is_word_in_document(kmo_id,type_docu,word):
    type_docu = 'ts_' + type_docu
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE \"ondernemingsNummer\" = %s AND %s @@ to_tsquery(\'dutch\',%s);',(kmo_id,type_docu,word))
    if not len(res.all()) == 0:
        return True
    return False

def is_keyword_close_to_words(kmo_id,type_docu,keyword,words):
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
    return ""
    

def insert_found_keyword(ondernemingsNr,keyword,context):
    pg_engine.execute('INSERT INTO kmo_durability_item VALUES (%s,%s,%s)',(ondernemingsNr,keyword,context))


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


def main():
    kmos_met_data = get_kmos_met_data()
    if not kmo_id_start == '':
        kmos_met_data = kmos_met_data[kmos_met_data.index(kmo_id_start):]
    keywords = get_all_keywords()
    fill_kmo_durability_item(keywords,kmos_met_data)

main()