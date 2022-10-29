from urllib.request import ProxyDigestAuthHandler
import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import random
import time
# def site_generator(bedrijfsnaam):
#     """"""
#     bedrijfsnaam = bedrijfsnaam.lower()
#     extensions = [".be", ".com", ".org", ".biz"]
#     bedrijf_woorden = bedrijfsnaam.split(" ")
#     sites = []
#     sites.append(bedrijfsnaam.replace(" ", ""))
#     for woord in bedrijf_woorden:
#         for ext in extensions:
#             sites.append(f"{woord}{ext}")

#     return sites
regions = ["uk-london",
           "uk-streaming-optimized",
           "uk-manchester",
           "uk-southampton",
           "de-berlin",
           "de-frankfurt",
           "dk-copenhagen",
           "dk-streaming-optimized",
           "netherlands",
           "ireland",
           "se-streaming-optimized",
           "se-stockholm",
           "norway",
           "es-valencia",
           "es-madrid",
           "monaco",
           "nigeria",
           "liechtenstein",
           "switzerland",
           "france",
           "slovenia",
           "luxembourg",
           "andorra",
           "poland",
           "serbia",
           "it-milano",
           "it-streaming-optimized",
           "czech-republic",
           "kazakhstan",
           "portugal",
           "belgium",
           "slovakia",
           "turkey",
           "fi-streaming-optimized",
           "fi-helsinki",
           "austria",
           "montenegro",
           "ukraine",
           "algeria",
           "morocco",
           "georgia",
           "malta",
           "armenia",
           "isle-of-man",
           "egypt",
           "north-macedonia",
           "cyprus",
           "latvia",
           "us-east-streaming-optimized",
           "us-baltimore",
           "us-houston",
           "us-west-streaming-optimized",
           "us-atlanta",
           "us-wilmington",
           "us-chicago",
           "us-east",
           "us-west",
           "us-new-york",
           "us-salt-lake-city",
           "us-california",
           "us-las-vegas",
           "us-silicon-valley",
           "us-texas",
           "us-denver",
           "us-florida",
           "us-honolulu",
           "us-seattle",
           "us-washington-dc",
           "chile",
           "venezuela",
           "bulgaria",
           "lithuania",
           "greece",
           "moldova",
           "romania",
           "albania",
           "bahamas",
           "ca-toronto",
           "ca-montreal",
           "ca-ontario",
           "ca-vancouver",
           "iceland",
           "argentina",
           "costa-rica",
           "colombia",
           "croatia",
           "saudi-arabia",
           "israel",
           "bosnia-and-herzegovina",
           "panama",
           "united-arab-emirates",
           "hungary",
           "estonia",
           "south-africa",
           "brazil",
           "jp-streaming-optimized",
           "jp-tokyo",
           "mexico",
           "china",
           "singapore",
           "hong-kong",
           "mongolia",
           "taiwan",
           "qatar",
           "malaysia",
           "au-perth",
           "au-melbourne",
           "au-sydney",
           "india",
           "vietnam",
           "greenland",
           "cambodia",
           "philippines",
           "new-zealand",
           "sri-lanka",
           "indonesia",
           "macao",
           "bangladesh"]

banned = []


def get_source(url):
    try:

        session = HTMLSession()
        response = session.get(url)
        if response.status_code == 429:
            print("Rate limit, stop programma")
            os.system(
                f'"C:\Program Files\Private Internet Access\piactl.exe" set region {random.choice(regions)}')

            time.sleep(15)

        return response

    except requests.exceptions.RequestException as e:
        print(e)


def zoek_site_bedrijf(bedrijfsnaam, adres, ondernemingsnummer):
    '''
    deze functie gaat de eerst gevonden site van de google results naar de database schrijven met behulp van de functie: schrijf_naar_database

    :par_bedrijfsnaam: naam van het bedrijf
    :par_ondernemingsnummer: het bedrijfsnummer van het bedrijf
    '''

    query = urllib.parse.quote_plus(f"{bedrijfsnaam} {adres}")
    print(query)
    response = get_source("https://www.google.com/search?q=" +
                          query + "&uule=w+CAIQICIHQmVsZ2l1bQ&gl=be&hl=nl")  # de gevonden resultaten voor de query opslaan als 'response'

    # al deze pagina's als links opslaan in links
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.',
                      'https://google.',
                      'https://webcache.googleusercontent.',
                      'http://webcache.googleusercontent.',
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://business.google.',
                      'https://facebook.',
                      'https://instagram.',
                      'https://twitter.',
                      'https://fonts.google'
                      )
    # gaat alle links die tot google domain behoren of niet eindigen op .be, .com,... verwijderen uit de gevonden links
    for url in links[:]:
        if url.startswith(google_domains) or not url.endswith((".be/", ".com/", ".eu/", ".org/")):
            links.remove(url)

    print(f"{links} is mogelijk de site van {bedrijfsnaam}")

    links = list(set(links))
    if links:
        with open("links_using_gemeente.txt", "a") as file:
            file.write(f"{bedrijfsnaam}:{ondernemingsnummer}:{links[0]} \n")

    return links[0]


def schrijf_naar_db(ondernemingsnummer, url):
    '''
    gaat de url van het bijhorend ondernemingsnummer schrijven naar de database

    :par_ondernemingsnummer: het bedrijfsnummer van het bedrijf waarvan we de url naar de db schrijven
    :par_url: de gevonden url die we naar de db willen schrijven
    '''
    # mycursor.execute(
    #     f"update bedrijven set Web_adres = '{url}' where Ondernemingsnummer = {ondernemingsnummer};")
    # db_connectie.commit()
    # print(f"web adres: {url} voor {ondernemingsnummer} naar db geschreven")


def excel_to_df(excel_path):
    df = pd.read_excel(excel_path, sheet_name="Lijst")
    return df


def main():
    '''
    gaat connectie maken met db
    gaat alle bedrijven nemen van de db waarvoor nog geen site is opgeslagen
    en gaat voor deze bedrijven de site zoeken 
    '''
    excel_path = r"C:\Users\jarno\Downloads\kmo's_Vlaanderen_2021.xlsx"
    df = excel_to_df(excel_path)

    with ProcessPoolExecutor(max_workers=8) as executor:
        for index, row in df.iterrows():
            executor.submit(zoek_site_bedrijf, row["Naam"], row["Gemeente"], row["Ondernemingsnummer"].replace(" ", ""))


if __name__ == "__main__":
    #! moet niet meer gerund worden
    main()
