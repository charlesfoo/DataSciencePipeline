import csv


# Task 1: Add back all the attributes that I trimmed off during blocking and matching to reduce complexity
# Task 2: Merge ltable and rtable in matched.csv together (which value to select? what is the schema of resulting table E?)
# Task 3: Add tuples from table A and table B that is not matched into table E


#Task 1
matchedCSV="matched.csv"
IMDB_completeCSV="cleaned_IMDB.csv"
RottenTomatoes_completeCSV="cleaned_rottentomatoes.csv"


attributes=['id','ltable_id','rtable_id','ltable_title','ltable_category','ltable_duration','ltable_rating','ltable_ratingCount','ltable_director','ltable_year', 'ltable_writer', 'ltable_dateInTheaters', 'ltable_language', 'ltable_country', 'ltable_filmingLocation', 'ltable_actors', 'ltable_movieDescription', 'ltable_story','rtable_title','rtable_category','rtable_duration','rtable_rating','rtable_ratingCount','rtable_director','rtable_year','rtable_movieRating','rtable_writer','rtable_dateInTheaters','rtable_dateOnDVD','rtable_boxOfficeEarnings','rtable_studios','rtable_actors','rtable_movieDescription']
with open('completeAttributes_matched.csv','w',newline='') as csvfile:
	csv_writer=csv.writer(csvfile)
	csv_writer.writerow(attributes)


filereader1=csv.reader(open(matchedCSV), delimiter=',') #all the fields in the csv, eg: title, year, actors are all separated by comma
next(filereader1) #remove header


filereader2=csv.reader(open(IMDB_completeCSV), delimiter=',')
next(filereader2) #remove header
filereader2=list(filereader2)

filereader3=csv.reader(open(RottenTomatoes_completeCSV),delimiter=',')
next(filereader3) #remove header
filereader3=list(filereader3)


for items in filereader1:
	#IMDB
	IMDB_id=int(items[1])  #ID of IMDB
	rottentomatoes_id=int(items[2])  #ID of rottentomatoes
	temp=items[10:]
	
	IMDBtuple=filereader2[IMDB_id]  #search for the ID in IMDB.csv and extract out the tuple

	items[10]=IMDBtuple[5]  #writers
	items[11]=IMDBtuple[6]  #date in theaters
	items[12]=IMDBtuple[10]  #language
	items[13]=IMDBtuple[11]  #country
	items[14]=IMDBtuple[12]  #filming location
	items[15]=IMDBtuple[13]  #actors
	items[16]=IMDBtuple[14]  #movie description
	items.append(IMDBtuple[15])  #story

	items.extend(temp) #add back the rtable attributes that we replaced
	################# Done adding the trimmed attributes of IMDB back to matched.csv
	#rottentomatoes
	rottentomatoesTuple=filereader3[rottentomatoes_id]

	items.append(rottentomatoesTuple[4])  #movie rating
	items.append(rottentomatoesTuple[6])  #writers
	items.append(rottentomatoesTuple[7])  #date in theaters
	items.append(rottentomatoesTuple[8])  #date on dvd
	items.append(rottentomatoesTuple[9])  #box office earnings
	items.append(rottentomatoesTuple[11])  #studios
	items.append(rottentomatoesTuple[14])  #actors
	items.append(rottentomatoesTuple[15])  #movie description

	with open("completeAttributes_matched.csv",'a',newline='') as csvfile:
		csv_writer=csv.writer(csvfile)
		csv_writer.writerow(items)
	



