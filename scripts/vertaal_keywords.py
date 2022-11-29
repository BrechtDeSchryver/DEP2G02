from connectie import get_database
import translators as ts
import json

pg_engine = get_database()


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

def vertaal_eng(keywords):
    keywords_eng = {}
    for domain in keywords.keys():
        res_dom = ts.google(domain, from_language='nl', to_language='en').lower()
        keywords_eng[res_dom] = {}
        for subdomain in keywords[domain].keys():
            res_sub = ts.google(subdomain, from_language='nl', to_language='en').lower()
            keywords_eng[res_dom][res_sub] = []
            words = []
            for word in keywords[domain][subdomain]:
                res = ts.google(word, from_language='nl', to_language='en').lower()
                if '-' in res: res=res.replace(' -','-')
                words.append(res)
            keywords_eng[res_dom][res_sub] = words

    return keywords_eng

keywords = get_all_keywords_by_domains()            
res = vertaal_eng(keywords)

with open('../data/keywords_eng.txt', 'w') as convert_file:
    convert_file.write(json.dumps(res))

# Om terug te lezen
# with open('convert.txt') as f:
#     data = f.read()

# js = json.loads(data)

print('Klaar let\'s go')



