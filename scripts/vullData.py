import csv
import sys
from nbb import get_id_onderneming
from sqlfunctions import insert_municipality,insert_stedelijkheidsklasse,insert_adress,insert_personeel,insert_sector
from connectie import get_database
import time


def insert_csvData():
    csv_data = csv.reader(open('woorden/kmo.csv'))
    header = next(csv_data)
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    for row in csv_data:
        # get the name field
        name = row[1]
        gemeente = row[2]
        nacebel = row[3]
        personeel = row[4]
        winst = row[5]
        if winst == 'n.b.':
            winst = 0
        omzet = row[6]
        btw = row[7].replace(' ', '')
        postcode = row[8]
        straat = row[9]
        telefoon = row[10]
        website = row[11]
        email = row[12]
        # nbb_id = get_id_onderneming(btw)

        conn.close()

def vull_sector():
    csv_data_nacebel = csv.reader(open('C:/woorden/kmo.csv'))
    csv_data_namen = csv.reader(open('C:/woorden/nace.csv'))
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    codes = {}
    inserted_sector = []
    for row in csv_data_namen:
        # get the name field
        code = row[1]
        naam = row[3]
        codes[code] = naam
    print(codes)
    for row in csv_data_nacebel:
        # get the name field
        nacebel = row[3]
        btw = row[7].replace(' ', '')
        if nacebel in codes.keys():
            if nacebel not in inserted_sector:
                insert_sector(codes.get(nacebel),nacebel,conn)
                print(nacebel,codes.get(nacebel))
                inserted_sector.append(nacebel)

    conn.close()
def vull_personeel():
    csv_data = csv.reader(open('C:/woorden/kmo.csv'))
    header = next(csv_data)
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    i=0
    for row in csv_data:
        personeel = row[4]
        btw = row[7].replace(' ', '')
        print(i,personeel,btw)
        insert_personeel(btw,personeel,conn)
        i+=1
    conn.close()
def vull_adress():
    csv_data = csv.reader(open('C:/woorden/kmo.csv'))
    header = next(csv_data)
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    i=0
    for row in csv_data:
        straat = row[9]
        btw = row[7].replace(' ', '')
        postcode = int(row[8])
        print(i,postcode,straat,btw)
        insert_adress(btw,straat,postcode,conn)
        i+=1
    conn.close()
def vull_municipallity():
    csv_data = csv.reader(open('C:/woorden/kmo.csv'))
    header = next(csv_data)
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    listinsert=[]
    i=0
    for row in csv_data:
        if int(row[8]) not in listinsert:
            postcode = int(row[8])
            gemeente = row[2]
            print(i,postcode,gemeente)
            insert_municipality(postcode, gemeente)
            listinsert.append(postcode)
        i+=1
    conn.close()
def vull_verstedelijking():
    csv_data = csv.reader(open('C:/woorden/std.csv'))
    header = next(csv_data)
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(0.5)
    for row in csv_data:
        postcode = int(row[0])
        verstedelijking = int(row[1])
        if verstedelijking == -99997:
            verstedelijking = 0
        print(postcode,verstedelijking)
        insert_stedelijkheidsklasse(verstedelijking,postcode,conn)
    conn.close()
if __name__=='__main__':
    vull_sector()