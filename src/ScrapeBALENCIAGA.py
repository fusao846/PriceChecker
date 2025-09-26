from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

def scrapeBALENCIAGA(cg, scraper, url, LOG, concat_size, priceNumber):
 
    driver = scraper.get_driver()
    LOG.debug("scrapeBALENCIAGA start")
    scraper.open(url)
    LOG.debug("open done")
    accept = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if len(accept) > 0:
        if accept[0].is_enabled:
            accept[0].click()

    priceEles = driver.find_elements(By.CLASS_NAME, 'c-price__value--current')
    if len(priceEles) > 0:
        priceFound = False
        for priceEle in priceEles:
            price = priceEle.get_attribute("innerText")
            if "\u00a5" in price:
                priceFound = True
                break
        if priceFound == False:
            price = "NOTFOUND"
    else:
        price = "NOTFOUND"
    LOG.debug(f"{url} {price}")
    zaiko = 0
    size = "OneSize"

    noZaiko = False
    if price != "NOTFOUND":
        price = priceNumber(price)

        sizeSelect = driver.find_elements(By.ID, "pdp-size-selector")
        if len(sizeSelect) > 0:
            print("size ari")
            optionEles = sizeSelect[0].find_elements(By.TAG_NAME, "option")
            sizeOption = []
            for option in optionEles:
                if option.get_attribute("data-available") == "true" and option.get_attribute("innerText").strip() != "U":
                    sizeOption.append(option)
            if len(sizeOption) > 0:
                size, noZaiko = concat_size(sizeOption)
            else:
                size = 'OneSize'

        sizeSelectEles = driver.find_elements(By.CLASS_NAME, "c-customselect__option")
        sizeFound = False
        if len(sizeSelectEles) > 0:
            for sizeSelect in sizeSelectEles:
                tx = sizeSelect.get_attribute("innerText")
                if tx and tx == "サイズを選ぶ":
                    sizeFound = True
                    break
        if sizeFound == True:
            optionEles = driver.find_elements(By.CLASS_NAME, "c-customselect__option")
            if len(optionEles) > 0:
                size, noZaiko = concat_size(optionEles)

        else:
            size = "OneSize"
            
        cartButton = driver.find_elements(By.CLASS_NAME, "c-product__addtocart")
        if len(cartButton) > 0:
            zaiko = 5
        else:
            LOG.debug("button not existed")
            print("button not existed")
            zaiko = 0
    else:
        zaiko = 0
        size = ""
    if noZaiko == True:
        zaiko = 0
    #print(zaiko)
    #print(size)
    return price, size, zaiko

