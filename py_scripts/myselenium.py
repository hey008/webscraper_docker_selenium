import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

def web_scraper(url, drivertype='remote'):
    if url == "":
        print(f'URL is empty')
        return False

    print(f'web_scraper: {url}')
    
    #load_time = get_load_time(url)
    #print(f'Check : Page load time: {load_time} seconds')

    browser = get_browser(drivertype)
    connect_browser(url, browser)
    sleep(10)
    html = browser.page_source
    write_2_file(html)
    return False

# Functional library ----- ----- ----- ----- ----- ----- ----- ----- ----- 

def get_browser(drivertype='remote'):
    # initialize options
    options = webdriver.ChromeOptions()
    # pass in headless argument to options
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--screen-size=1200x800")
    # initialize driver
    if drivertype == 'remote':
        options.add_argument("--disable-gpu")
        #options.add_argument("--remote-debugin-port=9222")
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def connect_browser(url, browser):    
    try:
        browser.get(url)
        WebDriverWait(browser, 5).until(
            EC.presence_of_element_located((By.ID, 'hnmain'))
        )
        return True
    except Exception as ex:
        print(f'Error connecting to {url}.')
    return False

def get_load_time(article_url):
    try:
        # set headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27'}
        # make get request to article_url
        response = requests.get(
            article_url, headers=headers, stream=True, timeout=3.000)
        # get page load time
        load_time = response.elapsed.total_seconds()
    except Exception as ex:
        load_time = 'Loading Error'
    return load_time

def write_2_file(html):
    current_date = str(datetime.now())
    filename = "HTMLs/"+str(current_date).replace(":","").replace(" ","_").replace("-","") + ".html"
    soupobj = BeautifulSoup(html, 'html.parser')

    f = open(filename, "a")
    f.write(str(soupobj.prettify().encode("utf-8")))
    f.close()