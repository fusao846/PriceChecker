from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException

from common.Chrome import Scraper
import time
import random

def scrapeLUISVUITTON(cg, scraper, url, LOG, CONFIG, DEBUGGING, DEB, concat_size, priceNumber,pcheck,CHROME_FOLDER):
    #url = url + "?insideproduct&utm_source=insidechat"
    print(url)
    driver = scraper.get_driver()
    #driver.delete_all_cookies()
    #LOG.debug("scraper del cookies 1")

    #time.sleep(1)
    #driver.refresh()

    #DEBUGGING = True
    #waits=[7,8,9,10]
    waits=[2,3,4]
    random_w = random.choice(waits)
    print(f"wait : {random_w}")
    time.sleep(random_w)

    scraper.open(url)

    if DEB == True:

        DEBUGGING = True
        cg.setMessage("message", "デバッグ中１")
        while DEBUGGING == True:
            time.sleep(3)
        cg.setMessage("message", "")


    #scraper.open("https://jp.louisvuitton.com/?search")
    #LOG.debug("scraper url open 1")
    #LOG.debug("open done")
    #cg.setMessage("message", "デバッグ中２")
    #DEBUGGING = True
    #while DEBUGGING == True:
    #    time.sleep(3)
    #cg.setMessage("message", "")

    accessOK = False
    while accessOK == False:
        driver = scraper.get_driver()
        body = driver.find_elements(By.TAG_NAME, "body")
        sec = CONFIG["error_wait"]
        if len(body) > 0:
            bodyText = body[0].get_attribute("innerText")
            if "このサイトにアクセスできません" in bodyText:
                #proxy.disable()
                print("delete all cookies")
                driver.delete_all_cookies()

                print(f"ua {scraper.get_user_agent()} rw {random_w}")

                #proxy_ip, proxy_port = proxy.getNextProxy()
                LOG.debug(f"サイトアクセスエラー {sec}秒待機")
                time.sleep(10)
                scraper.quit()
                LOG.debug("scraper quit 1")
                while sec > 0:
                    cg.setMessage("message", f"アクセス不可 {sec}秒待機")
                #    print(f"アクセス不可 {sec}秒待機中")
                    time.sleep(10)
                    sec = sec - 10
                cg.setMessage("message", f"")
                scraper = Scraper(f"{pcheck}\\{CHROME_FOLDER}", x=CONFIG["chrome_x"], y=CONFIG["chrome_y"])
                LOG.debug("scraper constructed 3")
                scraper.open(url)
                LOG.debug("scraper open 2")
            else:
                accessOK = True
    LOG.debug("サイトアクセス成功")
    LOG.debug("scraper OK 1")
    scraper.setWait(20)
    ##btns = driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector")
    btns = driver.find_elements(By.TAG_NAME, "button")
    print(f"btns count {len(btns)}")
    size = "OneSize"
    for btn in btns:
        tx = ""
        try:
            if btn.is_displayed() == False or btn.is_enabled() == False:
                continue
            tx = btn.get_attribute("innerText")
        except Exception as e:
            continue
        if "サイズを選んでください" in tx:
           btn.click()
           time.sleep(1) 
    
        if "サイズ：" in tx:
            print("サイズ：あり")
            #time.sleep(3)
            #eles = driver.find_elements(By.CLASS_NAME, "lv-product-variation-badges__item-name")
            eles = driver.find_elements(By.CLASS_NAME, "lv-product-variation-selector-dropdown__content-item")
            sizeAri = []
            print(f"eles count {len(eles)}")
            for ele in eles:
                #cl = ele.get_attribute("class")
                cl = ele.find_elements(By.TAG_NAME, "span")[0].get_attribute("class")
                print(cl)
                if "unavailable" in cl:
                    None
                else:
                    sizeAri.append(ele)
            size, noZaiko = concat_size(sizeAri)
            print(f"concat size {size} {noZaiko}")
            if noZaiko == True:
                zaiko = 0
            break
        else:
            size = "OneSize"
    price = scraper.get_text_by_class('lv-product__price', wait=5)
    scraper.resetWait()
    if price != "NOTFOUND":
        price = priceNumber(price)
        btTextEles = driver.find_elements(By.CLASS_NAME, 'lv-product-purchase-button')
        zaiko = 5
        print(f"btTextEles len {len(btTextEles)}")
        for btTextEle in btTextEles:
            tx =btTextEle.get_attribute("innerText")
            print(f"tx {tx}")
            if "入荷通知を受け取る" in tx:
                print("入荷通知を受け取る")
                zaiko = 0
                break
            if "在庫なし" in tx:
                print("在庫なし")
                zaiko = 0
                break
            if "電話で問合せる" in tx:
                print("電話で問合せる")
                zaiko = 0
                break
            if "ショッピングバッグに追加" in tx:
                print("ショッピングバッグあり　zaiko 5")
                zaiko = 5
                break
#            if "サイズを選んでください" in tx:
#                print("サイズを選らんでください　あり　zaiko 5")
#                zaiko = 5
#                break
    else:
        print("Priceなし")
        zaiko = 0
    print(f" {price} {size} {zaiko}")
    
    #time.sleep(1)
    return price, size, zaiko  ,""
