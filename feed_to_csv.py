import datetime
import sys
import csv
from itertools import ifilter, imap
from operator import itemgetter
import requests
from bs4 import BeautifulSoup


def get_xml(url='http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'):
    return requests.get(url).text

def listings_from_xml(xml):
    soup = BeautifulSoup(xml, 'xml')
    for listing in soup.find_all('Listing'):
        yield parse_listing(listing)

def parse_listing(listing_soup):
    listing = {
        column: getattr(listing_soup, column).get_text().strip()
        for column in (
            'MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price',
            'Bedrooms', 'Bathrooms', 'Description')
            # Eventually, we'll want to trim Description to only the first
            # 200 chars, but we need to keep the whole thing around for now
            # because we're deciding whether or not to include it based on
            # whether 'and' is part of the Description. That might be past
            # the 200-char mark, so we can't trim it yet.
    }
    if listing_soup.Appliances:
        listing['Appliances'] = ','.join(
            a.get_text().strip()
            for a in listing_soup.Appliances.find_all('Appliance')
        )
    else:
        listing['Appliances'] = ''

    if listing_soup.Rooms:
        listing['Rooms'] = ','.join(
            r.get_text().strip()
            for r in listing_soup.Rooms.find_all('Room')
        )
    else:
        listing['Rooms'] = ''

    return listing


#CURRENT_YEAR = str(datetime.datetime.now().year)
CURRENT_YEAR = '2016'
def should_include_listing(listing):
    requirements = (
        listing['DateListed'][:4] == CURRENT_YEAR,
        ' and ' in listing['Description'].lower(), # should this be ' and ', with spaces?
        # specs aren't clear, but that makes more sense
    )
    return all(requirements)

def write_csv(listing_dicts, f=sys.stdout):
    fieldnames = (
        'MlsId', 'MlsName', 'DateListed', 'StreetAddress', 'Price', 'Bedrooms',
        'Bathrooms', 'Appliances', 'Rooms', 'Description')
    writer = csv.DictWriter(f, fieldnames)

    writer.writeheader()
    for ld in listing_dicts:
        writer.writerow(ld)

def modify_before_writing(listing_dict):
    listing_dict['Description'] = listing_dict['Description'][:200]
    return listing_dict

def main():
    listings = listings_from_xml(get_xml())
    filtered_listings = ifilter(should_include_listing, listings)
    properly_ordered = sorted(filtered_listings, key=itemgetter('DateListed'))
    ready_to_write = imap(modify_before_writing, properly_ordered)
    write_csv(ready_to_write)

if __name__ == '__main__':
    main()
