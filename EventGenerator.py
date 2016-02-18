from random import randint
import time

# Below is the Event Value Generator 
class EventGenerator(object):
    mirror_count = 600
    signal_count = 0
    prev_signal = 'RED'

    def __init__(self):
        self.check_signal_count = 100*60   # pre-determined value for signal counter
        self.check_mir_count = 10*60       # pre-determined value for lane change counter
                                           # required to probe the value generator periodically, else probing will occur very frequently
    
    #Below method resets the counter for the signal    
    def resetSignal(self):
        EventGenerator.signal_count = 0
        EventGenerator.prev_signal = 'RED'
    
    #Below method resets the counter for the lane change         
    def resetMirrorSignal(self):
        EventGenerator.mirror_count = 0
    
    #Below method returns a random value to the controller related to the signal
    def probeSignal(self):
        
        signal = ['RED','AMBER','GREEN']
        EventGenerator.signal_count = EventGenerator.signal_count +1
        curr_signal = signal[randint(0,2)]
    
        if EventGenerator.signal_count == self.check_signal_count:  # generate value only if the counter reaches a pre-determined value...
            EventGenerator.signal_count = 0                        
            while 1:
                if EventGenerator.prev_signal == 'RED' and curr_signal == 'AMBER':     # validations for the signal color based on prev
                    curr_signal = signal[randint(0,2)]                                 # and current signal color generated.
                elif EventGenerator.prev_signal == 'GREEN' and curr_signal == 'RED':
                    curr_signal = signal[randint(0,2)] 
                elif EventGenerator.prev_signal == 'AMBER' and curr_signal == 'GREEN':
                    curr_signal = signal[randint(0,2)]  
                else:
                    break
    
            
            print("Current Signal: "+curr_signal+"\n")
            EventGenerator.prev_signal = curr_signal
            return curr_signal 
        else:
            return EventGenerator.prev_signal
    
    #Below method returns the value to determine the lane change
    def checkMirror(self):
        car = ["Y", "N"]
        EventGenerator.mirror_count = EventGenerator.mirror_count + 60
        if EventGenerator.mirror_count >= self.check_mir_count:
            EventGenerator.mirror_count = 0
            return car[randint(0,1)]
        return "N"
    
    #Below method returns the value to determine whether the car can move after stopping at the STOP sign
    def probeAllClear(self):
        status = ['GREEN','RED']
        time.sleep(2)
        return status[randint(0,1)]