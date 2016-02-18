import time
import EventGenerator
import Car
from Retriever import Retriever
from ExceptionalEvent import ExceptionalEvent

# Below is the Car Controller
class EventHandler(object):
    
    g = 127008
    displayCount = -1
    sig_cnt = -1
    speed_limit_flag = False
    
    def __init__(self, car):
        self.car = car
        self.rules = [['1',['signal:RED'],['acceleration:N']],     # rule base for signal, stop sign and speed limit
                      ['2',['signal:AMBER'],['acceleration:N']],
                      ['3',['signal:GREEN'],['acceleration:Y']],
                      ['4',['sign:STOP'],['acceleration:N']],
                      ['5',['speed:Y'],['aceleration:Y']],
                      ['6',['speed:N'],['acceleration:N']]]
        
        self.evtgen = EventGenerator.EventGenerator()    # creating random event generator object
        self.rt = Retriever('casebasedplan.txt')         # Retriever object for case retrieval
        self.exception_event = ExceptionalEvent()
        self.laneChanged = False
        
    # Below method handles the basic driving events 
    def handleEvent(self, event): #all the event handling goes here
        action = ''
        self.speed_limit = self.car.maxSpeed
        
        if event['turn'] != '' and self.car.currentLane == 'M':
            if self.car.distanceCovered >= .65*self.car.laneDist and self.laneChanged == False:  # changes lane after distance covered 
                print("\nAttempting to change lanes...")                                       # crosses the threshold (65% of lane dist)
                self.laneChanged = self.handleLaneChange(event)
        
        if 'signal' in event:        # checking if signal is present at the end of the lane
            signal = event['signal']
            
        if 'sign' in event:           # checking for lane signs (speed limit)
            sign = event['sign']
            if 'speed' in sign:
                self.speed_limit = int(sign[sign.find('~')+1:])
                if self.speed_limit_flag == False:
                    print("\nSpeed Limit Sign in view...Speed Limit: "+str(self.speed_limit))
                self.handleSpeedSign()
        
        excp_event = self.exception_event.giveExceptionalEvent()  # event generator generates exception event
        
        if excp_event != False:
            print("\nExceptional Event in Progress...")
            self.handleExpCase(excp_event)               # method for handling exceptional events
            time.sleep(1)
                   
        
        if signal == True:    # if signal is present at the end of the lane. Either signal or STOP sign at the end of the lane.
            if self.car.remainingDist <= self.getBrakingDist():
                print("\nBraking Distance Reached...Signal in view...")
                self.evtgen.resetSignal()
                time.sleep(2)
                action = self.handleSignalStopSign(1, 'SIGNAL', event)
                return action
        else:                # indicates stop sign is present at the end of the lane. 
            if self.car.remainingDist <= self.getBrakingDist():
                print("\nBraking Distance Reached...STOP sign in view...")
                time.sleep(2)
                action = self.handleSignalStopSign(1, 'STOP', event)
                return action
        
        self.speed_limit = self.car.maxSpeed
        
        if(self.car.speed < self.speed_limit):       # if speed is less than speed limit then accelerate
            self.car.accelerate(1, self.speed_limit)  
        self.car.move()   
                    
        return False
    
    # Below method handles the exceptional events
    def handleExpCase(self, event):
        
        event.speed['me'] = self.car.speed   
        retrievedCase = self.rt.findClosestMatch(event)   # case retrieved from case base
        self.printExcpCase(event,retrievedCase)           # prints the details of the event
        
        result = retrievedCase[1][0]
        action = result[0]
        priority = result[2]
        speed_limit = result[3]
        
        if action == 'decelerate':
            print("Reducing Speed to speed limit of "+str(speed_limit)+"\n")
        else:
            print("Increasing Speed to speed limit of "+str(speed_limit)+"\n") 
        time.sleep(1)        
        
        while True:
            self.displayFullDtls('Y') 
            time.sleep(0.1)
            if action == 'decelerate':
                if self.car.speed > speed_limit:
                    self.car.decelerate(priority, speed_limit)       # decelerate the car
                    self.car.move()
                    if speed_limit == 0 and self.car.speed <= 0.35:  # if the car's speed goes below 0.35 kmph, reduce speed to 0.
                        self.car.speed = 0                    # This is done because the car's speed never reaches 0, only close to 0.
                    
                else:
                    break
            elif action == 'accelerate':
                if self.car.speed < speed_limit:
                    self.car.accelerate(priority, speed_limit)  # accelerate the car
                    self.car.move()
                else:
                    break
               
        print("\nExceptional event concluded...")  
        if self.car.speed <= self.speed_limit:
            temp_str = "increased"
        else:
            temp_str = "decreased"  
                
        if action == 'decelerate':
            print("\nSpeed reduced to "+str(self.car.speed)+". Speed will be "+temp_str+" to speed limit: "+\
                  str(self.speed_limit)+"\n")
        else:
            print("\nSpeed increased to "+str(self.car.speed)+". Speed will be "+temp_str+" to speed limit: "+\
                  str(self.speed_limit)+"\n")     
            
        time.sleep(1)
        
    
    # Below method handles the speed sign       
    def handleSpeedSign(self):
        if self.car.speed <= self.speed_limit:
            if self.speed_limit_flag == False:
                print("Increasing speed to "+str(self.speed_limit)+"\n")
                self.speed_limit_flag = True
            action = self.getAction('speed:' + 'Y')
        else:
            if self.speed_limit_flag == False:
                print("Reducing speed to "+str(self.speed_limit)+"\n")
                self.speed_limit_flag = True
            action = self.getAction('speed:' + 'N')
        self.changeSpeed(1, action, self.speed_limit)

    
    # Below method returns the action based on the rule     
    def getAction(self, event):
        event_value = event[event.find(':')+1:]
        event_type  = event[:event.find(':')]
         
        for rule in self.rules:
            ante = rule[1][0]
            evalue = ante[ante.find(':')+1:]
            etype  = ante[:ante.find(':')]
                
            if etype == event_type and evalue == event_value:  # if event type and event value matches, then return the action 
                result = rule[2][0]
                result_value = result[result.find(':')+1:]
                return result_value              
             
    
    #Below method handles the Signal as well as the Stop sign depending on the event type
    def handleSignalStopSign(self, priority, event_type, event):
        flag = True
        is_last = False
        turn = event['turn']
        
        if turn == 'D':     # checking if this is the last lane i.e. is the destination on this lane
            is_last = True
            
        while 1:
            time.sleep(Car.Car().sleepTime)
            
            if event_type == 'SIGNAL':                      # if event type is Signal
                currentSignal = self.evtgen.probeSignal()   # probe the event value generator for signal value
            
            if self.laneChanged == False:
                self.laneChanged = self.handleLaneChange(event)  # handle lane change if lane not already changed
            
            if event_type == 'SIGNAL':
                self.displayFullDtls('N',currentSignal)
                action = self.getAction('signal:' + currentSignal)
            elif event_type == 'STOP':
                action = self.getAction('sign:' + event_type)    
            
            if action == 'Y':
                speed_limit = self.car.maxSpeed
            else:
                speed_limit = 0
                    
            flag  = self.changeSpeed(priority, action, speed_limit)  #adjust speed based on the action (acceleration/deceleration) 
            
            if flag == False:
                self.car.speed = 0   # car has stopped
                break
            else:
                self.displayFullDtls('N')
                if self.car.distanceCovered >= self.car.laneDist:   # checking if the lane distance has been reached
                    print("\nLane Distance Reached")
                    if is_last == False:
                        return False
                    return True
        
        print("Lane Distance covered: " + str(self.car.distanceCovered*1000)), 
        print(" Speed: " + str(self.car.speed)),
        print(" Remaining Lane Distance: "+str(self.car.remainingDist*1000))
        print("\nCar STOPPED...")
        if is_last == False:
            if event_type == 'SIGNAL':
                print("Waiting for signal to turn GREEN...\n")
            elif event_type == 'STOP':
                print("Waiting to move...\n")
        time.sleep(2)         
        
        if is_last == False:   # not the last lane
            while 1:
                if event_type == 'SIGNAL':
                    signal = self.evtgen.probeSignal()    #probe for signal till "GREEN" is received
                elif event_type == 'STOP':
                    signal = self.evtgen.probeAllClear()  #probe for all clear signal from the value generator
                    
                if signal == 'GREEN':    # if signal is GREEN, accelerate the car and start moving
                    while 1:
                        self.car.accelerate(1, self.speed_limit)
                        self.car.move() 
                        
                        self.displayFullDtls('N')
                        if self.car.distanceCovered >= self.car.laneDist:
                            print("Lane Distance covered: " + str(self.car.distanceCovered*1000)), 
                            print(" Speed: " + str(self.car.speed)),
                            print(" Remaining Lane Distance: "+str(self.car.remainingDist*1000))
                            print("\nLane Distance Reached")
                            time.sleep(2)
                            return False   # Once lane distance is reached, return back to caller
            
        return True            

    # Below method adjusts the speed of the car based on the priority
    def changeSpeed(self, priority, acc_yn, speed_limit):  # acc_yn: 'Y' - Acceleration, 'N' - Deceleration
        if acc_yn == 'N':
            self.car.decelerate(priority, speed_limit)
            self.car.move()
            
            if self.car.speed < 0.35 or self.car.remainingDist <= 0.001: 
                return False          
        else:
            if(self.car.speed < speed_limit):
                self.car.accelerate(1, speed_limit)  
            else:
                self.car.decelerate(1, speed_limit)       
            self.car.move()              
        
        return True     
    
    # braking distance - distance at which the brakes should be applied to stop the car
    def getBrakingDist(self):
        brakingDistance =  self.car.speed*self.car.speed/2/0.7/self.g
        return brakingDistance

    # Below method handles the lane change
    def handleLaneChange(self, event):
        changeLane = ''
        laneChangeRules =  [[{'lane':1,'turn':'L', 'car':'Y'},'notrequired'],   # rules for lane change
                            [{'lane':1, 'turn':'R', 'car':'Y'},'notrequired'],
                            [{'lane':1, 'turn':'L', 'car':'N'},'notrequired'],
                            [{'lane':1, 'turn':'R', 'car':'N'},'notrequired'],
                            [{'lane':2, 'turn':'L', 'car':'Y'},'no'],
                            [{'lane':2,'turn':'R','car':'Y'},'notrequired'],
                            [{'lane':2,'turn':'R','car':'N'},'notrequired'],
                            [{'lane':2,'turn':'L','car':'N'},'yes'],
                            [{'lane':3,'turn':'R','car':'Y'}, 'no'],
                            [{'lane':3,'turn':'L','car':'Y'}, 'no'],
                            [{'lane':3,'turn':'R','car':'N'}, 'yes'],
                            [{'lane':3,'turn':'L','car':'N'}, 'yes']]
        
        turn = event.get('turn')
        lane = event.get('lane')
        car = self.evtgen.checkMirror()  # probe value generator to check if its safe to change the lane
        for rules in laneChangeRules:
            ante = rules[0]
            if turn == ante.get('turn') and lane == ante.get('lane') and car == ante.get('car'):
                changeLane = rules[1]
                break
        
        if changeLane == 'yes':
            print "Lane change successful...\n"
            time.sleep(2)
            return True
        elif changeLane == 'notrequired':
            print "No need to change lanes but turn ahead...\n"
            time.sleep(2)
            return True
        elif changeLane == 'no':
            print "Cannot change lane right now...\n"
            time.sleep(2)
            return False
        
    # Below method displays the full or partial output based on the argument 'full_yn'. Required as output is displayed very often.
    # full_yn = 'Y' is used when the change in speed needs to be displayed when the priority for deceleration is high.  
    def displayFullDtls(self, full_yn, signal_color = ''):
        displayLimit = 20  # counter used to limit the number of display
        signalLimit = 500  # counter used to limit the number of display while probing signal
        
        if signal_color != '':
            self.sig_cnt = self.sig_cnt + 1
            if self.sig_cnt%signalLimit == 0:
                print("Current Signal: "+signal_color+". Reducing the speed of the car...\n")
                
                if self.sig_cnt != 0:
                        self.sig_cnt = -1
                    
        else:
            if full_yn == 'N':
                self.displayCount = self.displayCount + 1
                if self.displayCount%displayLimit == 0:    
                    print("Lane Distance covered: " + str(self.car.distanceCovered*1000)), 
                    print(" Speed: " + str(self.car.speed)),
                    print(" Remaining Lane Distance: "+str(self.car.remainingDist*1000))
                   
                    if self.displayCount != 0:
                        self.displayCount = -1
            else:
                print("Lane Distance covered: " + str(self.car.distanceCovered*1000)), 
                print(" Speed: " + str(self.car.speed)),
                print(" Remaining Lane Distance: "+str(self.car.remainingDist*1000))
    
    # Below method prints the details of the exceptional case - the occurred event and the retrieved case            
    def printExcpCase(self, event, retrievedCase):
        print("Object: "+str(event.target))
        print("Object Distance from Car: "+str(abs(event.distance[event.target])))
        print("Object Speed: "+str(event.speed[event.target]))
        print("Object Direction wrt Car: "+str(event.direction[event.target]))
        print("")
         
        print("Retrieved Case:")
        
        if len(retrievedCase[0]) == 0:
            print("No Similar Case found. Applying Default Case...\n")
        else:
            object = retrievedCase[0][2]
            object = object[object.find('=')+1:]
            
            dist = retrievedCase[0][0]
            dist = dist[dist.find(':')+1:dist.find('}')]
            dist = dist.strip(' ')
            
            dir = retrievedCase[0][1]
            dir = dir[dir.find(':')+1:dir.find('}')]
            dir = dir.strip(' ')
            
            speed = retrievedCase[0][4]
            speed = speed[speed.find('{')+1:speed.find('}')]
            
            print("Object: "+object)
            print("Distance from Car: "+str(abs(float(dist))))
            print("Direction wrt Car: "+dir)
            print("Speed of Car and Object: "+speed)
            print("")
        
        time.sleep(1)    
                    
                        
        
        