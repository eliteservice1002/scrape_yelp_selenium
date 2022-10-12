# Yelp Fusion API Python Code

## Overview
This program demonstrates the capability of the Yelp Fusion API
by using the Search API to query for businesses by a search term and location,
and the Business API to query additional information about the top result
from the search query.

Please refer to [API documentation](https://www.yelp.com/developers/documentation/v3)
for more details.


## Steps to run

To install the dependencies, run:
`pip install -r requirements.txt`.

Run the code sample to scrape all automatically with arguments in city.py and category.py files:
`python scrape_all.py`

Run the code sample with default arguments:
`python scrape.py`

Run the code sample by specifying the optional arguments:
`python scrape.py --term="active" --location="San Francisco, CA"`

Check duplicate in csv file and filter:
`python filter_csv.py`

## Contact Me
Skype: live:.cid.2c6d651287d6edc3
Email: khoa-dev@hotmail.com