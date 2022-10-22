import os
from sqlfunctions import *
def Get_woorden(path):
    with open(path, 'r') as f:
        woorden = f.read().split(",")
    return woorden
def load_woordenlijst(path):
    #connectie databank
    pg_conn = get_database()
    #flush woordenlijst
    flush_woordenlijst(pg_conn)
    categories = os.listdir(path)
    for category in categories:
        insert_durability_category(category,pg_conn)
        category_path = path + "/" + category
        terms = os.listdir(category_path)
        for term in terms:
            term_path = category_path + "/" + term
            termwords=Get_woorden(term_path)
            term=term.split(".")[0]
            insert_durability_term(term,category,pg_conn)
            for termword in termwords:
                insert_durability_keyword(term,termword,pg_conn)
    pg_conn.close()
    return "succesvol woordenlijst gevuld"
def main():
    print(load_woordenlijst("C:\woorden"))
if __name__ == "__main__":
    main()