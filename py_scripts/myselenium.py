import os
import requests
import json
import env
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
from pymongo import MongoClient

# Define Variables
storage_path = 'Storage/'
browser_mode = env.browser_mode
debug_mode = 0 # 0: Off, 1: On
json_data = {}

def web_scraper(url, drivertype='Remote'):
    global browser_mode, json_data
    browser_mode = drivertype
    
    json_data = None
    json_data = {
        'URL': "",
        'Revisions': "",
        'Date': "",
        'file_path': {},
        'head_tags': {},
        'html_tags': {}
    }

    if url == "":
        print(f'URL is empty')
        return False

    try:
        os.makedirs(storage_path + 'HTMLs', exist_ok=False)
        print(f'{str(datetime.now())} | HTMLs directory created')
    except OSError as error:
        print(f'{str(datetime.now())} | HTMLs directory exists')
    try:
        os.makedirs(storage_path + 'Screenshot', exist_ok=False)
        print(f'{str(datetime.now())} | Screenshot directory created')
    except OSError as error:
        print(f'{str(datetime.now())} | Screenshot directory exists')
    try:
        os.makedirs(storage_path + 'Json', exist_ok=False)
        print(f'{str(datetime.now())} | Json directory created')
    except OSError as error:
        print(f'{str(datetime.now())} | Json directory exists')
    
    file_name = browser_mode +"-"+ str(datetime.now()).replace(":","").replace(" ","_").replace("-","")
    file_html = storage_path + 'HTMLs/'+ file_name +'.html'
    file_screenshot = storage_path + 'Screenshot/'+ file_name + '.png'
    file_json = storage_path + 'Json/'+ file_name + '.json'

    json_data['URL'] = url
    json_data['Revisions'] = file_name
    json_data['Date'] = str(datetime.now())
    json_data['file_path']['HTML'] = file_html
    json_data['file_path']['Screenshot'] = file_screenshot
    json_data['file_path']['Json'] = file_json

    print(f'{str(datetime.now())} | Scrape URL: {url}')
    
    if url_status(url):
        browser = get_browser(drivertype)
        connect_browser(url, browser)
        sleep(10)
        html = browser.page_source
        write_html_file(html, file_html)
        try:
            browser.save_screenshot(file_screenshot)
            print(f'{str(datetime.now())} | Making screenshot Completed: '+ file_screenshot)
        except Exception as ex:
            print(f'{str(datetime.now())} | Error..! Making screenshot ')
            if debug_mode == 1:
                print(f'{ex}')
        browser.quit()
        write_json_file(html, file_json)
        write_mongo()
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
    html = str(soupobj)

    f = open(filename, "a", encoding='utf-8')
    f.write(html)
    f.close()
    print(f'{str(datetime.now())} | HTML File Created: {filename}')

def chk_tags(tags):
    r = []
    for tag in tags:
        if tag.text.strip() != "":
            r.append(tag.text.strip())
    return r

def write_json_file(html, filename=""):
    if filename == "":
        current_date = str(datetime.now())
        filename = storage_path +"Json/"+ str(current_date).replace(":","").replace(" ","_").replace("-","") + ".json"
    
    soupobj = BeautifulSoup(html, 'html.parser')

    head_tags_title = soupobj.title.text
    if head_tags_title:
        json_data['head_tags']['title'] = head_tags_title

    head_tags_description = soupobj.find('meta',{'name':'description'})
    if head_tags_description:
        json_data['head_tags']['description'] = head_tags_description.get('content')
    
    head_tags_keywords = soupobj.find('meta',{'name':'keywords'})
    if head_tags_keywords:
        json_data['head_tags']['keywords'] = list(filter(None, [s.strip() for s in head_tags_keywords.get('content').split(",")]))
    
    tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'footer', 'address', 'div', 'li', 'td', 'label', 'b', 'strong', 'span', 'center']
    for tag in tags:
        cl = chk_tags(soupobj.find_all(tag))
        if len(cl) > 0:
            json_data['html_tags'][tag] = cl

    link_tags = []
    links = soupobj.find_all('a')
    for link in links:
        link_tags.append({'text': link.text.strip(), 'href': link.get('href'.strip())})
    if len(link_tags) > 0:
        json_data['Links'] = link_tags

    images_tags = []
    images = soupobj.find_all('img')
    for image in images:
        try:
            title_attr=image.get('alt')
        except:
            title_attr=image.get('title')
        if title_attr:
            images_tags.append({'title': title_attr, 'src': image.get('src'.strip())})
        else:
            images_tags.append({'src': image.get('src'.strip())})
    if len(images_tags) > 0:
        json_data['Images'] = images_tags

    json_load = json.dumps(json_data)
    # print(json_load) # <-- Debug
    f = open(filename, 'w')
    f.write(json_load)
    f.closed
    print(f'{str(datetime.now())} | Json File Created: {filename}')
    return True

def write_mongo():
    mongo_client = MongoClient(
        host = env.mongo_host,
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = env.mongo_user,
        password = env.mongo_user_password,
    )
    mongo_db=mongo_client.bigdata
    mongo_db.webdata.insert_one(json_data)
    print(f'{str(datetime.now())} | Insert record to MongoDB completed')
    return False