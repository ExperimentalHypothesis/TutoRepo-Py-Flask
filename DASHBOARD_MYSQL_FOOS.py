import dash
import dash_table
import dash_html_components as html
from flask import Flask, render_template
import pymysql
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import dash_core_components as dcc
import datetime
   


host="vmi239120.contaboserver.net"
user="nirvikalpa"
password="password"
db="trading_automatic"


 ######### getting data for profitloss histogram  #########  
def select_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT profit_loss from iml_aos")
    pl = cur.fetchall()
    return pl

pl_tuple =  select_pl()

pl = []
for i in pl_tuple:
    pl.append(i[0])

numbered_pl = list(enumerate(pl, 1))

pl_trade_id = []
pl_trade_result = []
for i in numbered_pl:
    pl_trade_id.append(i[0])
    pl_trade_result.append(i[1])

# immitating runups and drawdowns
import random
runups = []
drawdowns = []
for i in pl_trade_result:
    runups.append(random.randint(0,190))
    drawdowns.append(random.randint(-200,0))
    
 ######### getting data for equity  #########  
def select_cum_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT cum_pl from iml_aos")
    result = cur.fetchall()
    return result

cum_pl_tuple = select_cum_pl()  

cum_pl = []
for i in cum_pl_tuple:
    cum_pl.append(i[0])

numbered_cum_pl = list(enumerate(cum_pl, 1))

cum_pl_trade_id = []
cum_pl_result = []
for i in numbered_cum_pl:
    cum_pl_trade_id.append(i[0])
    cum_pl_result.append(i[1])
     
######### getting % nr of trades for each symbol -> piechart #########
def select_symbol():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT  COUNT(*)  from iml_aos where symbol like '%YM__-CBOT%'")
    ym = cur.fetchall()
    cur.execute("SELECT  COUNT(*)  from iml_aos where symbol like '%NQ__-CME%'")
    nq = cur.fetchall()
    cur.execute("SELECT  COUNT(*)  from iml_aos where symbol like '%ES__-CME%'")
    es = cur.fetchall()
    cur.execute("SELECT  COUNT(*)  from iml_aos where symbol like'%RTY__-CME%'")
    rty = cur.fetchall()
    return (ym[0][0], nq[0][0], es[0][0], rty[0][0]) # returning number of trades for each symbol -- directly unpacked from tuple

ym, nq, es, rty = select_symbol()


########## geeting daily cumulative results -> histogram #########
def select_daily_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT entry_date, sum(profit_loss), count(*) from iml_aos group by entry_date")
    daily_pl = cur.fetchall()
    return daily_pl

daily_results = select_daily_pl()

daily_dt = []
daily_pl_sum = []
daily_trades_sum = []
for i in daily_results:
    daily_dt.append(i[0])
    daily_pl_sum.append(i[1])
    daily_trades_sum.append(i[2])

########## geeting quatninty of each direction -> piechart #########
def select_direction():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT qty, count(*) from iml_aos where qty < 0 group by qty")
    short = cur.fetchall()
    cur.execute("SELECT qty, count(*) from iml_aos where qty > 0 group by qty")
    long = cur.fetchall()
    return long[0][1], short[0][1]

long, short = select_direction()

########## geeting quatninty of each direction -> piechart #########
def select_pl_by_direction():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT qty, sum(profit_loss), count(*) from iml_aos where qty < 0 group by qty")
    short = cur.fetchall()
    cur.execute("SELECT qty, sum(profit_loss), count(*) from iml_aos where qty > 0 group by qty")
    long = cur.fetchall()
    return long[0][1], short[0][1]

win_long, win_short = select_pl_by_direction()

########## geeting time in possiton -> horizontal barchart #########
def select_time_in_position():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT TIMEDIFF(exit_datetime, entry_datetime) from iml_aos")
    time_in_pos = cur.fetchall()
    return time_in_pos

time_in_pos = select_time_in_position()

t_0_10 = t_11_20 = t_21_30 = t_31_40 = t_41_50 = t_51_60 = t_61_more = 0

for e in time_in_pos:
    if e[0] < datetime.timedelta(minutes=10):
        t_0_10 += 1
    elif e[0] >= datetime.timedelta(minutes=10) and e[0] < datetime.timedelta(minutes=20):
        t_11_20 += 1
    elif e[0] >= datetime.timedelta(minutes=20) and e[0] < datetime.timedelta(minutes=30):
        t_21_30 += 1 
    elif e[0] >= datetime.timedelta(minutes=30) and e[0] < datetime.timedelta(minutes=40):
        t_31_40 += 1 
    elif e[0] >= datetime.timedelta(minutes=40) and e[0] < datetime.timedelta(minutes=50):
        t_41_50 += 1 
    elif e[0] >= datetime.timedelta(minutes=50) and e[0] < datetime.timedelta(minutes=60):
        t_51_60 += 1 
    else:
        t_61_more += 1 
