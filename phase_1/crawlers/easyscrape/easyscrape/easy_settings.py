import re
import json
import sys

# Return default settings for spider
def get_default_settings_obj():
	settings_obj = {}
	settings_obj["save_html_to_directory"] = False
	settings_obj["save_data_to_csv"] = False
	settings_obj["allowed_domains"] = []
	settings_obj["start_urls"] = []
	settings_obj["csv_output_file"] = "scrape_data.csv"
	settings_obj["html_directory_name"] = "HTMLFiles"
	settings_obj["save_file_regex"] = None
	settings_obj["remove_url_query"] = False
	settings_obj["allow_page_regex"] = None
	settings_obj["deny_page_regex"] = None
	settings_obj["randomize_download_delay"] = 0
	settings_obj["download_delay"] = 0
	settings_obj["depth_priority"] = 1
	settings_obj["data_extract_path"] = None
	return settings_obj

# Download argument
def get_download_settings_obj(url):
	settings_obj = get_default_settings_obj()
	settings_obj["save_html_to_directory"] = True
	settings_obj["start_urls"] = [url]
	settings_obj["allowed_domains"] = [re.match('https?:\/\/([^/]+)', url).group(1)]
	settings_obj["html_directory_name"] = "HTMLFiles"
	settings_obj["save_file_regex"] = "https?:\/\/(.*)"
	settings_obj["remove_url_query"] = False

	return settings_obj

def get_settings_from_file(settings_file_name):
	settings_obj = None

	try:
		with open(settings_file_name, 'r') as jFile:
			settings_obj = json.load(jFile)
	except FileNotFoundError as ex:
		print("SETTINGS FILE NOT FOUND")
		sys.exit(-1)
	except ValueError as ex:
		print("SETTINGS FILE CORRUPTED OR INVALID JSON FORMAT")
		sys.exit(-1)

	return add_default_settings(settings_obj)

# Given the settings_obj, add default settings to fill up empty settings
def add_default_settings(settings_obj):
	temp_settings_obj = get_default_settings_obj()

	for key, value in settings_obj.items():
		temp_settings_obj[key] = value

	return temp_settings_obj