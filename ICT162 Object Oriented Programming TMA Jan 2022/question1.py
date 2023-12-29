#TMA Question 1

#1(a)***********************************************************

class Hole:
    
    def __init__(self, number, distance, par, index):
        """ constructor that execute when an object is created """
        self._number = number   
        self._distance = int(distance)   
        self._par = int(par)
        self._index = index   

    @property  # accessor / getter method
    def number(self):
        return self._number

    @property  # accessor / getter method
    def distance(self):
        return self._distance

    @property  # accessor / getter method
    def par(self):
        return self._par

    @property  # accessor / getter method
    def index(self):
        return self._index

    def getDuration(self):
        """ computes the estimated time to complete playing the hole. 
        Formula (in seconds)-> setup time + play time """
        
        if self._par <= 6:
            setup_sec = 180
        elif self._par <= 12:
            setup_sec = 150
        else:
            setup_sec = 120

        setup_time = self._par * setup_sec

        if self._distance <= 100:
            play_time = 60
        elif self._distance <= 200:
            play_time = 120
        elif self._distance <= 300:
            play_time = 180
        elif self.distance <= 400:
            play_time = 240
        elif self.distance <= 500:
            play_time = 300
        else:
            play_time = 360

        return setup_time + play_time

    def __str__(self):
        """ string representation of the object """
        return "{}   {}   {}   {}".format(self._number, self._par, self._index, self._distance)


#1(b)***********************************************************
from datetime import datetime, timedelta

class Course:

    def __init__(self, filename):
        """ constructor that execute when an object is created """
        self._name = filename.split(".", 1)[0]
        
        self._holes = []
        for holes in open(self._name + '.txt', 'r'):
            self._holes.append(holes.strip('\n'))
        
        self._totalPar = 0
        for holes in open(self._name + '.txt', 'r'):
            par, index, distance = holes.split(',')
            self._totalPar += int(par)
        
    @property  # accessor / getter method
    def name(self):
        return self._name
    
    def getPlaySchedule(self, teeTime):
        """ returns the estimated start and finish time for all 18 holes,
            given the teeTime (datetime) as parameter """
        
        teeTime = datetime.strptime(teeTime, "%H:%M")
        n = 1  #Hole counter
        startTime = teeTime
        
        line = f"""
Tee Off time: {teeTime.hour:02d}:{teeTime.minute:02d}
Course: {self._name}            Total PAR: {self._totalPar}
Hole     Par     Index     Distance     Start      Finish
"""
        #get estimated time to complete playing each hole
        for hole in self._holes:
            #create Hole
            par, index, distance = hole.split(',')
            hole = Hole(n, distance, par, index)
            
            #calculate estimated duration
            duration = timedelta(seconds = hole.getDuration())
            finishTime = startTime + duration

            line = line + str(n).ljust(10) + par.ljust(9) + index.ljust(10) + distance + 'm'.ljust(8) + \
            f"{startTime.hour}:{startTime.minute:02d}".ljust(11)  + f"{finishTime.hour}:{finishTime.minute:02d}" + '\n'
            
            startTime = finishTime + timedelta(minutes = 1)
            n += 1  
        
        return line

    def __str__(self):
        """ string representation of the object """
        n = 1
        line = f"""
Course: {self._name}            Total PAR: {self._totalPar}
Hole     Par      Index     Distance
"""
        for hole in self._holes:
            par, index, distance = hole.split(',')
            line = line + str(n).ljust(10) + par.ljust(9) + index.ljust(11) + distance + 'm' + '\n'
            n += 1

        return line


def main():
    #(i)***********************************************************
    course1 = Course('Pebble Bay.txt')
    course2 = Course('Laguna.txt')

    #(ii)***********************************************************
    print(course1.getPlaySchedule("07:08"))
    print(course1.getPlaySchedule("09:18"))

    print(course2.getPlaySchedule("07:08"))
    print(course2.getPlaySchedule("07:08"))

main()
    


