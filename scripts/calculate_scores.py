from connectie import get_database

pg_engine = get_database()

# Voer script alleen uit bij lege score tabel

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

# laatste ID van de tabel score
def get_laatste_id_score():
    res = pg_engine.execute('SELECT * FROM score ORDER BY "ID" desc fetch first 1 rows only').all()
    if len(res) == 0:
        return 0
    return res[0][0]

def get_domain_from_subdomain(subdomain,keywords):
    for domain in keywords.keys():
        if subdomain in keywords[domain].keys():
            return domain

def insert_kmo_into_score(id,domain_score,domain,kmo_id):
    args = (id,domain_score,domain,0,kmo_id)
    pg_engine.execute('INSERT INTO score VALUES (%s,%s,%s,%s,%s)',args)

def main():
    keywords = get_all_keywords_by_domains()
    id = get_laatste_id_score()+1
    res = pg_engine.execute('SELECT score,subdomain,\"ondernemingsNummer\" FROM subdomain_score ORDER BY \"ID\"').all()
    if len(res) == 0:
        print('subdomain_score table is empty')
    else:
        domain_score = 0
        vorig_domain = 'Environment'
        teller = 0
        for row in res:
            print(f'{round(teller/len(res),4)*100}%')
            sub_score, subdomain, kmo_id = float(row[0]),row[1],row[2]

            domain = get_domain_from_subdomain(subdomain,keywords)

            if not domain == vorig_domain:
                domain_score = domain_score/len(keywords[domain])# domain_score is de som van alle subdomain_scores en dan delen door het aantal subdomeinen van het domein. ~ Gemiddelde van de subdomeinscores
                insert_kmo_into_score(id,domain_score,vorig_domain,kmo_id)
                print(f'{kmo_id} : {vorig_domain} {domain_score} : ID {id}')
                id+=1
                domain_score = 0
            domain_score+=sub_score
            vorig_domain = domain
            
            teller+=1

# main()