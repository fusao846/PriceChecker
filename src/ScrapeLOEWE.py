from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

def scrapeLOEWE(cg, scraper, url, LOG, concat_size, priceNumber):
    driver = scraper.get_driver()
    LOG.debug("scrapeLOEWE start")
    scraper.open(url)
    LOG.debug("open done")
    accept = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if len(accept) > 0:
        if accept[0].is_enabled:
            accept[0].click()
    price = scraper.get_text_by_class('capds-product__price--active')
    LOG.debug(f"{url} {price}")
    zaiko = 0
    size = "OneSize"
    LOG.debug("get_driver")

    noZaiko = False
    if price != "NOTFOUND":
        price = priceNumber(price)
        sizeButton = scraper.get_text_by_class('js-size-button')
        sizeButton = sizeButton.strip()
        zaikoFlag = True
        if sizeButton == "NOTFOUND":
            size = "OneSize"
        else:
            if sizeButton.startswith("サイズガイド"):
                LOG.debug("サイズガイドボタンあり")
                size = "OneSize"
            else:
                sizEle = driver.find_element(By.ID, "js-size-selector")
                sizeTextEles = sizEle.find_elements(By.CLASS_NAME, 'capds-btn-square')
                if len(sizeTextEles) > 0:
                    size, noZaiko = concat_size(sizeTextEles)
                    LOG.debug(f"size:{size} noZaiko{noZaiko}")
                else:
                    LOG.debug(f"square button なし")
                    size = "OneSize"

        cartButton = driver.find_elements(By.ID, "capds-cart-button")
        LOG.debug("find_element capds-cart-button")

        if cartButton:
            LOG.debug('cartButton exists')
            divs = cartButton[0].find_elements(By.TAG_NAME, "DIV")
            LOG.debug("find_element DIV")

            zaiko = 0
            for div in divs:
                try:
                    tx = div.get_attribute("textContent")
                    print(tx)
                    if tx == "ショッピングバッグに追加":
                        zaiko = 5
                        break
                except Exception as e:
                    LOG.debug(f"{e}")
        else:
            LOG.debug("button not existed")
            zaiko = 0
    else:
        zaiko = 0
        size = ""
    if noZaiko == True:
        zaiko = 0
    #print(zaiko)
    #print(size)
    return price, size, zaiko

