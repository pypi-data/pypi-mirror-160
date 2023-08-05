#!/usr/bin/env python3
"""Standup CLI"""

from bs4 import BeautifulSoup
from .models import Comedian
from .models import Show
import concurrent.futures
import requests
import logging
import fire
import os


logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
if os.environ.get('ENVIRONMENT', 'production') == 'production':
    logging.disable(logging.INFO)


def standup(comedians: str, zipcode: int, radius: int = 25, max_threads: int = 100) -> None:
    """
    Find stand-up comedy shows that your favorite comedians are scheduled to perform near you.
    
    :param comedians: A filepath containing a newline-delimited list of comedians in the form of <firstname lastname>.
    :param zipcode: The zipcode to search near.
    :param radius: The radius in miles around the zipcode to search.
    :param max_threads: The maximum number of threads to create. A new thread is created for each URL to scrape.
    """
    # Input handling
    url = f'https://www.dead-frog.com/live-comedy/shows/{zipcode}/{radius}'
    with open(comedians, 'r') as infile:
        comedians_ = [Comedian(name.strip()) for name in infile.readlines()]
        logging.info(comedians_)

    def search_events(page: int) -> None:
        resp = requests.get(f'{url}/P{page}')
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Search all events on the page.
        event_records = soup.find_all(class_='event_row row')
        for tag in event_records:
            try:
                comedian_name = tag.find(class_='show_name').text.strip()
                logging.info(comedian_name)
            except:
                logging.error('Error locating comedian for this event.')
                continue
            for comedian in comedians_:
                if comedian_name == comedian.name:
                    try:
                        comedian.shows.append(Show.fromtag(tag))
                    except AttributeError:
                        logging.error("Couldn't create a show from this tag.")

    # Find the range of pages required to search.
    first_page = requests.get(url)
    soup = BeautifulSoup(first_page.text, 'html.parser')
    last_page_url = soup.find('a', text='Last ›')['href']
    last_page_number = int(last_page_url.split('/')[-1][1:])
    # Create a single thread for each URL to search. The site will only display 20 events at a time.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(search_events, range(0, last_page_number+1, 20))

    # Output handling
    for c in comedians_:
        if c.shows:
            print(c)


def main():
    fire.Fire(standup)


if __name__ == '__main__':
    main()
