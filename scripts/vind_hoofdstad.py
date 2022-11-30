import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from sqlfunctions import select_postcodes, insert_capital_city
from connectie import get_database
# todo:
# alle postcodes ophalen
# vinden tot welke hoofdstad deze behoort
# hoofdstad naar db schrijven


def get_capital_city(postcode):
    params = {'country': 'be', 'search_string': postcode}
    response = requests.get(
        'https://www.europacco.com/en/find-zip/be', params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'zip-search-result'})
    capital_city = table.find_all('td')[2].text.split(",")[0]
    print(capital_city)
    return capital_city


def write_to_json(postcode, capital_city):
    with open('data/postcodes.txt', 'a') as f:
        f.write(f'{postcode}: {capital_city}\n')


def get_capital_and_write_to_json(postcode):
    try:
        r = get_capital_city(str(postcode))
    except Exception as e:
        print(e)
        return
    if len(r) == 0:
        return
    else:
        write_to_json(postcode, r)


def create_postcode_dict():
    postcode_dict = {}
    with open('data/postcodes.txt', 'r') as f:
        data = [x.split("\t") for x in f.readlines()]
        for d in data:
            postcode_dict[d[1]] = [d[2], d[7]]
    return postcode_dict


def get_postcode_from_db_and_write_capital():
    db = get_database()
    post_code_dict = create_postcode_dict()
    post_code_dict["1931"] = "Brussel-Hoofdstad" #dat zijn alle bedrijven aan brussels airport fzo iets bruh
    data = select_postcodes()
    for i in data:
        try:
            print("Inserting ", post_code_dict[str(i[1])][0] ,"for postcode: ",
                i[1])
            insert_capital_city(i[0], post_code_dict[str(i[1])][1], db)
        except Exception as e:
            with open("error.txt", "a") as f:
                f.write(str(i[1]) + "\n")


def main():
    # with ThreadPoolExecutor(max_workers=10) as executor:
    #     for i in range(4950, 10000):
    #         executor.submit(get_capital_and_write_to_json, str(i))
    get_postcode_from_db_and_write_capital()


if __name__ == "__main__":
    main()
