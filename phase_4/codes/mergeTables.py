#!/usr/bin/env python3
import csv
import datetime

def title(x, y):         #choose longer title name
	return y if len(y) > len(x) else x

def cat(x, y):        #Let i be an element in y. If i not in x, add i into x. Do this for all elements in y.
	x = x.split(',')
	y = y.split(',')
	z = []
	for i in x:
		found = False
		for j in y:
			if i == j:
				found = True
				break
		if(not found):
			z += [i]

	return ','.join(y + z)

def aver(x, y):
	x = float(x)
	y = float(y)

	if x == 0:
		return y

	if y == 0:
		return x

	return (x + y) / 2

def checkAvailable(x,y):           #return IMDB if possible
	if x is not None and x!='N/A' and x!='':
		return x
	else:
		return y

def chooseDate(x,y):
	result1=None  #IMDB
	result2=None  #rottentomatoes

	#If x is none, y is not none
	if x is None or x=='N/A' or x=='':
		if y is not None and y!='N/A' and y!='':
			return y
		else:
			return x
	#If y is None, x is not none
	if y is None or y=='N/A' or y=='':
		if x is not None and x!='N/A' and x!='':
			return x
		else:
			return x
	#if x and y is not None
	try:
		datetime.datetime.strptime(x,"%m/%d/%Y")
		result1=True
	except ValueError:
		result1=False

	try:
		datetime.datetime.strptime(y,"%m/%d/%Y")
		result2=True
	except ValueError:
		result2=False

	if(result1):   #give priority to IMDB
		return x
	elif(result2):
		return y
	else:
		temp=title(x,y)
		return temp

def chooseYear(x,y):    #prioritise rottentomatoes
	if y is None or y=='N/A' or y=='':
		return x
	else:
		return y

def main():
	with open("a.csv", 'r') as in_f:
		with open("output.csv", 'w') as out_f:
			i_cs = csv.reader(in_f)
			o_cs = csv.writer(out_f)

			o_cs.writerow(['ltableID', 'rtableID','title', 'category', 'duration', 'rating', 'ratingCount', 'directors', 
				'year', 'movieRating', 'writers', 'dateInTheaters', 'language', 'country', 'filmingLocation', 
				'actors', 'dateOnDVD', 'boxOfficeEarnings', 'studios', 'movieDescription', 'story'])
			#num=0
			for row in i_cs:
				#a = num   #id                               		 #FIXED BY FZY
				id1=row[1]											 #FIXED BY FZY
				id2=row[2]											 #FIXED BY FZY
				b = title(row[3], row[18])   #title
				c = cat(row[4], row[19])  #category
				d = aver(row[5], row[20]) #duration
				e = aver(row[6], row[21]) #rating


				if row[7] is not None and row[7]!='' and row[7]!='N/A':
					ratingCount1=float(row[7])
				else:
					ratingCount1=0

				if row[22] is not None and row[22]!='' and row[22]!='N/A':
					ratingCount2=float(row[22])
				else:
					ratingCount2=0

				rating_Count=int(ratingCount1+ratingCount2)
				f = str(rating_Count) #ratingCount		 			 #FIXED BY FZY


				rtable_directors=row[23]
				rtable_directors=rtable_directors.rstrip(',')
				g = cat(row[8], rtable_directors) #directors     	 #FIXED BY FZY


				h = chooseYear(row[9], row[24]) #year           	 #FIXED BY FZY
				i = row[25] #movieRating
				j = cat(row[10], row[26]) #writers
				k = chooseDate(row[11], row[27]) #date In Theaters   #FIXED BY FZY
				l = row[12] #language
				m = row[13] #country
				n = row[14] #filming location
				o = cat(row[15], row[31]) #actors
				p = row[28] #dateOnDVD
				q = row[29] #boxOfficeEarnings
				r = row[30] #studios
				#s = title(row[16], row[32]) #movie description
				s=checkAvailable(row[16],row[32])             		 #FIXED BY FZY
				t = row[17] #story
				

				new_row = [id1,id2,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t]
				o_cs.writerow(new_row)
				#num=num+1

if __name__ == '__main__':
	main()