import glob
from pathlib import Path

import requests
from mutagen.flac import FLAC
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3
from pydantic import BaseModel

from rssmp3parser.Mp3File import Mp3File


class RSSMp3Downloader(BaseModel):
    mp3_files: Mp3File
    episode_number: int = 0
    audio_files_directory: Path

    def download_episode(self, episode):
        pass

    def download_all_episodes(self):
        mp3_file = self.mp3_files[self.episode_number]
        image_urls = []
        filenames = glob.glob("*.txt")
        image_file_path = self.handle_image(mp3_file.image, image_urls)
        # for mp3_file in mp3_files:
        #     handle_image(mp3_file.image)
        file = FLAC(image_file_path)
        art = file.pictures[0].data
        audio = MP3(mp3_file.file_path, ID3=ID3)
        audio.tags.add(APIC(encoding=3, mime="image/png", type=3, desc=u"Cover", data=art))
        audio.save()

    @staticmethod
    def download_file_image(image_url, image_file_path):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_file_path, 'wb') as file:
                file.write(response.content)
        else:
            pass

    @staticmethod
    def parse_image_url_for_file_name(image_url):
        return image_url.rsplit('/', 1)[-1]

    def handle_image(self, image_url, image_urls):
        image_file = self.parse_image_url_for_file_name(image_url)
        if image_url not in image_urls:
            self.download_file_image(image_url, image_file)
        return image_file
    # entries = parse_bioy_feed_for_mp3(requests.get(rss_feed).text)
    # for audio_file_link in entries:
    #     response = requests.get(audio_file_link)
    #     mp3_file = path.joinpath(audio_files_folder, path(unquote(urlparse(audio_file_link).path)).parts[-1])
    #     if not path.exists(mp3_file):
    #         with open(mp3_file, "wb") as file:
    #             file.write(response.content)
    #     raise "a"
