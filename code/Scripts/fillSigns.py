# This script is used to fill up the signs table
# Some parts commented out of this script were used to set up the signData table which is derived off the big 
# WGS84 Coordinate thing

import MySQLdb
import re

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

# Parse the string and see what days regulation are
# WRITE THIS FUNCTION. USE REGEX STUFF LIKE THAT IF NEEDED
def findDays(description):
    DaysReg=''

    daysOfWeek = 'SUN MON TUES WED THURS FRI SAT'.split()  # List containing how the days of week are stored
    THRUDays = 'SUN THRU ,MON THRU ,THURS THRU ,FRI THRU '.split(',')


    if 'THRU' in description:
        for dayThru in THRUDays:
            if dayThru in description:
                my_regex = re.escape(dayThru) + r"..."
                matchObj = re.findall(my_regex, description, re.DOTALL) # Is a list containing the ____ THRU ___. USE THE FIRST ELEMENT TO SIMPLIFY

                # Get a list with the two days it is in between
                try: 
                    twoDays = matchObj[0].split(' THRU ')
                except: 
                    return ""

                # Now make the string with all the days in between the days
                firstDay = twoDays[0]
                secondDay = twoDays[1]

                dow = 'SUN MON TUES WED THURS FRI SAT SUN MON TUES WED THURS FRI SAT'
                my_match = re.escape(firstDay) + r".*?" + re.escape(secondDay)
                matchObject = re.findall(my_match, dow, re.DOTALL) # List of days with spaces in between
                matchObject = matchObject[0]

                return matchObject
    
    # For those dealing with something like Monday-Friday
    elif re.search(r"DAY-", description) is not None:
        my_regex = r"..." + "DAY-" + r".*" + "DAY" 
        matchObj = re.findall(my_regex, description, re.DOTALL)

        l = matchObj[0].split('-')
        
        firstDay = l[0]
        secondDay = l[1]

        try:
            additionalDay = l[2]
        except:
            additionalDay = ''
        
        for day in daysOfWeek:
            if day in secondDay:
                secondDay = day

            elif day in additionalDay:
                additionalDay = day

        if 'PM' in additionalDay:
            additionalDay = ''

        # Change the first ones
        weekDict = {'SUNDAY':'SUN', 'MONDAY':'MON', 'UESDAY':'TUES', 'NESDAY':'WED', 'URSDAY':'THURS', 'FRIDAY':'FRI', 'TURDAY':'SAT'}
        firstDay = weekDict[firstDay]

        dow = 'SUN MON TUES WED THURS FRI SAT SUN MON TUES WED THURS FRI SAT'
        my_match = re.escape(firstDay) + r".*?" + re.escape(secondDay)
        matchObject = re.findall(my_match, dow, re.DOTALL) # List of days with spaces in between
        a = matchObject[0]
        a = a + ' ' +additionalDay

        return a

    # Stuff that has EXCEPT in it. Only these three days have except Day in it
    # Assume it is EXCEPT and only one day, no multiples
    elif re.search(r"EXCEPT (SUN|FRI|SATUR)DAY$", description) is not None:
        # Go simple, just do if statements
        if re.search(r"EXCEPT FRIDAY$", description) is not None:
            reg = "SUN MON TUES WED THURS SAT"
            return reg

        elif re.search(r"EXCEPT SATURDAY$", description) is not None:
            reg = "SUN MON TUES WED THURS FRI"
            return reg

        else: 
            reg = "MON TUES WED THURS FRI SAT"
            return reg

    # Does not have weird shit in it. Just individual days
    else:
        for day in daysOfWeek:     
            if day in description:
                DaysReg = DaysReg + day + ' '

        return DaysReg

# Get the information from the csv file. This is a dummy csv file that has only 100 entries
filename = 'signData.csv'
data = open(filename)

rowData = []

# Dictionary that stores the descriptions of signs corresponding to their signID
signDict = {}

# Make everything pretty
for line in data:
    rowData = line.split('\r') # Split by rows

    for elements in rowData:
        fields = elements.split(',')
        
        # Dont really need to set these values, but it makes things a lot more clear...
        Sign_ID  = fields[0]

        Sign_Desc = fields[1]
        Sign_Desc = Sign_Desc.replace('\n', '')

        days_Reg = findDays(Sign_Desc)
        
        myQ = "INSERT INTO signs (Sign_ID, Days_Reg, Desc_Sign) VALUES (%s, %s, %s)"

        try: 
            cursor.execute(myQ, (Sign_ID, days_Reg, Sign_Desc))

        # Print out troublesome cases for further analysis 
        except:
            print '{0}, {1}, {2}'.format(Sign_ID, Days_Reg, Desc_Sign)
            print
        
data.close()
