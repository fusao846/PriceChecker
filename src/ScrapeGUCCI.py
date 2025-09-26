from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

def scrapeGUCCI(cg, scraper, url, LOG, concat_size, priceNumber):
 
    driver = scraper.get_driver()
    LOG.debug("scrapeGUCCI start")
    scraper.open(url)
    LOG.debug("open done")
    accept = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if len(accept) > 0:
        if accept[0].is_enabled:
            accept[0].click()

    #print('sleeping 5')
    #time.sleep(5)
    #print('wake up')

    priceEles = driver.find_elements(By.ID, 'markedDown_full_Price')
    if len(priceEles) > 0:
        price = priceEles[0].get_attribute("innerText")
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

            
        cartButton = driver.find_elements(By.ID, "shopping-bag-cta")
        LOG.debug(f"find_element shopping-bag-cta {len(cartButton)}")
        print(f"find_element shopping-bag-cta {len(cartButton)}")

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

