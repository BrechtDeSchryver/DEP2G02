from langdetect import detect
import json
from connectie import get_database

pg_engine = get_database()

# path_kmo_languages = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\kmo_langs.txt'

def get_kmos_met_website():
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE website is not NULL;')
    kmos = [kmo_id[0] for kmo_id in res]

    return kmos

def get_kmos_met_jaarrekening():
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE jaarrekening is not NULL;')
    kmos = [kmo_id[0] for kmo_id in res]

    return kmos

#Detecteert taal van elke website en jaarrekening en schrijft die weg naar een tekstbestand voor later analyse en te verwijderen indien nodig
def main(path_kmo_languages):

    kmos_website = get_kmos_met_website()
    kmos_jaarrekening = get_kmos_met_jaarrekening()

    kmoid_lang = {'website': {},'jaarrekening': {}}# {'jaarrekening': {'dutch': [kmo_ids], 'english': [kmo_ids]}, 'website': {...}}
    teller=0
    print(f'{len(kmos_website)+len(kmos_jaarrekening)} KMO\'s')

    #website kmos
    for kmo_id in kmos_website:
        print(f'Websites : {teller} : {round(teller/(len(kmos_website)+len(kmos_jaarrekening)),4)*100}% : KMO {kmo_id}')
        website = pg_engine.execute('SELECT website FROM raw_data WHERE \"ondernemingsNummer\" = %s',(kmo_id)).all()[0][0]
        if (not len(website) == 0) and (not website.isspace()):
            lang = detect(website)
            if lang == 'nl': lang = 'dutch'
            if lang == 'en': lang = 'english'
            if not lang in kmoid_lang['website'].keys():
                kmoid_lang['website'][lang] = [kmo_id]
            else:
                kmoid_lang['website'][lang].append(kmo_id)
            print(lang)

        teller+=1

    for kmo_id in kmos_jaarrekening:
        print(f'Jaarrekeningen : {teller} : {round(teller/(len(kmos_website)+len(kmos_jaarrekening)),4)*100}% : KMO {kmo_id}')
        jaarrekening = pg_engine.execute('SELECT jaarrekening FROM raw_data WHERE \"ondernemingsNummer\" = %s',(kmo_id)).all()[0][0]
        if (not len(jaarrekening) == 0) and (not jaarrekening.isspace()):
            lang = detect(jaarrekening)
            if lang == 'nl': lang = 'dutch'
            if lang == 'en': lang = 'english'
            if not lang in kmoid_lang['jaarrekening'].keys():
                kmoid_lang['jaarrekening'][lang] = [kmo_id]
            else:
                kmoid_lang['jaarrekening'][lang].append(kmo_id)
            print(lang)

        teller+=1

        


    with open(path_kmo_languages, 'w') as convert_file:
        convert_file.write(json.dumps(kmoid_lang))

    # Om terug te lezen
    # with open('convert.txt') as f:
    #     data = f.read()

    # js = json.loads(data)

# main(r'C:\Users\manuv\Documents\School\test\DEP2G02\data\kmo_langs.txt')