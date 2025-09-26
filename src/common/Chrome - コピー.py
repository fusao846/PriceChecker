from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from selenium_stealth import stealth

from pprint import pprint
import os
import sys
import time
from os import path
import random

default_wait = 2

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
#    "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.0 Mobile/14C92 Safari/602.1",
#    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
]
def get_random_user_agent():
    return random.choice(user_agents)

class Proxy:
    def __init__(self):
        #GET PROXY LISTS
        self.driver = webdriver.Chrome()
        self.proxy_list = []
        proxy_list_url = "https://free-proxy-list.net/"
        self.driver.get(proxy_list_url)
        tbody = self.driver.find_elements(By.XPATH,'//*[@id="list"]/div/div[2]/div/table/tbody')
        trs = tbody[0].find_elements(By.TAG_NAME, "tr")
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")
            self.proxy_list.append(
                {
                    "ip":tds[0].text,
                    "port":tds[1].text,
                    "enable":True
                }
            )
        self.index = 0
        print(f"Proxy get complete cout {len(self.proxy_list)}")
        self.driver.quit()
    def getNextProxy(self):
        for i in range(len(self.proxy_list)):
            self.index = self.index + 1
            if self.index >= len(self.proxy_list):
                self.index = 0
            if self.proxy_list[self.index]["enable"] == True:
                return self.proxy_list[self.index]["ip"],self.proxy_list[self.index]["port"]
        return "",""
    def disable(self):
        self.proxy_list[self.index]["enable"] = False

class Scraper:
    def __init__(self, dir, x=0, y=345, ip="", port= 0):
        service = Service()
        service.creation_flags = 0x08000000   
        options = Options()
     #   options.add_argument("--disable-background-networking")                                      # 拡張機能の更新、セーフブラウジングサービス、アップグレード検出、翻訳、UMAを含む様々なバックグラウンドネットワークサービスを無効にする。
     #   options.add_argument("--disable-blink-features=AutomationControlled")                        # navigator.webdriver=false となる設定。確認⇒　driver.execute_script("return navigator.webdriver")
     #   options.add_argument("--disable-default-apps")                                               # デフォルトアプリのインストールを無効にする。
     #   options.add_argument("--disable-dev-shm-usage")                                              # ディスクのメモリスペースを使う。DockerやGcloudのメモリ対策でよく使われる。
     #   options.add_argument("--disable-extensions")                                                 # 拡張機能をすべて無効にする。
     #   options.add_argument('--disable-features=DownloadBubbleV2')                                  # `--incognito`を使うとき、ダイアログ(名前を付けて保存)を非表示にする。
     #   options.add_argument("--disable-features=Translate")                                         # Chromeの翻訳を無効にする。右クリック・アドレスバーから翻訳の項目が消える。
        options.add_argument("--hide-scrollbars")                                                    # スクロールバーを隠す。
     #   options.add_argument("--ignore-certificate-errors")                                          # SSL認証(この接続ではプライバシーが保護されません)を無効
     #   options.add_argument("--mute-audio")                                                         # すべてのオーディオをミュートする。
     #   options.add_argument("--no-default-browser-check")                                           # アドレスバー下に表示される「既定のブラウザとして設定」を無効にする。
     #   options.add_argument("--propagate-iph-for-testing")                                          # Chromeに表示される青いヒント(？)を非表示にする。
        options.add_argument(f"--window-position={x},{y}")                                            # ウィンドウの初期位置を指定する。--start-maximizedとは併用不可
        options.add_argument("--window-size=1200,1024")                                              # ウィンドウの初期サイズを設定する。--start-maximizedとは併用不可
        options.add_argument("--user-data-dir=" + dir)                                              # ウィンドウの初期サイズを設定する。--start-maximizedとは併用不可
        options.add_argument("--profile-directory=Default")   
    #    options.add_argument("--disable-http2")                                           # ウィンドウの初期サイズを設定する。--start-maximizedとは併用不可
    #    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])  # Chromeは自動テスト ソフトウェア~~ ｜ コンソールに表示されるエラー　を非表示
    #    options.add_argument("--disable-cache")
    #    options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")  
        options.add_argument("--disable-blink-features=AutomationControlled") 
        # exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
        # turn-off userAutomationExtension 
        options.add_experimental_option("useAutomationExtension", False) 

        if ip != "" and port != "":
            print(f"Proxy Set http://{ip}:{port}")
            options.add_argument(f"--proxy-server=http://{ip}:{port}")

        self.user_agent = get_random_user_agent()
       # print(f"Using User-Agent: {user_agent}")
        options.add_argument(f"user-agent={self.user_agent}")

        caps = DesiredCapabilities.CHROME.copy()
       # options.capabilities を使用して統合
        for key, value in caps.items():
            print(f"{key}:{value}")
            options.set_capability(key, value)
        
        self.driver = webdriver.Chrome(service=service,options=options)


        #self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        #    'source': '''
        #        Object.defineProperty(navigator, 'webdriver', {
        #        get: () => undefined
        #        });
        #    '''
        #})
        script = """
            Object.defineProperty(navigator, 'languages', {get: () => ['ja-JP', 'ja']});
            Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """
        self.driver.execute_script(script)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        #stealth(
        #    self.driver,
        #    languages=["ja-JP", "ja"],
        #    vendor="Google Inc.",
        #    platform="Win32",
        #    webgl_vendor="Intel Inc.",
        #    renderer="Intel Iris OpenGL Engine",
        #    fix_hairline=True,
        #)
    def get_user_agent(self):
        return self.user_agent
    def open(self, URL):
        self.driver.get(URL)
        self.driver.implicitly_wait(default_wait)
    def setWait(self, s):
        self.driver.implicitly_wait(s)
    def resetWait(self):
        self.driver.implicitly_wait(default_wait)
        
    def get_text_by_class(self, class_name, wait=0):
        ele = self.driver.find_elements(By.CLASS_NAME, class_name)
        time.sleep(wait)
        try:
            if len(ele) >= 1:
                return ele[0].get_attribute("textContent")
        except Exception as e:
            print(f"{e}")
            return 'NOTFOUND'
        return 'NOTFOUND'
    def get_text_by_id(self, id):
        ele = self.driver.find_element(By.ID, id)
        if ele != None:
            return ele.get_attribute('innerText')
        return ''
    def get_text_array_by_class(self, class_name):
        ele = self.driver.find_elements(By.CLASS_NAME, class_name)
        r = []
        for e in ele:
            r.append(e.text)
        return r
    def put_text_to_xpath(self, xpath, value):
        ele = self.driver.find_element(By.XPATH, xpath)
        ele.clear()
        ele.send_keys(value)
    def click_button(self, xpath):
        ele = self.driver.find_element(By.XPATH, xpath)
        ele.click()
        self.driver.implicitly_wait(10)
    def wait(self, n):
        self.driver.implicitly_wait(n)
    def get_text_by_th_value(self, th_value):
        ele_trs = self.driver.find_elements(By.TAG_NAME, 'tr')
        for ele_tr in ele_trs:
            ele_ths = ele_tr.find_elements(By.TAG_NAME, 'th')
            ele_tds = ele_tr.find_elements(By.TAG_NAME, 'td')
            n = 0
            for ele_th in ele_ths:
                if ele_th.text == th_value:
                    return ele_tds[n].text
                n = n + 1
        return 'NOTFOUND'
    def is_exist_tag_with_text(self, tag, text):
        eles = self.driver.find_elements(By.TAG_NAME, tag)
        for ele in eles:
            if ele.text == text:
                return True
        return False
    def take_screen_shot(self, file_name):
        wait = WebDriverWait(driver=self.driver, timeout=20)
        try:
            FILENAME = os.getcwd() + '\\image\\' + file_name
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))        
            w = self.driver.execute_script("return document.body.scrollWidth;")
            h = self.driver.execute_script("return document.body.scrollHeight;")
            self.driver.set_window_size(w,h)
            self.driver.save_screenshot(FILENAME)
            return FILENAME        
        except TimeoutException as te:
            return ''
        return ''
    def wait_for_xpath(self, xpath):
        try:
            # 最大10秒間、指定のXPathが見つかるまで待機
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return True
        except TimeoutException:
            return False
    def get_driver(self):
        return self.driver
    def back(self, URL):
        self.driver.back()
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.current_url == URL
        )
        time.sleep(5)
    def sleep(self, s):
        time.sleep(s)
    def get_tags(self, tag):
        return self.driver.find_elements(By.TAG_NAME, tag)
    def wait_tags(self, tag):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, tag))
        )
    def quit(self):
        self.driver.quit()
