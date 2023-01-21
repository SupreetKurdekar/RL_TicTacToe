import copy
from collections import deque
import numpy as np
import hashlib

import json

def checkWinCondition(state):

    t = 1
    if state[0] == t and state[3] == t and state[6] == t or \
        state[1] == t and state[4] == t and state[7] ==t or \
        state[2] == t and state[5] == t and state[8] == t or \
        state[0] == t and state[1] == t and state[2] == t or \
        state[3] == t and state[4] == t and state[5] == t or \
        state[6] == t and state[7] == t and state[8] == t or \
        state[0] == t and state[4] == t and state[8] == t or \
        state[2] == t and state[4] == t and state[6] == t:
        return t

    t = -1
    if state[0] == t and state[3] == t and state[6] == t or \
        state[1] == t and state[4] == t and state[7] ==t or \
        state[2] == t and state[5] == t and state[8] == t or \
        state[0] == t and state[1] == t and state[2] == t or \
        state[3] == t and state[4] == t and state[5] == t or \
        state[6] == t and state[7] == t and state[8] == t or \
        state[0] == t and state[4] == t and state[8] == t or \
        state[2] == t and state[4] == t and state[6] == t:
        return t

    # this is not really a draw
    return 0

def isDraw(state):
    if checkWinCondition(state) == 0 and len(np.where(state == 0)[0]) == 0:
        return 1
    else:
        return 0

def createAllStates():

    container = deque()
    container.append(np.array([0,0,0,0,0,0,0,0,0]))
    finalContainer = copy.deepcopy(container)
    # finalContainer.pop()
    storer = deque()
    t = 1
    while container:
        temp = container.popleft()
        
        if checkWinCondition(temp) == 0:
            for i,v in enumerate(temp):
                if v == 0:
                    toPush = copy.deepcopy(temp)
                    toPush[i] = t
                    storer.append(toPush)
                    finalContainer.append(toPush)
        
        
        if not container:
            t = -t
            while storer:
                container.append(storer.pop())

    return finalContainer

def initScore(state):
    if checkWinCondition(state) == 1:
        return 1
    elif checkWinCondition(state) == 0:
        return 0.5
    else:
        return 0

def initScoreWithLossPenalty(state):
    if checkWinCondition(state) == 1:
        return 1
    elif checkWinCondition(state) == -1:
        return -1
    elif isDraw(state):
        return 0
    else:
        return 0.1

# def hashFcn(state):
    
#     return hash(np.array2string(state, precision=4))

def hashFcn(state):
    
    b = state.view(np.uint8)
    hashlib.sha1(b).hexdigest()

def findInHash(dictionary,state):
    hashcode = hashFcn(state)

    for elem in dictionary[hashcode]:
        if np.array_equal(elem[0],state):
            return elem

def findBestNextState(state,nextInput,epsilon,stateTable):
    # nextInput might be 1 or -1

    # this returns the end of the episode
    if checkWinCondition(state) !=0 or isDraw(state):
        return False,state

    

    # find places with zeros. 
    # as its not ended we have place to add
    indices = np.where(state == 0)[0]

    # # if no place left we dont need this as interim state 
    # will always have 0s
    # if (len(indices) == 0):
    #     return False,state
  
    if nextInput == -1:

        index = np.random.choice(indices,replace=False)

        newState = copy.deepcopy(state)
        newState[index] = -1

        return True,newState
    
    elif nextInput == 1:
        temp = np.random.uniform()
        if temp < epsilon:
            index = np.random.choice(indices,replace=False)

            newState = copy.deepcopy(state)
            newState[index] = 1

            return True,newState
        else:
            maxVal = -1000.0
            maxIndexArray = []

            for index in indices:
                newState = copy.deepcopy(state)
                newState[index] = 1

                # score = findInHash(stateTable,newState)[1]
                score = -100000
                tempHashForState = hashFcn(newState)
                # print(tempHashForState)
                # print(len(np.where(state == 1)[0]))
                # print(len(np.where(state == 0)[0]))
                for elem in stateTable[tempHashForState]:
                    # print("len of elem ",len(elem))
                    if np.array_equal(elem[0],newState):
                        score = elem[1]

                if score > maxVal:
                    maxIndexArray = [index]
                    maxVal = score
                elif score == maxVal:
                    maxIndexArray.append(index)
                else:
                    pass

            maxIndex = np.random.choice(maxIndexArray,replace=False)

            newState = copy.deepcopy(state)
            newState[maxIndex] = 1

            return True, newState     

    else:
        return False,state


def createStateTable():
    finalContainer = createAllStates()

    # # create stateTable
    stateTable = dict()

    for state in finalContainer:
        hashCode = hashFcn(state)

        if hashCode in stateTable:
            stateTable[hashCode].append([state,initScoreWithLossPenalty(state)])
        else:
            stateTable[hashCode] = [[state,initScoreWithLossPenalty(state)]]

    return stateTable