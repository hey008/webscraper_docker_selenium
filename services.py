import sys, os
from os import listdir
from os.path import isfile, join
from datetime import datetime
from py_scripts.myselenium import web_scraper

browser_mode = 'Remote'; # Local, Remote
run_mode = "Test"

if len(sys.argv) > 1:
    if sys.argv[1] == 'production':
        run_mode = "Production"
        scan_path = 'Source'
        count = 0

        try:
            os.makedirs(scan_path, exist_ok=False)
            print(f'{str(datetime.now())} | Source directory created')
        except OSError as error:
            print(f'{str(datetime.now())} | Source directory exists')
        
        files = [f for f in listdir(scan_path) if isfile(join(scan_path, f))]
        # print(f'{files}')
        for file in files:
            print(f'{file}')
            ofile = open(scan_path +'/'+ file, 'r')
            
            while True:
                file_line = ofile.readline().strip()
                if not file_line:
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
        
        if count == 0:
            print(f'{str(datetime.now())} | Folder is empty')

if run_mode == "Test":
    
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
        count = 0
        for file in files:
            print(f'{file}')
            ofile = open(file_path +'/'+ file, 'r')
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