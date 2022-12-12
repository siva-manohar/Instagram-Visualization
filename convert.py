"""
	Takes raw data scraped to csv and converts numers like 18.3k to form 18,300
"""

import csv
import xlsxwriter

def processFile(accName):
	"""
		In: name of account(str)
		Out: converted numbers(.xlsx
	"""
	with open('CSV/' + accName + '.csv') as csvFile:
		reader = csv.reader(csvFile, delimiter=',', quotechar='"')
		rows = []
		for row in reader:
			rows.append(row)

		#---------------
		# rows = rows[:26]
		#---------------

		workbook = xlsxwriter.Workbook('XLSX/'+accName + '.xlsx')
		worksheet = workbook.add_worksheet()

		number = -1
		for row in rows:
			number += 1

			if number == 0:
				continue

			link = row[0]
			likes = convert(row[1])
			comments = convert(row[2])

			worksheet.write_row('A'+str(number), [number, link, likes, comments])

		workbook.close()



def convert(number):
	"""
		In: number in 18.3k form (str)
		Out: int equivalent
	"""
	number = number.replace(',', '')
	if 'k' in number:
		number = number[:-1]
		result = float(number) * 1000
	elif 'm' in number:
		number = number[:-1]
		result = float(number) * 1000000
	else:
		result = float(number)

	return(int(result))

processFile('wordporm')