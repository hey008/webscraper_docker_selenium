from fileinput import filename
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# Define Variables
browser_mode = 'Remote' # Remote: Docker Browser, Local: Machine Browser
debug_mode = 0 # 0: Off, 1: On 

def web_scraper(url, drivertype='Remote'):
    global browser_mode
    browser_mode = drivertype
    
    if url == "":
        print(f'URL is empty')
        return False

    print(f'{str(datetime.now())} | Scrape URL: {url}')
    
    if url_status(url):
        browser = get_browser(drivertype)
        connect_browser(url, browser)
        sleep(10)
        filename = browser_mode +"-"+ str(datetime.now()).replace(":","").replace(" ","_").replace("-","")
        write_html_file(browser.page_source, "HTMLs/"+ filename +".html")
        try:
            browser.save_screenshot("Screenshot/"+ filename + ".png")
            print(f'{str(datetime.now())} | Making screenshot Completed: Screenshot/'+ filename + '.png')
        except Exception as ex:
            print(f'{str(datetime.now())} | Error..! Making screenshot ')
        browser.quit()
        print(f'{str(datetime.now())} | Scrape URL Completed')
        return True
    
    return False

# Functional library ----- ----- ----- ----- ----- ----- ----- ----- ----- 

def get_browser(drivertype='Remote'):
    # initialize options
    options = webdriver.ChromeOptions()
    # pass in headless argument to options
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--screen-size=1280x800")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # initialize driver
    if drivertype == 'Remote':
        options.add_argument("--disable-gpu")
        #options.add_argument("--remote-debugin-port=9222")
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME,
                options=options)
    else:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print(f'{str(datetime.now())} | Browser Opened: {drivertype}')
    return driver

def connect_browser(url, browser):
    global debug_mode
    try:
        browser.get(url)
        WebDriverWait(browser, 5)
        #WebDriverWait(browser, 5).until( EC.presence_of_element_located((By.ID, 'tag_id')) )
        print(f'{str(datetime.now())} | Browser Connected: {url}')
        return True
    except Exception as ex:
        print(f'{str(datetime.now())} | Error connecting to {url}.')
        if debug_mode == 1:
            print(f'{ex}')
    return False

def url_status(url):
    result = False
    try:
        # set headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27'}
        # make get request to article_url
        response = requests.get(
            url, headers=headers, stream=True, timeout=3.000)
        # get page load time
        load_time = response.elapsed.total_seconds()
        print(f'{str(datetime.now())} | URL Check: Page load time: {load_time} seconds')
        result = True
    except Exception as ex:
        print(f'{str(datetime.now())} | URL Check: Page load time: Error')
        if debug_mode == 1:
            print(f'{ex}')
    return result

def write_html_file(html, filename=""):
    if filename == "":
        current_date = str(datetime.now())
        filename = "HTMLs/"+ str(current_date).replace(":","").replace(" ","_").replace("-","") + ".html"
    
    soupobj = BeautifulSoup(html, 'html.parser')

    f = open(filename, "a")
    f.write(str(soupobj.encode("utf-8")))
    f.close()
    print(f'{str(datetime.now())} | HTML File Created: {filename}')