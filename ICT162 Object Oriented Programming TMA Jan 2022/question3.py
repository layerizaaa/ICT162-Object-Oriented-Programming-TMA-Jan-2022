#TMA Question 3

#3(a)***********************************************************
from question2 import HandicappedGolfer, PCHolder, GolfingException, Flight, Golfer
from datetime import datetime
import calendar

class GolfCLub: 
    _TEE_SLOTS = ["07:08", "07:18", "07:28", "07:38", "07:48", "07:58"]

    def __init__(self, name, course, golfingDate):
        """ constructor that execute when an object is created """
        self._name = name
        self._golfers = {}
        self._course = course
        self._bookings = {}

        for teeSlots in self._TEE_SLOTS:
            self._bookings[teeSlots] = None

        self._golfingDate = datetime.strptime(golfingDate,"%d-%b-%Y")

    @classmethod
    def addTeeSlot(cls, teeSlot):
        cls._TEE_SLOTS.append(teeSlot)

    @property  # accessor / getter method
    def course(self):
        return self._course

    @property  # accessor / getter method
    def golfingDate(self):
        return self._golfingDate

    def setupGolfers(self, filename):
        """ Takes in a file name as a parameter and read the content of the 
        given file to setup all the golfers into _golfers dictionary """
        
        for g in open(filename, 'r'):
            if 'PC' in g:
                name, membership, PC, expiryDate = g.split(',')
                golfer = PCHolder(name, membership, expiryDate.strip())

            else:
                name, membership, handicap = g.split(',')
                golfer = HandicappedGolfer(name, membership, handicap)
       
            self._golfers[golfer.memberID] = golfer
            
        return self._golfers
           
    def searchGolfers(self, memberID):
        """ Searches and and returns the Golfer object matching memberID parameter
        If not found, method returns None """

        for golfer in self._golfers:
            if memberID == self._golfers.keys():  
                return golfer
            else:
                return None

    def searchBooking(self, teeTime):
        """ Searches and returns the Flight object playing at this Teetime slot
        If no flight has booked this TeeTime slot, method returns None."""
       
        for teeTime in self._bookings.keys():
            if teeTime is not None: 
                return self._bookings[teeTime]
            else:
                return None      

    def searchMemberBooking(self, memberID):
        """ Searches and returns the Teetime slot that this member has booked.
        If the member has no booking, the method returns None."""
        
        for teeTime in self._bookings:
            if self.searchGolfers(memberID) in self._bookings.values():
                return teeTime
            else:
                return None

    def addBooking(self, teeTime, flight):
        """ Allows flight to book TeeTime slot """
        
        result = self.searchBooking(teeTime)         

        if teeTime not in self._bookings.keys(): #No such TeeTime slot
            raise GolfingException("There is no such TeeTime.")
        
        elif result is not None: #Teetime is already taken up by another Flight
            raise GolfingException("TeeTime slot is already booked by another flight.")
        
        elif self._golfingDate.weekday() > 4: #Validate if members of flight are able to play on weekends
            eligibility = flight.getWeekendEligibility()
            if eligibility == False:
                raise GolfingException("Sorry, flight not eligible to play on weekend.")   
        
        else: #Validate if a golfer has another booking
           for member in flight.getGolfersID():
            search = self.searchMemberBooking(member)
            if search is not None:
                raise GolfingException("One member already has another booking.")
        
        self._bookings[teeTime] = flight

    def cancelBooking(self, teeTime):
        """ Removes the flight's booking of the Teetime slot """
        
        result = self.searchBooking(teeTime)         

        if teeTime not in self._bookings.keys(): #No such TeeTime slot
            raise GolfingException("There is no such TeeTime.")
        
        elif result is None: #No booking to cancel
            raise GolfingException("TeeTime slot has no booking to be cancelled.")
        
        self._bookings[teeTime] = None

    def getBookings(self):
        """ Returns a string representing all TeeTime slots and the memberID
        of the flight of golfers (if booked), or "no booking" if TeeTime slot 
        is not booked."""

        line = f"{key} - "
        for key in self._bookings.keys():
            if self._bookings[key] == None:
                 line += 'No Booking' + '\n'
            else:
                 line += flight.getGolfersID() + '\n' 

        return line

    def getEmptyTeeTimes(self):
        """ Returns a list of TeeTime slot times that are not booked """

        emptyTeeTimes = []
        for key in self._bookings.keys():
            if self._bookings[key] == None:
                emptyTeeTimes.append(key)
        return emptyTeeTimes

#3(b)***********************************************************

def getIntegerRange(userinput, min, max):
    """Ensure user inputs menu option within range"""
    while True:
        try:
            value = int(input(userinput))

            if min <= value <= max:
                return value
            else:
                print("Sorry, please re-enter within range ({}, {})".format(min, max))
        except:
            print("Sorry, I do not understand that. Please try again.")

def menuOption(golfingDate):
    golfingDate = datetime.strptime(golfingDate,"%d-%b-%Y")

    print(f"\nGolf Booking for {golfingDate.date()} {calendar.day_name[golfingDate.weekday()]}")
    print("======================================")
    print("1. Submit Booking")
    print("2. Cancel Booking")
    print("3. Edit Booking")
    print("4. Print play Schedule")
    print("5. Overview of Tee Schedule")
    print("0. Exit")
    option = getIntegerRange("Enter choice: ",0,5)
    return option

def formFlight(golfClub): #Get input of memberID
    print("\nEnter 3 or 4 golfers to form a flight")
    print("==========================================")
    golferFlightID = []
    n = 1
    status = True
    while True:
        golfer = int(input(f"Enter ID for golfer {n} or -1 to stop: "))
        golferFlightID.append(golfer)
        if golfer == -1:
            golferFlightID.remove(golfer)
            #Validate that flight has min 3 and max 4 golfers
            if len(golferFlightID) < 3:
                print("Not enough golfers in this flight.")
                status = False 
            break
        #Validate that the golfer's member ID is valid golfer
        elif golfer not in golfClub.setupGolfers('Golfers.txt').keys():
            print("Golfer not a valid golfer member.")
        elif len(golferFlightID) == 4:
            status = True
            break  
        else:
            n += 1
    return golferFlightID, status

def availTeeTimes(golfClub):
    #Display available tee times
    emptyTeeTime = golfClub.getEmptyTeeTimes()
    t = 1
    print("\nList of available tee times")
    print("=============================")
    for teeTime in emptyTeeTime:
        print(f"{t}. {teeTime} \n")
        t += 1
    return emptyTeeTime

def performAddBooking(golfClub, golfingDate, golfClubPlayers):
    #Get input of memberID
    golferFlightID, status = formFlight(golfClub)

    #Display available tee times
    if status == True:

        emptyTeeTime = availTeeTimes(golfClub)

        #Get input selection for tee time
        select = int(input("Enter selection: "))
        teetime = emptyTeeTime[select-1]
        
    #Add booking
    try:
        flightlist = []
        for g in golferFlightID:
            golfer = golfClubPlayers[g]
            flightlist.append(golfer)

        flight = Flight(flightlist)
        golfClub.addBooking(teetime, flight)
        #print(golfClub._bookings)
    except Exception as e:
        print(e)

    else:
        print(f"Tee Time {teetime} booked for flight with golfers {golferFlightID}")       

def performCancelBooking(golfClub):
    #Get input of memberID
    memberID = input("Enter member ID to cancel booking: ")
    
    #search for booking
    teetime = golfClub.searchMemberBooking(memberID)
    print(teetime)
    if teetime == None:
        print("You do not have any bookings. Cancellation of booking failed.")
    else:
        golfClub.cancelBooking(teetime)
        print(f"Tee Time {teetime} cancelled successfully.")

def performEditBooking():
    #Get input of tee time to edit
    editTeeTime = input("Enter TeeTime (HH:MM) to edit booking: ")
    pass

def printPlaySchedule():
    pass

def printTeeSchedOverview():
    pass

def dataSetUp(course, golfClub, golfingDate, golfClubPlayers):
    #add data to be used in main()
    golfClub.addTeeSlot("08:08")
    golfClub.addTeeSlot("08:18")
    golfClub.addTeeSlot("08:28")

    #Teeslot 07:28
    g1 = golfClubPlayers[21]
    g2 = golfClubPlayers[57]
    g3 = golfClubPlayers[58]
    g4 = golfClubPlayers[15]
    f1 = Flight([g1,g2,g3,g4])
    golfClub.addBooking("07:28", f1)

    #Teeslot 07:48
    #g5 = golfClubPlayers[8]
    #g6 = golfClubPlayers[18]
    #g7 = golfClubPlayers[17]
    #f2 = Flight([g5,g6,g7])
    #golfClub.addBooking("07:48", f2)

    #Teeslot 07:58
    #g8 = golfClubPlayers[9]
    #g9 = golfClubPlayers[27]
    #g10 = golfClubPlayers[24]
    #f3 = Flight([g1,g2,g3,g4])
    #golfClub.addBooking("07:58", f3)

def main():
  # display of menu, getting option and decision flow
    course = str(input("Please enter file name of golfcourse: "))
    golfingDate = input("Enter Golfing Date [dd-mmm-yyyy]: ").strip()
    golfClub = GolfCLub('Fantasy Golf Club', course, golfingDate)
    golfClubPlayers = golfClub.setupGolfers('Golfers.txt')
    dataSetUp(course, golfClub, golfingDate, golfClubPlayers)
    
    
    while True:
        option = menuOption(golfingDate)
        if option == 0:
            break
        elif option == 1:
            performAddBooking(golfClub, golfingDate, golfClubPlayers)
        elif option == 2:
            performCancelBooking(golfClub)
        elif option == 3:
            performEditBooking()
        elif option == 4:
            printPlaySchedule()
        else:
            printTeeSchedOverview()

main()


# basic classes are working
# 1 - create the "master" big class at begining of main()
# 2 - setup some basic data into the master class
# 3 - do the listing
# 4 - add, search
# 5 - delete, change/update