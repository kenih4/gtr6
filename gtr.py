#!/home/xfel/xfelopr/local/anaconda3/bin/python3

#	./gtr.py config_BL2_setting.xlsx config_BL2_sig.xlsx
#	./gtr.py config_BL3_setting.xlsx config_BL3_sig.xlsx
#	./gtr.py config_XSBT_setting.xlsx config_XSBT_sig.xlsx

#	./gtr.py config_BL2_setting_test.xlsx config_BL2_sig_test.xlsx


#	Normal
#	/home/xfel/xfelopr/local/anaconda3/bin/python3 -OO /home/xfel/xfelopr/kenichi/gtr/gtr.py /home/xfel/xfelopr/kenichi/gtr/config_XSBT_setting_SINGLE.xlsx /home/xfel/xfelopr/kenichi/gtr/config_XSBT_sig_SINGLE.xlsx 0
#	Time designation
#	/home/xfel/xfelopr/local/anaconda3/bin/python3 -OO /home/xfel/xfelopr/kenichi/gtr/gtr.py /home/xfel/xfelopr/kenichi/gtr/config_XSBT_setting_SINGLE.xlsx /home/xfel/xfelopr/kenichi/gtr/config_XSBT_sig_SINGLE.xlsx 0 2021/10/10+09:00:49 2021/10/10+09:10:49 


#	python3 -OO gtr.py config_XSBT_setting_SINGLE.xlsx config_XSBT_sig_SINGLE.xlsx 0

import time
import threading
from matplotlib import animation

import requests, bs4
from requests.exceptions import Timeout
import datetime
from datetime import datetime as dt
from datetime import timezone
import pytz
import re
import numpy as np
import matplotlib.pyplot as plt
import configparser
import time
import pandas as pd
import sys
import math
from matplotlib.dates import DateFormatter
from matplotlib.dates import num2date
from statistics import mean, median,variance,stdev
import queue
import pdb

#	for sound
import subprocess
#import winsound
#import seaborn as sns

plt.rcParams['font.family'] = "mikachan-PB"


print("arg len:",len(sys.argv))
print("argv:",sys.argv)
print("arg1:" + sys.argv[1])
conf_set = sys.argv[1]
conf_sig = sys.argv[2]
#if len(sys.argv) <= 3:
#	x_position = 0
#"else:
#	x_position = sys.argv[3]

x_position = sys.argv[3]
"""
"""
y_position = sys.argv[4]
x_size = sys.argv[5]
y_size = sys.argv[6]
print("x_position:",x_position)
print("y_position:",y_position)
print("x_size:",x_size)
print("y_size:",y_size)




df_set = pd.read_excel(conf_set, sheet_name="setting", header=None, index_col=0)
print(df_set)
df_sig = pd.read_excel(conf_sig, sheet_name="sig")
#df_sig = pd.read_excel(conf_sig, sheet_name="sig", encoding='cp932')
#df_sig = pd.read_excel(conf_sig, sheet_name="sig", encoding='shift-jis')	#DAME
#df_sig = pd.read_excel(conf_sig, sheet_name="sig", encoding='utf-8')	#DAME
#df_sig = pd.read_html(conf_sig, sheet_name="sig")		#DAME
#print(df_sig)

res = subprocess.run(["amixer", "sset", "Master", "on"], stdout=subprocess.PIPE)
#pdb.set_trace()


print("df_set.loc['interval']:	",df_set.loc['interval'])
"""
"""
if len(sys.argv) <= 7:
	strbegin = ""
	strend = ""
else:
	strbegin = sys.argv[7]
	strend = sys.argv[8]
	df_set.loc['interval'] = 100000000
print("begin:",strbegin)
print("end:",strend)

strbegin = strbegin.replace("+"," ")
strend = strend.replace("+"," ")
print("begin:",strbegin)
print("end:",strend)
print("df_set.loc['interval']:	",df_set.loc['interval'])






def is_nth_bit_set(num: int, n: int):
	if num & (1 << n):
		return True
	return False

def is_nth_bit_val(num: int, n: int):
	if num & (1 << n):
		return 1
	return 0

	

class SnaptoCursor(object):

    def __init__(self, ax):
        self.ax = ax
#        self.lx = ax.axhline(color='g')  # the horiz line
        self.ly = ax.axvline(color='g')  # the vert line
        #self.x = x
        #self.y = y
        # location of point
        
    def mouse_move(self, event):
        if not event.inaxes:
            return
        print('~~~~~~~~~~~~~~^')
        print(event)            
            
#        print('event.xdata = ' + str(event.xdata))
#        self.lx.set_ydata(-1000000000000000000)

        self.ly.set_xdata(event.xdata)
        self.ax.figure.canvas.draw()

#        if event.dblclick:
#        	print("double click")
#        	self.ly.set_xdata(event.xdata)
#        	self.ax.figure.canvas.draw()


x_min_fix=0

class Tesclick(object):
    def __init__(self, ax):
        self.ax = ax
        
    def onclick(self, event):
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(event)
        global x_fix_flg
    
        if event.dblclick:
            print("double click")
            x_fix_flg=False
            x_min_fix=0
            x_max_fix=0        
        elif event.button == 1:
            print('left click ---')
        elif event.button == 2:
            print('middle click ---')          
            self.ax.axvline(num2date(event.xdata).replace(tzinfo=None), color="snow", linewidth=0.5, linestyle="dashed")
            self.ax.annotate(num2date(event.xdata).replace(tzinfo=None).strftime("   %_m/%-d %H:%M"), xy = (num2date(event.xdata).replace(tzinfo=None), event.ydata), size = 25, color = "red", rotation = -90)
#            self.ax.axhline(event.ydata, color="snow", linewidth=1, linestyle="dashed")
#            self.ax.annotate(event.ydata, xy = (num2date(event.xdata).replace(tzinfo=None), event.ydata), size = 15, color = "snow")
        elif event.button == 3: 
            global x_min
            global x_max
            global x_min_fix
            if x_min_fix==0:
                x_min_fix = num2date(event.xdata).replace(tzinfo=None)
                print('right click ---	x_min_fix:	' + str(x_min_fix) )
            else:
                x_min=x_min_fix
                x_max=num2date(event.xdata).replace(tzinfo=None)
                print('right click ---	x_min:	' + str(x_min) + '	x_max:	' + str(x_max))          
                x_fix_flg=True


"""   
def onclick(event):
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(event)
    global x_fix_flg
    
    if event.dblclick:
        print("double click")
        x_fix_flg=False
        x_min_fix=0
        x_max_fix=0        
    elif event.button == 1:
        print('left click ---')
    elif event.button == 2:
        print('middle click ---')          
    elif event.button == 3: 
        global x_min
        global x_max
        global x_min_fix  
        if x_min_fix==0:
            x_min_fix = num2date(event.xdata).replace(tzinfo=None)
            print('right click ---	x_min_fix:	' + str(x_min_fix) )
        else:
            x_min=x_min_fix
            x_max=num2date(event.xdata).replace(tzinfo=None)
            print('right click ---	x_min:	' + str(x_min) + '	x_max:	' + str(x_max))          
            x_fix_flg=True
"""


def get_acc_sync(url):
    t = {}
    v = {}
#    print(url)
    try:
        res = requests.get(url, timeout=(30.0,30.0))   
    except Exception as e:
        print('Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!@get_acc_sync	' + url)
        print(e.args)
    else:
        res.raise_for_status()
        sp = res.text.split('<br>\n')        
        for line in sp:    
            m = re.search(r"(?P<tag>\d{1,10})(,)(\s)(?P<year>\d{4})(/)(?P<month>\d{1,2})(/)(?P<day>\d{1,2})(\s)(?P<Hour>\d{1,2})(:)(?P<minutes>\d{1,2})(:)(?P<sec>\d{1,2})(.)(?P<msec>\d{1,3})(,)(\s)(?P<val>.+)(,)", str(line))
            if m:
                t[int(m.group('tag'))] = datetime.datetime(int(m.group('year')),int(m.group('month')),int(m.group('day')),int(m.group('Hour')),int(m.group('minutes')),int(m.group('sec')),int(m.group('msec'))*1000)
                v[int(m.group('tag'))] = float(m.group('val'))
#                print(t)
#                print(v)
    finally:
	    return t,v
      
def get_exp_sync(url):
    t = {}
    v = {}
#    print(url)
    try:
        res = requests.get(url, timeout=(30.0,30.0))   
    except Exception as e:
        print('Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!@get_exp_sync	' + url)
        print(e.args)
    else:
        res.raise_for_status()
        sp = res.text.split('<br>\n')        
        for line in sp:
            m = re.search(r"(?P<tag>\d{1,11})(\s)(?P<year>\d{4})(-)(?P<month>\d{1,2})(-)(?P<day>\d{1,2})(\s)(?P<Hour>\d{1,2})(:)(?P<minutes>\d{1,2})(:)(?P<sec>\d{1,2})(.)(?P<usec>\d{1,6})(\s)(?P<val>.+)", str(line))
            if m:
                t[int(m.group('tag'))] = datetime.datetime(int(m.group('year')),int(m.group('month')),int(m.group('day')),int(m.group('Hour')),int(m.group('minutes')),int(m.group('sec')),int(m.group('usec')))
                if 'not' not in m.group('val') and 'sat' not in m.group('val'):
                    reobj=re.compile('.*\r')
                    o = reobj.match(m.group('val'))
                    if not o:
                        try:
                            v[int(m.group('tag'))] = float(m.group('val').replace("C","").replace("a.u.","").replace("V",""))             
                        except Exception as f:
                            print('Exception!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!@get_exp_sync	' + str(m.group('val')))
                            print(f.args)
                            v[int(m.group('tag'))] = 0
                else:
                    v[int(m.group('tag'))] = 0
    finally:
	    return t,v
    
    
    
class MyQ(queue.Queue):
    def show_value(self, i):
        print(self.queue[i])

    def sum(self):
        return sum(self.queue)

#    def ave(self):
#        return self.sum() / self.qsize()

    def ave(self):
        return np.mean(self.queue)

    def std(self):
    	return np.std(self.queue)
    	        

class SigInfo:
    def __init__(self, num):
        self.url = ''
        self.sta = ''
        self.sto = ''
        self.time = ''
        self.val = ''
        self.q = MyQ(num)
        self.rave = []
        self.rave_sigma = []
        self.t = {}
        self.d = {}        
        self.mu = 777
        self.sigma = 0
        self.flg_sound = 20
        
sig = [SigInfo(df_sig.loc[n]['rave']) for n in range(len(df_sig))]



sta = ''
flg_fist = 0
x_fix_flg= False
keys = []

ax = [] * len(df_sig)
#fig, (ax) = plt.subplots(nrows=len(df_sig), sharex="row", figsize=(12.0, 100))
fig, (ax) = plt.subplots(nrows=len(df_sig), sharex="row", figsize=(float(x_size), float(y_size)))
fig.patch.set_facecolor(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0])
fig.canvas.set_window_title(str(df_set.loc['title']).replace("1","").strip())

#fig.canvas.manager.window.move(int(x_position), 0)
fig.canvas.manager.window.move(int(x_position), int(y_position))
#fig.canvas.set_window_position(0,0)
#fig.window.SetPosition((0,0))

#fig.canvas.mpl_connect('button_press_event', onclick)
#fig.canvas.mpl_connect('button_press_event', Tesclick.onclick)




for a in ax:
	a.patch.set_facecolor('gray')
	a.grid(axis="x", linestyle=':', color='snow')
	a.set_position([0.0,0.0,0.0,0])

xax_bar = 0.012
#snap_cursor=[]
tes=[]
for n in range(len(df_sig)):
	if  df_sig.loc[n]['ax'] == 1:
#	    snap_cursor.append(SnaptoCursor(ax[n]))
	    tes.append(Tesclick(ax[n]))	    
	    ax[n].set_position([0, (max(df_sig.loc[:]['graph'])-df_sig.loc[n]['graph'])*(1/(max(df_sig.loc[:]['graph'])+1))+xax_bar, 1, 1/(max(df_sig.loc[:]['graph'])+1)])
	    ax[n].patch.set_facecolor( df_sig.loc[n]['fcolor'] )
	    
	if  df_sig.loc[n]['ax'] > 1:
	    for i in range(n):
	        if df_sig.loc[i]['graph'] == df_sig.loc[n]['graph']:
	            ax[n] = ax[i].twinx()
	            ax[n].set_position([0, (max(df_sig.loc[:]['graph'])-df_sig.loc[i]['graph'])*(1/(max(df_sig.loc[:]['graph'])+1))+xax_bar, 1, 1/(max(df_sig.loc[:]['graph'])+1)])

for n in range(len(tes)):
	fig.canvas.mpl_connect('button_press_event', tes[n].onclick)

""" OSOSUGI!!! 
for n in range(len(snap_cursor)):
	fig.canvas.mpl_connect('motion_notify_event', snap_cursor[n].mouse_move)
"""

"""
#	SCATTER
sx = [] * len(df_sig)
#fig2, (sx) = plt.subplots(nrows=len(df_sig), sharex="row", figsize=(2, 100))
fig2, (sx) = plt.subplots(nrows=len(df_sig)+1, sharex="row", figsize=(2, 100))
plt.subplots_adjust(wspace=2.0, hspace=0.0)
#plt.subplots_adjust(bottom=1, left=0, top=0, right=0)
fig2.patch.set_facecolor(str(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0]))
fig2.canvas.set_window_title(str(df_set.loc['title']).replace("1","").strip())

#	Histgram
sx = [] * len(df_sig)
fig2, (sx) = plt.subplots(nrows=len(df_sig)+1, sharex="row", figsize=(5, 100))
plt.subplots_adjust(wspace=2.0, hspace=0.0)
fig2.patch.set_facecolor(str(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0]))
fig2.canvas.set_window_title(str(df_set.loc['title']).replace("1","").strip())
"""


list_label=[]

for n, s in enumerate(sig, 0):
	list_label.append(df_sig.loc[n]['label'])
print("---------------------------------------------------------------")	
#print( list_label )

df = pd.DataFrame( columns=list_label )
#print( df )


def _update():
	global keys
	global df
	keys.clear()
	flg_fail = 0

	while True:
		now = datetime.datetime.now()
		global sta
		sta = sto if sta else now + datetime.timedelta(seconds=-int(df_set.loc['init-span']))
		sto = now + datetime.timedelta(seconds=-3)
		"""
		str_sta = '2021/05/12 9:30:00'
		sta	= dt.strptime(str_sta, '%Y/%m/%d %H:%M:%S')
		str_sto = '2021/05/12 9:50:00'
		sto	= dt.strptime(str_sto, '%Y/%m/%d %H:%M:%S')		
		"""
		if strbegin!="":
		    sta	= dt.strptime(strbegin, '%Y/%m/%d %H:%M:%S')
		    sto	= dt.strptime(strend, '%Y/%m/%d %H:%M:%S')		
		
		
		print('### Update start ###  ' + sta.strftime("%Y/%m/%d+%H:%M:%S") + ' ~ ' + sto.strftime("%Y/%m/%d+%H:%M:%S") + '  len(keys): ' +  str(len(keys)) )

		for n, s in enumerate(sig, 0):
			if 'exp' in df_sig.loc[n]['srv']:
			    s.url =  'http://websvr02.spring8.or.jp/cgi-bin/xdaq/plot_multi.cgi?&Command=data&LeftSignals=' + str(df_sig.loc[n]['sname']) + '&LeftMax=&LeftMin=&LeftLogy=&RightSignals=&RightMax=&RightMin=&RightLogy=&XSignals=&XMax=&XMin=&XLog=&XY=Trend&BeginTime=' + sta.strftime("%Y/%m/%d+%H:%M:%S") + '&EndTime=' + sto.strftime("%Y/%m/%d+%H:%M:%S") + '&Selection=Time'
			    s.time, s.val =  get_exp_sync(s.url)
			else:
			    s.url =  'http://xfweb-dmz-03.spring8.or.jp/cgi-bin/MDAQ/mdaq_sync_plot.py?daq_type=1&lsig=' + str(df_sig.loc[n]['sid']) + '&Selection=Time&begin_bt=' + sta.strftime("%Y/%m/%d+%H:%M:%S") + '&end_bt=' + sto.strftime("%Y/%m/%d+%H:%M:%S") + '&filter=time&sampling=-1&repetition_rate=30&remainder=0&data_order=asc&Command=text' if 'acc_SCSS' in df_sig.loc[n]['srv'] else 'http://srweb-csr-01.sp8.cntl.local/cgi-bin/MDAQ/mdaq_sync_plot.py?lsig=' + str(df_sig.loc[n]['sid']) + '&Selection=Time&begin_bt=' + sta.strftime("%Y/%m/%d+%H:%M:%S") + '&end_bt=' + sto.strftime("%Y/%m/%d+%H:%M:%S") + '&filter=time&sampling=-1&repetition_rate=30&remainder=0&data_order=asc&Command=text'	
			    s.time, s.val =  get_acc_sync(s.url)

#			print(s.url)
			
			if not s.time:
				print("Empty!!!!!!!!!!!!!!!!!!!!!!")
				flg_fail = 1
				print(s.url)
				sto = sta
				time.sleep(30)				
				break
			else:
				print("OK!!!!!!!!!!!!!!!!!!!")
				flg_fail = 0	
		
		if flg_fail==1:
			continue
		
		intersection_keys = set(sig[0].val.keys())
#		print(intersection_keys)
		for n, s in enumerate(sig, 0):
			intersection_keys = intersection_keys.intersection(  set(s.val.keys())     )
			s.t.clear()
			s.d.clear()
			s.rave.clear()
			s.rave_sigma.clear()	
#		print(intersection_keys)
		print('intersection_keys:	' + str(intersection_keys) ) 

		if not intersection_keys:
			print('NO intersection_keys !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
		else:
			print("len(intersection_keys):	" + str(len(intersection_keys)))
			for n, s in enumerate(sig, 0):
#				print("n	" + str(n))
#				print(s.time)
#				print(s.val)
				
				if pd.isnull( df_sig.loc[n]['bit']):
					if int(df_sig.loc[n]['calc-sigma'])==1:
						for x in intersection_keys:
#							print(str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x])+ ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]))
#							print(str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
							if ("TOPUP" in conf_set and sig[int(df_set.loc['prime'])].val[x]!=0) or \
							("SEP5U" in conf_set and sig[int(df_set.loc['prime'])].val[x] > 0) or \
							("CODBPM" in conf_set) or \
							("PLUS" in conf_set) or \
							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set or "XSBTBPM" in conf_set or "SSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 14)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 15) )):
#							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 12)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 13) )):
#								print(str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
#								print('A:	' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
								s.t[x] = s.time[x]
								s.d[x] = s.val[x]		
								"""							
								if s.q.full():
									s.q.get()
									s.q.put(s.val[x])
									s.rave.append(s.q.ave())
									s.rave_sigma.append(s.q.std()*3)					        		            								
								else:
									print('NOTFULL	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
									s.q.put(s.val[x])
									s.rave.append(s.val[x])
									s.rave_sigma.append(0)					
								"""								
					else:
						for x in intersection_keys:
#							print('DEBUG ' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) + ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]) + ' ' + str(sig[12].val[x]) + ' ' + str(sig[13].val[x])	)
#							print('Not Bit	DEBUG ' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
							if ("TOPUP" in conf_set and sig[int(df_set.loc['prime'])].val[x]!=0) or \
							("SEP5U" in conf_set and sig[int(df_set.loc['prime'])].val[x] > 0) or \
							("CODBPM" in conf_set) or \
							("PLUS" in conf_set) or \
							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set or "XSBTBPM" in conf_set or "SSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 14)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 15) )):
#							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 12)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 13) )):
#								print(conf_set + ' B:	' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) + ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]) + ' ' + str(sig[12].val[x]) + ' ' + str(sig[13].val[x])	)
#								print(conf_set + ' B:	' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) + ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]) 	)
								s.t[x] = s.time[x]			#ko re ga gen i n
								s.d[x] = s.val[x]
								"""							
								if s.q.full():
									s.q.get()
									s.q.put(s.val[x])								
									s.rave.append(s.q.ave())					        		            
								else:
									print('NOTFULL	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
									s.q.put(s.val[x])
									s.rave.append(s.val[x])
#								print("/-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-")
#								print(s.t)	# KOKO NI IRU!!									
#								print(s.rave)	# KOKO NI IRU!!
								"""
				else:
					if int(df_sig.loc[n]['calc-sigma'])==1:
						for x in intersection_keys:
#							print(str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x])+ ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]))
							if ("TOPUP" in conf_set and sig[int(df_set.loc['prime'])].val[x]!=0) or \
							("SEP5U" in conf_set and sig[int(df_set.loc['prime'])].val[x] > 0) or \
							("CODBPM" in conf_set) or \
							("PLUS" in conf_set) or \
							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set or "XSBTBPM" in conf_set or "SSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 14)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 15) )):
#							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 12)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 13) )):
#								print('C:	' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
								s.t[x] = s.time[x]
								s.d[x] = s.val[x]
					      	  #print('	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))		        
								"""				      	  
								if s.q.full():
									s.q.get()
									s.q.put(s.val[x])								
									s.rave.append(is_nth_bit_val(int(s.val[x]), int(df_sig.loc[n]['bit'])))			        
									s.rave_sigma.append(s.q.std()*3)
								else:
									print('NOTFULL	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
									s.q.put(s.val[x])
									s.rave.append(s.val[x])
									s.rave_sigma.append(0)					
								"""
					else:
						for x in intersection_keys:
#							print('TEST ' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x])+ ' ' + str(sig[5].val[x])+ ' ' + str(sig[6].val[x])+ ' ' + str(sig[7].val[x])+ ' ' + str(sig[8].val[x]) + ' ' + str(sig[9].val[x]) + ' ' + str(sig[10].val[x]) + ' ' + str(sig[11].val[x]) + ' ' + str(sig[12].val[x]) + ' ' + str(sig[13].val[x]))
#							print('BIT	TEST ' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
							if ("TOPUP" in conf_set and sig[int(df_set.loc['prime'])].val[x]!=0) or \
							("SEP5U" in conf_set and sig[int(df_set.loc['prime'])].val[x] > 0) or \
							("CODBPM" in conf_set) or \
							("PLUS" in conf_set) or \
							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set or "XSBTBPM" in conf_set or "SSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 14)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 15) )):
#							(("BL2" in conf_set or "BL3" in conf_set or "XSBT" in conf_set) and (is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), int(df_set.loc['route'])) and is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 8)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 12)  and not is_nth_bit_set(int(sig[int(df_set.loc['prime'])].val[x]), 13) )):
#								print('D:	' + str(x) + ' ' + str(sig[0].time[x]) + ' ' + str(sig[0].val[x]) + ' ' + str(sig[1].val[x])	+ ' ' + str(sig[2].val[x]) + ' ' + str(sig[3].val[x])+ ' ' + str(sig[4].val[x]) )
								s.t[x] = s.time[x]
#								s.d[x] = s.val[x]
								s.d[x] = is_nth_bit_val(int(s.val[x]), int(df_sig.loc[n]['bit']))
					      	  #print('	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
								"""
								if s.q.full():
									s.q.get()
									s.q.put(s.val[x])
									s.rave.append(is_nth_bit_val(int(s.val[x]), int(df_sig.loc[n]['bit'])))
#									print('D:	' + str(s.rave[-1]))
								else:
									print('NOTFULL	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
									s.q.put(s.val[x])
									s.rave.append(s.val[x])
								"""

				sortkeys = sorted(s.t.keys())
#				print(sortkeys)				
				for k in sortkeys:
#					print("intersection_keys:	" + str(k) + "	data" + str(s.d[k]))
					if s.q.full():
						s.q.get()
						s.q.put(s.d[k])		
						s.rave.append(s.q.ave())
#						df = pd.DataFrame({ 'test':sig[0].d[k]}	)
					else:
#						print('NOTFULL	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()))
						s.q.put(s.d[k])
						s.rave.append(s.d[k])

#				print("result----------------------------------------------------------------------------")
#				print(s.t)
#				print(s.d)
					
				if s.mu==777 and s.q.full():
					s.mu = s.q.ave() if pd.isnull( df_sig.loc[n]['bit']) else is_nth_bit_val(int(s.q.ave()), int(df_sig.loc[n]['bit']))
					s.sigma = s.q.std()
					print('HITTTTTTTTTTTTTTTTTTTTTTTTTTTTT	s.q.size() = ' + str(s.q.qsize()) + '	s.q.full() = ' + str(s.q.full()) + '  mu = ' + str(s.mu) + '	sigma = ' + str(s.sigma))
				else:

					if not pd.isnull( df_sig.loc[n]['sound']) and s.rave:
						if s.rave[-1]<(s.mu*df_sig.loc[n]['sound']) and s.flg_sound<=0:
							if s.flg_sound==0:
								print('SOUND	 latest=' + str(s.rave[-1])  + '	mu=' + str(s.mu) + '	s.flg_sound=' + str(s.flg_sound))
								res = subprocess.run(["amixer", "sset", "Master", "77%"], stdout=subprocess.PIPE)
								res = subprocess.run(["aplay", "o.wav"], stdout=subprocess.PIPE)
								s.flg_sound = 20
							else:
								s.flg_sound = 3
								print('+	s.flg_sound =' + str(s.flg_sound))
						else:
							s.flg_sound -= 1
							print('s.flg_sound =' + str(s.flg_sound))
							
					"""
					if not pd.isnull( df_sig.loc[n]['sound']) and s.rave:
						if s.rave[-1]<(s.mu*df_sig.loc[n]['sound']) and s.flg_sound<0:
							print('SOUND	 latest=' + str(s.rave[-1])  + '	mu=' + str(s.mu) )
							res = subprocess.run(["amixer", "sset", "Master", "80%"], stdout=subprocess.PIPE)
							res = subprocess.run(["aplay", "o.wav"], stdout=subprocess.PIPE)
							s.flg_sound = 10
						else:
							s.flg_sound -= 1
							print('s.flg_sound =' + str(s.flg_sound))
						
					if not pd.isnull( df_sig.loc[n]['sound']) and s.rave and s.rave[-1]<(s.mu*df_sig.loc[n]['sound']) and s.flg_sound<0:
						print('SOUND	 latest=' + str(s.rave[-1])  + '	mu=' + str(s.mu) )
						res = subprocess.run(["amixer", "sset", "Master", "80%"], stdout=subprocess.PIPE)
						res = subprocess.run(["aplay", "o.wav"], stdout=subprocess.PIPE)
						s.flg_sound = 10
					else:
						s.flg_sound -= 1
						print('s.flg_sound =' + str(s.flg_sound))
					"""

			
#			df.assign(df_sig.loc[0]['label']=sig[0].rave)			
			"""				
			tmp_se = pd.Series( [ sig[0].rave, sig[1].rave, sig[2].rave, sig[3].rave, sig[4].rave ], index=[df_sig.loc[0]['label'], df_sig.loc[1]['label'], df_sig.loc[2]['label'], df_sig.loc[3]['label'], df_sig.loc[4]['label']] )
#			tmp_se = pd.Series( [ i, i*i, i*3 ], index=df.columns, name='No.' + str(i) )
			df = df.append( tmp_se , ignore_index=True)
#			df = df.append( [ sig[0].rave, sig[1].rave, sig[2].rave, sig[3].rave, sig[4].rave ])
			print( sig[0].rave )
			print( sig[1].rave )
			print( sig[2].rave )
			print( sig[3].rave )
			print( sig[4].rave )
			if sig[0].rave:
				for n, s in enumerate(sig, 0):
					df[df_sig.loc[n]['label']] = s.rave					
			"""																

#			print( df )				
#			print("DEBUG:	intersection_keys:	" + str(len(intersection_keys)))
				
#			for s in sig:
#			    print("s.rave:	" + "	" +str(len(s.rave)))
#			    print("s.allval:	" + "	" +str(len(s.allval)))
#			    if len(s.allval)>=(len(intersection_keys)+int(df_set.loc['ave'])):
#				    del s.allval[:len(intersection_keys)]

#			print(sig[0].d)
#			print(sig[0].d.keys())
#			print("sig[0].d.keys():	" + str(sig[0].d.keys()))



#			print("-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-^-")
#			print(sig[0].t)	
#			print(sig[0].rave)	

			"""		
			"""					
#			print("~~~~~~~~~~~~~~~~~~")
#			print(sig[0].t.keys())
			keys = sorted(sig[0].t.keys())
#			print("******************")
#			print(keys)
			keys = [sig[0].t[int(s)] for s in keys]
#			print("keys-------------------")
#			print(keys)		
			"""			
			print("keys-------------------")
			keys = sig[0].datetime
			print(keys)
			"""			

			""" TESST """
			
			

			
			"""	data frame """
			if ("SEP5U" in conf_set):
				for n, data in enumerate(sig[0].rave, 0):
#					print("sig[0].rave[n]:	" + "	" +str(sig[0].rave[n]))
					tmplist=[]
					for s in sig:
						tmplist.append(s.rave[n])
					df.loc[keys[n]] = tmplist
#				print( df )
				print("-----------------------")
#				print( df.info() )				
#				print( df.corr() )
#				print( df[df[df_sig.loc[0]['label']] < 1000] )
				print("-----------------------")
#				print( df.query('900 < sep5u_i < 1000') )
#				print( df.query('900 < ' + df_sig.loc[0]['label'] + ' < 1000') )
										
#			df.corr().style.background_gradient(axis=None, cmap='viridis')
#			sns.heatmap(df.corr(), vmax=1, vmin=0, center=0)
#			plt.savefig('corr.png')
#			print("-----------------------")
			
			
			
			intersection_keys.clear()

#			print("keys:	" + str(len(keys)))
		
		""" TESST 
		print("-----------------------------------------------------------------------")
#		df = pd.DataFrame({ 'key':sig[0].d.keys()}	)
		df = pd.DataFrame({ 'key':sig[0].d.values()}	)
		print(df)

		print("-----------------------------------------------------------------------")
		df = pd.DataFrame('key':sig[0].d.values()	)
		print(df)
		"""		
#		print(sig[0].d.values())
		
		
		print('### Updated ###  ' + sta.strftime("%Y/%m/%d+%H:%M:%S") + ' ~ ' + sto.strftime("%Y/%m/%d+%H:%M:%S") + '  len(keys): ' +  str(len(keys)) )
		time.sleep(int(df_set.loc['interval']))






def _redraw(_):
	global flg_fist
	global x_min_init
	global x_fix_flg
	global x_min
	global x_max
	

#	plt.show()		#????

#	if not keys:
#		print('DEBUG@<<< redraw >>>		No keys[] '
#		return


	print(keys)
		
	if not keys:
		print('Debug@<<< redraw >>>	No key')
		return

	print('Debug@<<< redraw >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>	')	
	if flg_fist == 0 and keys:
#		print(keys)
		sorted_list = sorted(keys)
#		print(sorted_list)
		x_min = sorted_list[0]
		x_min_init = x_min


	if not 'x_min' in globals():
		return
		
	if not x_fix_flg and keys:	# Full SPAN
		x_min = x_min_init
		x_max = keys[-1]

	if not 'x_max' in globals():
		return
			
	for n, s in enumerate(sig, 0):
		ax[n].set_xlim([x_min, x_max + (x_max -x_min)/12])

#	if not keys:
#		return
		

	""" for debug """
	df_sig = pd.read_excel(conf_sig, sheet_name="sig")
	df_set = pd.read_excel(conf_set, sheet_name="setting", header=None, index_col=0)			
	
    
	for n, s in enumerate(sig, 0):
		if len(keys) != len(s.rave):
			print(str(df_sig.loc[n]['sname']) +	"	Not match dimension	keys:" + str(len(keys))	+ "		s.rave" + str(len(s.rave)))
			return

	"""	TEST
	if ("SEP5U" in conf_set):
		print("-----------------------")	
#		print( df )
		fig_test, axes = plt.subplots(nrows=3, ncols=2, figsize=(5, 5))
		df.plot(ax=axes[0, 0], legend=True, y=[df_sig.loc[1]['label']])
		df.plot(ax=axes[1, 0], y=[df_sig.loc[1]['label']], bins=50, legend=True, kind='hist')
#		df.plot(ax=axes[1, 0], y=[df_sig.loc[1]['label'],df_sig.loc[2]['label']], legend=False, kind='hist')		
#		df.plot(ax=axes[2, 0], x=df_sig.loc[1]['label'], y=df_sig.loc[2]['label'], kind='scatter', c=df_sig.loc[0]['label'], cmap='Blues')
		df.plot(ax=axes[0, 1], legend=True, y=[df_sig.loc[2]['label']])
		df.plot(ax=axes[1, 1], y=[df_sig.loc[2]['label']], bins=50, legend=True, kind='hist')
		
		df.plot(ax=axes[2, 0], x=df_sig.loc[1]['label'], y=df_sig.loc[2]['label'], kind='scatter', c=df_sig.loc[0]['label'], cmap='Blues')
		df.plot(ax=axes[2, 1], x=df_sig.loc[3]['label'], y=df_sig.loc[4]['label'], kind='scatter', c=df_sig.loc[0]['label'], cmap='Blues')
		fig_test.savefig('axes.png')
#		print( pd.pivot_table(df, index=[df_sig.loc[0]['label']], columns=[df_sig.loc[1]['label']] ) )
	"""
	
#	print(keys)

	print('<<< redraw >>>	' + str(x_min) + '	- 	' + str(x_max))	
#	print(sig[0].time)
	for n, s in enumerate(sig, 0):
#		print(n)
#		print(keys)
#		print(s.url)
#		print(s.time)
#		print(s.rave)
#		print(s.rave_sigma)
#		print(s.mu)
#		print(s.sigma)
		
		if s.mu!=777:
			y_range = s.sigma*float(df_sig.loc[n]['y_range'])*3 if int(df_sig.loc[n]['rave'])!=1 else float(df_sig.loc[n]['y_range'])*3
			y_tolerance = s.sigma*float(df_sig.loc[n]['y_range']) if int(df_sig.loc[n]['rave'])!=1 else float(df_sig.loc[n]['y_range'])

#	MOTO
#			y_range = s.sigma*float(df_set.loc['y_range']) if pd.isnull( df_sig.loc[n]['y_range'] ) else float(df_sig.loc[n]['y_range'])
#			y_tolerance = s.sigma*float(df_set.loc['y_tolerance']) if pd.isnull( df_sig.loc[n]['y_range'] ) else float(df_sig.loc[n]['y_range'])*0.3
			
			ax[n].set_ylim(s.mu-y_range, s.mu+y_range)
			if df_sig.loc[n]['ax']==1:
				ax[n].axhspan(s.mu-y_tolerance, s.mu+y_tolerance,	color='#333333')
					
			ax[n].axhline(s.mu, color=str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0], linewidth=0.1)
			if not pd.isnull( df_sig.loc[n]['sound']):
				ax[n].axhline(s.mu*float(df_sig.loc[n]['sound']), color="crimson", linewidth=0.3, linestyle="dashed")

	
		if int(df_sig.loc[n]['calc-sigma'])==0:
			if int(df_sig.loc[n]['rave'])==1:
				ax[n].plot(keys, s.rave, linestyle="solid", marker=str(df_sig.loc[n]['marker']).replace("1","").strip().splitlines()[0], markersize=df_sig.loc[n]['linewidth'], color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'], clip_on=False)
			else:
				ax[n].plot(keys, s.rave, linestyle="solid", linewidth=df_sig.loc[n]['linewidth'], color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'], clip_on=False)
		else:
			ax[n].errorbar(keys, s.rave, yerr = s.rave_sigma, elinewidth=0.001, capsize=1, capthick=0.3, alpha=0.5, marker=str(df_sig.loc[n]['marker']).replace("1","").strip().splitlines()[0], markersize=df_sig.loc[n]['linewidth'], linestyle="solid", color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'])
		"""
		if int(df_sig.loc[n]['calc-sigma'])==0:
			ax[n].plot(keys, s.rave, linestyle="solid", linewidth=df_sig.loc[n]['linewidth'], color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'], clip_on=False)
		else:
			ax[n].errorbar(keys, s.rave, yerr = s.rave_sigma, elinewidth=0.001, capsize=1, capthick=0.3, alpha=0.5, marker=str(df_sig.loc[n]['marker']).replace("1","").strip().splitlines()[0], markersize=df_sig.loc[n]['linewidth'], linestyle="solid", color=df_sig.loc[n]['color'], label=df_sig.loc[n]['label'])
		"""
#		ax[n].set_xlim([x_min, x_max + (x_max -x_min)/12])

#		ax[n].gca().spines['top'].set_visible(False)
#		ax[n].gca().spines['bottom'].set_visible(False)
		
		if flg_fist == 0:
			ax[n].legend(loc='upper left', bbox_to_anchor=(0.2*(df_sig.loc[n]['ax']-1), 0, 0.35, 0.3))
#			ax[n].legend(loc='upper left', bbox_to_anchor=(0.12*(df_sig.loc[n]['ax']-1), 0, 0.35, 0.3))				MOTO
#			ax[n].xaxis.set_major_formatter(DateFormatter('%d %H:%M'))
#			ax[n].xaxis.set_major_formatter(DateFormatter('%d %H:%M'))
			ax[n].xaxis.set_major_formatter(DateFormatter('%-m/%-d(%-H:%-M)'))
#			ax[n].xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
			ax[n].tick_params(axis='x', labelsize=14)

#	keys.clear()
	flg_fist = 1

"""
def _redraw2(_):
	if not keys:
		return

	df_sig = pd.read_excel(conf_sig, sheet_name="sig")
	df_set = pd.read_excel(conf_set, sheet_name="setting", header=None, index_col=0)

	for n, s in enumerate(sig, 0):
		if len(keys) != len(s.rave):
			print(str(df_sig.loc[n]['sname']) +	"	Not match dimension	keys:" + str(len(keys))	+ "		s.rave" + str(len(s.rave)))
			return
	
	print('--- redraw2 ---')
#	print(keys)

#	p=int(df_set.loc['pk'])
#	for n, s in enumerate(sig, 0):
#		if s.mu!=0:
#			sx[n].scatter(sig[p].rave, sig[n].rave, s=20, linewidths=0,	c=sig[1].rave, cmap='rainbow' , vmin=sig[1].mu-sig[1].sigma*3 , vmax=sig[1].mu+sig[1].sigma*3, clip_on=False)
#			sx[n].set_xlim(sig[p].mu-sig[p].sigma*10, sig[p].mu+sig[p].sigma*10)
#			sx[n].set_ylim(sig[n].mu-sig[n].sigma*10, sig[n].mu+sig[n].sigma*10)
#			sx[n].axhline(sig[n].mu, color=str(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0]), linewidth=0.5)
#			sx[n].axvline(sig[p].mu, color=str(str(df_set.loc['bcolor']).replace("1","").strip().splitlines()[0]), linewidth=0.5)
#			sx[n].set_xlabel(df_sig.loc[p]['label'])
#			sx[n].set_ylabel(df_sig.loc[n]['label'])
		
	for n, s in enumerate(sig, 0):
		if s.mu!=0:
			sx[n].hist(sig[n].rave, bins=20, alpha=0.65, label="Haiki", color="red", stacked=False)
#			sx[n].set_xlim(sig[p].mu-sig[p].sigma*10, sig[p].mu+sig[p].sigma*10)
#			sx[n].set_ylim(sig[n].mu-sig[n].sigma*10, sig[n].mu+sig[n].sigma*10)
"""



def _init():
	t = threading.Thread(target=_update)
	t.daemon = True
	t.start()

params = {
	'fig': fig,
	'func': _redraw,  # グラフを更新する関数
	'init_func': _init,  # グラフ初期化用の関数 (データ更新用スレッドの起動)
#	'fargs': keys,  # 関数の引数 (フレーム番号を除く)
	'interval': 13 * 1000,  # グラフを更新する間隔 (ミリ秒)
}
anime = animation.FuncAnimation(**params)

"""
params2 = {
	'fig': fig2,
	'func': _redraw2,  # グラフを更新する関数
	'init_func': _init,  # グラフ初期化用の関数 (データ更新用スレッドの起動)
#	'fargs': keys,  # 関数の引数 (フレーム番号を除く)
	'interval': 53 * 1000,  # グラフを更新する間隔 (ミリ秒)
}
anime2 = animation.FuncAnimation(**params2)
"""

plt.show()


