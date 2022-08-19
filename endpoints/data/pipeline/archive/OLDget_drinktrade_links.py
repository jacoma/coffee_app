import pandas as pd
from time import sleep
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

# "https://www.drinktrade.com/power-glory-blend/p/3366"
# URL = "https://www.drinktrade.com/coffee/all-coffee"

def get_cards_links(links, driver):
    cards = driver.find_elements(By.CLASS_NAME, value="product-card-wrapper")
  
    for card in cards:
        name = card.find_element(By.TAG_NAME, value = "a").get_attribute("href")
        
        links.add(name)
    
    return links

def scrape_dt_cards(links, driver):
    try:
        loadmore = driver.find_element(By.CLASS_NAME, value="load-more-btn")

        while loadmore.is_displayed():
            driver.execute_script("arguments[0].click();", loadmore)
            sleep(randint(5,10))

            links = get_cards_links(links, driver)
            sleep(randint(5,10))
            
    except StaleElementReferenceException:
        pass

    return links


edgedriver='endpoints\data\driver\msedgedriver.exe'
options = webdriver.EdgeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver=webdriver.Edge(executable_path=edgedriver, options = options)
driver.get("https://www.drinktrade.com/coffee/all-coffee")

# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "closeIconContainer"))
#     )
# finally:
#     driver.quit()


links = set()
links = scrape_dt_cards(links, driver)

driver.quit()

links_df = pd.DataFrame({'link':list(links)})
links_df.to_csv('coffee_links.csv')

from azure.storage.blob import BlockBlobService
from dotenv import dotenv_values

config = dotenv_values(".env")

block_blob_service = BlockBlobService(
    account_name=config['AZ_STORAGE_NAME'], 
    account_key=config['AZ_ACCOUNT_KEY'])

block_blob_service.create_blob_from_path(
    'coffeecontainer', 'ml/recommendations/data/coffee_links.csv', 'coffee_links.csv')
