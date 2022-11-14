import yfinance as yf
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlfunctions import *
import time
def beursgenoteerd(bedrijf):
    ticker=yf.Ticker(bedrijf)
    try:
        info = ticker.info
        return info
    except:
        return "Bedrijf niet gevonden"
def yahooscraperseleniumstartup():
    PATH="C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    url = 'https://finance.yahoo.com'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element(By.NAME,"agree").click()
    search = driver.find_element(By.ID, 'yfin-usr-qry')
    return driver, search
def yahoosearchbedrijf(bedrijf,driver,search):
    #driver, search = yahooscraperseleniumstartup()
    search.send_keys(bedrijf)
    time.sleep(0.1)
    result=False
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/div[2]/div[1]/div/ul[1]")
        bedrijf=driver.find_element(By.ID,"result-quotes-0").text
        if bedrijf.find("Equity - BRU") != -1:
            result=True
    except:
        pass
    search.clear()
    return result
def main():
    pg_conn = get_database()
    driver,search=yahooscraperseleniumstartup()
    bedrijven=select_naam_ondernemingsnummer_kmos(pg_conn)
    i=0
    for bedrijf in bedrijven:
        i+=1
        if yahoosearchbedrijf(bedrijf[1],driver,search):
            print(bedrijf[1])
            insert_beursgenoteerd(bedrijf[0],"TRUE",pg_conn)
        else:
            print("Niets gevonden")
            insert_beursgenoteerd(bedrijf[0],"FALSE",pg_conn)
        print(i)
    pg_conn.close()
if __name__ == "__main__":
    main()