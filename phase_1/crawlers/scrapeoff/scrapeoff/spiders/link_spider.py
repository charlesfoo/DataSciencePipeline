import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import csv

class linkSpider(CrawlSpider):
	name='link'

	global url_dict
	global remove_url_query

	csv_id=0

	url_dict={}


	#FILL IN THESE VALUE BEFORE PROCEEDING TO CRAWL

	remove_url_query=False         #if true, removes the query string ?search=...

	save_html_to_directory=True   #saves html scrapped to folder

	save_data_to_csv=True   #convert data scrapped to csv format


	allowed_domains=['www.rottentomatoes.com']    #subject to change
	start_urls=['https://www.rottentomatoes.com']           #subject to change
	#allow_regex=["\/m\/\w+\/?$","\/tv\/\w+\/\w+\/?$"]
	#allow_regex=["\/m\/.*\/?$"]
	#allow_regex=["\/m\/.*\/?$","\/tv\/\w+\/s\d+\/?$"]
	allow_regex=["\/m\/.*\/?$"]
	#deny_regex=["\/m\/.*\/\?.*\=.*\/?","\/m\/.*\/trailers\/.*\/?","\/m\/.+\/.+\/?"]
	#deny_regex=["\/m\/trailers.*\/?","\/m\/.*\/\?.*\=.*\/?" ,"\/m\/.*\/\d{8}\/?"]
	deny_regex=["\/m\/\w+\/\w+\/?"]

	global csv_filename
	csv_filename="rottentomatoes"    		#subject to change



	#BREADTH FIRST SEARCH
	#	depth_priority=1
	#   Uncomment scheduler_disk_queue and scheduler_memory_queue
	custom_settings={
			'DEPTH_PRIORITY':1,    
			'SCHEDULER_DISK_QUEUE':'scrapy.squeues.PickleFifoDiskQueue',
			'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
			'DOWNLOAD_DELAY':0.1,
			'RANDOMIZE_DOWNLOAD_DELAY':1,
			}

	def process_url(url):
		#Remove query string, eg, string that have http://www.imdb.com/ironman/?1234
		#Remove that ?1234


		if remove_url_query==False:
			return url

		# if remove_url_query==True:
		#Check if it has query string. query string usually have a "?" at the back
		result=re.match("(https?:\/\/.*)\?",url)

		#TO BE ADDED: if https, how? If http, how?

		#if has query string
		if result:
			#remove that "/" at the beginning and at the end of string
			final_result=result.group(1).strip("/")
			#if the url we haven't crawled before, keep it in dictionary to avoid duplication. 
			#The unique=true in Rule won't help because "Iron Man" with query string is equals to "Iron Man" wihout query string
			#What we are doing here is to remove query string only check if there's any duplication
			if final_result not in url_dict:
				url_dict[final_result]=None
				return final_result
			else:
				return None
		#if the link doesn't have any query string
		else:
			if url not in url_dict:
				url_dict[url]=None
				return url
			else:
				return None
		# elif remove_url_query==False:
		# 	#https can go to http, but http cannot reach https

		# 	#check if there's a "/" at the end of url
		# 	result=re.match("https?:\/\/.*\/$",url)
			
		# 	#if there is a "/" at the end of the string, strip it away
		# 	if result:
		# 		url=url.strip("/")


		# 	result1=re.match("(https)(:\/\/.*)",url)
		# 	#if the url is https, make it become http
		# 	if result1:
		# 		finalResult=result1.group(1).strip("s")
		# 		finalResult=finalResult+result1.group(2)
		# 		url=finalResult

		# 	if url not in url_dict:
		# 		url_dict[url]=None
		# 		return url
		# 	else:
		# 		return None


	rules= (
		Rule(LinkExtractor(process_value=process_url,allow=allow_regex,deny=deny_regex,unique=True),callback='parse_item',follow=True),
		#go to webpages that I don't want to so that I can get more links
		Rule(LinkExtractor(process_value=process_url,unique=True),follow=True),
		)

	list_attribute=["id","title","year","genres","movie_rating","directors","writers","date_in_theaters","date_on_dvd","box_office_earnings","duration","studios","audience_rating","num_of_audience_rating","actors","movie_description"]
	if save_data_to_csv==True:
		with open("%s.csv" %(csv_filename),"w",newline='')as csvfile:
			csv_writer=csv.writer(csvfile)
			csv_writer.writerow(list_attribute)

	

	def parse_item(self,response):
		#remember not to parse webapge that contains IRRELEVANT URL!!!!!!!!!!!!	
		processedURL=response.url.strip("/")


		result=re.match("(https)(:\/\/.*)",processedURL)
		#if the url is https, make it become http
		if result:
			finalResult=result.group(1).strip("s")
			finalResult=finalResult+result.group(2)
			processedURL=finalResult

		#if the url we haven't crawled before, keep it in dictionary to avoid duplication. 
		#The unique=true in Rule won't help because "Iron Man" with query string is equals to "Iron Man" wihout query string
		#What we are doing here is to remove query string only check if there's any duplication
		if processedURL not in url_dict:
			url_dict[processedURL]=None
		else:
			processedURL=None
			return 

		print(processedURL)
		

		#store html and convert into csv
		if processedURL==None:
			return
		#if the link is https://www.rottentomatoes.com/m/1082400_man_in_the_iron_mask, we only want the part behind /m/, which is 1082400 man in the iron mask
		elif processedURL.split("/")[-2]=='m':
			page_id=processedURL.split("/")[-1]
		#extract the string behind /tv/
		elif processedURL.split("/")[-3]=='tv':
			page_id=processedURL.split("/")[-2]+"_"+processedURL.split("/")[-1]

		if self.save_html_to_directory==True:
			if page_id is not None:
				filename='%s.html' %page_id
				with open(filename,"wb") as htmlFile:
					htmlFile.write(response.body)

		if self.save_data_to_csv==True:
			if page_id is not None:
				self.parse_to_csv(page_id)



	def parse_to_csv(self,pageID):
		

		movieTitle=""
		movieYear=""
		movie_genres=""
		movie_rating=""
		movie_directors=""
		movie_writers=""
		movie_inTheaters=""
		movie_onDVD=""
		movie_boxOffice=""
		movie_runtime=""
		movie_studios=""
		movie_averageRating=""
		movie_userRatings=""
		movie_actors=""
		movie_description=""


		soup=BeautifulSoup(open("%s.html" %(pageID)),"lxml")

		movieTitle=soup.find('title').string   												
		subString=" - Rotten Tomatoes"
		if subString in movieTitle:
			movieTitle=movieTitle.replace(subString,"")
		pattern=re.compile(".+(\(\d+\))")
		result=pattern.match(movieTitle)
		if result is not None:
			movieYear=result.group(1)
			if movieYear in movieTitle:
				movieTitle=movieTitle.replace(movieYear,"")							#this is the movie title
			movieYear=movieYear.replace("(","")
			movieYear=movieYear.replace(")","")										#this is the movie year
		# print(movieTitle)
		# print(movieYear)

		info=soup.find(id='movieSynopsis').string   								#this is the movie description
		movie_description=info.strip()
		#print(movie_description)


		# allGenres=soup.find_all("genre:link")        									#this is for genres
		# for genre in allGenres:
		# 	movie_genres=movie_genres+genre.span.string+","
		#print(movie_genres)


		temp=soup.find("section",class_="panel panel-rt panel-box movie_info media") 
		elements=temp.find_all("div",class_="meta-label subtle")       
		for i in elements:
			if "Rating:" in i.string:
				movie_rating=i.next_sibling.next_sibling.string									#this is for ratings
				#print(movie_rating)
			elif "Genre" in i.string:
				genres=i.next_sibling.next_sibling.find_all("a")
				for genre in genres:
					movie_genres=movie_genres+genre.string.strip()+", "
			elif "Directed By:" in i.string:
				directors=i.next_sibling.next_sibling.find_all("a")
				#print("directors:")
				for director in directors:														#This is for director
					movie_directors=movie_directors+director.string+","
				#print(movie_directors)
			elif "Written By:" in i.string:
				writers=i.next_sibling.next_sibling.find_all("a")							#this is for writers
				#print("writers:")
				for writer in writers:
					movie_writers=movie_writers+writer.string+","
				#print(movie_writers)
			elif "In Theaters:" in i.string:
				movie_inTheaters=i.next_sibling.next_sibling.find("time").string		 #this is for in theaters
				#print(movie_inTheaters)
			elif "On Disc" in i.string:
				movie_onDVD=i.next_sibling.next_sibling.find("time").string 					#this is for on DVD
				#print(movie_onDVD)
			elif "Box Office:" in i.string:
				movie_boxOffice=i.next_sibling.next_sibling.string								#this is Box office
				#print(movie_boxOffice)
			elif "Runtime:" in i.string:
				duration=i.next_sibling.next_sibling.find("time").stripped_strings				#this is runtime
				for z in duration:
					movie_runtime=z
				#print(movie_runtime)
			elif "Studio:" in i.string:
				studios=i.next_sibling.next_sibling.find_all("a")								#this is studio
				if(studios!=None):
					for studio in studios:
						movie_studios=movie_studios+studio.string+","
				else:
					additional_studios=i.next_sibling.next_sibling
					if(additional_studios!=None):
						movie_studios=movie_studios+additional_studio.string+","
				#print(movie_studios)

		actor_sections=soup.find_all("h2",class_="panel-heading")								#this is actors
		for actor_section in actor_sections:
			if actor_section.string=="Cast":
				actor_panel=actor_section.next_sibling.next_sibling
		actors=actor_panel.find_all("div",class_="media-body")
		for actor in actors:
			actor_names=actor.a.span.stripped_strings
			for i in actor_names:
				actor_name=i
			role_name=actor.find("span",class_="characters subtle smaller")
			#theActor=actor_name+" "+role_name.contents[1]        #uncomment if want blablabla as Iron Man
			theActor=actor_name
			movie_actors=movie_actors+theActor+","
		#print(movie_actors)


		audienceRatings_panel=soup.find("div",class_="audience-info hidden-xs superPageFontColor")
		audienceRatings_elements=audienceRatings_panel.find_all("span",class_="subtle superPageFontColor")
		#print("Audience Score")																		#this is audience score
		for i in audienceRatings_elements:
			if i.string=="Average Rating:":
				movie_averageRating=i.next_sibling.string.strip()
			elif i.string=="User Ratings:":
				movie_userRatings=i.next_sibling.string.strip()
		#print(movie_averageRating)
		#print(movie_userRatings)

		#Remove unicode. Convert all of them into ASCII
		def convertToASCII(str):
			str=str.encode("utf-8").decode("ascii","ignore")
			return str

		movieTitle=convertToASCII(movieTitle)
		movieYear=convertToASCII(movieYear)
		movie_genres=convertToASCII(movie_genres)
		movie_rating=convertToASCII(movie_rating)
		movie_directors=convertToASCII(movie_directors)
		movie_writers=convertToASCII(movie_writers)
		movie_inTheaters=convertToASCII(movie_inTheaters)
		movie_onDVD=convertToASCII(movie_onDVD)
		movie_boxOffice=convertToASCII(movie_boxOffice)
		movie_runtime=convertToASCII(movie_runtime)
		movie_studios=convertToASCII(movie_studios)
		movie_averageRating=convertToASCII(movie_averageRating)
		movie_userRatings=convertToASCII(movie_userRatings)
		movie_actors=convertToASCII(movie_actors)
		movie_description=convertToASCII(movie_description)


		global csv_filename
		with open("%s.csv" %(csv_filename),"a",newline='')as csvfile:
			csv_writer=csv.writer(csvfile)
			csv_writer.writerow([self.csv_id,movieTitle,movieYear,movie_genres,movie_rating,movie_directors,movie_writers,movie_inTheaters,movie_onDVD,movie_boxOffice,movie_runtime,movie_studios,movie_averageRating,movie_userRatings,movie_actors,movie_description])
			self.csv_id=self.csv_id+1



	
