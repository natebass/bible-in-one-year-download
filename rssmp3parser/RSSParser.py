import os
import re
from datetime import datetime
from pathlib import Path
from typing import Literal

import pandas as pd
from lxml import etree
from natsort import natsort_keygen
from pydantic import BaseModel, Field

from rssmp3parser.Mp3File import Mp3File


class RSSParser(BaseModel):
    rss_type: str | None
    config_file: str = Literal['rss_mp3_downloader_cache.yml']
    feed_xml: str | None
    feed_url: str | None

    @staticmethod
    def parse_pub_date(item):
        return datetime.strptime(item.xpath("pubDate")[0].text, "%a, %d %b %Y %H:%M:%S %Z").date()

    @staticmethod
    def parse_image(item):
        return \
            item.xpath("itunes:image", namespaces={"itunes": "https://www.itunes.com/dtds/podcast-1.0.dtd"})[0].attrib[
                "href"]

    @staticmethod
    def parse_guid(item):
        return item.xpath("guid")[0].text

    @staticmethod
    def parse_link(item):
        return item.xpath("link")[0].text

    @staticmethod
    def parse_title(item_title):
        return item_title[0].text

    @staticmethod
    def parse_file_path(item_title):
        return Path(f"{item_title[0].text}.mp3")

    @staticmethod
    def parse_description(item):
        return item.xpath("description")[0].text

    @staticmethod
    def get_feed_from_file(filename):
        return etree.parse(filename)

    def save_rss_as_file(self, path, feed_xml=""):
        rss_page_title = feed_xml.xpath("//channel/title/text()")[0]
        if not os.path.exists(rss_page_title):
            with open(f"{rss_page_title}.xml", "wb") as file:
                file.write(etree.tostring(feed_xml))

    def parse_rss(self, feed_file):
        self.feed_xml = etree.parse(feed_file)
        mp3_files = self.parse_rss_for_mp3(self.feed_xml, self.feed_type)

    def get_mp3_files(self, feed_xml, feed_type):
        results = []
        for item in feed_xml.xpath("//item"):
            item_title = item.xpath("title")
            options = {
                "file_path": self.parse_file_path(item_title),
                "name": self.parse_title(item_title),
                "description": self.parse_description(item),
                "link": self.parse_link(item),
                "guid": self.parse_guid(item),
                "image": self.parse_image(item),
                "duration": 1,
                "episode": 1,
                "season": 1,
                "publishedDate": self.parse_pub_date(item)
            }
            results.append(Mp3File(**options))
        if feed_type == 'bioy':
            return self.filter_and_sort_bioy(results)
        else:
            return results

    @staticmethod
    def parse_episode_days(name):
        episode_day = re.findall(r'\d+', name)
        return episode_day[0] if episode_day else None

    def filter_and_sort_bioy(self, mp3_files):
        df = pd.DataFrame([dict(mp3file) for mp3file in mp3_files])
        df['day'] = df['name'].apply(self.parse_episode_days)
        # df = df[(~df['name'].duplicated()) | df['name'].isna()]
        df.drop_duplicates(subset=['day'], keep='first', inplace=True)
        # Bug: natsort_keygen gives Unexpected type warning
        df.sort_values(by='day', key=natsort_keygen(), inplace=True)
        df.drop('day', axis=1, inplace=True)
        return [Mp3File(**config) for config in df.to_dict('records')]
