from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

def scrapePRADA(cg, scraper, url, LOG, concat_size, priceNumber):
 
    driver = scraper.get_driver()
    LOG.debug("scrapePRADA start")
    scraper.open(url)
    LOG.debug("open done")
    # Cookie許容
    accept = driver.find_elements(By.CLASS_NAME, "banner_cta cta_accept")
    if len(accept) > 0:
        if accept[0].is_enabled:
            accept[0].click()

    # 価格
    scraper.setWait(60)
    priceEles = driver.find_elements(By.TAG_NAME, 'p')
    scraper.resetWait()
    if len(priceEles) > 0:
        priceFound = False
        for priceEle in priceEles:
            priceDataEle = priceEle.get_attribute("data-element")
            if priceDataEle and priceDataEle == "product-current-price":
                price = priceEle.get_attribute("innerText")
                priceFound = True
                break
        if priceFound == False:
            LOG.debug(f"Pタグに対象なし {len(priceEles)}")
            price = "NOTFOUND"
    else:
        LOG.debug(f"Pタグなし")
        price = "NOTFOUND"
    LOG.debug(f"{url} {price}")
    zaiko = 0
    size = "OneSize"

    noZaiko = False
    if price != "NOTFOUND":
        price = priceNumber(price)


        sizeSelectEles = driver.find_elements(By.CLASS_NAME, "size-picker-tabs__item")
        sizeFound = False
        if len(sizeSelectEles) > 0:
            for sizeSelect in sizeSelectEles:
                tx = sizeSelect.get_attribute("innerText")
                if tx and tx == "サイズを選択":
                    sizeFound = True
                    break
        if sizeFound == True:
            ulEles = driver.find_elements(By.CLASS_NAME, "size-picker-drawer__list")
            if len(ulEles) > 0:
                selEles = ulEles[0].find_elements(By.TAG_NAME,"button")
                if len(selEles) > 0:
                    validButton = []
                    for selEle in selEles:
                        tind = selEle.get_attribute("tabindex")
                        if tind != "-1":
                            validButton.append(selEle)
                    size, noZaiko = concat_size(validButton)
                else:
                    size = "OneSize"
            else:
                size = "OneSize"
        else:
            size = "OneSize"
            
        cartButtonEles = driver.find_elements(By.TAG_NAME, "button")
        if len(cartButtonEles) > 0:
            buttonFound = False
            for cartButton in cartButtonEles:
                tx = cartButton.get_attribute("innerText")
                if tx and tx == "ショッピングバッグに追加":
                    zaiko = 5
                    buttonFound = True
                    break
            if buttonFound == False:
                zaiko = 0
        else:
            LOG.debug("button not existed")
            print("button not existed")
            zaiko = 0
    else:
        zaiko = 0
        size = ""
    if noZaiko == True:
        zaiko = 0
    #print(zaiko)"
    #print(size)
    driver.delete_all_cookies() 

    return price, size, zaiko

