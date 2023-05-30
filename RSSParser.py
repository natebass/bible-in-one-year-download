import glob
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path
import re
import requests
from lxml import etree
import pandas as pd
from mutagen.flac import FLAC
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from natsort import natsort_keygen

from Mp3File import Mp3File


def save_rss_as_file(feed_xml):
    rss_page_title = feed_xml.xpath("//channel/title/text()")[0]
    if not os.path.exists(rss_page_title):
        with open(f"{rss_page_title}.xml", "wb") as file:
            file.write(etree.tostring(feed_xml))


def parse_pub_date(item):
    return datetime.strptime(item.xpath("pubDate")[0].text, "%a, %d %b %Y %H:%M:%S %Z").date()


def parse_image(item):
    return item.xpath("itunes:image", namespaces={"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"})[0].attrib[
        "href"]


def parse_guid(item):
    return item.xpath("guid")[0].text


def parse_link(item):
    return item.xpath("link")[0].text


def parse_title(item_title):
    return item_title[0].text


def parse_file_path(item_title):
    return Path(f"{item_title[0].text}.mp3")


def parse_description(item):
    return item.xpath("description")[0].text


def get_feed_from_file(filename):
    return etree.parse(filename)


def p(name):
    episode_day = re.findall(r'\d+', name)
    return episode_day[0] if episode_day else None


def parse_rss_for_mp3(feed_xml, feed_type):
    results = []
    for item in feed_xml.xpath("//item"):
        item_title = item.xpath("title")
        options = {
            "file_path": parse_file_path(item_title),
            "name": parse_title(item_title),
            "description": parse_description(item),
            "link": parse_link(item),
            "guid": parse_guid(item),
            "image": parse_image(item),
            "duration": 1,
            "episode": 1,
            "season": 1,
            "publishedDate": parse_pub_date(item)
        }
        results.append(Mp3File(**options))
    if feed_type is 'bioy':
        return filter_and_sort_bioy(results)
    else:
        return results


def download_file_image(image_url, image_file_path):
    response = requests.get(image_url, timeout=0.5)
    if response.status_code == 200:
        with open(image_file_path, 'wb') as file:
            file.write(response.content)
    else:
        pass


def parse_image_url_for_file_name(image_url):
    return image_url.rsplit('/', 1)[-1]


def handle_image(image_url, image_urls):
    image_file = parse_image_url_for_file_name(image_url)
    if image_url not in image_urls:
        download_file_image(image_url, image_file)
    return image_file


def download_episode(episode_number, rss_file, feed_type='bioy'):
    # Todo: Prompt "There is an xml file in your current directory. Would you like to use that next time by running ..."
    rss_file = next(glob.iglob("*.xml"), False)
    if rss_file:
        feed_xml = etree.parse(rss_file)
    else:
        feed_xml = etree.parse("https://media.rss.com/bibleinoneyear/feed.xml")
        save_rss_as_file(feed_xml)
    mp3_files = parse_rss_for_mp3(feed_xml, feed_type)
    mp3_file = mp3_files[episode_number]
    image_urls = []
    filenames = glob.glob("*.txt")
    image_file_path = handle_image(mp3_file.image, image_urls)
    # for mp3_file in mp3_files:
    #     handle_image(mp3_file.image)
    file = FLAC(image_file_path)
    art = file.pictures[0].data
    audio = MP3(mp3_file.file_path, ID3=ID3)
    # audio.tags.add(APIC(encoding=0))
    audio.tags.add(APIC(encoding=3, mime="image/png", type=3, desc=u"Cover", data=art))
    audio.save()


def filter_and_sort_bioy(mp3_files):
    df = pd.DataFrame([dict(mp3file) for mp3file in mp3_files])
    df['day'] = df['name'].apply(p)
    # df = df[(~df['name'].duplicated()) | df['name'].isna()]
    df.drop_duplicates(subset=['day'], keep='first', inplace=True)
    # Bug: natsort_keygen gives Unexpected type warning
    df.sort_values(by='day', key=natsort_keygen(), inplace=True)
    df.drop('day', axis=1, inplace=True)
    return [Mp3File(**config) for config in df.to_dict('records')]
