
from utils import *

# table1 = createStateTable()

# table2 = createStateTable()

# np.save('table1.npy',table1)
# np.save('table2.npy',table2)

table = np.load("finalStateTable.npy",allow_pickle=True).item()
# table2 = np.load("table2.npy",allow_pickle=True).item()

# if hashFcn(np.array([0,0,0,0,0,0,0,0,0])) not in table1:
#     print("you fd up")
# # check if both have exactly same keys
# notInTable2 = []
# for key in table1:
#     if key not in table2:
#         notInTable2.append(key)

# print(notInTable2)

# test = np.array([0,0,1,1])

# n = np.where(test == 0)[0]

# print(n)

# test = [1,2,3,4,5,6]

# index = np.random.choice(test,replace=False)

# print(index)

# state = np.array([1,-1,0])
# b = state.view(np.uint8)
# print(b)

# print(table)

stateList = list(table.values())
stateList = stateList[0]
scoreList = [state[1] for state in stateList]

print(scoreList)