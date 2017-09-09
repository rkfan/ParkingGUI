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

filename = 'blockData.csv'
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
	
		# The needle is ready, time for the injection...
		myQ = "INSERT INTO Block (Order_Num, Boro_Code, Main_Str, Inter_1, Inter_2, Side_of_Street) VALUES (%s, %s, %s, %s, %s, %s)" 

		try: 
			cursor.execute(myQ, (orderNumber, boro, mainStreet, inter1, inter2, sideStr))

		# Print out troublesome cases for further analysis 
		except:
			print (orderNumber, boro, mainStreet, inter1, inter2, sideStr)
			print 
		
data.close()

print 'Execution complete.'