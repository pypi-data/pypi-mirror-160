from dataclasses import dataclass

import bs4
from models import PodcastValue
from typing import Optional
from bs4 import BeautifulSoup

import requests


@dataclass
class FeedService:

    provider = requests.request

    def value_block(self, feed_url) -> Optional[PodcastValue]:
        response = self.provider.get(feed_url)

        if response.status_code != requests.status_codes.codes.ok:
            return

        try:
            feed_soup = BeautifulSoup(response.text, "lxml")
        except:
            return

        podcast_value_soup = next(
            iter(feed_soup.find_all("podcast:value", recursive=True, limit=True)), None
        )
        if podcast_value_soup is None:
            return
