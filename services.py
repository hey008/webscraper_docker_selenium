import sys
from py_scripts.myselenium import web_scraper

# ---
# print (f'__name__: {__name__}')
# ---


# ---
print (f'1: Sample Test: Remote')
print (f'2: Sample Test: Local')
menu = input('Please select: ')

if (menu == '1'):
    web_scraper('https://www.welovephuket.com')
elif (menu == '2'):
    web_scraper('https://www.welovephuket.com', 'Local')
elif (menu == '3'):
    url = input('Enter URL: ')
    web_scraper(url)
elif (menu == '4'):
    print(f'Call CSV')
else:
    print(f'Command not found')