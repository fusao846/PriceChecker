from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import os
import json
import re

def getBy(key):
    if key == "id":
        return By.ID
    if key == "class":
        return By.CLASS_NAME
    if key == "tag":
        return By.TAG_NAME
    if key == "xpath":
        return "xpath"
    if key == "css":
        return By.CSS_SELECTOR
    return None

def scrape(name, cg, scraper, url, LOG, concat_size, priceNumber, color = ''):
    current = os.getcwd()
    DEFINE = []
    DEF = {}
    json_file = f"{current}\\scrape_define.json"
    try:
        with open(json_file, encoding='utf-8') as s:
            DEFINE = json.load(s)
    except OSError as e:
        print(e)
        return
    for d in DEFINE:
        if d["name"] == name:
            DEF = d
            break 
    driver = scraper.get_driver()
    LOG.debug(f"scrape {name} start")
    scraper.open(url)
    LOG.debug("open done")

    if "accept_button_caption" in DEF:
        AC = DEF["accept_button_caption"]
        btns = driver.find_elements(By.TAG_NAME, 'button')
        for btn in btns:
            try:
                tx = btn.get_attribute("innerText")
                if tx == AC["value"]:
                    if btn.is_enabled():
                        btn.click()
                        break
            except Exception as e:
                print(e)
                print('continue')
                continue
                
    if "accept" in DEF:
        AC = DEF["accept"]
        accept = driver.find_elements(getBy(AC["key"]), AC["value"])
        if len(accept) > 0:
            if accept[0].is_enabled:
                accept[0].click()
    if "accept2" in DEF:
        AC = DEF["accept2"]
        accept = driver.find_elements(getBy(AC["key"]), AC["value"])
        if len(accept) > 0:
            if accept[0].is_enabled:
                accept[0].click()

    PR = DEF["price"]
    parent = driver
    if "parent" in PR:
        if len(driver.find_elements(getBy(PR["parent"]["key"]), PR["parent"]["value"])) > 0:
            parent = driver.find_elements(getBy(PR["parent"]["key"]), PR["parent"]["value"])[0]
        else:
            print('parent 0')
            if "parent2" in PR:
                if len(driver.find_elements(getBy(PR["parent2"]["key"]), PR["parent2"]["value"])) > 0:
                    print('parent2 ari')
                    parent = driver.find_elements(getBy(PR["parent2"]["key"]), PR["parent2"]["value"])[0]
                else:
                    print('parent2 0')
    priceEles = parent.find_elements(getBy(PR["key"]), PR["value"])
    if len(priceEles) > 0:
        if "attribute" in PR:
            priceFound = False
            for priceEle in priceEles:
                att = priceEle.get_attribute(PR["attribute"]["key"])
                if PR["attribute"]["value"] in att:
                    price = priceEle.get_attribute("innerText")
                    price = re.sub(r'\D', '', price) 
                    if price == "":
                        price = 0
                    else:
                        price = int(price) 
                    priceFound = True
                    break
            if priceFound == False:
                price = "NOTFOUND"
        else:
            price = priceEles[0].get_attribute("innerText")
            price = re.sub(r'\D', '', price) 
            if price == "":
                price = 0
            else:
                price = int(price) 
    else:
        price = "NOTFOUND"
    

    LOG.debug(f"{url} {price}")
    print(f"URL PRICE {url} {price}")
    
    zaiko = 0
    size = "OneSize"
    
    bodyText = driver.find_elements(By.TAG_NAME, 'body')[0].get_attribute("innerText")
    if "ngword" in DEF:
        ngwords = DEF["ngword"]
        for ngw in ngwords:
            if ngw in bodyText:
                print(f"ngw {ngw} found will retrun soldout")
                return "NOTFOUND", "OneSize", 0

    noZaiko = False

    if "color-check" in DEF:
        CC = DEF["color-check"]
        colorCheck = driver.find_elements(getBy(CC["key"]), CC["value"])
        print(f"colorCheck len {len(colorCheck)}")
        if len(colorCheck) > 0:
            attFound = False
            for cc in colorCheck:
                att = cc.get_attribute(CC["attribute"]["key"])
                if att:
                    print(f" attval {att.upper()}")
                    if color.upper() == att.upper():                
                        print("color found")
                        attFound = True
                        break
            if attFound == False:
                print("color check 一致なし zaiko 0")
                noZaiko = True      

    if price != "NOTFOUND":
        if "euro" in PR:
            price = priceNumber(price, euro = True)
        else:
            price = priceNumber(price)
        # SIZE確認
        SZS = DEF["size_select"]
        print(f"key: {SZS['key']} val:{SZS['value']}")
        sizeSelect = driver.find_elements(getBy(SZS["key"]), SZS["value"])
        
        print(f"sizeSelect len {len(sizeSelect)}")
        if len(sizeSelect) > 0:
            print(sizeSelect[0].get_attribute("innerText"))
            if "action" in SZS:
                sizeSelect[0].click()
                scraper.sleep(3)
            SZ = DEF["size"]
            parent = driver
            if SZ["parent"]["type"] == "root":
                parent = driver
            else:
                parentEles = driver.find_elements(getBy(SZ["parent"]["key"]), SZ["parent"]["value"])
                if len(parentEles) > 0:
                    parent = parentEles[0]

            optionEles = parent.find_elements(getBy(SZ["key"]), SZ["value"])
            print(f"optionEles len {len(optionEles)}")
            sizeOption = []
            for option in optionEles:
                if "attribute" in SZ:
                    print("attribute ari")
                    att = option.get_attribute(SZ["attribute"]["key"])
                    if att == SZ["attribute"]["value"]:
                        if "except" in SZ:
                            print("except ari")
                            exp = option.get_attribute(SZ["except"]["key"]).strip()
                            print(f"SZEXP {SZ["except"]["value"] } {exp}")
                            if SZ["except"]["value"] in exp:
                                None
                            else:
                                sizeOption.append(option)
                        else:
                            print("except nashi")
                else:
                    print("attribute nashi")
                    if "except" in SZ:
                        print("except ari2")
                        exp = option.get_attribute(SZ["except"]["key"]).strip()
                        print(f"SZEXP {SZ["except"]["value"] } {exp}")
                        if SZ["except"]["value"] in exp:
                            None
                        else:
                            sizeOption.append(option)
                            print("except nashi")
                    else:
                        sizeOption.append(option)
            if len(sizeOption) > 0:
                size, noZaiko = concat_size(sizeOption)
                print(f"concat size {size} {noZaiko}")
            else:
                size = 'OneSize'
            if size == "Misura":
                size = 'OneSize'
            if noZaiko == False:
                return price, size, 5
            else:
                return price, size, 0
        CB = DEF["cart"]
        cartButton = driver.find_elements(getBy(CB["key"]), CB["value"])
        print(f"cartButton len {len(cartButton)}")
        if len(cartButton) > 0:
            if "attribute" in CB:
                print("attr ari")
                attFound = False
                for bt in cartButton:
                    att = bt.get_attribute(CB["attribute"]["key"])
                    print(f" attval {CB["attribute"]["value"].upper()}|{att.upper()}")
                    if CB["attribute"]["value"].upper() in att.upper():
                        print("zaiko5 1")
                        zaiko = 5
                        attFound = True
                        break
                if attFound == False:
                    print("att 一致なし")
                    zaiko = 0                    
            else:
                # 定義にAtt なし
                print("att nashi")
                zaiko = 5
        else:
            # ボタンなし
            print("zaiko 0 x1")
            zaiko = 0
            
        #CART2　在庫なしのとき、cart2もチェック
        if zaiko == 0 and "cart2" in DEF:
            CB = DEF["cart2"]
            cartButton = driver.find_elements(getBy(CB["key"]), CB["value"])
            print(f"cartButton2 len {len(cartButton)}")
            if len(cartButton) > 0:
                if "attribute" in CB:
                    print("attr2 ari")
                    attFound = False
                    for bt in cartButton:
                        att = bt.get_attribute(CB["attribute"]["key"])
                        print(f" attval2 {CB["attribute"]["value"].upper()}|{att.upper()}")
                        if CB["attribute"]["value"].upper() in att.upper():
                            print("zaiko5 21")
                            zaiko = 5
                            attFound = True
                            break
                    if attFound == False:
                        print("att2 一致なし")
                        zaiko = 0                    
                else:
                    # 定義にAtt なし
                    print("att2 nashi")
                    zaiko = 5
            else:
                # ボタンなし
                print("zaiko 0 2x1")
                zaiko = 0
        


    if noZaiko == True:
        print("zaiko 0 x3")
        zaiko = 0
    #print(zaiko)
    #print(size)
    
    return price, size, zaiko

