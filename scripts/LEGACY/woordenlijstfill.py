import os

from sqlalchemy import null
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
def woordenlijst_infile(path):
    woordenlijsten={}
    categories = os.listdir(path)
    for category in categories:
        category_path = path + "/" + category
        woordenlijst={}
        terms = os.listdir(category_path)
        for term in terms:
            term_path = category_path + "/" + term
            termwords=Get_woorden(term_path)
            term=term.split(".")[0]
            woordenlijst[term]=termwords
        woordenlijsten[category]=woordenlijst
    return woordenlijsten
def woordenlijst_insql():
    #connectie databank
    woordenlijsten={}
    pg_conn = get_database()
    categories=get_durability_category(pg_conn)
    for category in categories:
        woordenlijst={}
        category=category[0]
        terms=get_durability_terms_fromcategory(category,pg_conn)
        for term in terms:
            term=term[0]
            keywords=get_durability_keyword_fromterm(term,pg_conn)
            lijst=[]
            for keyword in keywords:
                lijst.append(keyword[0])
            woordenlijst[term]=lijst
            woordenlijsten[category]=woordenlijst
    return woordenlijsten
def compare_woordenlijst(path):
    sql=woordenlijst_insql()
    new=woordenlijst_infile(path)
    verwijderd=[]
    toegevoegd=[]
    for category in sql:
        for term in sql[category]:
            for keyword in sql[category][term]:
                if keyword not in new[category][term]:
                    print("keyword " + keyword + " in term " + term + " in category " + category + " is niet meer in de nieuwe woordenlijst") 
                    #delete_durability_keyword_and_hits(keyword)
                    verwijderd.append(keyword)
    for category in new:
        for term in new[category]:
            for keyword in new[category][term]:
                if keyword not in sql[category][term]:
                    print("keyword " + keyword + " in term " + term + " in category " + category + " is nieuw in de nieuwe woordenlijst")
                    toegevoegd.append([term,keyword])
                    #insert_durability_keyword(term,keyword)
    return [verwijderd,toegevoegd]
def load_new_woordenlijst(path):
    changes=compare_woordenlijst(path)
    print(changes)
    for change in changes[0]:
        delete_durability_keyword_and_hits(change)
    for change in changes[1]:
        insert_durability_keyword(change[0],change[1])
def main():
    load_new_woordenlijst("C:/woorden")
if __name__ == "__main__":
    main()
    #energiebron, energie vermindering, energie reductie, energie-intensiteit, energiegebruik, energieverbruik, recyclage, recycleren, circulaire economie, hernieuwbare energie, refuse, reduce, resell, reuse,repurpose, repair, maintenance, remine, recover energy, herstel,  hergebruik, refurbish, remanufacture, afval, afvalproductie, verspilling, verantwoorde consumptie en productie, betaalbare en duurzame energie, materialenverbruik