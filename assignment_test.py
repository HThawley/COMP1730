# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 20:22:28 2020

@author: hmtha
"""

import csv

with open("aqi_data_civic.csv") as file:
    reader = csv.reader(file)
    next(reader)
    raw_data = [row for row in reader]

data = []
for row in raw_data:
    new_row = [row[2][6:10], row[2][3:5], row[2][0:2], row[17], row[14]]
    data.append(new_row)
    
data.sort()

year = int(data[0][0])
month = int(data[0][1])
day = int(data[0][2])
count = 0

for row in data: 
    if row[4] == '':
        pass
    elif int(row[4]) >= 100: 
        if int(row[0]) == year:
            if int(row[2]) == day:
                if int(row[1]) != month:
                    count += 1
                    day = int(row[2])
                    month = int(row[1])
            else:
                count +=1 
                day = int(row[2])
                month = int(row[1])
        else:
            print("In " + str(year) + " there were " + str(count) + " days with PM2.5 above 100")
            count = 0 
            year += 1 
            month = 0
            day=0
            if int(row[0]) == year:
                if int(row[2]) != day:
                    count += 1
                    day = int(row[2])  
           
PM_100 = []
for x in data:
    if x[4] == '':
        pass
    elif int(x[4]) >= 100: 
        PM_100.append(x) 
print(len(PM_100))


    