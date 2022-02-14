from os import listdir
from os.path import isfile, join
from py_scripts.myselenium import web_scraper

browser_mode = ''; # Local, Remote

# ---
print (f'1: Sample Test: Local')
print (f'2: Sample Test: Remote')
print (f'3: Custom URL: Local')
print (f'4: Custom URL: Remote')
print (f'5: Sample File')
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
elif (menu == '5'):
    browser_mode = 'Local'
    file_path = 'sample'
    files = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    # print(f'{files}')
    for file in files:
        print(f'{file}')
        ofile = open(file_path +'/'+ file, 'r')
        count = 0
        while True:
            file_line = ofile.readline().strip()
            if not file_line or count == 10:
                break
            count += 1
            print(f'{count} | {file_line}')
            if file_line.startswith('http://') or file_line.startswith('https://'):
               web_scraper(file_line, browser_mode)
            elif web_scraper('https://'+ file_line, browser_mode):
                continue
            elif web_scraper('http://'+ file_line, browser_mode):
                continue
        ofile.close()
else:
    print(f'Command not found')