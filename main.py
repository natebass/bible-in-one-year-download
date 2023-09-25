from os import path, mkdir, remove, listdir
from pathlib import Path
from lxml import etree
from rssmp3parser.CommandLineArguments import CommandLineArguments
from rssmp3parser.RSSMp3Downloader import RSSMp3Downloader
from rssmp3parser.RSSParser import RSSParser
from rssmp3parser.RSSType import parse_rss_type


def print_error(error_message: str):
    """Print cli errors, library exceptions, and other error messages to the console.
    :parameter error_message: str The error message text
    """
    print(error_message)


def parse_arguments():
    """Parse arguments passed to the CLI and define the type of RSS feed to parse.
    NOTE: This file needs to be robustly tested because it handles raw user input.
    :return: (arguments: CommandLineArguments, rss_type: str) Return the parsed command line arguments and RSS type.
    """
    arguments = CommandLineArguments()
    rss_type = parse_rss_type('')
    # Implicit arguments

    # Explicit arguments are placed after implicit arguments, thus override what was previously defined.
    arguments.download_all = Path(__file__).parent / 'Audio Files'
    arguments.episode = Path(__file__).parent / 'Audio Files'
    arguments.number_of_episodes = Path(__file__).parent / 'Audio Files'
    arguments.cache_enabled = Path(__file__).parent / f'{rss_type}.xml'
    arguments.remove_cache = Path(__file__).parent / f'{rss_type}.xml'
    arguments.feed_url = Path(__file__).parent / f'{rss_type}.xml'
    arguments.audio_files_directory = Path(__file__).parent / 'Audio Files'
    return arguments, rss_type


def main():
    """Download Bible in One Year episodes. This script is meant to be run through a command line.
    TIP: This is not an ordinary file. This is meant to be verbose and the main point of coding. Other files should be refactored to expose their configurations to here.
    MARKDOWN:
    # Bible in One Year podcast downloader CLI
    ## Numbered arguments
    1. cli-argument str episode_number: The episode to be downloaded.
    2. cli-argument str rss_file: Either the URL or the file path of a local RSS file.
    ## Explicit arguments
    * --cache-enabled bool: Specify whether to cache RSS file information
    * --download_all
    * --episode
    * --number_of_episodes
    * --remove_cache
    * --feed_url
    * --audio_files_directory
    """
    # Create an RSSParser based on the arguments passed to the CLI
    arguments, rss_type = parse_arguments()
    # Parse RSS file
    if arguments.go:
        etree.parse(arguments.feed_url)
        rss_parser = RSSParser(rss_type=rss_type, feed_xml=arguments.feed_url)
        #  Handle caching data about the RSS file
        mkdir(arguments.audio_files_directory)
        if arguments.cache_enabled:
            rss_parser.save_rss_as_file(Path.cwd())
        elif arguments.remove_cache:
            for file in listdir('.'):
                if file.endswith('.xml') or file.endswith('.rss') or file == rss_parser.config_file:
                    remove(file)
        # Download the files
        downloader = RSSMp3Downloader(mp3_files=rss_parser.get_mp3_files(), episode_number=arguments.episode,
                                      audio_files_directory=arguments.audio_files_directory)
        if arguments.download_all:
            try:
                downloader.download_all_episodes()
            except Exception as exception:
                print_error(str(exception))
        else:
            try:
                downloader.download_episode(arguments.episode)
            except Exception as exception:
                print_error(str(exception))


if __name__ == '__main__':
    main()
