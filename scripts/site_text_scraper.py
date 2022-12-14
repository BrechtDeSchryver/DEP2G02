from sqlfunctions import insertRawWebsite, select_kmos, select_bedrijven_zonder_site
from connectie import get_database
from concurrent.futures import ThreadPoolExecutor
from webscraper import Webscraper

keywords = ["duurzaamheid", "milieu", "missie"]
blacklisted_words = ("/en", "/fr", "/de", "/pt", "/producten", "/products", "/product",
                     "/images", "/resources", "/account", "/password", "/user", "/dashboard", "username", "image", "product",
                     "hobby", "merken", "mode", "en", ".pdf", ".jpg", ".jpeg", ".docx", ".ppt", ".pptx", "login", "assets", "mailto",
                     "asset", ".mp4"
                     )


def cleanup_text(text):
    '''
    gaat de tekst die meegegeven is als parameter schoon maken

    :par_text = de tekst die we willen schoon maken
    :return = de tekst zonder leestekens, onnodige spaties en backspaces
    '''
    text = text.lower().replace("\n", " ").replace(
        "\t", " ").replace("   ", "").replace("?", " ").replace(".", " ").replace("!", " ")

    return text


def get_text(site):
    '''
    gaat alle tekst van site scrapen 

    :par_site = de site van bedrijf
    :return : (str) alle tekst van site
    '''
    webscraper = Webscraper(3, blacklisted_words, keywords, 20)
    big_string = ""
    all_links = webscraper.GetallLinksSite(site)
    print(f"-----------------------------------------------")
    print(f"Volgende geldige URLs gevonden: {all_links}")
    print(f"Start met scrapen text vd urls")

    for link in all_links:
        print(f"Text van link {link} toevoegen aan grote string")
        text = webscraper.GetallTextHtml(webscraper.GetWebpage(link))
        text = cleanup_text(text)
        print(f"{len(text)} karakters text gevonden")
        big_string += text
        print(f"Totale lengte van string: {len(big_string)}")

    return big_string


def do_all(site, on, db):
    print(f"--------Bedrijf {on} met site {site} wordt verwerkt------------")
    r = get_text(site)
    insertRawWebsite(on, r, db)


def main():
    # TODO: Over alle bedrijven itereren en schrijven naar db met functie insertRawWebsite
    # r = get_text("https://www.haviland.be/")
    # with open("test.txt", "w", encoding="utf-8") as f:
    #     f.write(r)
    db = get_database()
    kmos = select_bedrijven_zonder_site(db)

    with ThreadPoolExecutor(max_workers=12) as executor:
        for kmo in kmos:
            on = kmo[0]
            site = kmo[4].rstrip()
            # print(on, site)
            if site:
                executor.submit(do_all, site, on, db)

    # for kmo in kmos:
    #     on = kmo[0]
    #     site = kmo[4].rstrip()
    #     if site:
    #         # print(on, site)
    #         do_all(site, on, db)


if __name__ == "__main__":
    main()
# 0415468816
