import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from dotenv import dotenv_values
from azure.storage.blob import BlockBlobService

def initialize_driver():
    edgedriver='endpoints\data\driver\msedgedriver.exe'

    options = webdriver.EdgeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver=webdriver.Edge(executable_path=edgedriver, options = options)

    return driver

def get_coffee_page(driver):
    driver.implicitly_wait(5)
    driver.get("https://www.drinktrade.com/coffee/all-coffee")

def get_cards_links(links, driver):
    cards = driver.find_elements(By.CLASS_NAME, value="product-card-wrapper")
  
    for card in cards:
        name = card.find_element(By.TAG_NAME, value = "a").get_attribute("href")
        
        links.add(name)
    
    return links

def scrape_dt_cards(links, driver):
    try:
        loadmore = driver.find_element(By.CLASS_NAME, value="load-more-btn")
        print('load more button found')

        while loadmore.is_displayed():
            driver.execute_script("arguments[0].click();", loadmore)
            print('button clicked')

            sleep(randint(5,10))

            links = get_cards_links(links, driver)

            sleep(randint(5,10))
        
        return links
            
    except StaleElementReferenceException:
        print('Could not retrieve all links.')

        pass

def save_links(links):
    links_df = pd.DataFrame({'link':list(links)})
    links_df.to_csv('coffee_links.csv')

def upload_links_to_storage():
    config = dotenv_values(".env")

    block_blob_service = BlockBlobService(
        account_name=config['AZ_STORAGE_NAME'], 
        account_key=config['AZ_ACCOUNT_KEY'])

    block_blob_service.create_blob_from_path(
        'coffeecontainer', 
        'ml/recommendations/data/coffee_links.csv', 
        'coffee_links.csv')