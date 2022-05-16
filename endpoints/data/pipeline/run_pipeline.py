from prefect import task, Flow, Parameter
from typing import Any, Dict, List
import os
import re
import pandas as pd
from dotenv import dotenv_values
from collections import defaultdict
from endpoints.data.pipeline.get_coffee_links import *
from endpoints.data.pipeline.get_coffee_info import *
from endpoints.data.functions.helper import *

@task
def create_coffee_info(links_df):
    """This function creates the final dataframe with all of the coffee information scraped from the drinktrade.com website.

    Args:
        links_df (_type_): _description_
    """

    ###
    # Create empty dictionary of lists for storing the different types of information.
    ###  
    keys = ['product_id', 'name', 'process', 'subregion', 'farmer', 'elevation', 'variety', 'roaster', 'roaster_notes', 'roaster_url', 'image_url', 'other_notes']
    info_dict = defaultdict(list)

    for key in keys:
        info_dict[key] = list()

    pages = links_df.link

    ###
    # For each page, retrieve the page html, parse the javascript component for product ID and roaster URL, 
    # then parse the HTML for the other pieces of information.
    ### 
    for page in pages:
        soup = get_coffee_page(page)

        info_dict = get_parsed_javascript(soup, info_dict)

        info_dict = get_parsed_html(soup, info_dict)

    ###
    # Create a dataframe of the information.
    ### 
    trade_coffee_df = pd.DataFrame()

    for k, v in info_dict.items():
        trade_coffee_df[k] = v

    trade_coffee_df['trade_link'] = pages
    trade_coffee_df['storage_path'] = ''

    ###
    # Clean data.
    ###


    ###
    # Upload the dataframe to Azure Storage.
    ### 
    config = dotenv_values(".env")

    block_blob_service = BlockBlobService(
        account_name=config['AZ_STORAGE_NAME'], 
        account_key=config['AZ_ACCOUNT_KEY']
    )

    upload_coffee_images(trade_coffee_df, block_blob_service)



with Flow('data-engineer') as flow:

    # Define parameters

    # Define tasks
    driver = initialize_driver()

    get_coffee_page(driver)

    links = set()
    links = scrape_dt_cards(links, driver)
    save_links(links)

    upload_links_to_storage()

    ###
    # Get Coffee Page Info
    ###
    info = get_coffee_info(links)

    trade_df = create_dataframe(info)

    blob = BlockBlobService(
        account_name=config['AZ_STORAGE_NAME'], 
        account_key=config['AZ_ACCOUNT_KEY']
    )

    trade_df['storage_path'] = trade_df.apply(lambda row: get_image_data(row, blob), axis = 1)



flow.run()



