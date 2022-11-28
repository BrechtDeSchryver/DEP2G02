import yfinance as yf
import requests
import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlfunctions import *
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
from threading import BoundedSemaphore
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
    driver.find_element(By.NAME,"agree").click()
    return driver
def yahoosearchbedrijf(bedrijfnaam,bedrijfnummer,driver):
    search = driver.find_element(By.ID, 'yfin-usr-qry')
    search.send_keys(bedrijfnaam)
    time.sleep(1.5)
    try:
        driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/div/div[1]/div[1]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div/form/div[2]/div[1]/div/ul[1]")
        bedrijf=driver.find_element(By.ID,"result-quotes-0").text
        if bedrijf.find("Equity - BRU") != -1:
            insert_beursgenoteerd(bedrijfnummer,"TRUE")
            print("true ",bedrijfnaam)
            search.clear()
        else:
            insert_beursgenoteerd(bedrijfnummer,"FALSE")
            print("false ",bedrijfnaam)
            search.clear()
    except:
        insert_beursgenoteerd(bedrijfnummer,"FALSE")
        print("false err",bedrijfnaam)
        search.clear()
def main():
    bedrijven=select_naam_ondernemingsnummer_kmos()
    driver=yahooscraperseleniumstartup()
    i=0
    for bedrijf in bedrijven:
        i+=1
        if i>=12561:
            print(i)
            yahoosearchbedrijf(bedrijf[1],bedrijf[0],driver)
if __name__ == "__main__":
    main()
