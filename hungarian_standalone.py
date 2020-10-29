import pandas as pd
import numpy as np
from scipy.optimize import linear_sum_assignment
from munkres import Munkres
import sys

m = Munkres()



data = pd.read_excel('dataset.xlsx', index_col=0)

ordinaryPriority = data.loc[data["Do you want to use your sib pref?"] != "Yes",
                            ["LASID","2A - If yes, please choose \"ONE\" option below:"," Portuguese ONLY Dual Lang  Choice # 1 "," Portuguese ONLY Dual Lang  Choice #  2",
                             "Spanish ONLY Dual Lang  Choice # 1 ","Spanish ONLY Dual Lang  Choice # 2",
                             " Portuguese FIRST Dual Lang  Choice # 1 "," Portuguese FIRST Dual Lang  Choice # 2 "," Spanish SECOND Dual Lang  Choice # 3 "," Spanish SECOND Dual Lang  Choice # 4",
                             " Spanish FIRST Dual Lang  Choice # 1 "," Spanish FIRST Dual Lang  Choice # 2"," Portuguese SECOND Dual Lang  Choice # 3 "," Portuguese SECOND Dual Lang  Choice # 4",
                             "  Choice # 1 ","  Choice # 2","  Choice # 3","  Choice # 4","  Choice #  5","  Choice # 6","  Choice # 7","  Choice # 8 "]];

# print(ordinaryPriority)
schools = {
    "Barbieri Elementary School":0,
    "Brophy Elementary School":1,
    "Potter Road Elementary School":2,
    "Woodrow Wilson Elementary School":3,
    "Dunning":4,
    "Hemenway":5,
    "Potter Road":6,
    "Brophy":7,
    "McCarthy":8,
    "King":9,
    "Woodrow Wilson":10,
    "Stapleton":11}

def get_key(val):
    for key, value in schools.items():
         if val == value:
             return key
#
places=[44,45,8,8,30,30,30,30,30,30,30,30]
test = np.zeros((345,345))


n = 0
for row in ordinaryPriority.itertuples():
    for i in range(15,23):
        id = schools[row[i]]
        test[n][sum(places[:id]):sum(places[:id])+places[id]]=[i-10] * places[id]
    n+=1

n = 0
for row in ordinaryPriority.itertuples():
    if row[1] == "Spanish Only":
        for i in range(5, 9):
            if i<7:
                id = schools[row[i]]
                test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [i - 4] * places[id]
            else:
                id = i-5
                test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [12] * places[id]
    elif row[1]=="Portuguese Only":
        for i in range(3, 7):
            if i<5:
                id = schools[row[i]]
                test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [i - 2] * places[id]
            else:
                id = i-3
                test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [12] * places[id]
    elif row[1]=="Spanish as first choice + Portuguese as a second choice":
        for i in range(11, 15):
            id = schools[row[i]]
            test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [i - 10] * places[id]
    elif row[1]=="Portuguese as first choice + Spanish as a second choice":
        for i in range(7, 11):
            id = schools[row[i]]
            test[n][sum(places[:id]):sum(places[:id]) + places[id]] = [i - 6] * places[id]
    else:
        print(row[1])
        test[n][:sum(places[:4])] = [12] * sum(places[:4])
        print(test[n])

print(test[:20])
# labels, results =linear_sum_assignment(test)

# results2=m.compute(test)
#
# output=[]
#
# statsSingle = np.zeros(2)
# statsDouble = np.zeros(4)
# statsEng = np.zeros(8)
#
# n = 0
# for row in ordinaryPriority.itertuples():
#     k = results[n]
#     k2= results2[n][1]
#     for i in range(len(places)):
#         if k<sum(places[:i+1]):
#             output.append([row[1],get_key(i)])
#
#             if row[2] == "Spanish Only":
#                 for m in range(5, 7):
#                     if (get_key(i) == row[m]):
#                         statsSingle[m - 5] += 1
#             elif row[2] == "Portuguese Only":
#                 for m in range(3, 5):
#                     if (get_key(i) == row[m]):
#                         statsSingle[m - 3] += 1
#
#             elif row[2] == "Spanish as first choice + Portuguese as a second choice":
#                 for m in range(11, 15):
#                     if (get_key(i) == row[m]):
#                         statsDouble[m - 11] += 1
#
#             elif row[2] == "Portuguese as first choice + Spanish as a second choice":
#                 for m in range(7, 11):
#                     if (get_key(i) == row[m]):
#                         statsDouble[m - 6] += 1
#             else:
#                 for m in range(15,23):
#                     if (get_key(i) == row[m]):
#                         statsEng[m - 15] += 1
#             break
#     n+=1
#
# print(statsSingle)
# print(statsDouble)
# print(statsEng)
#
# outputDataFrame = pd.DataFrame(data=output, columns=["StudentID","Assigned school"])
# outputDataFrame.to_excel("assignmentOutput.xlsx")



















