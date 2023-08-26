from os import path, mkdir, remove, listdir
from pathlib import Path

from lxml import etree

from rssmp3parser.CommandLineArguments import CommandLineArguments
from rssmp3parser.RSSMp3Downloader import RSSMp3Downloader
from rssmp3parser.RSSParser import RSSParser
from rssmp3parser.RSSType import parse_rss_type


def print_error(error_message):
    """
    Print cli errors, library exceptions, and other error messages to the console.
    :parameter str error_message: The error message text
    """
    print(error_message)


def create_directory(directory):
    """
    Check if valid directory and create if it doesn't already exist.
    :parameter Path directory: The error message text
    """
    if not path.exists(directory):
        mkdir(directory)


def parse_arguments():
    """
    Parse arguments passed to the CLI. Configure an RSSParser during this process.
    :return RSSParser: A class that fetches and parses the required RSS file.
    """
    arguments = CommandLineArguments()
    rss_type = parse_rss_type('')
    # TODO: Add parameter [int] for days. 1 is one day ahead and back. -1 is behind. +1 is future.
    # if (arguments_count := len(sys.argv)) < 2:
    #     print_error('This script requires at least one argument.')
    #     raise SystemExit(2)
    # argument1 = sys.argv[1]
    # argument2 = sys.argv[2]
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--bar', help='Do the bar option')
    # parser.add_argument('--foo', help='Foo the program')
    # args = parser.parse_args()
    # print(f'Args: {args}\nCommand Line: {sys.argv}\nfoo: {args.foo}')
    # print(f'Dict format: {vars(args)}')
    arguments.audio_files_directory = Path(__file__).parent / 'Audio Files'
    arguments.feed_url = Path(__file__).parent / f'{rss_type}.xml'
    return arguments, rss_type


def main():
    """
    Download Bible in One Year episodes. This script is meant to be run through a command line.
    1. cli-argument str episode_number: The episode to be downloaded.
    2. cli-argument str rss_file: Either the URL or the file path of a local RSS file.
    * --cache-enabled bool: Specify whether to cache RSS file information
    """
    # 1. Create an RSSParser based on the arguments passed to the CLI
    arguments, rss_type = parse_arguments()
    # 2. Parse RSS file
    # etree.parse(arguments.feed_url)
    # rss_parser = RSSParser(rss_type=rss_type, feed_xml=arguments.feed_url)
    # # 2. Handle caching data about the RSS file
    # create_directory(arguments.audio_files_directory)
    # if arguments.cache_enabled:
    #     rss_parser.save_rss_as_file(Path.cwd())
    # elif arguments.remove_cache:
    #     for file in listdir('.'):
    #         if file.endswith('.xml') or file.endswith('.rss') or file == rss_parser.config_file:
    #             remove(file)
    # # 3. Download the files
    # downloader = RSSMp3Downloader(mp3_files=rss_parser.get_mp3_files(), episode_number=arguments.episode,
    #                               audio_files_directory=arguments.audio_files_directory)
    # if arguments.download_all:
    #     try:
    #         downloader.download_all_episodes()
    #     except Exception as exception:
    #         print_error(str(exception))
    # else:
    #     try:
    #         downloader.download_episode(arguments.episode)
    #     except Exception as exception:
    #         print_error(str(exception))


if __name__ == '__main__':
    main()

# else:
#     print_error('Please specify and episode.')
#     raise SystemExit(2)
# if next(glob.iglob('*.xml'), False):
#     raise Exception('There is an xml file in your current directory. Would you like to use that next time by '
#                     'running main.py -f <rss_file>?')
