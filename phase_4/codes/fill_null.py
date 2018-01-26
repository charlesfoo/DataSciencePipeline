#!/usr/bin/env python3
import csv

class attr:
	label = 0
	_id = 1
	ltable_Id = 2
	rtable_Id = 3
	ltable_Title = 4
	ltable_Category = 5
	ltable_Duration = 6
	ltable_Rating = 7
	ltable_Rating_Count = 8
	table_Director = 9 
	rtable_Title = 10
	rtable_Category = 11
	rtable_Duration = 12
	rtable_Rating = 13
	rtable_Rating_Count = 14
	rtable_Director = 15

def fill_null(row, pos, value):
	if not row[pos]:
		row[pos] = value

def main():
	with open('sampleA.csv', 'r') as file1:
		with open('filled.csv', 'w') as file2:
			in_r = csv.reader(file1)
			out_r = csv.writer(file2)

			for row in in_r:
				fill_null(row, attr.rtable_Duration, 0)
				out_r.writerow(row)

if __name__ == '__main__':
	main()