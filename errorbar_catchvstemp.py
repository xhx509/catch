# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:19:40 2015

@author: hxu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:28:36 2015
plot Histogram of lobster catch vs temp (include error bar) in a graph:
(1)temp in one haul period(if more than 4days, set period as 4 days) vs time catch. 
(2)temp change in on haul days(if more than 4days, set period as 4 days) period change vs catch .
(3)abs temp change in on haul days(if more than 4days, set period as 4 days) period change vs catch .

Please modify input below before you run this program

@author: hxu
"""

#############################INPUT##################
days=4
files='sqldump_2016_01_BN.csv'
catches=''     # get only long lobster catch or both short and long lobster catch
######################################################
import math
from pandas import *
from matplotlib.dates import date2num, num2date
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np
import netCDF4
from getemolt_function import getobs_tempsalt_bysite
from pylab import *
def autolabel(rects,ax,nums):
    # attach some text labels
    for rect in range(len(rects)):
        height = rects[rect].get_height()
        if math.isnan(height)==True: 
             height=1.5
        ax=ax
        ax.text(rects[rect].get_x()*0.965+rects[rect].get_width()/2., 1.05*height, '%d'%int(nums[rect]),
                ha='center', va='bottom')

#f=np.genfromtxt('/data5/jmanning/fish/lobster/sqldump_test.dat')
#f=np.genfromtxt('sqldump_test.dat')
variables=['ser_num','num','site_n','lat','lon','time_s','nan','nan','nan','depth','num_traps','catch','egger','short','idepth','nan']
df=pd.read_csv(files,names=variables)
site=df.site_n[0]
depth=[df.depth[0]+30,df.depth[0]-10] # temp depth and site depth are not same. max,min
variables_temp=['site','la','lo','de','time_t','temp']
#edf=pd.read_csv(file_e,skiprows=1,names=variables_temp)
time1=df.time_s[0]
time2=df.time_s[len(df.time_s)-1]
mindtime=dt.datetime.strptime(time1,'%Y-%m-%d:%H:%M')
maxdtime=dt.datetime.strptime(time2,'%Y-%m-%d:%H:%M') 
input_time=[mindtime,maxdtime]
time,sea_water_temperature,depth2,sites,lat,lon=getobs_tempsalt_bysite(site,input_time,depth)
idx=[]
for i in range(len(df.time_s)):   #get index of site time by catch time
    idx.append((np.abs(date2num(time)-date2num(dt.datetime.strptime(df.time_s[i],'%Y-%m-%d:%H:%M')))).argmin())
temp,temp_std,times,times_t=[],[],[],[]
for q in range(len(idx)-1):   # for substracting previous one
    times.append(time[idx[q+1]])
    if idx[q+1]-idx[q]>96:          # if the period between the haul and previous one is more than 96 hours, set the period to 96 hours
        temp.append(np.mean(sea_water_temperature[idx[q+1]-24*days:idx[q+1]]))
        temp_std.append(np.std(sea_water_temperature[idx[q+1]-24*days:idx[q+1]]))
    else:
        temp.append(np.mean(sea_water_temperature[idx[q]:idx[q+1]]))
        temp_std.append(np.std(sea_water_temperature[idx[q]:idx[q+1]]))
if catches=='short egger and long':
    list_short=[];egger=[]
    for h in df['short'].tolist():
        if h=='     ':
            h=0  
        list_short.append(int(h))
    for e in  df['egger'].tolist():
        if e=='     ':
            e=0
        egger.append(int(e))   
    list_catch=(np.array(df['catch'].tolist()[1:])+np.array( list_short[1:])+np.array(egger[1:]))/12.0
    #list_catch=(np.array(df['catch'].tolist()[1:])+np.array( list_short[1:]))/np.array(df['num_traps'].tolist()[1:])
else:
    list_catch=np.array(df['catch'].tolist()[1:])/np.array(df['num_traps'].tolist()[1:])
catch_a=[];temp_r=[]
catch_a_std=[];num_catch_a=[]
for i in range(1,14): #set y columns to 30 columns
             catch_a.append(np.mean([list_catch[x] for x in range(len(list_catch)) if i+1>temp[x] >= i]))             
             temp_r.append(str(i)) # for setting y label
             #catch_a_max.append(max([list_catch[x] for x in range(len(list_catch)) if i+1>temp[x] >= i]))
             #catch_a_min.append(min([list_catch[x] for x in range(len(list_catch)) if i+1>temp[x] >= i]))
             catch_a_std.append(np.std([list_catch[x] for x in range(len(list_catch)) if i+1>temp[x] >= i]))
             num_catch_a.append(len([list_catch[x] for x in range(len(list_catch)) if i+1>temp[x] >= i]))
catch_a_c=[];temp_r_c=[];catch_a_cstd=[];num_catch_a_c=[]
for i in range(0,9):
    #catch_a_c.append(sum([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)-1.4)>(temp[x+1]-temp[x]) >= (0.2*i-1.4)])/len([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)-1.4)>(temp[x+1]-temp[x]) >= (0.2*i-1.4)]))
    temp_r_c.append(str(round(i-4.5,1)))
    catch_a_c.append(np.mean([list_catch[x+1] for x in range(len(list_catch)-1) if (i-3.5)>(temp[x+1]-temp[x]) >= (i-4.5)]))
    num_catch_a_c.append(len([list_catch[x+1] for x in range(len(list_catch)-1) if (i-3.5)>(temp[x+1]-temp[x]) >= (i-4.5)]))
    catch_a_cstd.append(np.std([list_catch[x+1] for x in range(len(list_catch)-1) if (i-3.5)>(temp[x+1]-temp[x]) >= (i-4.5)]))
catch_std,temp_r_std=[],[];num_catch_std=[];std_catch_std=[]
for i in range(0,8): #get std_dev
    temp_r_std.append(str(round(0.2*i,1)))
    catch_std.append(np.mean([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
    std_catch_std.append(np.std([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
    num_catch_std.append(len([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
df_p=DataFrame(catch_a,index=temp_r,columns=['catches vs temp'])   #set df for plot histogram
fig, axes = plt.subplots(nrows=1, ncols=3)
#axes.set_ylim([0,2.5])
#plt.title('BN01 from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
#df_p.plot(ax=axes[0],kind='bar',color='red')  
rects1 = axes[0].bar(np.arange(len(temp_r)), catch_a, color='r',)
#axes[0].set_title('BN01 '+catches+' from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
#axes[0].plt.hist()
axes[0].set_xlabel(' temperature (C)', color='r',fontsize=16)
axes[0].set_ylabel(' average catch', color='r',fontsize=17)
axes[0].errorbar(np.arange(len(temp_r))+0.5, catch_a, yerr=[catch_a_std,catch_a_std], fmt='o',color='black',capthick=4)
axes[0].set_ylim([0,2.5])
axes[0].set_xlim([0,len(temp_r)])
#plt.xticks(axes[0],np.arange(len(temp_r)), temp_r)

plt.setp( axes[0],xticks=np.arange(len(temp_r)),xticklabels=temp_r )

autolabel(rects1,axes[0],num_catch_a)
df_pc=DataFrame(catch_a_c,index=temp_r_c,columns=['catches vs temp change'])
#df_pc.plot(ax=axes[1],kind='bar',colors='yellow') 
rects2 = axes[1].bar(np.arange(len(temp_r_c)), catch_a_c, color='yellow',)
plt.setp( axes[1],xticks=np.arange(len(temp_r_c)),xticklabels=temp_r_c )
setp( axes[1].get_yticklabels(), visible=False) #hide y a
autolabel(rects2,axes[1],num_catch_a_c)
#axes[1].set_title(files[-6:-4]+' All Catch from '+mindtime.strftime("%Y")+' to '+maxdtime.strftime("%Y"),fontsize=25)
axes[1].set_title(files[-6:-4]+'01 CATCH VS '+4days+' TEMPERATURE STATISTICS',fontsize=25)
axes[1].set_xlabel(' temperature change(C)', color='b',fontsize=16)
#axes[1].set_ylabel(' average catch', color='yellow',fontsize=15)
axes[1].errorbar(np.arange(len(temp_r_c))+0.5, catch_a_c, yerr=[catch_a_cstd,catch_a_cstd], fmt='o',color='black',capthick=4)
axes[1].set_ylim([0,2.5])

df_pstd=DataFrame(catch_std,index=temp_r_std,columns=['catches vs temp std'])
#df_pstd.plot(ax=axes[2],kind='bar',colors='green')
rects3 = axes[2].bar(np.arange(len(temp_r_std)), catch_std, color='green',)
axes[2].set_xlabel('temperature std_dev ', color='g',fontsize=16)
#axes[2].set_ylabel(' average catch', color='g',fontsize=15)
axes[2].errorbar(np.arange(len(temp_r_std))+0.5, catch_std, yerr=[std_catch_std,std_catch_std], fmt='o',color='black',capthick=4)
axes[2].set_ylim([0,2.5])
plt.setp( axes[2],xticks=np.arange(len(temp_r_std)),xticklabels=temp_r_std )
setp( axes[2].get_yticklabels(), visible=False) #hide y axis 
autolabel(rects3,axes[2],num_catch_std)
#plt.title('BN01 from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
plt.gcf().autofmt_xdate()

plt.get_current_fig_manager().window.showMaximized()
plt.show() 
plt.savefig(files[-6:-4]+'_catch_vs_temp.png',dpi=360) 
