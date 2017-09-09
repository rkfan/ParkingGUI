# This program is used to clean up the block csv file

# This is a test to fill up the block table

import re

# Get the information from the csv file. This is a dummy csv file that has only 100 entries
filename = 'blocksData.csv'
data = open(filename)

rowData = []

for line in data:
	rowData = line.split('\r') # Split by rows

for elements in rowData:
	fields = elements.split(',')

	# Dont really need to set these values, but it makes things a lot more clear...
	orderNumber = fields[0]
	boro = fields[1]
	mainStreet = fields[2]
	inter1 = fields[3]
	inter2 = fields[4]
	sideStr = fields[5]

	# Gets rid of the spaces first and foremost
	mainStreet = re.sub(r'\s\s+', ' ', mainStreet)
	inter1 = re.sub(r'\s\s+', ' ', inter1)
	inter2 = re.sub(r'\s\s+', ' ', inter2)

	# Removes the weird astericks shit
	mainStreet = re.sub(r'\*.+', '', mainStreet)
	inter1 = re.sub(r'\*.+', '', inter1)
	inter2 = re.sub(r'\*.+', '', inter2)

	print '{0},{1},{2},{3},{4},{5}'.format(orderNumber, boro, mainStreet, inter1, inter2, sideStr)

data.close()


