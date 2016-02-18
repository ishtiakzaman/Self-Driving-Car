import sys
from State import State

class Retriever:

	def __init__(self, memoryPlanFileName):		
		self.__memoryFileObject = self.__openFile(memoryPlanFileName)		
		self.__processFile(self.__memoryFileObject, 'plan_memory')		
		
		# Defining the similarity matrix
		self.__similar = {'bus':{'car':0.8},'pedestrian':{'deer':0.3,'dog':0.5},'deer':{'dog':0.3},\
			'water':{'bus':0,'pedestrian':0,'deer':0,'car':0}}

	def __openFile(self, fileName):
		try:
			fo = open(fileName, "r")
		except IOError:
			print "File", fileName, "cannot be read"
			sys.exit()
		return fo
			
	def __processFile(self, fo, strListName):
		content = fo.read()
		content = content.replace('\r','')
		exec('self.' + strListName + '=' + content)
				
	def findClosestMatch(self, currentState):	
		# Find a closest match from the case based to the currentState
		
		# Keep a record of similarity
		
		# maxSimilarityValue is equal to min threshold, which is 50% of max possible similarity(=5)
		maxSimilarityValue = 2.5
		retrievedCase = []		
		
		# Loop through all plans in the case based
		for plan in self.plan_memory:
			
			currentStateList = plan[0]		
			
			# Create a state for the plan we are accessing at the moment
			currentStateMemory = State("currentStateMemory")									
			for stateItem in currentStateList:						
				exec("currentStateMemory."+stateItem)					
				
			# Get the similarity value of this state with our state
			similarityValue = self.__getSimilarityValueState(currentState, currentStateMemory) 	
						
			#print "SIMILARITY VALUE", similarityValue
			
			# if exceeds max threshold(4.5 = 90% of 5), returns this and skip the rest
			if similarityValue > 4.5:
				return plan
				
			# Checking this similarity with maximum similarity found so far
			if similarityValue > maxSimilarityValue:
				maxSimilarityValue = similarityValue
				retrievedCase = plan			
		
		if len(retrievedCase) == 0:
			# No match found, returns the default action of stopping immediately	
			retrievedCase.append([])
			retrievedCase.append([('decelerate', 'me', 150, 0)])
			
		return retrievedCase
				
	def __getSimilarityValueState(self, state1, state2):
		# Returns similarity value between two given states
		targetMatch = self.__getTargetSimilarity(state1.target, state2.target)
		value = 0
		propList = ['speed','distance','direction','lane']
		for prop in propList:			
			
			if hasattr(state1, prop) and hasattr(state2, prop):				
				value = value + self.__getSimilarityValueProp(prop, state1, state2)
				
		return value * targetMatch
		
	def __getTargetSimilarity(self, target1, target2):
		# Target is the most important properties of a state
		# Returns the similarity of the two given targets
		if target1 == target2:
			return 1
		
		try:
			value = self.__similar[target1][target2]
		except KeyError:
			try:
				value = self.__similar[target2][target1]
			except KeyError:
				value = 0.1
				
		return value
		
	def __getSimilarityValueProp(self, propName, state1, state2):
		# Returns a value between 0(no similarity) and 1(exact similar) for a property of the states
		pair1 = getattr(state1, propName)
		pair2 = getattr(state2, propName)
		#print "H", propName, pair1, pair2
				
		key1 = pair1.keys()[0]
		value1 = pair1[key1]
		
		key2 = pair2.keys()[0]
		value2 = pair2[key2]
		
		# If they are same, perfect match return 1
		if key1 == key2 and value1 == value2:
			value = 1
			
		elif propName == 'speed':	
			# Compare speed properties
			value1 = pair1['me']
			value2 = pair2['me']	
			if value2 > value1:
				temp = value1
				value1 = value2
				value2 = temp	
				
			if value1 == 0:
				value = 0
			else:
				value = 1.0 - ((value1 - value2) * 1.0 / value1)
			
			value1 = pair1[state1.target]
			value2 = pair2[state2.target]	
			if value2 > value1:
				temp = value1
				value1 = value2
				value2 = temp		
			
			if value1 == 0:
				value = 0
			else:				
				value = value + (1.0 - ((value1 - value2) * 1.0 / value1))
			
		elif propName == 'distance':	
			# Compare distance properties
			if value2 > value1:
				temp = value1
				value1 = value2
				value2 = temp
			if value2 < 0:
				value1 = value1 - value2
				value2 = 0
			
			if value1 == 0:
				value = 0
			else:
				value = 1.0 - ((value1 - value2) * 1.0 / value1)
			
						
		elif propName == 'direction':	
			# Compare direction properties
			if (value1 == 'same' and value2 == 'opposite') or \
				(value2 == 'same' and value1 == 'opposite'):
				# Opposite direction
				value = 0			
			else:
				value = 0.5
		
		elif propName == 'lane':	
			# Compare lane properties
			if (value1 == 'same' and value2 == 'opposite') or \
				(value2 == 'same' and value1 == 'opposite'):
				# Opposite direction
				value = 0			
			else:
				value = 0.5
		
		#print "Value:", propName, pair1, pair2, value
		return value
				
				
				
			