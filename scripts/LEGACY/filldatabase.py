import csv
import sys
from nbb import get_id_onderneming
from sqlfunctions import insert_kmo, select_onderneemsningsnummers
from connectie import get_database
import time

csv_data = csv.reader(open('data\kmosss.csv'))
header = next(csv_data)


def insert_csvData():
    conn = get_database()
    print('Importing the CSV Files')
    time.sleep(1)
    print("ARE YOU READY?")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("GO!")
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

        insert_kmo([btw, name, email, telefoon, website, "w.i.p", nacebel], conn)
    conn.close()

