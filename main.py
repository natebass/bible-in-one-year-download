import sys

import requests
import os
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import unquote, urlparse
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from pydantic import BaseModel
from lxml import etree
from io import StringIO, BytesIO


class Mp3File(BaseModel):
    file_path: Path
    name = str


def get_feed(rss_feed_url):
    rss_feed_data = requests.get(rss_feed_url)
    return etree.parse(BytesIO(rss_feed_data.content))


def save_rss_as_file(feed_xml):
    rss_page_title = feed_xml.xpath("//channel/title/text()")[0]
    if not os.path.exists(rss_page_title):
        with open(f"{rss_page_title}.xml", "wb") as file:
            file.write(etree.tostring(feed_xml))


def parse_rss_for_mp3(feed_xml):
    results = []
    for item in feed_xml.find_elements_by_xpath("//item"):
        item_title = item.xpath("//title")
        mp3_file = Mp3File(file_path=f"{item_title}.mp3", name=item_title[0], description=item.xpath("//description"),
        item.xpath
    results
    # file = FLAC(path_flac)
    # art = file.pictures[0].data
    # audio = MP3(path_mp3, ID3=ID3)
    # # audio.tags.add(APIC(encoding=0))
    # audio.tags.add(APIC(encoding=3, mime='image/png', type=3, desc=u'Cover', data=art))
    # audio.save()


def download_episode(episode_number):
    feed_xml = get_feed("https://media.rss.com/bibleinoneyear/feed.xml")
    save_rss_as_file(feed_xml)  # For debugging purposes
    parse_rss_for_mp3(feed_xml)


def main():
    '''
    Python script to be run in the console
    '''
    print(*sys.argv)
    if len(sys.argv) != 2:
        print("This script requires one argument.")

    argument1 = sys.argv[1]
    download_episode(argument1)


if __name__ == '__main__':
    main()

# audio_files_folder = Path.joinpath(Path(__file__).parent, "Audio Files")
# if not Path.exists(audio_files_folder):
#     os.mkdir(audio_files_folder)
#
# entries = parse_bioy_feed_for_mp3(requests.get(rss_feed).text)
# for audio_file_link in entries:
#     response = requests.get(audio_file_link)
#     mp3_file = Path.joinpath(audio_files_folder, Path(unquote(urlparse(audio_file_link).path)).parts[-1])
#     if not Path.exists(mp3_file):
#         with open(mp3_file, "wb") as file:
#             file.write(response.content)
#     raise "a"
#
