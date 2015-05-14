# -*- coding: utf-8 -*-
"""
Created on Thu May 14 10:52:51 2015

@author: hxu
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  6 13:28:36 2015
plot :
(1)temp, catch vs day average time . 
(2)temp change in 4 day period , catch vs time .
(3)abs temp change in 4 day period, catch vs time
@author: hxu
"""
from matplotlib.dates import date2num, num2date
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np
import netCDF4
from getemolt_function import getobs_tempsalt_bysite
file_e='emolt2015-05-06 15:49.csv'
files='sqldump_2015_05_BN.csv'
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
for i in range(len(df.time_s)):    #get index of site time by catch time
    idx.append((np.abs(date2num(time)-date2num(dt.datetime.strptime(df.time_s[i],'%Y-%m-%d:%H:%M')))).argmin())
temp,times,times_t=[],[],[]
for q in range(len(idx)):
    times.append(time[idx[q]])
'''
for i in range(len(idx)-1):
    temp_c.append(sea_water_temperature[idx[i+1]]-sea_water_temperature[idx[i+1]])
    times_c.append(time[idx[i+1]])
'''
for n in range(len(time)/24-1):
    temp.append(np.mean(sea_water_temperature[24*n+2:24*n+9]))
    times_t.append(num2date(np.mean(date2num(time[24*n+2:24*n+9]))))
temp4,times4,catch4,times_c,temp_c,catch4_c=[],[],[],[],[],[] 

for m in idx[1:]:
    temp4.append(np.mean(sea_water_temperature[m-96:m]))
for n in range(len(idx)-1):
    catch4.append((df.catch[n+1])/8.0)
    times4.append(num2date((date2num(times[n+1]))-2))
    
for m in range(len(idx)-2):
    temp_c.append(np.mean(sea_water_temperature[(idx[m+2]-96):idx[m+2]])-np.mean(sea_water_temperature[(idx[m+1]-96):idx[m+1]]))
    catch4_c.append((df.catch[m+2])/8.0-(df.catch[m+1])/8.0)
    times_c.append(num2date((date2num(times[m+2]))-2))

'''   
for m in range(len(idx)/4): 
    temp4.append((temp[4*m]+temp[4*m+1]+temp[4*m+2]+temp[4*m+3])/4.0)
    catch4.append((df.catch[4*m]+df.catch[4*m+1]+df.catch[4*m+2]+df.catch[4*m+3])/32.0)
    times4.append(num2date((date2num(times[4*m])+date2num(times[4*m+1])+date2num(times[4*m+2])+date2num(times[4*m+3]))/4))
for m in range(len(idx)/4-1): 
    temp_c.append((temp[4*(m+1)]+temp[4*(m+1)+1]+temp[4*(m+1)+2]+temp[4*(m+1)+3])/4.0-(temp[4*m]+temp[4*m+1]+temp[4*m+2]+temp[4*m+3])/4.0)
    catch4_c.append((df.catch[4*(m+1)]+df.catch[4*(m+1)+1]+df.catch[4*(m+1)+2]+df.catch[4*(m+1)+3])/32.0-(df.catch[4*m]+df.catch[4*m+1]+df.catch[4*m+2]+df.catch[4*m+3])/32.0)
    times_c.append(num2date((date2num(times[4*(m+1)])+date2num(times[4*(m+1)+1])+date2num(times[4*(m+1)+2])+date2num(times[4*(m+1)+3]))/4))
'''
fig, axes = plt.subplots(nrows=3, ncols=1)
ax1=axes[0]    # plot temp,catch vs time
#fig, ax1 = plt.subplots(211)   
ax1.set_title('Lobsters kept and Temperature at BN01',fontsize=25)
ax1.plot(times_t,temp,'b')
#ax1.set_xlabel('time ',fontsize=21)
ax1.set_ylabel('1 day average temp(C)', color='b',fontsize=15)
ax1.legend()
ax2 = ax1.twinx()
ax2.plot(times4,catch4,'r')
ax2.set_ylabel('1 haul  catch', color='r',fontsize=15)
ax2.legend()
ax3=axes[1]
ax3.plot(times_c,temp_c,'b')
#ax3.set_xlabel('time ',fontsize=21)
ax3.set_ylabel('temp(C) change', color='b',fontsize=15)
ax3.legend()
ax4 = ax3.twinx()
ax4.plot(times_c,catch4[1:],'r')
#ax4.set_ylabel('4 hauls average catch change', color='r',fontsize=15)
ax4.legend()
ax5=axes[2]
ax5.plot(times_c,np.abs(temp_c),'b')
ax5.set_xlabel('time ',fontsize=21)
ax5.set_ylabel('ABS temp(C) change', color='b',fontsize=15)
ax5.legend()
ax6 = ax5.twinx()
ax6.plot(times_c,catch4[1:],'r')
ax6.set_ylabel('1 haul catch', color='r',fontsize=15)
ax6.legend()
plt.gcf().autofmt_xdate() #beautify time axis


plt.show()
#temp=edf[:,6]
#time_e=edf[:,3]

