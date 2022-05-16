import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from time import sleep
from random import randint
from collections import defaultdict


# "https://www.drinktrade.com/power-glory-blend/p/3366"
# URL = "https://www.drinktrade.com/coffee/all-coffee"

def ListDiff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

links_df = pd.read_csv('endpoints/data/tmp/coffee_links.csv')
pages = links_df.link
all_titles=['Process', 'Sub Region', 'Producer', 'Elevation', 'Variety']
keys = ['product_id', 'name', 'process', 'subregion', 'farmer', 'elevation', 'varietals', 'roaster', 'roaster_notes', 'roaster_url', 'image_url', 'other_notes']
info_dict = defaultdict(list)

for key in keys:
    info_dict[key] = list()


##****** SCRAPE WEB PAGES ******##
headers = {"Accept-Language": "en-US, en;q=0.5"}

i = 0
for page in pages:
    getpage= requests.get(page, headers=headers)

    soup= BeautifulSoup(getpage.content, 'html.parser')

    scripts = soup.find('script', type='text/javascript')
    pattern = re.compile('(\w*):(.*)')

    script_strings = scripts.string.split(',')

    my_dict={}
    for s in script_strings:
        s_removed = s.replace('"', '')
        for x, y in re.findall(pattern, s_removed):
            my_dict[x]=y

    if "product_id" in my_dict.keys():
        info_dict['product_id'].append(my_dict['product_id'])
    else:
        info_dict['product_id'].append('NA')
        
    if "websiteUrl" in my_dict.keys():
        info_dict['roaster_url'].append(my_dict['websiteUrl'])
    else:
        info_dict['roaster_url'].append("NA")

    ###--- Extract HTML tag information ---### 
    try:
        image = soup.find('img', class_='product-image')
        info_dict['image_url'].append(image.get('src'))
    except:
        info_dict['image_url'].append(None)

    try:
        coffee = soup.find('h1', class_='product-name').text
        info_dict['name'].append(coffee.strip())
    except:
        info_dict['name'].append(None)
    
    try:
        roast = soup.find('h2', class_='roaster-name').text
        info_dict['roaster'].append(roast.strip())
    except:
        info_dict['roaster'].append(None)
    
    try:
        on = soup.find('div', class_='description-container').text
        info_dict['other_notes'].append(on.strip())
    except:
        info_dict['other_notes'].append(None)

    try:
        rn = soup.find('div', class_='roaster-notes-body').text
        info_dict['roaster_notes'].append(rn.strip())
    except:
        info_dict['roaster_notes'].append(None)

        # tf = soup.find('div', class_='spec-subtitle')

        # prod_divs=soup.find_all('div', class_='product-spec-section')
    
    ###--- Extract HTML tag information from info section ---### 
    titles=[]
    try:
        items = soup.find_all('div', class_='coffee-info-list__text')
        for item in items:
            title = item.find('div', class_='list-title').text
            titles.append(title)
            
            if title =='Process':
                list_value = item.find('div', class_='list-value').text
                info_dict['process'].append(list_value)
            elif title =='Sub Region':
                list_value = item.find('div', class_='list-value').text
                info_dict['subregion'].append(list_value)
            elif title =='Elevation':
                list_value = item.find('div', class_='list-value').text
                info_dict['elevation'].append(list_value)
            elif title =='Producer':
                list_value = item.find('div', class_='list-value').text
                info_dict['farmer'].append(list_value)
            elif title =='Variety':
                list_value = item.find('div', class_='list-value').text
                info_dict['varietals'].append(list_value)
    except:
        pass

    no_values = ListDiff(titles, all_titles)

    for nv in no_values:
        if nv =='Process':
            info_dict['process'].append(None)
        elif nv =='Sub Region':
            info_dict['subregion'].append(None)
        elif nv =='Elevation':
            info_dict['elevation'].append(9999)
        elif nv =='Producer':
            info_dict['farmer'].append(None)
        elif nv =='Variety':
            info_dict['varietals'].append(None)

    print(i, " of ", len(pages))
    i+=1

    sleep(randint(2,10))


##****** CONVERT TO DATAFRAME ******##
trade_coffee_df = pd.DataFrame()

for k, v in info_dict.items():
    trade_coffee_df[k] = v

trade_coffee_df['trade_link'] = pages
trade_coffee_df['storage_path'] = ''

##****** GET IMAGES ******##
from azure.storage.blob import BlockBlobService
from dotenv import dotenv_values

config = dotenv_values(".env")

block_blob_service = BlockBlobService(
    account_name=config['AZ_STORAGE_NAME'], 
    account_key=config['AZ_ACCOUNT_KEY'])

for i in range(245, len(trade_coffee_df)):

    try:
        img_data = requests.get(trade_coffee_df.image_url[i]).content
        id = trade_coffee_df.product_id[i]
        with open(f'static/assets/img/image_{id}.jpg', 'wb') as handler:
            handler.write(img_data)
        
        local_img_path = 'static/assets/img/image_{}.jpg'.format(trade_coffee_df.product_id[i])
        adls_img_path = 'assets/img/image_{}.jpg'.format(trade_coffee_df.product_id[i])
        
        block_blob_service.create_blob_from_path(
        'static', 
        adls_img_path, 
        local_img_path
        )

        trade_coffee_df.storage_path[i] = adls_img_path

        os.remove(local_img_path)
    except:
        pass

    print(i, " of ", len(trade_coffee_df))

    sleep(randint(2,6))    



trade_coffee_df.to_csv('endpoints/data/tmp/coffee_pages_20220512.csv', index=False, header=True)

block_blob_service.create_blob_from_path(
        'coffeecontainer', 
        'ml/recommendations/data/coffee_info.csv', 
        'endpoints/data/tmp/coffee_pages_20220512.csv'
        )
