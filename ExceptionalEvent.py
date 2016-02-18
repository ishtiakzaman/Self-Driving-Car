import sys
from State import State
import random

class ExceptionalEvent:	

	def __init__(self):		
		self.__name = 'exceptional_event'	
		self.__target = ['bus', 'pedestrian', 'deer', 'car', 'water']
		self.__direction = ['same', 'opposite', 'left', 'right']
		self.__lane = ['same', 'opposite', 'left', 'right']		
				
	def giveExceptionalEvent(self):
		# Returns an exceptional event with 0.5% chances, returns false otherwise
		if random.random() < 0.005:
			
			# Create the exceptional event state
			event = State('event');
			
			event.speed = {}
			event.distance = {}
			event.direction = {}
			event.lane = {}			
						
			# Randomly fill out the properties of the exceptional event
			event.target = self.__getRandomTarget()
			event.speed[event.target] = self.__getRandomSpeed()
			event.distance[event.target] = self.__getRandomDistance()
			event.direction[event.target] = self.__getRandomDirection()
			event.lane[event.target] = self.__getRandomLane()
			return event
		else:		
			return False
			
	def __getRandomTarget(self):
		return self.__target[int(random.random()*len(self.__target))]
		
	def __getRandomSpeed(self):
		return round(random.random()*30, 2)
		
	def __getRandomDistance(self):
		return round(random.random()*60-30, 2)
		
	def __getRandomDirection(self):		
		return self.__direction[int(random.random()*len(self.__direction))]
		
	def __getRandomLane(self):
		return self.__lane[int(random.random()*len(self.__lane))]
				

				
				
				
			