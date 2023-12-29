#TMA Question 2

#2(a)***********************************************************

from abc import ABC, abstractmethod
from datetime import datetime

class Golfer:
    _NEXT_ID = 1
    
    def __init__(self, name, membership):
        """ constructor that execute when an object is created """
        self._memberID = Golfer._NEXT_ID 
        Golfer._NEXT_ID += 1  
        self._name = name   
        self._membership = membership
        self._status = True 
        
    @property  # accessor / getter method
    def memberID(self):
        return self._memberID
        
    @property  # accessor / getter method
    def name(self):
        return self._name

    @property  # accessor / getter method
    def membership(self):
        return self._membership

    @membership.setter
    def membership(self, newValue):
        self._membership = newValue

    def getMembershipStatus(self):
        """ returns the value of _status """
        return self._status

    def setMembershipStatus(self, newValue):
        """ accepts a Boolean value as parameter and assign to _status """
        self._status = newValue

    @abstractmethod
    def getHandicap(self): 
        """ returns the handicap number for golfer """
        pass

    def __str__(self):
        """ string representation of a Golfer object """
        if self._status == True:
            status = "(A)"
        else:
            status = "(I)"
        return f"Member ID: {self._memberID}   Name: {self._name}   Membership: {self._membership}{status}"

#2(b)***********************************************************

class HandicappedGolfer(Golfer):
    
    def __init__(self, name, membership, handicap):
        """ constructor that execute when an object is created """
        super().__init__(name, membership)
        self._handicap = handicap
    
    def getHandicap(self):
        """ returns the handicap number for this golfer """
        return self._handicap

    def __str__(self):
        """ string representation of a HandicappedGolfer object """    
        return super().__str__() + f"   Handicap:{self._handicap}"

class PCHolder(Golfer):

    def __init__(self, name, membership, expiryDate):
        """ constructor that execute when an object is created """
        super().__init__(name, membership)
        self._expiryDate = datetime.strptime(expiryDate,"%d-%b-%Y")
    
    def getMembershipStatus(self):
        """
        returns False if the expiry date of the Proficiency Certificate has lapsed (compare to current datetime). 
        Otherwise, it returns the membership status of this golfer.
        """
        if self._expiryDate >= datetime.now():
            return self._membership
        else:
            self.setMembershipStatus(False)
            return self._status

    def renew(self, newExpiryDate):
        """ accepts and set a new expiry date for the Proficiency Certificate """
        self._expiryDate = datetime.strptime(newExpiryDate,"%d-%b-%Y")

    def getHandicap(self):
        """ return 99.9 for PCHolders """
        return 99.9 

    def __str__(self):
        """ string representation of a PCHolder object """
        return super().__str__() + f'   Expiry: {datetime.strftime(self._expiryDate,"%d-%b-%Y")}'        

#2(c)***********************************************************

class GolfingException(Exception):
    """for raising exception when golfing rule is violated"""
    pass

#2(d)***********************************************************

class Flight:

    def __init__(self, golfers):
        """ constructor that execute when an object is created """
        self._golfers = golfers
        
        #Validate number of golfers to be min 3 and max 4
        if len(self._golfers) < 3 or len(self._golfers) > 4:
            raise GolfingException("Sorry, a flight can only consist of 3 or 4 golfers.")
        
        #Validate that membership status of golfers in the flight are active
        for golfers in self._golfers:
            if golfers.getMembershipStatus() == False:
                raise GolfingException("Sorry, a member in your flight has an inactive membership.") 

    def searchGolfer(self, memberID):
        """ 
        Using the parameter memberID, this method searches and returns the Golfer object
        if there is a golfer in the flight with matching memberID. If not found, returns None.
        """
        for golfer in self._golfers:
            if memberID == golfer.memberID:  
                return golfer
            else:
                return None

    def getGolfersID(self):
        """
        returns the flight's golfers' memberID in a list
        """
        GolfersID = []
        for golfer in self._golfers:
            GolfersID.append(golfer.memberID)
        
        return GolfersID

    def getWeekendEligibility(self):
        """
        return a Boolean value indicating if this flight of golfers
        can book a golf session on a weekend
        """
        for golfer in self._golfers:
            if golfer.membership == 'Basic':
                weekendEligibility = False
                break 
            elif golfer.getMembershipStatus() == False:
                weekendEligibility = False
                break
            else: 
                weekendEligibility = True
                
        return weekendEligibility
            

#2(e)***********************************************************

def main():

    print('(i)********************************************************')

    print('--before--')
    #Print the weekend eligibility of this flight
    g1 = HandicappedGolfer('Jeff', 'Full', 13.1)
    g2 = HandicappedGolfer('Jim', 'Basic', 4)
    g3 = HandicappedGolfer('Joe', 'Full', 19)
    g4 = HandicappedGolfer('Jack', 'Full', 2.3)

    try:
        f1 = Flight([g1,g2,g3,g4])
        print(f1.getWeekendEligibility())  
    except Exception as e:
        print(e) 

    print('--after--')
    #Write necessary statements to update golfers details 
    #so f1 is eligible to play golf on weekend
    
    g2.membership = 'Full' #set new membership
    
    try:
        f1 = Flight([g1,g2,g3,g4])
        print(f1.getWeekendEligibility())   
    except Exception as e:
        print(e)

    print('(ii)********************************************************')

    print('--before--')
    g5 = HandicappedGolfer('Tom', 'Full', 11)
    g6 = HandicappedGolfer('Neil', 'Full', 2.5)
    g7 = PCHolder('Charles', 'Full', '30-Jul-2021')
    print(g7.getMembershipStatus())
    
    #Handle the exception from the above creation
    try:
        f2 = Flight([g5,g6,g7])
        print(f2.getWeekendEligibility())   
        print('Eligible for Weekend Tee Booking.') 
    except Exception as e:
        print(e)

    print('--after--')
    #Write necessary statements to update golfers' details 
    #so Flight f2 can be created successfully

    g7.renew('20-Apr-2023')

    try:
        f2 = Flight([g5,g6,g7])
        print(f2.getWeekendEligibility())   
        print('Eligible for Weekend Tee Booking.') 
    except Exception as e:
        print(e)
    
main()




