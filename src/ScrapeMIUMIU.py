from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

def scrapeMIUMIU(cg, scraper, url, LOG, concat_size, priceNumber):
    driver = scraper.get_driver()
    LOG.debug("scrapeMIUMIU start")
    scraper.open(url)
    LOG.debug("open done")
    accept = driver.find_elements(By.CLASS_NAME, "cta_accept")
    if accept and len(accept) > 0:
        if accept[0].is_enabled:
            accept[0].click()

    priceEles = driver.find_elements(By.TAG_NAME, 'p')
    priceFound = False
    print(f"priceEles len {len(priceEles)}")
    for priceEle in priceEles:
        price = priceEle.get_attribute("innerText")
        if "\u00a5" in price:
            pr = priceNumber(price)
            if pr == 0:
                price = "NOTFOUND"
                break
            else:
                priceFound = True
                break
    if priceFound == False:
        price = "NOTFOUND"

    LOG.debug(f"{url} {price}")
    zaiko = 0
    size = "OneSize"

    sizeSelExist = False
    pEles = driver.find_elements(By.TAG_NAME, 'p')
    for pEle in pEles:
        if pEle.is_displayed() == False:
            continue
        tx = pEle.get_attribute("innerText")
        if "サイズを選択" in tx:
            # サイズあり
            validButtons = []
            buttonEles = driver.find_elements(By.TAG_NAME, 'button')
            for buttonEle in buttonEles:
                lb = buttonEle.get_attribute("aria-label")
                if lb and "サイズを選択" in lb:
                    outerHTML = buttonEle.get_attribute("outerHTML")
                    if "line-through" in outerHTML:
                        None
                    else:
                        validButtons.append(buttonEle)
            if len(validButtons) > 0:
                size,  noZaiko = concat_size(validButtons)
            else:
                size = "OneSize"
            break
    noZaiko = False
    if price != "NOTFOUND":
        price = priceNumber(price)

        cartButtonExist = False
        cartButtonEles = driver.find_elements(By.TAG_NAME, "button")
        for cartButtonEle in cartButtonEles:
            tx = cartButtonEle.get_attribute("innerText")
            #print(tx)
            if tx == "ショッピングバッグに追加":
                cartButtonExist = True
                zaiko = 5
        if cartButtonExist == False:
            zaiko = 0

    else:
        zaiko = 0
        size = ""
    if noZaiko == True:
        zaiko = 0
    driver.delete_all_cookies() 
    return price, size, zaiko

