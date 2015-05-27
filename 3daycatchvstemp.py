# -*- coding: utf-8 -*-
"""
Created on Thu May 21 11:19:40 2015

@author: hxu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:28:36 2015
plot Histogram:
(1)temp in 4 days period vs time catch. 
(2)temp change in 4 days period change vs catch .
#  (3)abs temp change, catch change vs time

@author: hxu
"""

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

file_e='emolt2015-05-06 15:49.csv'
files='sqldump_2015_05_BN.csv'
catches=''     # get only long lobster catch or both short and long lobster catch
#f=np.genfromtxt('/data5/jmanning/fish/lobster/sqldump_test.dat')
#f=np.genfromtxt('sqldump_test.dat')
variables=['ser_num','num','site_n','lat','lon','time_s','nan','nan','nan','depth','num_traps','catch','egger','short','idepth','nan']
df=pd.read_csv(files,names=variables)
site=df.site_n[0]
depth=[df.depth[0]+30,df.depth[0]-10] # temp depth and site depth are not same. max,min
variables_temp=['site','la','lo','de','time_t','temp']
edf=pd.read_csv(file_e,skiprows=1,names=variables_temp)
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
        temp.append(np.mean(sea_water_temperature[idx[q+1]-96:idx[q+1]]))
        temp_std.append(np.std(sea_water_temperature[idx[q+1]-96:idx[q+1]]))
    else:
        temp.append(np.mean(sea_water_temperature[idx[q]:idx[q+1]]))
        temp_std.append(np.std(sea_water_temperature[idx[q]:idx[q+1]]))
if catches=='short and long':
    list_short=[]
    for h in df['short'].tolist():
        list_short.append(int(h))
    list_catch=np.array(df['catch'].tolist()[1:])/8.0+np.array( list_short[1:])/8.0
else:
    list_catch=np.array(df['catch'].tolist()[1:])/8.0
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
for i in range(0,8):
    temp_r_std.append(str(round(0.2*i,1)))
    catch_std.append(np.mean([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
    std_catch_std.append(np.std([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
    num_catch_std.append(len([list_catch[x+1] for x in range(len(list_catch)-1) if (0.2*(i+1)>(temp_std[x+1]) >= 0.2*i)]))
print num_catch_a,num_catch_a_c,num_catch_std
df_p=DataFrame(catch_a,index=temp_r,columns=['catches vs temp'])   #set df for plot histogram
fig, axes = plt.subplots(nrows=1, ncols=3)
#plt.title('BN01 from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
#df_p.plot(ax=axes[0],kind='bar',color='red')  
rects1 = axes[0].bar(np.arange(len(temp_r)), catch_a, color='r',)
#axes[0].set_title('BN01 '+catches+' from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
#axes[0].plt.hist()
axes[0].set_xlabel(' temperature (C)', color='r',fontsize=15)
axes[0].set_ylabel(' average catch', color='r',fontsize=15)
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
setp( axes[1].get_yticklabels(), visible=False)
autolabel(rects2,axes[1],num_catch_a_c)
axes[1].set_title('BN01 from '+mindtime.strftime("%Y")+' to '+maxdtime.strftime("%Y"),fontsize=25)
axes[1].set_xlabel(' temperature change(C)', color='b',fontsize=15)
#axes[1].set_ylabel(' average catch', color='yellow',fontsize=15)
axes[1].errorbar(np.arange(len(temp_r_c))+0.5, catch_a_c, yerr=[catch_a_cstd,catch_a_cstd], fmt='o',color='black',capthick=4)
axes[1].set_ylim([0,2.5])

df_pstd=DataFrame(catch_std,index=temp_r_std,columns=['catches vs temp std'])
#df_pstd.plot(ax=axes[2],kind='bar',colors='green')
rects3 = axes[2].bar(np.arange(len(temp_r_std)), catch_std, color='green',)
axes[2].set_xlabel('temperature std_dev ', color='g',fontsize=15)
#axes[2].set_ylabel(' average catch', color='g',fontsize=15)
axes[2].errorbar(np.arange(len(temp_r_std))+0.5, catch_std, yerr=[std_catch_std,std_catch_std], fmt='o',color='black',capthick=4)
axes[2].set_ylim([0,2.5])
plt.setp( axes[2],xticks=np.arange(len(temp_r_std)),xticklabels=temp_r_std )
setp( axes[2].get_yticklabels(), visible=False)
autolabel(rects3,axes[2],num_catch_std)
#plt.title('BN01 from '+mindtime.strftime("%d/%m/%y")+' to '+maxdtime.strftime("%d/%m/%y"))
plt.gcf().autofmt_xdate()
plt.show()  
'''
for i in range(len(idx)-1):
    temp_c.append(sea_water_temperature[idx[i+1]]-sea_water_temperature[idx[i+1]])
    times_c.append(time[idx[i+1]])

for n in range(len(time)/7):
    temp.append(np.mean(sea_water_temperature[7*n:7*n+7]))
    times_t.append(num2date(np.mean(date2num(time[7*n:7*n+7]))))
temp4,times4,catch4,times_c,temp_c,catch4_c=[],[],[],[],[],[]    
for m in range(len(idx)/4): 
    temp4.append((temp[4*m]+temp[4*m+1]+temp[4*m+2]+temp[4*m+3])/4.0)
    catch4.append((df.catch[4*m]+df.catch[4*m+1]+df.catch[4*m+2]+df.catch[4*m+3])/32.0)
    times4.append(num2date((date2num(times[4*m])+date2num(times[4*m+1])+date2num(times[4*m+2])+date2num(times[4*m+3]))/4))
for m in range(len(idx)/4-1): 
    temp_c.append((temp[4*(m+1)]+temp[4*(m+1)+1]+temp[4*(m+1)+2]+temp[4*(m+1)+3])/4.0-(temp[4*m]+temp[4*m+1]+temp[4*m+2]+temp[4*m+3])/4.0)
    catch4_c.append((df.catch[4*(m+1)]+df.catch[4*(m+1)+1]+df.catch[4*(m+1)+2]+df.catch[4*(m+1)+3])/32.0-(df.catch[4*m]+df.catch[4*m+1]+df.catch[4*m+2]+df.catch[4*m+3])/32.0)
    times_c.append(num2date((date2num(times[4*(m+1)])+date2num(times[4*(m+1)+1])+date2num(times[4*(m+1)+2])+date2num(times[4*(m+1)+3]))/4))


fig, axes = plt.subplots(nrows=3, ncols=1)
ax1=axes[0]
#fig, ax1 = plt.subplots(211)   
ax1.set_title('Lobsters kept and Temperature at BN01',fontsize=25)
ax1.plot(times_t,temp,'b')
#ax1.set_xlabel('time ',fontsize=21)
ax1.set_ylabel('7 days average temp(C)', color='b',fontsize=15)
ax1.legend()
ax2 = ax1.twinx()
ax2.plot(times4,catch4,'r')
ax2.set_ylabel('4 hauls average catch change', color='r',fontsize=15)
ax2.legend()
ax3=axes[1]
ax3.plot(times_c,temp_c,'b')
#ax3.set_xlabel('time ',fontsize=21)
ax3.set_ylabel('temp(C) change', color='b',fontsize=15)
ax3.legend()
ax4 = ax3.twinx()
ax4.plot(times_c,catch4_c,'r')
#ax4.set_ylabel('4 hauls average catch change', color='r',fontsize=15)
ax4.legend()
ax5=axes[2]
ax5.plot(times_c,np.abs(temp_c),'b')
ax5.set_xlabel('time ',fontsize=21)
ax5.set_ylabel('ABS temp(C) change', color='b',fontsize=15)
ax5.legend()
ax6 = ax5.twinx()
ax6.plot(times_c,catch4_c,'r')
ax6.set_ylabel('4 hauls average catch change', color='r',fontsize=15)
ax6.legend()
plt.gcf().autofmt_xdate() #beautify time axis
'''

#temp=edf[:,6]
#time_e=edf[:,3]

