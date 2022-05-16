import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from time import sleep
from random import randint
from collections import defaultdict
from azure.storage.blob import BlockBlobService
from dotenv import dotenv_values

config = dotenv_values(".env")

def ListDiff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def get_coffee_page(page):
    getpage= requests.get(page, headers=headers)
    soup= BeautifulSoup(getpage.content, 'html.parser')

    return soup

def get_parsed_javascript(soup, info_dict):
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

    return info_dict

def get_parsed_html(soup, info_dict):
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
                info_dict['variety'].append(list_value)
    except:
        pass

    all_titles=['Process', 'Sub Region', 'Producer', 'Elevation', 'Variety']
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
            info_dict['variety'].append(None)

    return info_dict

def create_dataframe(info_dict):
    df = pd.DataFrame()

    for k, v in info_dict.items():
        df[k] = v

    df['trade_link'] = pages
    df['storage_path'] = ''

    return df

def get_image_data(row, blob_conn):
    try:
        img_data = requests.get(row.image_url).content
        id = row.product_id
        with open(f'static/assets/img/image_{id}.jpg', 'wb') as handler:
            handler.write(img_data)
        
        local_img_path = 'static/assets/img/image_{}.jpg'.format(id)
        adls_img_path = 'assets/img/image_{}.jpg'.format(id)
        
        blob_conn.create_blob_from_path(
            'static', 
            adls_img_path, 
            local_img_path
        )

        os.remove(local_img_path)
    except:
        pass

    sleep(randint(2,6))

    return adls_img_path
    

     

links_df = pd.read_csv('endpoints/data/tmp/coffee_links.csv')
pages = links_df.link
all_titles=['Process', 'Sub Region', 'Producer', 'Elevation', 'Variety']



##****** SCRAPE WEB PAGES ******##
def get_coffee_info(pages):
    keys = ['product_id', 'name', 'process', 'subregion', 'farmer', 'elevation', 'varietals', 'roaster', 'roaster_notes', 'roaster_url', 'image_url', 'other_notes']
    info_dict = defaultdict(list)
    for key in keys:
        info_dict[key] = list()

    headers = {"Accept-Language": "en-US, en;q=0.5"}

    for page in pages:
        
        soup = get_coffee_page(page)

        info_dict = get_parsed_javascript(soup, info_dict)

        info_dict = get_parsed_html(soup, info_dict)

    return info_dict


### CAN YOU PASS THIS BLOB TO THE get_image_data() FUNCTION??


##****** GET IMAGES ******##
trade_df.to_csv('endpoints/data/tmp/coffee_pages_20220512.csv', index=False, header=True)

block_blob_service.create_blob_from_path(
        'coffeecontainer', 
        'ml/recommendations/data/coffee_info.csv', 
        'endpoints/data/tmp/coffee_pages_20220512.csv'
        )
