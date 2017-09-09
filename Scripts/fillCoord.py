# This script is used to fill up the signs table

import MySQLdb

conn = MySQLdb.connect (
                        host = "localhost",
                        user = "root",
                        passwd = "opensesamechicken",
                        db = "Parking",
                        port = 3306)

cursor = conn.cursor()

# Function designed to execute queries 
def exQ(myQuery):
	cursor.execute(myQuery)

# Function to display things 
def display(aCursor):
    rows  = cursor.fetchall()
    for r in rows:
        print r

# Get the information from the csv file. This is a dummy csv file that has only 100 entries
filename = 'testCoord.csv'
data = open(filename)

rowData = []

# Make everything pretty
for line in data:
	rowData = line.split('\r') # Split by rows

	for elements in rowData:
		fields = elements.split(',')

		# Dont really need to set these values, but it makes things a lot more clear...
		Object_ID = fields[0]
		Block_ID = fields[1]
		Sign_ID  = fields[2]
		xCoord = fields[3]
		yCoord = fields[4]
		Sign_Seq = fields[5]
		# Sign_Desc = fields[6] NO DESCRIPTION IN THIS ONE
		Arrow_Points = fields[7]

		Arrow_Points = Arrow_Points.replace('\n', '')   # Gets rid of some annoying stuff with this field

		
		# The needle is ready, time for the injection...
		myQ = "INSERT INTO coord (Object_ID, Block_Id, Sign_ID, x_Coord, y_Coord, Sign_Seq, Arrow_Points) VALUES (%s, %s, %s, %s, %s, %s, %s)" 

		try: 
			cursor.execute(myQ, (Object_ID, Block_ID, Sign_ID, xCoord, yCoord, Sign_Seq, Arrow_Points))

		# Print out troublesome cases for further analysis 
		except:
			print '{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(Object_ID, Block_ID, Sign_ID, xCoord, yCoord, Sign_Seq, Arrow_Points)
			print 
		
data.close()
