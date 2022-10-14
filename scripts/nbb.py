import requests
import json
from concurrent.futures import ProcessPoolExecutor
import urllib
import sys
import os 
import pandas as pd

def get_id_onderneming(on): 
    '''
    deze functie gaat het id-nummer van een onderneming geven met behulp van het ondernemingsnummer

    :par_on = ondernemingsnummer van het bedrijf waarvan we het id willen weten
    :return = id-nummer 
    '''
    URL = f"https://consult.cbso.nbb.be/api/rs-consult/published-deposits?page=0&size=10&enterpriseNumber={on}&sort=periodEndDate,desc&sort=depositDate,desc"
    r = requests.get(URL, headers={
                     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})
    json_data = json.loads(r.text)
    id = ""
    for x in json_data["content"]:
        if x["periodEndDateYear"] == 2021:
            id = x["id"]
            break
    print(id)

    return id

total = 0

def get_pdf(id): 
    '''
    gaat de pdf ophalen van het bedrijf met het gegeven id 

    par_id = id-nummer van het bedrijf waarvan we de pdf willen ophalen
    return = 
    '''
    URL = f"https://consult.cbso.nbb.be/api/external/broker/public/deposits/pdf/{id}"
    request = urllib.request.Request(URL)
    request.add_header(
        "User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0")
    r = urllib.request.urlopen(request)
    if r.status != 200:
        print("Rate limit / ban")
        sys.exit(1)


    return r.read()


def save_as_pdf(on, id, bytes_): 
    '''
    gaat het jaarraport van het bedrijf opslaan als pdf

    par_on = het ondernemingsnummer van het bedrijf
    par_bytes_ = 
    '''
    
    with open(fr"C:\Users\jarno\OneDrive - Hogeschool Gent\Data_engineering2\jaarraport_{on}_{id}.pdf", 'wb') as f:
        f.write(bytes_)
    
def download_pdf_on(on):
    '''
    gaat de pdf van het bedrijf downloaden 

    par_on = het ondernemingsnummer van het bedrijf
    '''
    id = get_id_onderneming(on)
    bytes_ = get_pdf(id)
    save_as_pdf(on, id, bytes_)

def schrijf_id_naar_db(ondernemingsnummer):
    '''
    gaat het id-nummer van het bedrijf met gegeven ondernemingsnummer schijven naar de database d.m.v. de functie set_nbb_id dat geÃ¯mporteerd is van sqlstatements.py

    par_ondernemingsnummer = het ondernemingsnummer van het bedrijf
    '''
    id_ = get_id_onderneming(ondernemingsnummer)
    # set_nbb_id(ondernemingsnummer, id_)

def get_bedrijven_nrs():
    """
    Haalt alle bedrijvennummers van de locale excel file
    """
    files = ["Antw.csv", "Limb.csv", "Oost-vl.csv", "Vl-braba.csv", "West-vl.csv"]
    path = r"C:\Users\jarno\OneDrive - Hogeschool Gent\Data_engineering2"
    
    # os list files in directory
    nrs = [x.split("_")[1] for x in os.listdir(path) if x != "script.bash"]

    for file in files:
        data = pd.read_csv(f"DEP2G02/data/{file}", encoding= 'ISO-8859-1')
        nrs.extend(data["Ondernemingsnummer"].tolist())
        nrs = [x.replace(" ", "") for x in nrs]
    
    nrs = list(set(nrs))

    return nrs

def main():
    bedrijven_nummers = get_bedrijven_nrs()
    print(len(bedrijven_nummers))

    with ProcessPoolExecutor(max_workers=12) as executor:
        for on in bedrijven_nummers:
            executor.submit(download_pdf_on, on)
        # schrijf_id_naar_db(on)


if __name__ == "__main__":
    main()



