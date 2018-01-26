#!/usr/bin/env python3
import csv

class attr:
	_id = 0
	ltable_Id = 1
	rtable_Id = 2
	ltable_Title = 3
	ltable_Category = 4
	ltable_Duration = 5
	ltable_Rating = 6
	ltable_Rating_Count = 7
	ltable_Director = 8
	rtable_Title = 9
	rtable_Category = 10
	rtable_Duration = 11
	rtable_Rating = 12
	rtable_Rating_Count = 13
	rtable_Director = 14

def main():
	with open('setC.csv', 'r') as file1:
		with open('setC_year.csv', 'w') as file2:
			with open('cleaned_IMDB.csv', 'r') as file3:
				with open('cleaned_rottentomatoes.csv', 'r') as file4:
					in_r = csv.reader(file1)
					out_r = csv.writer(file2)
					imdb_r = csv.reader(file3)
					rotten_r = csv.reader(file4)

					imdb_year = [row[2] for row in imdb_r]
					imdb_year = imdb_year[1:]

					rotten_year = [row[2] for row in rotten_r]
					rotten_year = rotten_year[1:]

					for row in in_r:
						lid = int(row[attr.ltable_Id])
						rid = int(row[attr.rtable_Id])

						row = row[:attr.ltable_Director + 1] + [imdb_year[lid]] + row[attr.rtable_Title:] + [rotten_year[rid]]

						out_r.writerow(row)

if __name__ == '__main__':
	main()