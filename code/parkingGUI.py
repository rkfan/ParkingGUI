# Some of the back buttons are not funtional as of yet. Not too worried about it
# Also need cases for backbutton setting, some will lead back to pages for members while others will lead to those for guests

try:
        import tkinter as tk
except ImportError:
        import Tkinter as tk
        
from myWidgets import *
import MySQLdb, time, re

# Make a class for quit button since it is ubiquitous throughout the program
# Would like a class to have query commands that are inherited
# Function designed to execute queries 
def exQ(myQuery):
    cursor.execute(myQuery)

# Function to display things mainly for diagnostic testing. Can remove later
def display(aCursor):
    rows  = cursor.fetchall()
    for r in rows:
        print r

# Class that inherits from. Current displays and such.
class ParkingProgram(tk.Tk):
        # args = any number of variables that can be passed
        # kwargs = key word arguments, passing thru dictionaries usually
        
        # Initialization of the ParkingProgram
        def __init__(self, *args, **kwargs):
                conn = MySQLdb.connect (
                        host = "localhost",
                        user = "root",
                        passwd = "opensesamechicken",
                        db = "parking",
                        port = 3306)

                global cursor
                cursor = conn.cursor()

                Tk.__init__(self, *args, **kwargs)      # Removed tk from tk.Tk__init__ so if anything weird happens, add it back!
                ParkingProgram.container = tk.Frame(self)              # Frame called container
                ParkingProgram.container.pack(side="top", fill="both", expand = True)

                # Configures location of container more specifically than pack
                ParkingProgram.container.grid_rowconfigure(0, weight=1)
                ParkingProgram.container.grid_columnconfigure(0, weight=1)

                # Dictionary containing the frames in it. Slab all frames with that container
                # and when a button is clicked, it brings up that page with the key you specified
                ParkingProgram.frames = {}

                # Saves frames into self.frames
                # Add pages to your list in this for loop to be able to go through pages
                pages = [StartPage, createUser, guestMainPage, updateLoc, searchLoc]

                #Packs all the pages in the dictionary "frames"
                for F in pages:
                        frame = F(ParkingProgram.container, self)  # Creates an instance of respective pages in the list above

                        ParkingProgram.frames[F] = frame      # The pages name stores the class instance

                        frame.grid(row=0, column=0, stick="nsew")

                # Assigns place for grid. Tkinter conforms to place you specified; sticky for directionality. nsew
                # stretches in all directions
                frame.grid(row=0, column=0, sticky="nsew")

                self.show_frame(StartPage)

        # Looking for the value of self.frames with the key (cont)
        def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise() # Shows the frame
                
class StartPage(tk.Frame):
        
        # Controller is the key word argument that is passed. Essentially the name of the frame.
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                loginFrame = Frame(self)
                loginFrame.pack()

                welcomeLabel = tk.Label(loginFrame, text = "Welcome ", font=("Helvetica",18))
                welcomeLabel.pack(anchor=CENTER)

                passwordInputLabel = tk.Label(loginFrame, text = "Please enter your Username and Password")
                passwordInputLabel.pack(anchor=CENTER)
                
                inputUsername = regularEntry(loginFrame, 'Username:')
                inputUsername.pack(side=LEFT, anchor=CENTER, fill=X)

                # Password input has to be done manually in order to hide password input
                passwordLabel = Label(loginFrame)
                passwordLabel['text'] = 'Password:'
                passwordLabel.pack(side=LEFT, anchor=CENTER, fill=X)

                passwordEntry = Entry(loginFrame, show="*")
                passwordEntry.pack(side=LEFT, anchor=CENTER, fill=X)

                # Creates a dictionary with all username and password key pairs
                # Does this only once so that you dont always have to do it
                login_dictionary = {}
                cursor.execute("SELECT username, password FROM user")
                username_list = cursor.fetchall()
                for u in username_list:
                    login_dictionary[u[0]] = u[1] 

                def login():
                    uName = inputUsername.get()
                    uName = uName.lower()         # In the database, all the usernames are lowercase  
                    pWord = passwordEntry.get()

                    # Limits to five attempts? Does not work properly at the moment, but can always log in as a guest.
                    # Probably not neccesary.
                    '''
                    def limitLogin():
                        #global loginAttempts
                        print loginAttempts
                        if loginAttempts == 5:
                            app.destroy()
                    '''

                    # Login checks. Checks for unsuccesful logins first
                    # Invalid Username
                    if uName not in login_dictionary.keys():
                        badLogin = tk.Label(self, text = "Incorrect Username/Password")
                        badLogin.pack(side=BOTTOM) # Want it to be in middle
                        badLogin.after(500, badLogin.destroy)
                        #limitLogin()

                    # If you reach here, that means Username is valid. 

                    # Valid login invalid password
                    elif login_dictionary[uName] != pWord:
                        badLogin = tk.Label(self, text = "Incorrect Username/Password")
                        badLogin.pack(side=BOTTOM) # Want it to be in middle
                        badLogin.after(500, badLogin.destroy)

                    # Sucessful Login 
                    else:
                        # Sets class variable to uName if succesfully logged in so that you can reference it later in other classes
                        self.userLoggedOn = uName

                        # Create an instance of the memberMainPage class. You cant do the show frames thingy here either! 
                        # This is because it will not get the user that is logged on
                        memberMain = memberMainPage(ParkingProgram.container, self)  
                        memberMain.grid(row=0, column=0, stick="nsew")
                        memberMain.tkraise()

                logonButton = Button(loginFrame, text="Login",
                                     command=login)
                logonButton.pack(side=LEFT,anchor=CENTER)

                # The Create button
                createButton = Button(self, text="Create a Username",
                                        command=lambda:app.show_frame(createUser))
                createButton.pack(side=LEFT, anchor = SW)

                # The guest Button
                guestButton = Button(self, text="Continue as Guest",
                                     command=lambda:app.show_frame(guestMainPage))
                guestButton.pack(side=LEFT, anchor=SW)

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

class createUser(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "Please enter desired username and password.")
                label.pack()

                label2 = tk.Label(self, text = "Username should be at least 4 characters long. Password should be at least 5 characters.")
                label2.pack()

                inputUsername = regularEntry(self, 'Username:')
                inputUsername.pack(side=LEFT, fill=X)

                # Password input has to be done manually in order to hide password input
                passwordLabel = Label(self)
                passwordLabel['text'] = 'Password:'
                passwordLabel.pack(side=LEFT, fill=X)

                passwordEntry = Entry(self, show="*")
                passwordEntry.pack(side=LEFT, fill=X)

                # Function that creates a user
                def createUserLogin():
                    uName = inputUsername.get()
                    uName = uName.lower()           
                    pWord = passwordEntry.get()

                    # Dictionary with all username and password key pairs
                    cursor.execute("SELECT username FROM user")
                    username_list = cursor.fetchall()
                    usernamelist = [l[0] for l in username_list]
        
                    cursor.execute("SELECT password FROM user")
                    password_list = cursor.fetchall()
                    passwordlist = [l[0] for l in password_list]
        
                    login_dictionary = dict(zip(usernamelist, passwordlist))

                    # Error Message and try again if the username/password does not match specs
                    if len(uName) < 4 or len(pWord) <8:  
                        badUser = tk.Label(self, text = "Invalid Input")
                        badUser.pack(side=BOTTOM) # Want it to be in middle
                        badUser.after(1000, badUser.destroy)

                    elif uName in login_dictionary:
                        badUser = tk.Label(self, text = "Username Exists. Try again")
                        badUser.pack(side=BOTTOM) # Want it to be in middle
                        badUser.after(1000, badUser.destroy)

                        # some way to clear the label of the contents on it when you go back?
                        # Double check if password is a match before proceeding
                    
                    # Proceed with creation 
                    else: 
                        #createUser = "INSERT INTO user (Username, Password) VALUES ((%s), (%s))"
                        #cursor.execute(createUser, (uName, pWord)) 
                        success = tk.Label(self, text = "Username created. Press Back to Return to Main Page")
                        success.pack(side=BOTTOM) # Want it to be in middle
                        success.after(3000, success.destroy)

                        # Want to automatically go back to the mainpage after a delay
                        #lambda: app.show_frame(StartPage).after(3000)
                        
                        #These work but dont work the way i want it to
                        #time.sleep(3)
                        #app.show_frame(StartPage)


                createButton = tk.Button(self, text = "Create Username", 
                                       command=createUserLogin)
                createButton.pack(side=LEFT)

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(mainPage))
                backButton.pack(side=BOTTOM, anchor=SE)


class guestMainPage(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "MAIN PAGE", font=("Helvetica", 18))
                label.pack()

                searchButton = tk.Button(self, text="Search Location",
                                         command=lambda:app.show_frame(searchLoc))
                searchButton.pack()

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(StartPage))
                backButton.pack(side=BOTTOM, anchor=SE)

class memberMainPage(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)

                # Greets the user. 
                userLoggedOn = app.frames[StartPage].userLoggedOn # Sets the user logged on for quick reference
                label = tk.Label(self, text = "Welcome, {0}".format(userLoggedOn), font=("Helvetica", 18))
                label.pack()

                label2 = tk.Label(self, text = "What Would you like to do?\n", font=("Helvetica", 14))
                label2.pack()

                # Only availible to people with usernames 
                updateButton = tk.Button(self, text="Update Location",
                                               command=lambda:app.show_frame(updateLoc))
                updateButton.pack()

                searchButton = tk.Button(self, text="Search Location",
                                         command=lambda:app.show_frame(searchLoc))
                searchButton.pack()

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(StartPage))
                backButton.pack(side=BOTTOM, anchor=SE)

class updateLoc(tk.Frame):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                label = tk.Label(self, text = "This is the page where you update info about where you last parked.")
                label.pack()

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(mainPage))
                backButton.pack(side=BOTTOM, anchor=SE)

class searchLoc(tk.Frame, ParkingProgram):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)

                # Select a borough first
                boroFrame = Frame(self)
                boroFrame.pack()
                # This is the all important dictionary that holds the signIDs of relevant stuff
                searchLoc.signIDDict = {}
              
                # Commands linked to the button to select a boro
                def boroMenuFunct():
                    boroLabel = tk.Label(boroFrame, text = 'Select Borough')
                    boroLabel.pack(side=LEFT, fill=X)

                    # Drop down menu with all the boroughs 
                    var = tk.StringVar(boroFrame)
                    var.set('Manhattan')
                    choices = ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island']
                    boroMenu = tk.OptionMenu(boroFrame, var, *choices)
                    boroMenu.pack(side=LEFT, padx=10, pady=10)

                    def selectBoro():
                        boro = var.get()        # The menu, depending on what you choose will change the value of var

                        # Need to translate the variable into it's proper form according to the tables
                        boroDict = {'Manhattan':'M', 'Brooklyn':'K', 'Queens':'Q', 'Bronx':'B', 'Staten Island':'S'}

                        # Boro is chosen, can't be going around reselecting a boro and messing things up!
                        # For now, do one run through it before making things like switching boroughs possible
                        boroFrame.destroy()

                        setBoroFrame = Frame(self)
                        setBoroFrame.pack()

                        newBoroLabel = tk.Label(setBoroFrame, text = 'Borough Selected: {0}'.format(boro), font=("Helvetica", 14))
                        newBoroLabel.pack(side=LEFT, fill=X)

                        # Pack the next thing once boro is selected. Passes the boro as B, K, M, Q, or S to the next function
                        searchStreetFunct(boroDict[boro])

                    boroButton = tk.Button(boroFrame, text='Select Borough', command=selectBoro)
                    boroButton.pack(side=LEFT)

                boroMenuFunct()

                def searchStreetFunct(boro):
                    mainStrFrame = Frame(self)
                    mainStrFrame.pack()

                    mainStreetLabel = tk.Label(mainStrFrame, text = "Please enter the main street of your destination.")
                    mainStreetLabel.pack()

                    mainStrEntry = Entry(mainStrFrame)
                    mainStrEntry.pack(fill=X)

                    def searchMainStreet():
                        mainStreet = mainStrEntry.get()

                        # Existence check of this Main Street entered. Has to be on the correct boro as well!
                        query1 = "SELECT distinct main_str FROM block WHERE main_str = %s AND boro_code = %s"
                        cursor.execute(query1, (mainStreet, boro))     # Can refer to boro since same scope as mainStreetFunct
                        mainExists = cursor.fetchall()

                        # If the main street entered exists within that boro
                        if mainExists:
                            mainStreet = mainExists[0][0]
                            mainStrFrame.destroy()

                            setMainStrFrame = Frame(self)
                            setMainStrFrame.pack()

                            newMainStreetLabel = tk.Label(setMainStrFrame, text = 'Main Street: {0}'.format(mainStreet), font=("Helvetica", 14))
                            newMainStreetLabel.pack()

                            # Now you need the search things for inter 1 and inter 2. Each of the choices are dependent 
                            # on one another, so sadly I don't think you can do a single function to do it all
                            def searchInter1():
                                inter1Frame = Frame(self)
                                inter1Frame.pack()

                                inter1Label = tk.Label(inter1Frame, text="Please select an intersecting street")
                                inter1Label.pack(side=LEFT, fill=X)

                                # Query for all streets that intersect this main_Str
                                query1 = "SELECT DISTINCT inter_1, inter_2 from block where main_str = %s and boro_code = %s"
                                cursor.execute(query1, (mainStreet,boro)) 
                                rows = cursor.fetchall()

                                def makeStreetDict(rows):
                                    # This dictionary will hold all the unique street names that intersect with this main street. 
                                    # This step is used to get the unique inter_1 and inter_2 since the two values are pretty interchangable
                                    streetDict = {}

                                    for rowTuple in rows:
                                        for element in rowTuple:
                                            if element not in streetDict:
                                                streetDict.update({element: ''})
                                    return streetDict

                                streetDict = makeStreetDict(rows)
                                # Drop down menu created for inter1
                                var = tk.StringVar(inter1Frame)
                                var.set('')
                                choices = streetDict.keys()
                                choices.sort()
                                inter1Menu = tk.OptionMenu(inter1Frame, var, *choices)
                                inter1Menu.pack(side = LEFT, padx=30, pady=30)

                                def selectInter1():
                                    Inter1 = var.get() 
                                    inter1Frame.destroy()

                                    SetInter1Frame = Frame(self)
                                    SetInter1Frame.pack()

                                    newStreet1 = tk.Label(SetInter1Frame, text = 'Street 1: {0}'.format(Inter1),font=("Helvetica", 14))
                                    newStreet1.pack(side=LEFT, fill=X)

                                    def searchInter2():
                                        inter2Frame = Frame(self)
                                        inter2Frame.pack()
                                        
                                        inter2Label = tk.Label(inter2Frame, text="Please select adjacent street")
                                        inter2Label.pack(side=LEFT, fill=X)

                                        # Query for all streets that intersect this main_Str and that intersection

                                        # Query searches the database for any mainstreet + either inter_1 or inter_2 having the user entry
                                        query1 = "SELECT DISTINCT inter_1, inter_2 from block WHERE main_str = %s and (inter_1=%s or inter_2=%s) and boro_code = %s;"
                                        cursor.execute(query1, (mainStreet, Inter1, Inter1, boro)) 
                                        rows = cursor.fetchall()

                                        # Dictionary with distinct streets found tupled with the user choice are kept
                                        # In the end, the user's first choice for the street is deleted from the list 
                                        street2Dict = makeStreetDict(rows)
                                        Inter2List = street2Dict.keys()
                                        Inter2List.remove(Inter1)

                                        # Drop down menu created for inter2
                                        var = tk.StringVar(inter2Frame)
                                        var.set('')
                                        choices = Inter2List
                                        inter2Menu = tk.OptionMenu(inter2Frame, var, *choices)
                                        inter2Menu.pack(side = LEFT, padx=30, pady=30)
                                        
                                        def selectInter2():
                                            Inter2 = var.get() 
                                            inter2Frame.destroy()

                                            SetInter2Frame = Frame(self)
                                            SetInter2Frame.pack()

                                            newStreet2 = tk.Label(SetInter2Frame, text = 'Street 2: {0}'.format(Inter2), font=("Helvetica", 14))
                                            newStreet2.pack(side=LEFT, fill=X)

                                            '''All this Information are contained within this scope. I can print these without
                                               fail right here
                                            print mainStreet
                                            print boro
                                            print Inter1
                                            print Inter2
                                            '''

                                            # At this point the streets and stuff have all been selected. Next step is to display parking info
                                            def displayParkingInfo():
                                                query1 = "SELECT DISTINCT Order_Num FROM block where main_str=%s AND boro_code=%s AND((inter_1=%s AND inter_2=%s) or (inter_1=%s AND inter_2=%s));"
                                                cursor.execute(query1, (mainStreet, boro, Inter1, Inter2, Inter2, Inter1)) 
                                                rows = cursor.fetchall()

                                                # Now you have the order number which connects to everything in the other tables 
                                                # It is the key to everything

                                                # List comprehension to collect the order numbers that were retrieved in a list
                                                orderNumberList = [rows[i][0] for i in range(len(rows))]

                                                # For each order number that was retrieved get the signID of signs on that block (OrderNum).
                                                def getSignID(orderNumber):
                                                    query1 = "SELECT DISTINCT c.sign_ID from coord c INNER JOIN block b on b.order_num = c.block_id WHERE b.order_num = %s;"
                                                    cursor.execute(query1, (orderNumber,))

                                                    # This retrieves all the sign IDs from within 
                                                    rows = cursor.fetchall()
                                                    return rows

                                                # Dictionary for signs is made. Key: order numbers. Values: Sign IDs that correspond
                                                for n in orderNumberList:
                                                    if n not in searchLoc.signIDDict.keys():
                                                        searchLoc.signIDDict[n] = getSignID(n)
                                                
                                                def makeResultSearch():
                                                    rS = resultSearch(ParkingProgram.container, self)  
                                                    #ParkingProgram.frames[resultSearch] = rS
                                                    rS.grid(row=0, column=0, stick="nsew")

                                                    return rS
                                                
                                                # Makes a result search page and shows it
                                                rsFrame = makeResultSearch()
                                                rsFrame.tkraise()
         
                                            displayParkingInfo()

                                        selectStreet2 = tk.Button(inter2Frame, text="Select Street", command=selectInter2)
                                        selectStreet2.pack(side=LEFT)

                                    # Functions for searching for intersection 2 are embedded in the function
                                    # to select intersection 1. So it is a cascade 

                                    searchInter2()      # Now take care of the second intersection

                                selectStreet1 = tk.Button(inter1Frame, text="Select Street", command=selectInter1)
                                selectStreet1.pack(side=LEFT)

                            # Calls the function after the frames are set up once the Main street is chosen
                            searchInter1()

                        else:
                            nonExistStreet = tk.Label(mainStrFrame, text = "This Entry was not found in the Database", font=("Helvetica", 16))
                            nonExistStreet.pack(side=BOTTOM)
                            nonExistStreet.after(1000, nonExistStreet.destroy)

                    goButton = tk.Button(mainStrFrame, text = "Search",
                                         command=searchMainStreet)
                    goButton.pack()

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(mainPage))
                backButton.pack(side=BOTTOM, anchor=SE)
                
class resultSearch(tk.Frame, searchLoc):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)   

                # Make it prettier. This dictionary has the block ID and all the signs on that side of the particular block
                # Want to display information about that block
                signIDDict = searchLoc.signIDDict

                # Make it a class variable so that it can be accessed by vicinity if needed
                # You just need the keys
                resultSearch.blockKeys = signIDDict.keys()
                
                for key in signIDDict.keys():
                    tempList = []
                    for tuples in signIDDict[key]:
                        tempList.append(tuples[0])
                    signIDDict[key] = tempList  

                # List that stores the "blah blah street between blah blah"
                resultSearch.streetOutputDict = {}

                # This will print out something like "EAST 68 STREET between LEXINGTON AVENUE and PARK AVENUE on the S side in MANHATTAN, NY"
                for key in searchLoc.signIDDict.keys():
                    # Information about the block like street names
                    query1 = "SELECT * from block where Order_Num = %s;"
                    cursor.execute(query1, (key,))
                    blockInfo = cursor.fetchall()
                    blockInfo = blockInfo[0]    # Gets of annoying tuples in tuples
                    boroDict = {'K':'BROOKLYN', 'B':'BRONX', 'Q':'QUEENS', 'S':'STATEN ISLAND', 'M':'MANHATTAN'}

                    borough = blockInfo[1]
                    borough = boroDict[borough]
                    mainS = blockInfo[2]
                    i1 = blockInfo[3]
                    i2 = blockInfo[4]
                    sideOfStreet = blockInfo[5]

                    # This prints out the location of the block. X between Y and Z
                    streetOutput ='{0} between {1} and {2} on the {3} side of street in {4}, NY'.format(mainS, i1, i2, sideOfStreet, borough)
                    signInfoList = []

                    for signID in searchLoc.signIDDict[key]:
                        # For each block, look up each sign within the block and print out the description
                        myQ = 'SELECT * FROM signs where sign_ID = %s' # Something like this
                        cursor.execute(myQ, (signID,))
                        signInfo =  cursor.fetchall()
                        signInfo = signInfo[0]
                        # For simplicity's sake, just keep the ones that deal with parking info. So no standing or no parking
                        if re.search(r"(NO PARKING|NO STANDING)", signInfo[2]) is not None:
                            signInfoList.append(signInfo)
                    # Add the Block ID to the end of the Dictionary
                    resultSearch.streetOutputDict[streetOutput] = signInfoList

                # Make a frame for each one and display findings
                for key in resultSearch.streetOutputDict.keys():
                    resultFrame = Frame(self)
                    resultFrame.pack()

                    resultLabel = tk.Label(resultFrame, text = key + "\n")
                    resultLabel.pack(side=LEFT, fill=X)

                    for sign in resultSearch.streetOutputDict[key]:
                        resultFrame2 = Frame(self)
                        resultFrame2.pack()
                        resultLabel2 = tk.Label(resultFrame2, text = sign[2])
                        resultLabel2.pack(side=BOTTOM, fill=X)

                    # Some sort of separation between
                    spaceFrame = Frame(self)
                    spaceFrame.pack()

                    spaceLabel = tk.Label(spaceFrame, text = "\n___________________________________________________________________\n")
                    spaceLabel.pack(side=BOTTOM, fill=X)

                # Since vicinity button needs the block information, you need to reinitiate it and pass on things via inheritance. 
                # Same way to do it as raising the result search thing
                def makeVicinityPage():
                    vP = vicinity(ParkingProgram.container, self)  
                    vP.grid(row=0, column=0, stick="nsew")
                    vP.tkraise()

                # Makes a result search page and shows it

                # Raises the new one you just created (Hopefully)
                vicinityButton = tk.Button(self, text = "Calculate Vicinity",
                                           command=makeVicinityPage)
                vicinityButton.pack()

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(mainPage))
                backButton.pack(side=BOTTOM, anchor=SE)
                

# ********************
# Think about what this would display. This is the brunt of the program and very important!!!!
# ********************
class vicinity(tk.Frame, resultSearch):
        def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                streetOutputDict = resultSearch.streetOutputDict # Perhaps not necc
                #print streetOutputDict
                blockIDKeys = resultSearch.blockKeys

                # Take the block ID keys, find the coordinates. find the midpoint of the two blocks and go from there.
                # Assumes that block is properly defined as to having two constitutents, the N and S side 
                # or E and W side. 
                myQ = 'SELECT avg(x_Coord), avg(y_coord) from coord where Block_ID = %s or Block_ID = %s'
                cursor.execute(myQ, (blockIDKeys[0], blockIDKeys[1])) # Acknowledged: there are some list range issues due to 
                                                                      # non uniformity of the data. Some will have weird output
                coordData = cursor.fetchall()
                coordData = str(coordData)

                # Format it so it is proper
                coordData = coordData.split(',')
                coordData.pop() # Removes that last empty index. HOPEFULLY THERE ARE NO STRANGE THINGS HAPPENINGS BECAUSE OF THIS
                                # Takes advantage of how the string/tuple is formatted
                avgCoords = []  # Holds the average x and y of that block

                for item in coordData:
                    item = item.split('\'')

                    if re.search(r"\d+", item[1]) is not None:
                        avgCoords.append(item[1])
                
                # Float conversion is neccesary for ranges
                xCoord = float(avgCoords[0])
                yCoord = float(avgCoords[1])
                
                # Now you have the two coordinates, calculate and look for stuff that are in that range. 
                '''LAST PART OF THE PROJECT. SHOULDNT BE SUPER DIFFICULT.

                    Looked up Signs for Bay ridge ave btwn 11 and 12 and b. ridge ave btwn 10 and 11.
                    Used difference in x and y btwn the first signs that appear on the block (should be bus signs)
                    differences are set as variables below. Took abs value of differences btwn them
                '''

                # This hard sets the differences in the x and y coordinate for an avenue
                # y difference though? Is this neccesary? Just go with it...
                xDifference = 610.970235 * 0.50
                yDifference = 485.25231 * 0.50

                # The x and y differences are based on an avenue. an avenue is around three blocks. 
                # This plus minus data will have 
                upperLimitXCoord = xCoord + xDifference
                lowerLimitXCoord = xCoord - xDifference

                upperLimitYCoord = yCoord + yDifference
                lowerLimitYCoord = yCoord - yDifference

                '''
                print upperLimitXCoord
                print lowerLimitXCoord
                print upperLimitYCoord
                print lowerLimitYCoord
                '''

                # Select distinct signs that are within the vicinity. This is a ~3 block rectangle around the selected block
                # The street that was selected would most likely be included in that vicinity search. 
                # Can easily omitt all data pertaining to block you selected, but was too lazy to...
                myQ = "SELECT DISTINCT b.order_Num, b.boro_code, b.main_str, b.inter_1, b.inter_2 FROM block b INNER JOIN (SELECT DISTINCT block_iD FROM coord WHERE (x_Coord < %s  AND x_coord > %s) AND (y_Coord < %s AND y_Coord > %s))a ON b.order_num = a.block_ID;"
                cursor.execute(myQ, (upperLimitXCoord, lowerLimitXCoord, upperLimitYCoord, lowerLimitYCoord))
                vicinityInfo = cursor.fetchall()

                # This dictionary stores each street name in the area as the key and then the corresponding signs as a list.
                streetVicinityDict = {}
                for tuples in vicinityInfo:
                    order_Num = tuples[0]    # This is the unique block ID for each block
                    streetFormat = "{0} between {1} and {2}".format(tuples[2], tuples[3], tuples[4])

                    # Selects the distinct signs in each of each block
                    myQ = "SELECT distinct s.desc_sign, s.days_reg FROM coord c INNER JOIN signs s ON s.sign_ID=c.sign_ID WHERE c.block_ID = %s AND s.days_reg IS NOT NULL GROUP BY s.days_reg;"
                    cursor.execute(myQ, (order_Num,))
                    tempRetrieve = cursor.fetchall()

                    # This does per each tuple that was retrieved. Each tuple is a desc_sign and days_reg
                    # Purpose of this loop is to make the good output list (goodOutputList) which is a list of lists. 
                    # Each list in the list has desc_sign days_reg in it
                    for t in tempRetrieve:
                        goodOutputList = []
                        signDesc = t[0]
                        daysReg = t[1]

                        # Only Takes signs that have descriptions of no parking or no standing. There should only be one regulation per street!
                        if re.search(r"([NO PARKING|NO STANDING])", signDesc) is not None:
                            # Add the stuff that are good
                            goodOutputList.append(signDesc)
                            goodOutputList.append(daysReg)

                    streetVicinityDict[streetFormat] = goodOutputList

                # Maybe this byDate dictionary is not neccessary. Just create it arranged by date from the get go. 
                # Don't worry for now, optimize later
                # Sets up the byDate dictionary to have days of the week and then lists
                byDate = {}

                # Sometimes problematic streets (keys) have nothing contained in the lists.
                # For simplicity's sake, delete these entries from the dictionary
                # This will prevent any out of range headaches that may appear later

                for key in streetVicinityDict:
                    # If the length of the list inside is zero
                    if len(streetVicinityDict[key]) == 0:
                        del streetVicinityDict[key]

                for key in streetVicinityDict.keys():
                    day = streetVicinityDict[key][1]

                    tempList = []

                    # Add the respective information into tempList
                    tempList.append(key)
                    description = streetVicinityDict[key][0]
                    tempList.append(description)

                    # Not in the dictionary yet
                    if day not in byDate.keys():
                        byDate[day] = [tempList]

                    # Is in the dictionary
                    else:
                        byDate[day].append(tempList)

                # print byDate # For testing purposes

                # Make a frame for each one of the keys (which are the signs categorized to days of the week) and display findings
                # Acknowledged: Things with a lot of signs in the vicinity will go out of page. Can't view everything
                # on one screen. Also back and quit buttons are not shown on the screen.
                for key in byDate.keys():
                    dayFrame = Frame(self)
                    dayFrame.pack()

                    dayLabel = tk.Label(dayFrame, text = key, font=("Helvetica", 16))
                    dayLabel.pack(side=LEFT, fill=X)

                    # This is looking at the list within each list
                    for signList in byDate[key]:
                        signFrame = Frame(self)
                        signFrame.pack()

                        # Format the text so it is more readable
                        streetData = signList[0]
                        regulationData = signList[1]

                        signLabel = tk.Label(signFrame, text = "{0}\n{1}\n".format(streetData, regulationData))
                        signLabel.pack(side=BOTTOM, fill=X)

                quitButton = tk.Button(self, text = "Quit",
                                      command = lambda:app.destroy())
                quitButton.pack(side=BOTTOM, anchor=SE)

                backButton = tk.Button(self, text = "Back",
                                       command=lambda:app.show_frame(mainPage))
                backButton.pack(side=BOTTOM, anchor=SE)

# Maybe another class after vicinity that is a shortcut to return home or to do another search?

app = ParkingProgram()
app.title("Parking Program v1")
# app.resizable(width=FALSE, height=FALSE)
# app.geometry('{}x{}'.format(300, 500))
app.mainloop()