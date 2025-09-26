from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# create a new Service instance and specify path to Chromedriver executable
service = ChromeService(executable_path=ChromeDriverManager().install())
 
# create ChromeOptions object
options = webdriver.ChromeOptions()
options.add_argument('--headless')


# create a new Chrome webdriver instance, passing in the Service and options objects
driver = webdriver.Chrome(service=service, options=options)

# navigate to the webpage
driver.get('https://opensea.io/')
 
# take a screenshot of the webpage
driver.save_screenshot('opensea-blocked.png')
 
# close the webdriver
driver.quit()
