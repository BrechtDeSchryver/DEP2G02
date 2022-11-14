import requests


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


def ZoekmachineWebsite(text):
    '''
    deze functie gaat het voorkomen van Zoekterm1 en Zoekterm2 zoeken binnen een range van 50 woorden op de website 

    :par_text: alle tekst van de website waarin we de 2 zoektermen willen in zoeken
    :return(list(int,int)): geeft terug hoeveel keer de 2 zoektermen voorkomen binnen een range van 50 woorden 
                          : geeft ook terug wat de average afstand was wanneer de 2 zoektermen binnen 50 woorden werden gevonden
    '''
    ZOEKTERMEN = {
        'Zoekterm1': ['duurzaamheid', 'duurzame', 'duurzaamheidsstrategie', 'duurzaam'],
        'Zoekterm2': ['strategie', 'strategisch', 'strategische', 'strategieën', 'beleid', 'engagement', ]
    }
    text = text.split()
    i = 0
    combinatie = 0
    averagewoorden = []
    zoekterm1 = False
    a = 0
    for word in text:
        for zoekterm in ZOEKTERMEN['Zoekterm1']:
            if zoekterm in word:
                zoekterm1 = True
        if zoekterm1 == True:
            i += 1
            for zoekterm in ZOEKTERMEN['Zoekterm2']:
                if zoekterm in word:
                    averagewoorden.append(i)
                    combinatie += 1
                    zoekterm1 = False
                    i = 0
        if i == 50:
            i = 0
    if combinatie != 0:
        a = 0
        b = len(averagewoorden)
        for value in averagewoorden:
            a += value/b
    return [combinatie, a]


def main():

    # r = get_text("https://www.haviland.be/")
    print(Zoekmachine("https://www.kbc.be/"))
    # with open("test.txt", "w", encoding="utf-8") as f:
    #     f.write(r)


if __name__ == "__main__":
    main()
