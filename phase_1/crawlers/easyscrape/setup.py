from setuptools import setup, find_packages

setup(
	name = 'easyscrape',
	version = '0.25',
	packages = find_packages(),
	install_requires=[
		'scrapy',
	],
	entry_points={
		'console_scripts': ['easyscrape=easyscrape.easy_scrape:main']
	},

	# metadata
	author = 'Wayne Chew',
	author_email = 'xpheal@gmail.com',
	description = 'Easy to use web scraper',
	license = 'GPL',
	url = 'https://github.com/xpheal/easyscrape',
)