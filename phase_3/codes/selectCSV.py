import csv

list_attribute=["id","title","year","directors","writers","date_in_theaters","duration","genres","actors"]


#fill in the position number of the attributes
#rottenTomatoes
movie_id=0
movie_title=1
movie_year=2
movie_directors=5
movie_writers=6
movie_dateInTheaters=7
movie_duration=10
movie_genres=3
movie_actors=14

#IMDB
# movie_id=0
# movie_title=1
# movie_year=2
# movie_directors=4
# movie_writers=5
# movie_dateInTheaters=6
# movie_duration=7
# movie_genres=3
# movie_actors=13


filename_writeTo='selected_rottentomatoes.csv'


with open(filename_writeTo,'w',newline='')as csvfile:
	csv_writer=csv.writer(csvfile)
	csv_writer.writerow(list_attribute)

#

filename_readFrom='cleaned_rottentomatoes.csv'


filereader=csv.reader(open(filename_readFrom),delimiter=',')

next(filereader)

for items in filereader:
	li=[]
	li.append(items[movie_id])
	li.append(items[movie_title])
	li.append(items[movie_year])
	li.append(items[movie_directors])
	li.append(items[movie_writers])
	li.append(items[movie_dateInTheaters])
	li.append(items[movie_duration])
	li.append(items[movie_genres])
	li.append(items[movie_actors])

	with open(filename_writeTo,"a",newline='')as csvfile:
		csv_writer=csv.writer(csvfile)
		csv_writer.writerow(li)
