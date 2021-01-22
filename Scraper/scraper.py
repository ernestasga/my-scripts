#   2021-January-21
#   by E.G
from argparse import ArgumentParser, FileType
from urllib import request
import bs4 as bs
from openpyxl import Workbook

def main():
    choose_website()

def choose_website():
    websites = ['Autogidas.lt', 'Autoplius.lt', 'Skelbiu.lt']
    functions = [scrape_autogidas, scrape_autoplius, scrape_skelbiu]
    print('Choose which website to scrape:')
    for it, website in enumerate(websites):
        print(str(it+1)+': '+website)

    choice = verify_int('Choose which website to scrape: ', 0, len(websites))    
    base = verify_url(websites[choice-1])
    result_count = verify_int('Enter how many results to scrape: ', 0, 1000000)

    for i, function in enumerate(functions):
        if choice-1 == i:
            function(base, result_count)
#
# Scrape AUTOGIDAS
#
def scrape_autogidas(base, result_count):
    domain = 'https://autogidas.lt'
    urls = []
    items = []
    page = base
    page_index = 1 
    while True:
        sauce = request.urlopen(page).read()
        print('Searching page '+str(page_index)+'...')
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for i, item in enumerate(soup.find_all('article', class_='list-item')):
            a = item.find_all('a', class_='item-link')
            for url in a:
                if len(items)<result_count:
                    try:
                        url = domain+url.get('href')
                        urls.append(url)
                        print('#'+str(i+1)+' Scraping '+url+'...')
                        psauce = request.urlopen(url).read()
                        psoup = bs.BeautifulSoup(psauce, 'lxml')
                        title = psoup.find('h1', class_='title').text
                        price = psoup.find('div', class_='price').text
                        phone = psoup.find('div', class_='seller-phones').text
                        location = psoup.find('div', class_='seller-location').text
                        items.append({'Title':title.strip(), 'Price':price.strip(), 'Phone':phone.strip(), 'Location':location.strip(), 'Url':url})
                    except:
                        print('Fail...')
                else:
                    break
        page = base+'&page='+str(page_index)
        if not soup.find('div', class_='next-page-inner') or len(items)>=result_count:
            break
        page_index+=1
    item_count = len(items)
    print('Scraped '+str(len(items))+' results')
    make_spreadsheet('autogidas', items) if item_count>0 else print('Nothing to save.')



#
# Scrape AUTOPLIUS
#
def scrape_autoplius(base, result_count):
    domain = 'https://autoplius.lt'
    urls = []
    items = []
    page = base
    page_index = 1 
    while True:
        sauce = request.urlopen(page).read()
        print('Scraping page '+str(page_index)+'...')
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for i, url in enumerate(soup.find_all('a', class_='announcement-item')):
            if len(items)<result_count:
                try:
                    url = url.get('href')
                    urls.append(url)
                    print('#'+str(i+1)+' Scraping '+url+'...')
                    psauce = request.urlopen(url).read()
                    psoup = bs.BeautifulSoup(psauce, 'lxml')
                    title = psoup.find('h1').text
                    price = psoup.find('div', class_='price').text
                    phone = psoup.find('div', class_='seller-phone-number').text
                    location = psoup.find('span', class_='seller-contact-location').text
                    items.append({'Title':title.strip(), 'Price':price.strip(), 'Phone':phone.strip(), 'Location':location.strip(), 'Url':url})
                except:
                    print('Fail...')
            else:
                break
        page_index+=1
        next_page = soup.find('a', class_="next")
        if not next_page or len(items)>=result_count:
            break
        else: 
            page  = domain+next_page.get('href') 
    item_count = len(items)
    print('Scraped '+str(item_count)+' results')
    make_spreadsheet('autoplius', items) if item_count>0 else print('Nothing to save.')

#
# Scrape SKELBIU
#
def scrape_skelbiu(base, result_count):
    domain = 'https://skelbiu.lt'
    urls = []
    items = []
    page = base
    page_index = 1 
    
    while True:
        sauce = request.urlopen(page).read()
        print('Scraping page '+str(page_index)+'...')
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for i, url in enumerate(soup.find_all('a', class_='js-cfuser-link')):
            if len(items)<result_count:
                try:
                    url = url.get('href')
                    url = domain+url
                    urls.append(url)
                    print('#'+str(i+1)+' Scraping '+url+'...')
                    psauce = request.urlopen(url).read()
                    psoup = bs.BeautifulSoup(psauce, 'lxml')
                    title = psoup.find('h1').text
                    price = psoup.find('p', class_='price')
                    if not price:
                        price = '0'
                    else:
                        price = psoup.find('p', class_='price').text

                    phone = psoup.find('div', class_='phone-button').find('div', class_='primary').text
                    
                    location = psoup.find('p', class_='cities').text
                    items.append({'Title':title.strip(), 'Phone':phone.strip(), 'Price':price.strip(), 'Location':location.strip(), 'Url':url})
                except:
                    print('Fail...')
            else:
                break
        page_index+=1
        next_page = soup.find('a', rel_="next")
        if not next_page or len(items)>=result_count:
            break
        else: 
            page  = domain+next_page.get('href') 
    item_count = len(items)
    print('Scraped '+str(item_count)+' results')
    make_spreadsheet('skelbiu', items) if item_count>0 else print('Nothing to save.')



#
# Input verification
#
def verify_url(website):
    while True:
        try:
            url = input('Enter base url to start scraping on '+website+': \n')
            return url if website.lower() in url.lower() else int('notint')
        except:
            print('----Input url of base page to start scraping----')

def verify_int(input_text, min, max):
    while True:
        try:
            choice = int(input(input_text))
            return choice if choice>=min and choice<=max else int('notint')
        except:
            print('----Input must be an integer between '+str(min)+' and '+str(max)+'----')
#
# Generating spreadsheets
#

def make_spreadsheet(website, results):
    # Results format [{...},{...}...]
    try:
        print('Generating spreadsheet...')
        wb = Workbook()
        sheet = wb.active
        sheet.title = website+' scrape results'
        for i, key in enumerate(results[0].keys()):
            alpha = chr(ord('@')+i+1)
            sheet[alpha+'1'] = key
            try:
                for i2, result in enumerate(results):
                    value = result[key]
                    position = alpha+str(i2+2)
                    sheet[position] = value
            except:
                pass

        if args.outfile:
            wb.save(args.outfile.name)
        else:
            wb.save(website+'_scrape_results.xlsx')   
    except:
        print('Failed to generate spreadsheet.')
#
# Main
#
if __name__ == "__main__":
    parser = ArgumentParser(
                        description='Information scraper for various websites')
    parser.add_argument('-o', '--outfile', type=FileType('w'),
                        help='Write to spreadsheet file')
    args = parser.parse_args()
    main()

