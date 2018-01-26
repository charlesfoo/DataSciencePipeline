#!/usr/bin/env python3
import csv
import json
from io import StringIO
from lxml import etree
from os import listdir

class easy_parser():
	def __init__(self, data_extract_path, csv_file):
		self.csv_file = open(csv_file, 'w')

		self.settings_func = []
		for i in data_extract_path:
			self.settings_func.append(etree.XPath(i['xPathString']))

		self.csv_writer = csv.writer(self.csv_file)

		self.csv_writer.writerow([i['colName'] for i in data_extract_path])

	def extract_data_to_csv(self, html_string):
		data_row = self.extract_data(html_string)
		self.csv_writer.writerow(data_row)

	def extract_data(self, html_string):
		tree = etree.parse(StringIO(html_string), etree.HTMLParser())

		data_row = []

		for i in self.settings_func:
			data = i(tree)

			if len(data) <= 0:
				data_row.append(None)
			else:
				data_row.append(",".join(data).strip())

		return data_row

	def extract_file(self, file):
		with open(file, 'r') as f:
			self.extract_data_to_csv(f.read())

	def extract_directory(self, directory):
		for file_name in listdir(directory):
			with open(directory + '/' + file_name, 'r') as f:
					print(file_name)
					self.extract_data_to_csv(f.read())

	def __del__(self):
		self.csv_file.close()