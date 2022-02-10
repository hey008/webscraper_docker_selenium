import sys
from py_scripts.myselenium import web_scraper

browser_mode = ''; # Local, Remote

# ---
print (f'1: Sample Test: Local')
print (f'2: Sample Test: Remote')
print (f'3: Custom URL: Local')
print (f'4: Custom URL: Remote')
menu = input('Please select: ')

if (menu == '1'):
    browser_mode = 'Local'
    web_scraper('https://www.welovephuket.com', browser_mode)
elif (menu == '2'):
    browser_mode = 'Remote'
    web_scraper('https://www.welovephuket.com', browser_mode)
elif (menu == '3'):
    browser_mode = 'Local'
    url = input('Enter URL (Eg. https://jane-maverick.com): ')
    web_scraper(url, browser_mode)
elif (menu == '4'):
    browser_mode = 'Remote'
    url = input('Enter URL (Eg. https://jane-maverick.com): ')
    web_scraper(url, browser_mode)
else:
    print(f'Command not found')