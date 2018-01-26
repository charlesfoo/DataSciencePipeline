#!/usr/bin/python3

import csv
import re
import datetime



list_attribute=["id","title","year","genres","movie_rating","directors","writers","date_in_theaters","date_on_dvd","box_office_earnings","duration","studios","audience_rating","num_of_audience_rating","actors","movie_description"]
with open("cleaned_rottentomatoes.csv","w",newline='') as csvfile:
	csv_writer=csv.writer(csvfile)
	csv_writer.writerow(list_attribute)


filereader=csv.reader(open("rottentomatoes.csv"),delimiter=",")

next(filereader)


def stripComma(attribute):
	if attribute!='' and attribute is not None:
		result=attribute.rstrip(",")
		return result
	else:
		return attribute


for items in filereader:
	dateInTheaters=items[7]
	if dateInTheaters!='' and dateInTheaters is not None:
		d1=datetime.datetime.strptime(dateInTheaters,"%b %d, %Y")
		items[7]=d1.strftime("%m/%d/%Y")
	#print(date)

	duration=items[10]
	if duration is not None:
		items[10]=duration.replace(" minutes","")
	#print(duration)

	rating=items[12]
	if rating is not None and rating!='' and rating!='N/A':
		rating=rating.replace("/5","")
		floatRating=float(rating)*20
		intRating=int(floatRating)
		rating=str(intRating)
		items[12]=rating
	#print(items[12])

	dateOnDVD=items[8]
	if dateOnDVD!='' and dateOnDVD is not None:
		d2=datetime.datetime.strptime(dateOnDVD,"%b %d, %Y")
		items[8]=d2.strftime("%m/%d/%Y")

	genress=items[3]
	items[3]=stripComma(genress)

	directorss=items[5]
	items[5]=stripComma(directorss)

	writerss=items[6]
	items[6]=stripComma(writerss)

	studioss=items[11]
	items[11]=stripComma(studioss)

	actorss=items[14]
	items[14]=stripComma(actorss)

	boxOfficeEarnings=items[9]
	if boxOfficeEarnings!='' and boxOfficeEarnings is not None:
		boxOfficeEarnings=boxOfficeEarnings.replace(",","")
		boxOfficeEarnings=boxOfficeEarnings.replace(".00","")
		boxOfficeEarnings=boxOfficeEarnings.replace("$","")
		items[9]=boxOfficeEarnings



	with open("cleaned_rottentomatoes.csv","a",newline='') as csvfile:
		csv_writer=csv.writer(csvfile)
		csv_writer.writerow(items)
