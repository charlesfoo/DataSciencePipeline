#!/usr/bin/env python3
import random
import csv

def main():
	with open('setC_year.csv', 'r') as file1:
		with open('sampleA_year.csv', 'w') as file2:
			in_r = csv.reader(file1)
			out_r = csv.writer(file2)

			random.seed(10)
			in_r = list(in_r)
			sample = random.sample(in_r, 800)

			for row in sample:
				out_r.writerow([-1] + row)

if __name__ == '__main__':
	main()