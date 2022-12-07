import json
import numpy as np

# path_kmos_nl_en = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\kmos_nl_en.txt'
# path_kmo_langs = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\data\kmo_langs.txt'

#prints het aantal kmos een website in een bepaalde taal heeft
def print_languages_of_kmos(kmo_langs):
    array = np.array(list(kmo_langs.values()))
    count_langs = {}

    for lang in array:
        if lang in count_langs:
            count_langs[lang] += 1
        else:
            count_langs[lang] = 1
        
    count_langs = dict(sorted(count_langs.items(), key=lambda item: item[1],reverse=True))
    for item in count_langs:
        print(item,count_langs[item])

def main(path_kmo_langs,path_kmos_nl_en):
    with open(path_kmo_langs) as f:
        data = f.read()

    kmo_langs = json.loads(data)

    print_languages_of_kmos(kmo_langs)

    #draait de kmo_langs dict omgekeerd voor makkelijker kmo_ids te krijgen per taal
    reversedDict = dict()
    for kmo_id in kmo_langs:
        val = kmo_langs[kmo_id]
        if val in reversedDict:
            reversedDict[val].append(kmo_id)
        else:
            reversedDict[val] = [kmo_id]
    
    #Schrijft nederlandse en engelse kmo_ids naar een textfile
    with open(path_kmos_nl_en, 'w') as convert_file:
        convert_file.write(json.dumps({'dutch': reversedDict['nl'], 'english': reversedDict['en']}))


# main()