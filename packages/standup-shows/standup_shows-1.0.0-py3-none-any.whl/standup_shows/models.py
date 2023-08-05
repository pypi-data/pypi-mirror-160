from datetime import datetime
from typing import List
import logging
import fire


class Show:
    """Created by scraping dead-frog.com."""

    def __init__(self, venue: str, date: datetime, tickets_url: str = None):
        """
        Create a new Show.
        
        :param venue: The venue that this Show is taking place at.
        :param date: The date and time that this Show is taking place at.
        :param tickets_url: A URL to purchase tickets for this Show at.
        """
        self.venue = venue
        self.date = date
        self.tickets_url = tickets_url

    @classmethod
    def fromtag(cls, tag: 'bs4.tag') -> 'Show':
        """
        Create a new Show from a BeautifulSoup4 tag.

        :param tag: A BeautifulSoup4 tag obtained from scraping https://www.dead-frog.com/live-comedy/shows/.
        :returns: A Show object.
        :raises AttributeError: If a required attribute cannot be scraped from the tag.
        """
        base_url = 'https://www.dead-frog.com'
        tickets_url = None
        # Parse venue.
        try:
            event_tag = tag.find(class_='comic_venue')
            venue = event_tag.find('a').text.strip()
        except:
            raise AttributeError("Couldn't find the venue for this event.")

        # Parse date.
        try:
            time_part = tag.find(class_='col-xs-12 showtime_line').text.strip()
        except:
            logging.error("Couldn't find the showtime for this event.")
        try:
            date_part = tag.find_previous_sibling(class_='day_head').text.replace(' | ', ', ')
        except:
            raise AttributeError("Couldn't find the date for this event.")
        date = datetime.strptime(date_part + ' ' + time_part, '%A, %B %d %I:%M %p')
        if date.month > datetime.now().month:
            date = date.replace(year=datetime.now().year)
        else:
            date = date.replace(year=datetime.now().year + 1)

        # Parse tickets_url.
        try:
            tickets_uri = tag.find(class_='btn btn-sm btn-custom')['href']
            tickets_url = base_url + tickets_uri
        except:
            logging.error("Couldn't find the tickets link for this event.")

        return cls(venue, date, tickets_url)

    def __repr__(self) -> str:
        return str(vars(self))

    def __str__(self) -> str:
        return f'{self.venue} - {self.date.strftime("%A, %B %d at %I:%M %p")} - {self.tickets_url}'


class Comedian:
    """Created from the user's list of comedians. Used to group output of `standup.py`."""

    def __init__(self, name: str, shows: List[Show] = None):
        """
        Create a new Comedian.
        
        :param name: The name of the Comedian.
        :param shows: A list of Show objects that the Comedian is scheduled to perform at.
        """
        self.name = name
        self.shows = shows or []

    def __str__(self):
        """Return a string representation of the Comedian and their Shows."""
        out = f'{self.name}:\n'
        for show in self.shows:
            out += f'    {show}\n'
        return out + '\n'

    def __repr__(self):
        return f'<{self.name} {len(self.shows)}>'


if __name__ == '__main__':
    fire.Fire()
