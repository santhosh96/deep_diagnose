# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import re
import random
import datetime

""" Section for creating names dataframe """

names = pd.read_csv("name_gender.csv")
names = names["name"]
name = list()

for _ in range(25760):
    name.append(names[random.randint(0,95025)])

Name = pd.DataFrame(columns=["name"], data=name)

""" Section for creating target variable dataframe """

res = ['positive', 'negative']
tar = list()

for _ in range(25760):
    tar.append(random.choice(res))
    
Result = pd.DataFrame(columns=["result"], data=tar)
    
""" Section for creating date dataframe """

time = list()
date = list()
timestamp = list()

date1 = '2017-02-03'
date2 = '2018-02-05'
start = datetime.datetime.strptime(date1, '%Y-%m-%d')
end = datetime.datetime.strptime(date2, '%Y-%m-%d')
step = datetime.timedelta(days=1)
while start <= end:
    startdate = str(start.date())
    starttime = ' 09:00:00'
    final = startdate + starttime
    for x in pd.date_range(start=final, periods=70, freq='8min'):
        a,b = re.split('\s+',str(x))
        timestamp.append(x)
        date.append(str(a))
        time.append(str(b))
    start += step
    
Timestamp = pd.DataFrame(columns=['timestamp'], data=timestamp)
Date = pd.DataFrame(columns=['date'], data=date)
Time = pd.DataFrame(columns=['time'], data=time)

""" Merging all the dataframe into a master dataframe called stats """

Stats = pd.DataFrame()
Stats = Timestamp.join(Name.join(Date.join(Time.join(Result))))
Stats.set_index('timestamp')

""" Exporting the data to csv file """

Stats.to_csv('Stats.csv')
