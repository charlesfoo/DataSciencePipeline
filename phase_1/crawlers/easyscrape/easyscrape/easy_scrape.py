#!/usr/bin/env python3
import json
import re
import sys
import argparse
import scrapy
from scrapy.crawler import CrawlerProcess
from easyscrape.easy_spider import easy_spider
from easyscrape.easy_parser import easy_parser
import easyscrape.easy_settings as easy_settings

def start_crawler(settings_obj):
	process = CrawlerProcess({
		'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; WINDOWS NT 5.1'
	})

	# Load spider settings
	easy_spider.load_settings(easy_spider, settings_obj)

	# Start crawling
	process.crawl(easy_spider)
	process.start()

# Download argument
def download(args):
	start_crawler(get_download_settings_obj(args.url))

# Run argument
def run(args):
	start_crawler(easy_settings.get_settings_from_file(args.settings))

# ScrapeFile argument
def scrapeFile(args):
	settings_obj = (easy_settings.get_settings_from_file(args.settings))

	data_parser = easy_parser(settings_obj['data_extract_path'], settings_obj['csv_output_file'])
	data_parser.extract_file(args.file)

# ScrapeDirectory argument
def scrapeDirectory(args):
	settings_obj = (easy_settings.get_settings_from_file(args.settings))
	
	data_parser = easy_parser(settings_obj['data_extract_path'], settings_obj['csv_output_file'])
	data_parser.extract_directory(args.directory)

def main():
	# Parser
	parser = argparse.ArgumentParser(prog='easyscrape', description='Download or scrape the given url, see documentation for more info.')
	subparsers = parser.add_subparsers(title='command', dest='cmd', description='Command for easyscrape, choose from download, run, scrapefile or scrapedirectory')
	subparsers.required = True

	run_parser = subparsers.add_parser('run', help='Run the scraper using the settings file')
	run_parser.add_argument('settings', help='Settings to be loaded')
	run_parser.set_defaults(func=run)

	download_parser = subparsers.add_parser('download', help='Download all the html files and save it in a directory')
	download_parser.add_argument('url', help='Start crawling from this url')
	download_parser.set_defaults(func=download)

	scrape_parser = subparsers.add_parser('scrapefile', help='Scrape data from a html file to a csv file')
	scrape_parser.add_argument('file', help='Scrape data from this html file')
	scrape_parser.add_argument('settings', help='Settings to be loaded, only data_extract_path is needed')
	scrape_parser.set_defaults(func=scrapeFile)

	scrape_parser = subparsers.add_parser('scrapedirectory', help='Scrape data from a directory of html files to a csv file')
	scrape_parser.add_argument('directory', help='Scrape data from this directory')
	scrape_parser.add_argument('settings', help='Settings to be loaded, only data_extract_path is needed')
	scrape_parser.set_defaults(func=scrapeDirectory)

	# Parse arguments
	args = parser.parse_args()

	args.func(args)

if __name__ == '__main__':
	main()