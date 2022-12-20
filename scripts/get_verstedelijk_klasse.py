import csv
import pandas as pd
from connectie import get_database

pg_engine = get_database()

#Convert postcode naar NIS code via een csv file
def get_nis_code(postcode):
    # 
    f = open('../data/nis_to_zip.xlsx')
    rows = list(csv.reader(f))
    for row in rows[1:]:
        zipcode = int(row[1])
        # nis = row[2]
        if postcode == zipcode:
            return int(row[2])

    return None

#Krijg type van verstedeleking: 0=landelijk, 1=randstedelijk, 2=verstedelijkt op basis van NIS door een Excel file
def get_type(nis_code_kmo):
    df = pd.read_excel('../data/lu_vrl_vlaa_2013.dbf.xlsx')
    # df['NISCODE']
    # df['type']
    row = df.loc[df['NISCODE'] == nis_code_kmo]
    type = row['type'].mode()
    if not len(type) == 0:
        return type.values[0]
    return None

#Update de DB met stedelijkheidsklasse in municipality
def insert_type(type,postcode):
    print(f'{postcode} : {type}')
    if type == 'randstedelijk':
        type = 1
    elif type == 'verstedelijkt':
        type = 2
    elif type == 'landelijk':
        type = 0

    pg_engine.execute(f'UPDATE municipality SET stedelijkheidsklasse = {type} WHERE zipcode = {postcode}')

#Krijg stedelijkheidsklasse van postcodes in DB en update DB op basis daarvan
def main():
    zips = pg_engine.execute('SELECT zipcode FROM municipality').all()
    zips = [zip[0] for zip in zips]

    teller = 0
    for postcode in zips:
        print(f'{len(zips)-teller} zips to go')
        nis_code = get_nis_code(postcode)
        type_versted = get_type(nis_code)

        if not type_versted == None:
            insert_type(type_versted,postcode)

        teller +=1
    


main()