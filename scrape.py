# -*- coding: utf-8 -*-
"""
Yelp Fusion API code.

This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to http://www.yelp.com/developers/v3/documentation for the API
documentation.

This program requires the Python requests library, which you can install via:
`pip install -r requirements.txt`.

Sample usage of the program:
`python scrape.py --term="bars" --location="San Francisco, CA"`
"""
from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import csv
import time
#selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

#Custom
from category import categories
from city import cities
from config import isFirst

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode


# Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app
API_KEY= 'GFGXvLuZW2QErce9kv75J0X-u6c21vkEMt5Zqi8qhUSZr0KCsLm4aBPOSPPyFmjTLFC4w8dlCNBQDdI3c-s9c9y-BRThCynhZRkUpRRpo9kzuACSv8Lhge4kxt47YXYx'


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


# Defaults for our simple example.
DEFAULT_TERM = 'yoga'
DEFAULT_LOCATION = 'Irvine'
SEARCH_LIMIT = 50
OFFSET = 50
FILE_PATH = 'data.csv'
FILTERD_FILE_PATH = 'filterd_data.csv'
FIELD_NAME = ['Business Name', 'Category', 'About the Business', 'Website', 'Phone number', 'Address', 'Pictures', 'Category Title', 'City', 'ZipCode']
#selenium config
options = Options()
options.headless = True
options.page_load_strategy = 'normal'
driver = webdriver.Chrome(options=options)
# driver.set_page_load_timeout(10000)

def request(host, path, api_key, url_params=None):
    """Given your API_KEY, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location, offset = 0):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    responses = search(API_KEY, term, location)
    print(u'Searching businesses for {0} in {1}'.format(term,location))
    total = responses.get('total')
    for i in range(0, total, OFFSET):
        responses = search(API_KEY, term, location, i)
        businesses = responses.get('businesses')
        print(u'Total businesses for {0}-{1} in {2} found.'.format(i, i+OFFSET, total))
        
        if not businesses:
            print(u'No businesses for {0} in {1} found.'.format(term, location))
            return
        for j in range(0, len(businesses)):
            business_id = businesses[j]['id']
            response = get_business(API_KEY, business_id)
            # time.sleep(1)
            #selenium
            link = phonenumber = detail = ''

            try:
                url = response['url']
                driver.get(url)

                #link & phone number
                decriptionTags = driver.find_elements_by_class_name("css-aml4xx")
                for p in decriptionTags:
                    try:
                        if p.get_attribute("innerHTML") == "Phone number":
                            phonenumber = p.find_element_by_xpath('..').find_elements_by_xpath(".//*")[1].get_attribute("innerHTML")
                            break
                        elif p.get_attribute("innerHTML") == "Business website":
                            link = p.find_element_by_xpath('..').find_element_by_tag_name("a").get_attribute("innerHTML")
                            
                    except:
                        pass
                # print(u'website link: {0}'.format(link))
                # print(u'phone number: {0}'.format(phonenumber))

                #find business detail
                modalBtns = driver.find_elements_by_class_name("css-1dfi1ro")
                # print(u'modalBtns: {0}'.format(modalBtns))
                for k in modalBtns:
                    try:
                        c = k.find_element_by_tag_name("span").get_attribute("innerHTML")
                        # print(u'span innerHtml: {0}'.format(c))
                        if c == 'Read more':
                            k.click()
                            details = driver.find_elements_by_class_name(
                                "css-7tnmsu")
                            detail = details[0].get_attribute("innerHTML")
                            break
                    except:
                        pass
                #close tab in unheadless mode
                # driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')

                end_data(FILE_PATH,response['name'],term, detail, link, phonenumber,response['location']['display_address'],response['photos'], response['categories'], response['location']['city'],response['location']['zip_code'])
            except:
                print(u'error in response')
                pass

#write in csv file
def end_data(file_path, Name, Category, About, RedrLink, Phone, Address, Photos, CategoryTitle, City, ZipCode):

    tmpTitle = tmpAddress = tmpPhotos = ''

    for title in CategoryTitle:
        tmpTitle += title['title'] + ','
    for adds in Address:
        tmpAddress += adds + ' '
    for photo in Photos:
        tmpPhotos += photo + ','
    with open(file_path, "a",encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=FIELD_NAME )
        # writer.writeheader()
        writer.writerow({
            "Business Name": Name,
            "Category": Category,
            "About the Business": About,
            "Website": RedrLink,
            "Phone number": Phone,
            "Address": tmpAddress,
            "Pictures": tmpPhotos,
            "Category Title": tmpTitle,
            "City": City,
            "ZipCode": ZipCode
        })


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    # write a header for the first time
    if isFirst == 'true':
        with open(FILE_PATH, "a",encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=FIELD_NAME )
            writer.writeheader()

    # scrape all
    # for category in categories1:
    #     for city in cities:

    #         try:
    #             query_api(category, city)
    #         except HTTPError as error:
    #             sys.exit(
    #                 'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
    #                     error.code,
    #                     error.url,
    #                     error.read(),
    #                 )
    #             )

    # scrape from input or default
    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )
    #close selenium
    driver.quit()

    #check duplicate
    print(u'check duplicate and write in... {0}'.format(FILTERD_FILE_PATH))
    with open(FILE_PATH, 'r') as in_file, open(FILTERD_FILE_PATH, 'w') as out_file:
        seen = set()  # set for fast O(1) amortized lookup
        for line in in_file:
            if line in seen:
                continue  # skip duplicate

            seen.add(line)
            out_file.write(line)

# main entry
if __name__ == '__main__':
    main()
