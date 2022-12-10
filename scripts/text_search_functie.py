import os
from connectie import get_database
# Import ts_rank_full_text_search.py
# Import vertaal_keywords.py, detect_lang.py
# Import calculate_scores.py
# Import calculate_kmoscores.py
import vertaal_keywords
import detect_lang
import calculate_scores
import calculate_kmoscores
import ts_rank_full_text_search

PATH_KEYWORDS_ENG = r'C:\Users\manuv\Documents\School\test\DEP2G02\data\keywords_eng.txt'
PATH_KMO_LANGS = r'C:\Users\manuv\Documents\School\test\DEP2G02\data\kmo_langs.txt'

pg_engine = get_database()

def check_table_empty(tablename):
    res = pg_engine.execute(f'SELECT * from {tablename}').all()
    if len(res) == 0:
        return True
    return False

def empty_table(tablename):
    tables_can_be_deleted = ['score','subdomain_score']
    if tablename in tables_can_be_deleted:
        pg_engine.execute(f'DELETE FROM {tablename}')
    else:
        raise Exception(f'Only delete {tables_can_be_deleted}')

def fill_tables_with_score():
    # Executing scripts voor meertaligheid
    if not os.path.exists(PATH_KEYWORDS_ENG):
        try:
            print('Executing vertaal_keywords.py ......')
            vertaal_keywords.main(PATH_KEYWORDS_ENG)
        except:
            raise Exception('Vertaal_keywords failed')
    
    if not os.path.exists(PATH_KMO_LANGS):
        try:
            print('Executing detect_lang.py ......')
            detect_lang.main(PATH_KMO_LANGS)
        except:
            raise Exception('detect_lang failed')

    # Executing script to fill subdomain_score
    try:
        empty_table('subdomain_score')
        print('Executing ts_rank_full_text_search.py ......')
        ts_rank_full_text_search.main(PATH_KEYWORDS_ENG,PATH_KMO_LANGS)
    except:
        raise Exception('ts_rank_full_text failed')

    # Executing script to fill score
    try:
        empty_table('subdomain_score')
        print('Executing calculate_scores.py ......')
        calculate_scores.main()
    except:
        raise Exception('calculate_scores failed')

    # Executing script to fill kmo score column
    try:
        print('Executing calculate_kmoscores.py ......')
        calculate_kmoscores.main()
    except:
        raise Exception('calculate_kmoscores failed')

    print('Klaar')

# fill_tables_with_score()