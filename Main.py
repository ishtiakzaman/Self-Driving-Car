import Car
import EventHandler

class Main:
    def __init__(self):
    
       # Please note that the distance is in km. and the speed is in kmph. in the code.
       # However while displaying the distance is displayed in 'meters' for readability purpose. The speed is displayed in kmph.
       # Also, the values in the output are purposefully not rounded off so that the minute changes in the distance and speed is visible 
       
       # Below is the structure of the path that will be created from the text file. 
       # The values can be changed in the text file 
       
       #         path = [{'Src':'FP','Dest':'IMU','Dist':0.5,
       #                       'event': [{'turn':'L','move':0.1,'lane':2,'signal':True,'sign':'speed~20'},
       #                                 {'turn':'R','move':0.1,'lane':2,'signal':True,'sign':'speed~40'},
       #                                 {'turn':'','move':0.1,'lane':1,'signal':False,'sign':'speed~10'}]}]
        
        path_file = open('path.txt','r')    #The input text file is opened for reading
        s=''
        main_dict = {}
        inner_dict = {}
        main_list = []
        inner_list = []
        flag = False
        while 1:
            s = path_file.readline()
            temp = s.split(',')
            
            for item in temp:
                key = item[:item.find(':')]
                value = item[item.find(':')+1:]
                value = value.strip('\n')
                
                
                if key == 'NoOfLanes':             #Based on the 'NoOfLanes', the lane data is added to the list 
                    for i in range(int(value)):
                        s = path_file.readline()
                        temp1 = s.split(',')
                        for item1 in temp1:
                            key = item1[:item1.find(':')]
                            value = item1[item1.find(':')+1:]
                            value = value.strip('\n')
                            
                            if value!='':
                                if key == 'lane' :
                                    value = int(value)
                                elif key == 'signal':
                                    if value == 'False':
                                        value = False
                                    else:
                                        value = True       
                                        
                                inner_dict[key]=value
                                
                
                        inner_list.append(inner_dict)        
                        inner_dict = {}    
                    main_dict['event'] = inner_list
                    main_list.append(main_dict)
                    flag = True
                    break
                else:
                    main_dict[key]=value
            
            if flag == True:
                break
        
        self.path = main_list
    
    def start(self):
        c = Car.Car()                      # creating the Car object
        e = EventHandler.EventHandler(c)   # the event handler object is created. The Car object is passed as an argument
        c.setEventHandler(e)
        c.startCar()                       # method in car class is invoked to start the car
    
if __name__ == "__main__":   #The program starts from here
    main = Main()
    main.start()