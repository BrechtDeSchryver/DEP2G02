from http.client import InvalidURL
from urllib.error import URLError
from bs4 import BeautifulSoup
import urllib.request
import ssl
import random
import requests
import socket
import sys
import urllib.parse

context = ssl._create_unverified_context()


def getProxie(banned=[]):
    '''
    haalt uit de lijst PROXIES 1 random proxie die we dan gaan gebruiken

    :par_banned : optionele lijst die je kan meegeven van proxies die al gebanned zijn en die worden dan uit de random keuze gehaald
    :return (dictionary) : geeft een dictionary terug (omdat we met http en https zitten) van de willekeurige proxie
    '''
    PROXIES = "154.21.62.209:5276,171.22.132.64:7517,154.95.38.220:5878,92.118.55.192:6549,23.236.255.216:7267,45.128.246.98:7113,104.144.99.118:7151,192.153.171.80:6153,154.21.62.76:5143,193.23.245.229:8800,154.21.39.9:5847,92.118.55.217:6574,5.183.34.90:6441,154.12.102.228:6355,45.137.43.43:7597,154.95.1.245:6767,186.179.7.68:8145,92.242.189.120:6971,45.136.228.17:6072,45.192.155.29:7040,154.55.89.203:6059,138.128.114.143:7709,209.127.115.203:6299,154.85.125.107:6318,104.227.173.223:8286,193.8.215.82:8101,5.181.42.1:6062,23.236.255.185:7236,192.186.172.151:9151,45.136.231.189:7245,185.196.1.35:5251,181.177.94.47:7621,45.128.245.9:9020,154.92.112.180:5201,192.241.94.137:7692,45.192.147.198:5846,23.229.119.208:7235,45.12.140.29:5608,107.152.146.156:8674,45.57.253.106:7643,45.128.247.230:7731,80.253.250.223:5560,104.144.235.114:7194,104.144.235.128:7208,104.227.28.228:9286,154.12.97.245:6598,45.72.55.237:7274,185.213.242.124:8588,192.186.172.50:9050,138.128.106.113:8678"
    a = PROXIES.split(",")
    proxielist = []
    for proxie in a:
        if proxie not in banned:
            proxielist.append(proxie)
    proxie = random.choice(proxielist)
    a = {'http': "http://"+proxie, "https": "https://"+proxie}
    return a


def GetapiProxie(banned=[]):
    r = requests.get(
        "https://proxy.webshare.io/proxy/list/download/jbuhwbfvgutffymtbezdkgxjxccugvpjwdvrrnje/-/http/port/direct/")
    print(r.json())


class Webscraper:
    def __init__(self, depth, blacklisted_words, keywords, max_pages) -> None:
        self.depth = depth
        self.blacklisted_words = blacklisted_words
        self.max_pages = max_pages
        self.keywords = keywords
        self.links = []
        self.voldoende_links = False

    def UrlChecker(self, string):
        '''
        deze functie gaat checken of de gegeven url een geldige url is 
        '''
        a = ""
        if string[0:12] == "https://www." or string[0:11] == "http://www.":
            return string
        else:
            if string[0:8] == "https://":
                string[8:12] == "www."

            elif string[0:7] == "http://":
                string[7:11] == "www."

            elif string[0:3] == "www":
                string = "https://" + string

            else:
                a = "https://www."
                string = a+string

        return string

    def clear_invalid_links(self):
        for link in self.links:
            if link.endswith(self.blacklisted_words):
                self.links.remove(link)

    def GetWebpage(self, url):
        # try:
        url = self.UrlChecker(url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        request = urllib.request.Request(url.replace(" ", ""), headers=headers)
        try:
            webUrl = urllib.request.urlopen(request, timeout=3)
        except urllib.error.HTTPError:
            return ''
        except URLError as e:
            # if 'timed out' in str(e):
            #     sys.exit()
            return ''
        except TimeoutError as e:
            return ''

        if webUrl.url.endswith(self.blacklisted_words):
            print("url/pagina in blacklisted words...")
            return ''
        htmlfile = webUrl.read()
        soup = BeautifulSoup(htmlfile, 'lxml')
        return soup.prettify()
        # except urllib.error.HTTPError as e:
        #     print("Error op " + url + " reden: " + str(e))
        #     return ''

        # except InvalidURL as e:
        #     print("Error op " + url + " reden: " + str(e))
        #     return ''
        # except socket.timeout as e:
        #     print("Timeout Error op " + url + " reden: " + str(e))
        #     return ''

    def GetAllLinksHtml(self, html, url):
        url = self.UrlChecker(url)
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.find_all('a', href=True)
        tags = [tag["href"] for tag in tags]
        links = []
        for tag in tags:
            if len(self.links) > self.max_pages:
                print(f"{len(self.links)} links gevonden, stop")
                self.voldoende_links = True
                break

            try:
                if tag == "/" or len(tag.split("/")) - 4 > self.depth:
                    continue

                if url in tag:
                    self.links.append(tag)

                elif tag.startswith("/"):
                    self.links.append(f"{url}/{tag[1:]}")

            except KeyError:
                print(tag)
                print("no href found in tag")

        self.links.extend(links)
        self.clear_invalid_links()
        return links

    def GetallTextHtml(self, html):
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.find_all('p')
        return soup.text
        # for tag in tags:
        #     if tag.string is not None:
        #         print(tag.string)

    def check_keyword_pages(self, url):
        """ Check of de site pages heeft met de keywords, hier geven we prioriteit aan """
        found = []
        for keyword in self.keywords:
            try:
                tempurl = self.UrlChecker(f"{url}/{keyword}")
                print(f"Kijken of {tempurl} bestaat")
                r = self.GetWebpage(tempurl)
                if r == '':
                    continue
                self.links.append(tempurl)
                found.append(tempurl)
                print(f"Keyword pagina: {url} gevonden")
            except urllib.error.HTTPError:
                print(f"{keyword} pagina niet gevonden")
                continue

        return found

    def GetallLinksSite(self, url):
        self.check_keyword_pages(url)
        url = self.UrlChecker(url)
        self.links.append(url)
        for link in self.links:
            self.clear_invalid_links()
            if self.voldoende_links:
                break
            if url in link and True not in [sub in self.blacklisted_words for sub in link.split("/")]:
                newUrl = link
                print(f"HTML opvragen van {newUrl}")
                page = self.GetWebpage(newUrl)
                print(f"Zoeken voor nieuwe links in {newUrl}")
                pagesLinks = self.GetAllLinksHtml(page, url)
                print(f"{len(pagesLinks)} nieuwe links gevonden")

                for link in pagesLinks:
                    if link not in self.links and url in link and True not in [sub in self.blacklisted_words for sub in link.split("/")]:
                        self.links.append(link)

        self.links.extend(self.links)
        self.links = list(set(self.links))

        return self.links
