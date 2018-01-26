import os
import json
import re
import scrapy
import csv
from easyscrape.easy_parser import easy_parser
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class easy_spider(CrawlSpider):
	# Default Settings
	name = 'easy_spider'

	# Customize functions
	# Hashmap to make sure there's no repetition when parsing url to follow
	global url_hashMap1 # For Rule 1
	global url_hashMap2 # For Rule 2
	url_hashMap1 = dict()
	url_hashMap2 = dict()

	# Load spider settings
	def load_settings(self, settings_obj):
		self.save_html_to_directory = settings_obj["save_html_to_directory"]
		self.save_data_to_csv = settings_obj["save_data_to_csv"]
		self.allowed_domains = settings_obj["allowed_domains"]
		self.start_urls = settings_obj["start_urls"]
		self.csv_output_file = settings_obj["csv_output_file"]
		self.html_directory_name = settings_obj["html_directory_name"]
		self.save_file_regex = settings_obj["save_file_regex"]
		
		# If true, remove url query string when crawling pages		
		global remove_url_query
		remove_url_query = settings_obj["remove_url_query"]
		
		self.allow_page_regex = settings_obj["allow_page_regex"]
		self.deny_page_regex = settings_obj["deny_page_regex"]
		self.randomize_download_delay = settings_obj["randomize_download_delay"]
		self.download_delay = settings_obj["download_delay"]
		self.depth_priority = settings_obj["depth_priority"]
		self.data_extract_path = settings_obj["data_extract_path"]

		# Set crawler settings
		self.custom_settings = {
			'RANDOMIZE_DOWNLOAD_DELAY': self.randomize_download_delay,
			'DOWNLOAD_DELAY': self.download_delay,
			'DEPTH_PRIORITY': self.depth_priority,
		}

		# Spider will start by crawling start_urls
		# If any url match the rules, it will execute the first matched rules and any given callback function
		# If follow=true, it will follow the url that it matches

		# Rules to follow, crawl all pages, repeated pages are process at process_url, callback parse_items if match movie page
		self.rules = (
			Rule(LinkExtractor(process_value=self.process_url1, allow=(self.allow_page_regex), deny=(self.deny_page_regex)), callback='parse_items', follow=True),
			Rule(LinkExtractor(process_value=self.process_url2), follow=True)
		)

		if self.save_data_to_csv:
			self.data_parser = easy_parser(self.data_extract_path, self.csv_output_file)

	# Write content to filename, create directory if it doesn't exist
	def write_html_file(self, filename, content):
		'''
		Create a file name filename and write the content to the file
		'''
		try:
			os.makedirs(re.sub('/[^/]*$', '', filename), exist_ok=True)
		except OSError as ex:
			print("FAILED TO CREATE DIRECTORY: " + re.sub('/[^/]*$', '', filename))
			print(format(ex))
			return

		with open(filename, 'wb') as htmlfile:
			htmlfile.write(content)

	def parse_items(self, response):
		'''
		Parse the response
		Save the body of the response to a unique html file
		Parse the data into an object to be stored in data format (JSON, CSV, XML)
		'''
		# Save the html pages to a folder htmlFiles
		if self.save_html_to_directory:
			page_id = re.search(self.save_file_regex, response.url)

			try:
				filename = self.html_directory_name + '/%s.html' % page_id.group(1).rstrip('/')
				self.write_html_file(filename, response.body)
			except AttributeError as ex:
				print("URL: " + response.url)
				print("has no match for regex: " + self.save_file_regex)
				print(format(ex))

		# Save the data to csv file
		if self.save_data_to_csv:
			self.data_parser.extract_data_to_csv(response.body.decode('utf-8'))

	# Parse the url to be followed, remove query string and disallow repetition (For Rule 1)
	def process_url1(url):
		'''
		Process the url before the spider starts to crawl that page
		Remove the query string and check for repetition
		If that page has not been crawled before, store in dictionary and return url, else return None
		'''
		if not remove_url_query:
			return url

		url = re.sub('^https', 'http', url)
		result = re.match('(.*)\?', url)

		# Make sure that there's no repetition using a dictionary
		if result:
			result_url = result.group(1).strip("/")

			if result_url not in url_hashMap1:
				url_hashMap1[result_url] = None
				return result_url
			else:
				return None
		else:
			if url not in url_hashMap1:
				url_hashMap1[url] = None
				return url
			else:
				return None

	# Parse the url to be followed, remove query string and disallow repetition (For Rule 2)
	def process_url2(url):
		'''
		Process the url before the spider starts to crawl that page
		Remove the query string and check for repetition
		If that page has not been crawled before, store in dictionary and return url, else return None
		'''
		if not remove_url_query:
			return url

		url = re.sub('^https', 'http', url)
		result = re.match('(.*)\?', url)

		# Make sure that there's no repetition using a dictionary
		if result:
			result_url = result.group(1).strip("/")

			if result_url not in url_hashMap2:
				url_hashMap2[result_url] = None
				return result_url
			else:
				return None
		else:
			if url not in url_hashMap2:
				url_hashMap2[url] = None
				return url
			else:
				return None	