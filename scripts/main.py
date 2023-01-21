from collections import deque
import copy
import json

from utils import *

# finalContainer = createAllStates()

stateTable = createStateTable()

print(type(stateTable))
# # # create stateTable
# stateTable = dict()

# for state in finalContainer:
#     hashCode = hashFcn(state)

#     if hashCode in stateTable:
#         stateTable[hashCode].append([state,initScore(state)])
#     else:
#         stateTable[hashCode] = [[state,initScore(state)]]

np.save('stateTables\\initStateTableLossPenalty.npy',stateTable)

# stateTable = np.load("stateTable.npy",allow_pickle=True)

# stateTable = stateTable.item()

# print(len(stateTable))

initState = np.array([0,0,0,0,0,0,0,0,0])


numberOfEpisodes = 100

illegalStatesC = []
illegalStatesN = []
while(numberOfEpisodes > 0):
    # initialization:
    t = 1
    initState = np.array([0,0,0,0,0,0,0,0,0])
    epsilon = 0.15
    count = 100
    alpha = 0.1
    currentState = copy.deepcopy(initState)
    running = True
    nextState = copy.deepcopy(initState)

    while(count > 0 and running):
    # Find Next state
        ret,nextState = findBestNextState(currentState,t,epsilon,stateTable)
        if ret == False:
            running = False
            continue
    # update current state value

        # if hashFcn(currentState) in stateTable:
        #     for currElem in stateTable[hashFcn(currentState)]:
        #         if np.array_equal(currElem[0],currentState):
        #             for newElem in stateTable[hashFcn(nextState)]:
        #                 if np.array_equal(newElem[0],nextState):
        #                     currElem[1] += alpha*newElem[1]
        #                     break
        #             break
        # else:

        # current state value
        id = 0
        score = 0
        if hashFcn(currentState) in stateTable:
            for idx,currElem in enumerate(stateTable[hashFcn(currentState)]):
                if np.array_equal(currElem[0],currentState):
                    id = idx
                    score = currElem[1]

                    break
        else:
            illegalStatesC.append([currentState,score,hashFcn(currentState)])

            with open('{}.npy'.format("illegalC.npy"), 'wb') as f:
                np.save(f, illegalStatesC)

        idn = 0
        scoren = 0
        if hashFcn(nextState) in stateTable:
            for idx,currElem in enumerate(stateTable[hashFcn(nextState)]):
                if np.array_equal(currElem[0],nextState):
                    idn = idx
                    scoren = currElem[1]

                    break
        else:
            illegalStatesN.append([nextState,score,hashFcn(nextState)])


            with open('{}.npy'.format("illegalN.npy"), 'wb') as f:
                np.save(f, illegalStatesN)

        stateTable[hashFcn(currentState)][id][1] += alpha*stateTable[hashFcn(nextState)][idn][1]                 


    # set next state as current state
        currentState = copy.deepcopy(nextState)
    # update input
        t = -t
        count -=1

        if(count%10 == 0):
            print("count :",count)

    numberOfEpisodes -= 1
    print("numberOfEpisodes :",numberOfEpisodes)

    if numberOfEpisodes%10 == 0:
        np.save("stateTables\\StateTableLossPenalty100eps.npy",stateTable,allow_pickle=True)


np.save("stateTables\\finalStateTableLossPenalty100eps",stateTable,allow_pickle=True)


        






