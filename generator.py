import sys
import random
from State import State
from copy import deepcopy
	
target = ['bus', 'pedestrian', 'deer', 'car', 'water']
direction = ['same', 'opposite', 'left', 'right']
lane = ['same', 'opposite', 'left', 'right']
	
def getRandomTarget():
	return target[int(random.random()*len(target))]
	
def getRandomDirection():
	return direction[int(random.random()*len(direction))]
	
def getRandomLane():
	return lane[int(random.random()*len(lane))]

def getRandomSpeed():
	return round(random.random()*30, 2)
		
def getRandomDistance():
	return round(random.random()*60-30, 2)
				
def generate_state_string(state, tab):
	# Generates a string that correspond to the state
	# so that the string will be written in the text file as a case
	stateStr = ''
	firstLoop = True
	for (name,val) in vars(state).items():
		if name != '__name__':
			if isinstance(val, basestring):
				val = '\'' + val + '\''
			strVal = str(val)
			strVal = strVal.replace('\'', '\\\'')					
			delimeter = ',\n'
			if firstLoop == True:
				delimeter = ''
				firstLoop = False
			stateStr = stateStr + delimeter + tab + '\'' + name + '=' + strVal + '\''
	tab = tab[:len(tab)-1]
	stateStr = stateStr + '\n' + tab + ']'
	return stateStr
	
def find_plan(state):
	# Returns a realistic plan for the state
	target = state.target
	if target == 'water':
		# Slippery road, slow down to 15
		plan = ['decelerate', 'me', 10, 15]
		return plan
	if state.direction[target] == 'same' and state.speed[target] < state.speed['me'] \
		and state.distance[target] > 0:
		# Follow the speed of the car in front
		plan = ['decelerate', 'me', 50, 0]
		plan[3] = state.speed[target]
		return plan
	if state.direction[target] == 'same' and state.speed[target] > state.speed['me'] \
		and state.distance[target] < 0:
		# Increase the speed to the car following
		plan = ['accelerate', 'me', 50, 0]
		plan[3] = state.speed[target]
		return plan
	if state.direction[target] == 'opposite' and state.lane[target] == 'same':
		# Stop immediately
		plan = ['decelerate', 'me', 100, 0]
		return plan
	if state.direction[target] == 'left' or state.direction[target] == 'left':
		# Someone crossing
		if state.distance[target] > 15:
			# Stop
			plan = ['decelerate', 'me', 100, 0]
			return plan
		elif state.distance[target] > -5:
			# Increase speed and pass
			plan = ['accelerate', 'me', 20, 0]
			plan[3] = state.speed['me'] + 15
			return plan
	return False
		
			
	
if __name__ == "__main__":
		
	noOfProblem = 100
		
	tab = ''
	fileStr = '[\n'
	tab = tab + '\t'
	
	count = 0
	
	# Populate 100 problems
	while count < noOfProblem:
		
		# Create the event state
		state = State('state')
		
		state.speed = {}
		state.distance = {}
		state.direction = {}
		state.lane = {}
		
		# Randomly fill out the properties of the exceptional event
		state.target = getRandomTarget()		
		state.speed['me'] = getRandomSpeed()
		state.speed[state.target] = getRandomSpeed()		
		state.distance[state.target] = getRandomDistance()
		state.direction[state.target] = getRandomDirection()
		state.lane[state.target] = getRandomLane()
		
		# find a realistic plan for this event
		plan = find_plan(state)
		
		if plan != False:			
			# plan created, now create a string that will be written to the text file
			# Do all kinds of formatting of the string so that the text file is readable
			fileStr = fileStr + tab + '(\n'				
			tab = tab + '\t'
			
			fileStr = fileStr + tab + '[\n'				
			tab = tab + '\t'
			fileStr = fileStr + generate_state_string(state, tab) + '\n'
			tab = tab[:len(tab)-1]					
			
			tab = tab[:len(tab)-1]
			fileStr = fileStr + tab + ',\n'
			strPlan = str(plan)
			tab = tab + '\t'
			
			strPlan = strPlan.replace('[','[\n'+tab+'(')			
			strPlan = strPlan.replace('),','),\n'+tab)
			strPlan = strPlan.replace(' (\'','(\'')			
			tab = tab[:len(tab)-1]
			strPlan = strPlan.replace(']',')\n'+tab+']')
			
			fileStr = fileStr + tab + strPlan + '),\n'
			
			count = count + 1
			
	fileStr = fileStr[:len(fileStr)-2] + '\n'
	fileStr = fileStr + ']'
	
	# Write the generated fileStr string to the text file
	f = open('casebasedplan.txt', 'w')
	f.write(fileStr)	
	f.close()
	print "Successfully generated", noOfProblem, "random plans on the file", "\'casebasedplan.txt\'"
