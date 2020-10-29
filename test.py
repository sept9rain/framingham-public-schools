from scipy.optimize import linear_sum_assignment

import pandas as pd
import numpy as np
import time
import datetime
import os
import smtplib, ssl


with open("/www/djangoProject/timestamp", "r") as f:
    timestamp = f.read()
    

if float(timestamp) == os.path.getmtime('/www/djangoProject/data/dataset.xlsx'):
    print("No changes! exit")
    quit()
else:
    with open("/www/djangoProject/timestamp","w") as f:
        print("New changes! reassigned")
        f.write(str(os.path.getmtime('/www/djangoProject/data/dataset.xlsx'))) 

data = pd.read_excel('/www/djangoProject/data/dataset.xlsx', index_col=0)
ordinaryPriority = data.loc[data["Do you want to use your sib pref?"] != "Yes",["LASID","  Choice # 1 ","  Choice # 2","  Choice # 3","  Choice # 4","  Choice #  5",
                                                                                "  Choice # 6","  Choice # 7","  Choice # 8 "] ];
row, column= ordinaryPriority.shape
schools = {"Dunning":0,
           "Hemenway":1,
           "Potter Road":2,
           "Brophy":3,
           "McCarthy":4,
           "King":5,
           "Woodrow Wilson":6,
           "Stapleton":7}

def get_key(val):
    for key, value in schools.items():
         if val == value:
             return key

test = np.zeros((row,row))
stats = np.zeros(len(schools))

places=[74,80,70,64,62,70,61,51]

data['school sib pref:'] = data['school sib pref:'].replace([' Wilson'],'Woodrow Wilson')
sib = data[['LASID','Do you want to use your sib pref?','school sib pref:']]
siblingAssigned = sib.loc[sib['Do you want to use your sib pref?'] == 'Yes'][['LASID', 'school sib pref:']]
siblingAssigned=siblingAssigned.rename(columns={"LASID": "StudentID", "school sib pref:": "Assigned school"})
siblingPrefAssignedLabels = siblingAssigned['Assigned school'].value_counts().index.tolist()
siblingPrefAssignedPlaces = siblingAssigned['Assigned school'].value_counts()

for i in range(len(siblingPrefAssignedPlaces)):
    if siblingPrefAssignedLabels[i]!='Barbieri ':
        places[schools[siblingPrefAssignedLabels[i]]]-=siblingPrefAssignedPlaces[i]

n = 0
for row in ordinaryPriority.itertuples():
    for i in range(2,10):
        id = schools[row[i]]
        test[n][sum(places[:id]):sum(places[:id])+places[id]]=[i-1] * places[id]
    n+=1

labels, results =linear_sum_assignment(test)
output=[]
n = 0
for row in ordinaryPriority.itertuples():
    k = results[n]
    for i in range(len(places)):
        if k<sum(places[:i+1]):
            output.append([row[1],get_key(i)])
            for m in range(2,10):
                if(get_key(i)==row[m]):
                    stats[m-2]+=1
            break
    n+=1




outputDataFrame = pd.DataFrame(data=output, columns=["StudentID","Assigned school"])
outputDataFrame = pd.concat([outputDataFrame,siblingAssigned],axis=0)
outputDataFrame.to_excel("/www/djangoProject/data/assignmentOutput.xlsx")



port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "EMAIL_HERE"  # Enter your address
receiver_email = "EMAIL_HERE"  # Enter receiver address
password = "PASSWORDHERE"
message = """\
Subject: NOTICE: Assignment Output are Ready

Hi There, you assignment output are ready.
Please vist https://501dl.sept9rain.com """

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
