import time
import Main

# Below is the Car class. The simulation starts from here.
class Car:
    'Handles all car information as well as actions'
    maxSpeed = 25     # default speed of the car in kmph
    sleepTime = 0.01  # sleep so that the running output of the program is visible to the user 
    
    laneDist = 0
    distanceCovered = 0
    remainingDist = 0
    speed = 0
    currentLane = 'M'
    
    def __init__(self):
        self.path = Main.Main().path
        self.totalDist = self.path[0]['Dist']   # Total distance from the Source to the Destination
                
    def setEventHandler(self,event):
        self.eventHandler = event
        
    def startCar(self):
        print "Hello, I'm BayMax, your Self-Driving Car. "  # Name inspired from the AI robot in the animated movie "Big Hero 6"
        time.sleep(2)
        print "Please note that all distances displayed are in meters and the speed is in kmph."
        time.sleep(3) 
        print "Let's get ready for a drive\n"
        time.sleep(2)
        print "Source: ", self.path[0]['Src']
        time.sleep(1)
        print "Destination: ", self.path[0]['Dest']
        time.sleep(1)
        print "Distance: ", self.path[0]['Dist'] 
        time.sleep(1)
        print "Fasten your seat-belts..."
        time.sleep(2)
        print "Starting Car...\n"
        time.sleep(1)
        start_time = time.time()
        self.startSimulation()
        print("Destination: "+self.path[0]['Dest']+", Reached")
        print("Total Journey Time: "+str(time.time()-start_time)+" seconds")  
    
    def accelerate(self, priority, speed_limit): #accelerates the car
        time.sleep(self.sleepTime)                           # priority determines the rate at which the car accelerates
        self.speed = min(self.speed + 18014 * self.sleepTime * priority/3600, speed_limit) # 18014 is unit adjustment factor
          
    def  decelerate(self, priority, speed_limit): #decelerates the car
        time.sleep(self.sleepTime)
        a = self.speed*self.speed/2/self.remainingDist    # motion equation
        self.speed = max(self.speed - a*0.1*priority/3600.0, speed_limit) # priority determines the rate at which the car decelerates
        
     
    def startSimulation(self): #simulates events one after the other
        
        events = self.path[0]['event']
        
        for e in range(len(events)):
            self.currentLane = 'M'
            
            event = events[e]
            next_turn = event['turn']
              
            self.simulate(events[e])
              
            if next_turn == 'L':
                print("Taking a left turn...\n")
            elif next_turn == 'R':    
                print("Taking a right turn...\n")
            elif next_turn == 'S':
                print("Going straight...\n")
            time.sleep(3)       
                     
    
    def move(self):  # increases the distance covered by the car
        self.distanceCovered += self.speed * self.sleepTime/3600.0
        self.remainingDist = self.laneDist - self.distanceCovered 
            
    def simulate(self, event):                          #simulates one event(lane) at a time
        self.laneDist = round(float(event['move']),2)   #total lane distance
        self.distanceCovered = 0                        #distance covered by car in current lane(initially)
        self.remainingDist = self.laneDist - self.distanceCovered
        self.eventHandler.laneChanged = False
        self.eventHandler.speed_limit_flag = False
        self.eventHandler.sig_cnt = -1
        self.eventHandler.displayCount = -1
        
        while self.distanceCovered <= self.laneDist:
            time.sleep(self.sleepTime)
                                                        # 'Y' - displays full output 
            self.eventHandler.displayFullDtls('N')      # 'N' - displays partial output (once every 20 iterations), else the output will
                                                        #  be printed on the console very often
            is_dest = self.eventHandler.handleEvent(event)       
            
            if is_dest == True:
                break
            
            
        
        
        
             
