#!/usr/bin/python3

import csv
import re
import datetime



list_attribute=["id","title","year","genres","directors","writers","date_in_theaters","duration","audience_rating","num_of_audience_rating","language","country","filming_location","actors","movie_description","story"]
with open("cleaned_IMDB.csv","w",newline='') as csvfile:
	csv_writer=csv.writer(csvfile)
	csv_writer.writerow(list_attribute)

#BE VERY CAREFUL ABOUT THIS. ALWAYS MAKE SURE li=items

movieID=0

filereader=csv.reader(open("IMDB.csv"),delimiter=",")

next(filereader)


def stripComma(attribute):
	if attribute!='' and attribute is not None and attribute!='N/A':
		result=attribute.rstrip(",")
		return result
	else:
		return attribute

def dateValidate(date, date_format):
    try:
        datetime.datetime.strptime(date, date_format)
        return True
    except ValueError:
        return False

#Comment this. I take in IMDB.csv, for every tuple, remove utf-8, then write it to a temp.csv. Rename temp.csv as IMDB.csv and delete the previous IMDB.csv.
#Then, I continue cleaning data on IMDB.csv

#Clean the utf-8 symbols first
# for tuples in filereader:
# 	for j in range(len(tuples)):
# 		tuples[j]=tuples[j].encode("utf-8").decode("ascii","ignore")

# 	with open("new_IMDB.csv","a",newline='') as csvfile:
# 		csv_writer=csv.writer(csvfile)
# 		csv_writer.writerow(tuples)



for items in filereader:
	li=[]


	li.append(movieID)                                                  									#ID
	movieID=movieID+1

	movie_title=items[0]
	movie_title=stripComma(movie_title)                               										 #movie title
	li.append(movie_title)

	releaseDate=items[11]
	if releaseDate is not None and releaseDate!='' and releaseDate!='N/A':
		releaseDate=releaseDate.replace(",","")
		releaseDate=releaseDate.strip()
		releaseDate=re.search("(\d{4}) \(.*\)$",releaseDate)                            					#year
		year=releaseDate.group(1)
		li.append(year)
	else:
		li.append(releaseDate)


	movie_genres=items[1]
	if movie_genres is not None and movie_genres!='' and movie_genres!='N/A':
		genresList=movie_genres.split(",")
		for k in range(len(genresList)):																	#Genres
			if genresList[k]=='Talk-Show':
				genresList[k]='Television'
			elif genresList[k]=='Game-Show':
				genresList[k]='Television'
			elif genresList[k]=='Reality-TV':
				genresList[k]='Television'
			elif genresList[k]=='Action':
				genresList[k]='Action & Adventure'
			elif genresList[k]=='Sci-Fi':
				genresList[k]='Science Fiction & Fantasy'
			elif genresList[k]=='Family':
				genresList[k]='Kids & Family'
			elif genresList[k]=='Sport':
				genresList[k]='Sports & Fitness'
			elif genresList[k]=='Music':
				genresList[k]='Musical & Performing Arts'
			elif genresList[k]=='Adventure':
				genresList[k]='Action & Adventure'
			elif genresList[k]=='Mystery':
				genresList[k]='Mystery & Suspense'
			elif genresList[k]=='Fantasy':
				genresList[k]='Science Fiction & Fantasy'
			elif genresList[k]=='Musical':
				genresList[k]='Musical & Performing Arts'
		
		genresList=list(set(genresList))
		newGenres=""
		for s in range(len(genresList)):
			newGenres=newGenres+genresList[s]+","

		newGenres=stripComma(newGenres)
		movie_genres=newGenres
	li.append(movie_genres)



	directors=items[5]
	creators=items[6]
	if creators!=None and creators!='' and creators!='N/A':
		if directors!=None and directors!='' and directors!='N/A':											
			directors=directors+", "																		#directors
		directors=directors+creators
	li.append(directors)


	movie_writers=items[7]																					#writers
	li.append(movie_writers)



	movie_releaseDate=items[11]
	if movie_releaseDate is not None and movie_releaseDate!='' and movie_releaseDate!='N/A':
		movie_releaseDate=movie_releaseDate.replace(",","")                                            		#release Date
		movie_releaseDate=movie_releaseDate.strip()
		resultss=re.search("(.*) (\(.*\))$",movie_releaseDate)
		if resultss:
			movie_releaseDate=resultss.group(1)
			if dateValidate(movie_releaseDate,"%d %B %Y")==True:
				d1=datetime.datetime.strptime(movie_releaseDate,"%d %B %Y")
				movie_releaseDate=d1.strftime("%m/%d/%Y")
			else:
				pass
		else:
			pass

	li.append(movie_releaseDate)


	movie_duration=items[2]
	movie_hour=0
	movie_minutes=0
	if movie_duration is not None and movie_duration!='' and movie_duration!='N/A':
		results1=re.search("(\d+)h",movie_duration)															#movie duration
		if results1:
			movie_hour=int(results1.group(1))
		#no space in front of min, eg 6min
		results2=re.search("(\d+)min",movie_duration)
		if results2:
			movie_minutes=int(results2.group(1))
		#space in front of min, eg 6 min
		results3=re.search("(\d+) min",movie_duration)
		if results3:
			movie_minutes=int(results3.group(1))

		int_movie_duration=(movie_hour*60)+movie_minutes
		movie_duration=str(int_movie_duration)
	li.append(movie_duration)

	movie_audienceRatings=items[3]
	if movie_audienceRatings is not None and movie_audienceRatings!='' and movie_audienceRatings!='N/A':
		floatRating=float(movie_audienceRatings)*10															#audience ratings
		intRating=int(floatRating)
		movie_audienceRatings=str(intRating)
	li.append(movie_audienceRatings)


	movie_ratingsCount=items[4]																				#num of audience ratings
	li.append(movie_ratingsCount)


	movie_language=items[9]
	li.append(movie_language)																				#language

	country=items[10]
	li.append(country)																						#country

	film_location=items[12]
	li.append(film_location)																				#film location


	movie_actors=items[8]
	li.append(movie_actors)																					#actors

	description=items[13]
	li.append(description)																					#description

	story=items[14]
	li.append(story)																						#story

	


	with open("cleaned_IMDB.csv","a",newline='') as csvfile:
		csv_writer=csv.writer(csvfile)
		csv_writer.writerow(li)
