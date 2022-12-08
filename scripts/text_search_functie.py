import os
import simplepush
# Import ts_rank_full_text_search.py
# Import vertaal_keywords.py, detect_lang.py , get_nl_en_kmo_ids.py
# Import calculate_scores.py
# Import calculate_kmoscores.py
import vertaal_keywords
import detect_lang
import get_nl_eng_kmo_ids
import calculate_scores
import calculate_kmoscores
import ts_rank_full_text_search

PATH_KEYWORDS_ENG = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\scripts\data\keywords_eng.txt'
PATH_KMO_LANGS = r'C:\Users\manuv\Documents\School\DEP2\OudProjectTeam\DEP2G02\scripts\data\kmo_langs.txt'

def fill_tables_with_score():
    # Executing scripts voor meertaligheid
    if not os.path.exists(PATH_KEYWORDS_ENG):
        try:
            print('Executing vertaal_keywords.py ......')
            vertaal_keywords.main(PATH_KEYWORDS_ENG)
        except:
            pass
    
    if not os.path.exists(PATH_KMO_LANGS):
        try:
            print('Executing detect_lang.py ......')
            detect_lang.main(PATH_KMO_LANGS)
        except:
            pass

    # Executing script to fill subdomain_score
    try:
        print('Executing ts_rank_full_text_search.py ......')
        ts_rank_full_text_search.main(PATH_KEYWORDS_ENG,PATH_KMO_LANGS)
    except:
        pass

    # Executing script to fill score
    try:
        print('Executing calculate_scores.py ......')
        calculate_scores.main()
    except:
        pass

    # Executing script to fill kmo score column
    try:
        print('Executing calculate_kmoscores.py ......')
        calculate_kmoscores.main()
    except:
        pass

# fill_tables_with_score()