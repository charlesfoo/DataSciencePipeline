# Documentation

```
easyscrape {download, run, scrapefile, scrapedirectory}
```

## 1) download
```
easyscrape download (url)
```
Function: Download the whole domain of the given url  
url: The absolute url of the domain

## 2) scrapefile
```
easyscrape scrapefile (file) (data_extract_path)
```
Function: Crawl the given file and extract data to csv  
file: Name of the file, most likely to be a html file  
data_extract_path: JSON file that contains an array of (colName, xPathString)  

### data_extract_path object format:
```json
[
	{
		"colName": "column name for csv",
		"xPathString": "xpath to the data you want to extract"
	},
	{
		"colName": "Column 1",
		"xPathString": "//div/text()"
	}
]
```
Basically, it will crawl the url given and extract any data that match the given xpath into the csv column  

## 3) scrapedirectory
```
easyscrape scrapedirectory (directory) (data_extract_path)
```
Function: Crawl all the files in the directory and extract data to csv  
directory: Name of the directory  
data_extract_path: JSON file that contains an array of (colName, xPathString)  

## 4) run
```
easyscrape run (settings)
```
Function: Run the given settings file, default settings is used if setting is not given  

#### Some examples of settings file: [imdb.json](https://github.com/xpheal/easyscrape/blob/master/test/imdb.json) | [rotten.json](https://github.com/xpheal/easyscrape/blob/master/test/rotten.json) | [cars.json](https://github.com/xpheal/easyscrape/blob/master/test/cars.json)  
#### Some examples of results in CSV: [IMDB_scrape_data.csv](https://github.com/xpheal/easyscrape/blob/master/test/IMDB_scrape_data.csv) | [Rotten_scrape_data.csv](https://github.com/xpheal/easyscrape/blob/master/test/Rotten_scrape_data.csv) | [cars.csv](https://github.com/xpheal/easyscrape/blob/master/test/cars.csv)

### Default settings:
```json
{	
	"save_html_to_directory": false,
	"save_data_to_csv": false,
	"allowed_domains": [],
	"start_urls": [],
	"csv_output_file": "scrape_data.csv",
	"html_directory_name": "HTMLFiles",
	"save_file_regex": ".*",
	"remove_url_query": false,
	"deny_page_regex": [],
	"allow_page_regex": [],
	"randomize_download_delay": 0,
	"download_delay": 0,
	"depth_priority": 1,
	"data_extract_path": null
}
```

### 1. save_html_to_directory | Value: boolean  
If True, download pages into the directory, If False, do nothing.  
Name of directory: (html_directory_name)  
Pages allowed: (allow_page_regex) - (deny_page_regex)  
Page naming: (save_file_regex)  

### 2. save_data_to_csv | Value: boolean  
If True, extract data from pages that match the XPath and save them in CSV, If False, do nothing.  
Name of CSV output file: (csv_output_file)  
Pages allowed: (allow_page_regex) - (deny_page_regex)  
XPath to match: (data_extract_path)  

### 3. allowed_domains | Value: array of strings  
An array of domains that the spider is allowed to crawl  
The spider will not visit domains that are not listed in (allowed_domains)  
Examples:  
```
["www.facebook.com"]  
["waynedev.me"]  
["quotes.toscrape.com", "www.google.com", "www.facebook.com"]  
```

### 4. start_urls | Value: array of strings  
An array of absolute urls for the spider to start crawling  
The spider will start crawling from this list of urls  
Examples:
```
["https://www.facebook.com"]  
["http://quotes.toscrape.com", "https://www.wikipedia.org"]  
["https://docs.python.org/3/library/index.html"]  
```

### 5. csv_output_file | string  
Name of the csv output file to store the extracted data  

### 6. html_directory_name | string  
Name of the directory to store the downloaded html pages  

### 7. save_file_regex | string  
Regex to match the url and use it as the name of the html file  
The first regex group that is matched with the url will be used  
Filepath = working_directory/html_directory_name/matched_regex.html  
Example:  
```
url: "http://quotes.toscrape.com/tag/love/page/2"
regex: "([^/]+)$" (match the last word that does not contain "/")
filename: "2.html"

url: "http://quotes.toscrape.com/tag/love/page/2"
regex: "([^/]/[^/]/[^/]+)$" (match the last three words of the url divided by two "/")
filename: "love/page/2.html"
full file path: working_directory/html_directory_name/love/page/2.html
```

### 8. remove_url_query | boolean  
If True, remove the url query string when the spider crawls, else, do nothing.  

### 9. deny_page_regex | array of strings  
List of regex to filter of urls  
If any of the regex matches the url, the page will not be downloaded or data will not be extracted from that page.  
But, the spider will still crawl through that page.  
Example:  
```
deny_page_regex = ["/news/", "/list/", "/[0-9]+/"]
Example pages that will be denied:
http://www.example.com/news/
http://www.example.com/ex1/123423/example
```

### 10. allow_page_regex | array of strings  
List of regex to match pages that will be downloaded or will have their data extracted  
Only if the regex matches the url, the page will be downloaded or data will be extracted.  
Keep in mind that (deny_page_regex) has higher priority  
Example:
```
allow_page_regex = ["/page/[0-9]+"]
Example pages that will be allowed:
http://www.example.com/page/12312
```

### 11. randomize_download_delay | 0 or 1
If 0, the download delay is not randomized, if 1, the download delay is randomized  
Cause the spider crawling speed to be random, prevent getting blocked for crawling    

### 12. download_delay | seconds
Control the crawling speed of the spider, the amount of time it takes for the spider to crawl the next url  
To decrease the chances of getting block by certain websites  
If set to 0, there will be no delay

### 13. depth_priority | integer
If 0, no priority adjustment for depth, a depth first crawl  
If positive integer, will prioritize lower depth request, breadth first crawl  

### 14. data_extract_path | array of (colName, xPathString)  
An array of (colName, xPathString) object to specify data to be extracted  
Only pages that are allowed by (allow_page_regex) and (deny_page_regex) will have their data extracted  
colName: Name of the column of in the csv file  
xPathString: XPath to the data you want to extract, will written to its csv column  
Example:
```json
[
	{
		"colName": "column name for csv",
		"xPathString": "xpath to the data you want to extract"
	},
	{
		"colName": "Column 1",
		"xPathString": "//div/text()"
	}
]
```