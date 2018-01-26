#!/usr/bin/env python3
import csv

def convert(x):
	if x == 'Music':
		return 'Musical'
	elif x == 'Game-Show':
		return 'Television'
	elif x == 'Reality-TV':
		return 'Television'
	elif x == 'Talk-Show':
		return 'Television'
	elif x == 'Thriller':
		return 'Mystery'
	else:
		return x

def main():
	with open('setA.csv', 'r') as in_f:
		with open('imdb_7d.csv', 'w') as out_f:
			cr = csv.reader(in_f)
			otr = csv.writer(out_f)

			for row in cr:
				genre = row[2].split(',')
				genre = [convert(i) for i in genre]
				new_genre = []
				has = {}
				for i in genre:
					if not i in has:
						new_genre += [i]
						has[i] = None

				row[2] = ','.join(new_genre)
				otr.writerow(row)

if __name__ == '__main__':
	main()