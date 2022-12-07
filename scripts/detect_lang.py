from langdetect import detect
from connectie import get_database
import json

start_from_specific_id = 0
pg_engine = get_database()

# path_kmo_languages = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\kmo_langs.txt'

def get_kmos_met_data():
    res = pg_engine.execute('SELECT \"ondernemingsNummer\" FROM raw_data WHERE website is not NULL;')
    kmos = [kmo_id[0] for kmo_id in res]

    return kmos

#Detecteert taal van elke website en schrijft die weg naar een tekstbestand voor later analyse en te verwijderen indien nodig
def main(path_kmo_languages):

    kmos = get_kmos_met_data()

    kmoid_lang = {}
    teller=0
    print(f'{len(kmos)} KMO\'s')
    for kmo_id in kmos[start_from_specific_id:]:
        print(f'{teller} : {round(teller/len(kmos),4)*100}% : KMO {kmo_id}')
        document = pg_engine.execute('SELECT website FROM raw_data WHERE \"ondernemingsNummer\" = %s',(kmo_id)).all()[0][0]
        if (not len(document) == 0) and (not document.isspace()):
            lang = detect(document)
            kmoid_lang[kmo_id] = lang
            print(lang)

        
        teller+=1

        


    with open(path_kmo_languages, 'w') as convert_file:
        convert_file.write(json.dumps(kmoid_lang))

    # Om terug te lezen
    # with open('convert.txt') as f:
    #     data = f.read()

    # js = json.loads(data)

# main()