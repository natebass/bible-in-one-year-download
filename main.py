import sys

from RSSParser import download_episode


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
