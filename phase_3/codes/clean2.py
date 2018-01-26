#!/usr/bin/env python3
import csv

def grab_row(row, cols):
	return [row[i] for i in cols]

def convert(x):
	if x == 'Anime':
		return 'Animation'
	elif x == 'Manga':
		return 'Animation'
	elif x == 'Suspense':
		return 'Mystery'
	elif x == 'Lesbian':
		return 'Adult'
	elif x == 'Gay':
		return 'Adult'
	else:
		return x

def main():
	with open('setD.csv', 'r') as in_f:
		with open('setD4.csv', 'w') as out_f:
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