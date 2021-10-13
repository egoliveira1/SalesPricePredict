# IMPORTS
import re
import os
import sqlite3
import logging
import requests
import pandas   as pd
import numpy    as np
from datetime   import datetime
from bs4        import BeautifulSoup
from sqlalchemy import create_engine


def data_collection (url, headers):
    
    # Pagination
    pagination_page = requests.get(url, headers = headers)
    
    # Beautiful Soup object for pagination
    soup_pagination = BeautifulSoup(pagination_page.text, 'html.parser')
    total_item = soup_pagination.find_all('h2', class_='load-more-heading')[0].get('data-total')
    itens_per_page = 36
    page_number = np.ceil(int(total_item) / itens_per_page)
    url_pagination = url + '?page-size=' + str(int(page_number * itens_per_page))

    # Product Data
    # Request to URL
    main_page = requests.get(url_pagination, headers = headers)
    
    # Beautiful Soup object
    soup = BeautifulSoup(main_page.text, 'html.parser')
    products = soup.find('ul', class_='products-listing small')
    products_list_article = products.find_all('article', class_ = 'hm-product-item')
    
    # product_id
    product_id = [p.get('data-articlecode') for p in products_list_article]
    
    # product_category
    product_category = [p.get('data-category') for p in products_list_article]
    
    # product_name
    products_list_link = products.find_all('a', class_ = 'link')
    product_name = [p.get_text() for p in products_list_link]
    
    # product_price
    product_list_span = products.find_all('span', class_ = 'price regular')
    product_price = [p.get_text() for p in product_list_span]
    
    # Construct DataFrame
    data = pd.DataFrame([product_id, product_category, product_name, product_price]).T
    data.columns = ['product_id', 'product_category', 'product_name', 'product_price']
    
    return data


def data_collection_by_product(data, headers):
    
    # Empty DataFrame
    df_compositions = pd.DataFrame()

    # Unique columns for all products
    aux = []

    # DataFrame pattern
    df_pattern = pd.DataFrame(columns = ['Art. No.', 
                                         'Composition', 
                                         'Fit', 
                                         'Product safety',
                                         'Size', 
                                         'More sustainable materials'])

    for i in range(len(data)):
        # API request 
        url_products = 'https://www2.hm.com/en_us/productpage.' + data.loc[i, 'product_id'] + '.html'
        page_product = requests.get(url_products, headers = headers)
        logger.debug('Product: %s', url_products)
            
        # Beautiful Soup Object
        soup = BeautifulSoup(page_product.text, 'html.parser')
    
        # product_color
        product_list = soup.find_all('a', class_ = 'filter-option miniature active') + soup.find_all('a', class_ = 'filter-option miniature')
        color_name = [p.get('data-color') for p in product_list]
    
        #product_id
        product_id = [p.get('data-articlecode') for p in product_list]
        df_color = pd.DataFrame([product_id, color_name]).T
        df_color.columns = ['product_id', 'color_name']
            
        for j in range(len(df_color)):
            # API request 
            url_color = 'https://www2.hm.com/en_us/productpage.' + df_color.loc[j, 'product_id'] + '.html'
            logger.debug('Color: %s', url_color)
            page_product_color = requests.get(url_color, headers = headers)
                    
            # Beautiful Soup Object
            soup = BeautifulSoup(page_product_color.text, 'html.parser')
    
            # product_name
            product_name = soup.find_all('h1', class_ = 'primary product-item-headline')
            if len(product_name) > 0:
                product_name = product_name[0].get_text()
                    
            # product_price
            product_price = soup.find_all('div', class_ = 'primary-row product-item-price')
            if len(product_price) > 0:
                product_price = re.findall(r'\d+\.?\d+', product_price[0].get_text())[0]
            
            # product_composition
            product_composition_list = soup.find_all('div', class_ = 'pdp-description-list-item')
            if len(product_composition_list) > 0:
                product_composition = [list(filter(None, p.get_text().split('\n'))) for p in product_composition_list]
            
                # Rename DataFrame
                df_composition = pd.DataFrame(product_composition).T
                df_composition.columns = df_composition.iloc[0]
    
                # Delete first row
                df_composition = df_composition.iloc[1:].fillna(method = 'ffill')
    
                # Remove Pocket lining, Shell and Lining
                df_composition['Composition'] = df_composition['Composition'].replace('Pocket lining: ', '', regex = True)
                df_composition['Composition'] = df_composition['Composition'].replace('Shell: ', '', regex = True)
                df_composition['Composition'] = df_composition['Composition'].str.replace('Lining: ', '', regex = True)
    
                # Garantee the same number of columns
                df_composition = pd.concat([df_pattern, df_composition], axis = 0)
    
                # Rename columns
                df_composition.columns = ['product_id', 'composition', 'fit', 'product_safety', 'size', 'more_sust_materials']
                df_composition['product_name'] = product_name
                df_composition['product_price'] = product_price
    
            # Keep new columns if it show up
            aux = aux + df_composition.columns.tolist()
    
            # Merge Composition + color
            df_composition = pd.merge(df_composition, df_color, how = 'left', on = 'product_id')
    
            # All products
            df_compositions = pd.concat([df_compositions, df_composition], axis = 0)
    
    # Create Style Code and Color Code
    df_compositions['style_id'] = df_compositions['product_id'].apply(lambda x: x[:-3])
    df_compositions['color_id'] = df_compositions['product_id'].apply(lambda x: x[-3:]) 
    
    # Scrapy datetime
    df_compositions['scrapy_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df_compositions
    
    
def data_cleaning(data_product):

    df_data = data_product.copy()

    # product_name
    df_data['product_name'] = df_data['product_name'].str.replace('\n', '')
    df_data['product_name'] = df_data['product_name'].str.replace('\t', '')
    df_data['product_name'] = df_data['product_name'].str.replace('/', '_')
    df_data['product_name'] = df_data['product_name'].str.replace('  ', '')
    df_data['product_name'] = df_data['product_name'].str.replace(' ', '_').str.lower()
    
    # product_price
    df_data['product_price'] = df_data['product_price'].astype(float)
    
    # color_name
    # df_data = df_data.dropna(subset = ['color_name'])
    # df_data = df_data.drop(columns = ['color_name_x', 'color_name_y'])
    df_data['color_name'] = df_data['color_name'].str.replace(' ', '_').str.lower()
    
    # fit
    df_data['fit'] = df_data['fit'].str.replace(' ', '_').str.lower()
    
    # Size --->>> size_model and size_number
    # size_model
    df_data['size_model'] = df_data['size'].apply(lambda x: re.search('\d{3}cm', x).group(0) if pd.notnull(x) else x)
    df_data['size_model'] = df_data['size_model'].apply(lambda x: re.search('\d+', x).group(0) if pd.notnull(x) else x)
    
    # size_number
    df_data['size_number'] = df_data['size'].str.extract('(\d+/\\d+)')
    
    # Composition
    # Break composition by comma and create a new DataSet
    df1 = df_data['composition'].str.split(',', expand = True).reset_index(drop = True)
    
    # Create a reference DataSet - Columns --> cotton | polyester | elastane | elasterell
    df_ref = pd.DataFrame(index = np.arange(len(df_data)), columns = ['cotton', 'polyester', 'elastane', 'elasterell'])
    
    # Cotton
    df_cotton_0 = df1.loc[df1[0].str.contains('Cotton', na = True), 0]
    df_cotton_0.name = 'cotton'
    
    df_cotton_1 = df1.loc[df1[1].str.contains('Cotton', na = True), 1]
    df_cotton_1.name = 'cotton'
    
    df_cotton = df_cotton_0.combine_first(df_cotton_1)
    
    df_ref = pd.concat([df_ref, df_cotton], axis = 1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep = 'last')]
    
    # Polyester
    df_polyester_0 = df1.loc[df1[0].str.contains('Polyester', na = True), 0]
    df_polyester_0.name = 'polyester'
    
    df_polyester_1 = df1.loc[df1[1].str.contains('Polyester', na = True), 1]
    df_polyester_1.name = 'polyester'
    
    df_polyester = df_polyester_0.combine_first(df_polyester_1)
    
    df_ref = pd.concat([df_ref, df_polyester], axis = 1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep = 'last')]
    
    # Elastane 
    df_elastane_1 = df1.loc[df1[1].str.contains('Elastane', na = True), 1]
    df_elastane_1.name = 'elastane'
    
    df_elastane_2 = df1.loc[df1[2].str.contains('Elastane', na = True), 2]
    df_elastane_2.name = 'elastane'
    
    df_elastane_3 = df1.loc[df1[3].str.contains('Elastane', na = True), 3]
    df_elastane_3.name = 'elastane'
    
    df_elastane_c2 = df_elastane_1.combine_first(df_elastane_2)
    df_elastane = df_elastane_c2.combine_first(df_elastane_3)
    
    df_ref = pd.concat([df_ref, df_elastane], axis = 1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep = 'last')]
    
    # Elasterell
    df_elasterell = df1.loc[df1[1].str.contains('Elasterell', na = True), 1]
    df_elasterell.name = 'elasterell'
    
    df_ref = pd.concat([df_ref, df_elasterell], axis = 1)
    df_ref = df_ref.iloc[:, ~df_ref.columns.duplicated(keep = 'last')]
    
    # Join of product ID
    df_aux = pd.concat([df_data['product_id'].reset_index(drop = True), df_ref], axis = 1)
    
    # Format composition data
    df_aux['cotton']     = df_aux['cotton'].apply(lambda x: int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['polyester']  = df_aux['polyester'].apply(lambda x: int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['elastane']   = df_aux['elastane'].apply(lambda x: int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    df_aux['elasterell'] = df_aux['elasterell'].apply(lambda x: int(re.search('\d+', x).group(0))/100 if pd.notnull(x) else x)
    
    # Combine product IDs and replace NAs
    df_aux = df_aux.groupby('product_id').max().reset_index().fillna(0)
    
    # Join with Data Raw
    df_data = pd.merge(df_data, df_aux, on = 'product_id', how = 'left')
    
    # Drop unused columns
    df_data = df_data.drop(columns = ['composition', 'product_safety', 'size', 'more_sust_materials'], axis = 1)
    
    # Drop duplicates
    df_data = df_data.drop_duplicates().reset_index(drop = True)
    
    return df_data


def data_insert(df_data):
    
    data_insert = df_data[[
        'product_id', 
        'style_id',
        'color_id',
        'product_name',
        'color_name',
        'fit', 
        'product_price', 
        'size_number',
        'size_model',
        'cotton',
        'polyester', 
        'elastane', 
        'elasterell',
        'scrapy_datetime'
    ]]
    
    # Create database connection
    conn = create_engine('sqlite:///database_hm.sqlite', echo = False)
    
    # Data Insert
    data_insert.to_sql('vitrine', con = conn, if_exists = 'append', index = False)
    
    return None


if __name__ == '__main__':
    
    # Logging
    path = '/home/eron/repos/SalesPricePredict/'
    
    if not os.path.exists(path + 'Logs'):
        os.makedirs(path + 'Logs')
        
    logging.basicConfig(
        filename = path + 'Logs/webscraping_hm.log',
        format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        level = logging.DEBUG
        )
    
    logger = logging.getLogger('webscraping_hm')
    
    # parameters and constants
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15'}
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
  
    # data collection
    data = data_collection(url, headers)
    logger.info('data collect done')
    
    # data collection by product
    data_product = data_collection_by_product(data, headers)
    logger.info('data collection by product done')
    
    # data cleaning
    data_cleaned = data_cleaning(data_product)
    logger.info('data cleaning done')
    
    # data insert
    data_insert(data_cleaned)
    logger.info('data insertion done')