import glob
import os
from datetime import datetime
from io import BytesIO
from pathlib import Path

import requests
from lxml import etree

from Mp3File import Mp3File


def get_feed_from_download(rss_feed_url):
    rss_feed_data = requests.get(rss_feed_url)
    return etree.parse(BytesIO(rss_feed_data.content))


def save_rss_as_file(feed_xml):
    rss_page_title = feed_xml.xpath("//channel/title/text()")[0]
    if not os.path.exists(rss_page_title):
        with open(f"{rss_page_title}.xml", "wb") as file:
            file.write(etree.tostring(feed_xml))


def parse_rss_for_mp3(feed_xml):
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
    return results


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


def download_file_image(files):
    files
    pass


def get_feed_from_file(filename):
    return etree.parse(filename)


def download_episode(episode_number):
    rss_file = next(glob.iglob("*.xml"), False)
    if rss_file:
        feed_xml = etree.parse(rss_file)
    else:
        feed_xml = etree.parse("https://media.rss.com/bibleinoneyear/feed.xml")
        save_rss_as_file(feed_xml)
    mp3_files = parse_rss_for_mp3(feed_xml)
    download_file_image(mp3_files)
    # file = FLAC(path_flac)
    # art = file.pictures[0].data
    # audio = MP3(path_mp3, ID3=ID3)
    # # audio.tags.add(APIC(encoding=0))
    # audio.tags.add(APIC(encoding=3, mime="image/png", type=3, desc=u"Cover", data=art))
    # audio.save()
