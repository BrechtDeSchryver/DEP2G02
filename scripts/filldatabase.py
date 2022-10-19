import csv
import sys
from nbb import get_id_onderneming

csv_data = csv.reader(open('data\kmosss.csv'))
header = next(csv_data)


def get_csv_data():

    print('Importing the CSV Files')
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
        telegram = row[10]
        website = row[11]
        email = row[12]
        nbb_id = get_id_onderneming(btw)

        print(winst)