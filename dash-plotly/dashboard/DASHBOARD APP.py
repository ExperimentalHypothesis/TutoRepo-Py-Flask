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

######### getting profitloss for each symbol -> piechart #########

def get_pl_for_each_symbol():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE SYMBOL LIKE '%YM__-CBOT%'")
    pl_ym = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE SYMBOL LIKE '%NQ__-CME%'")
    pl_nq = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE SYMBOL LIKE '%ES__-CME%'")
    pl_es = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE SYMBOL LIKE '%RTY__-CME%'")
    pl_rty = cur.fetchall()
    
    return pl_ym[0][0], pl_nq[0][0], pl_es[0][0], pl_rty[0][0]

pl_ym, pl_nq, pl_es, pl_rty = get_pl_for_each_symbol()



########## geeting daily cumulative results -> histogram + daily winloss ratio #########
def select_daily_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT entry_date, sum(profit_loss), count(*) from iml_aos group by entry_date")
    daily_results = cur.fetchall()
    return daily_results
   
daily_results = select_daily_pl()

daily_dt = []
daily_pl_sum = []
daily_trades_sum = []
for i in daily_results:
    daily_dt.append(i[0])
    daily_pl_sum.append(i[1])
    daily_trades_sum.append(i[2])
    winning_days = loosing_days = 0
    for i in daily_pl_sum:
        if i > 0:
            winning_days += 1
        elif i < 0:
           loosing_days += 1
        else:
            pass

daily_winloss_ratio = winning_days/loosing_days
  
        



     

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

t_0_5 = t_6_10 = t_11_15 = t_16_20 = t_21_25 = t_26_30 = t_31_35 = t_36_40 = t_41_45 = t_46_50 = t_51_55 = t_56_60 = t_61_more = 0

for e in time_in_pos:
    if e[0] <= datetime.timedelta(minutes=5):
        t_0_5 += 1
    elif e[0] > datetime.timedelta(minutes=5) and e[0] <= datetime.timedelta(minutes=10):
        t_6_10 += 1
    elif e[0] > datetime.timedelta(minutes=10) and e[0] <= datetime.timedelta(minutes=15):
        t_11_15 += 1
    elif e[0] > datetime.timedelta(minutes=15) and e[0] <= datetime.timedelta(minutes=20):
        t_16_20 += 1 
    elif e[0] > datetime.timedelta(minutes=20) and e[0] <= datetime.timedelta(minutes=25):
        t_21_25 += 1 
    elif e[0] > datetime.timedelta(minutes=25) and e[0] <= datetime.timedelta(minutes=30):
        t_26_30 += 1 
    elif e[0] > datetime.timedelta(minutes=30) and e[0] <= datetime.timedelta(minutes=35):
        t_31_35 += 1 
    elif e[0] > datetime.timedelta(minutes=35) and e[0] <= datetime.timedelta(minutes=40):
        t_36_40 += 1 
    elif e[0] > datetime.timedelta(minutes=40) and e[0] <= datetime.timedelta(minutes=45):
        t_41_45 += 1 
    elif e[0] > datetime.timedelta(minutes=45) and e[0] <= datetime.timedelta(minutes=50):
        t_46_50 += 1
    elif e[0] > datetime.timedelta(minutes=50) and e[0] <= datetime.timedelta(minutes=55):
        t_51_55 += 1 
    elif e[0] > datetime.timedelta(minutes=55) and e[0] <= datetime.timedelta(minutes=60):
        t_56_60 += 1       
    else:
        t_61_more += 1 

def get_performance_by_time_in_position():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) < 600)")
    perf_t_0_10 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) >= 600 AND TIMEDIFF(exit_datetime, entry_datetime) < 1200)")
    perf_t_10_20 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) >= 1200 AND TIMEDIFF(exit_datetime, entry_datetime) < 1800)")
    perf_t_20_30 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) >= 1800 AND TIMEDIFF(exit_datetime, entry_datetime) < 2400)")
    perf_t_30_40 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) >= 2400 AND TIMEDIFF(exit_datetime, entry_datetime) < 3000)")
    perf_t_40_50 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) >= 3000 AND TIMEDIFF(exit_datetime, entry_datetime) < 3600)")
    perf_t_50_60 = cur.fetchall()
    cur.execute("SELECT SUM(profit_loss) from iml_aos WHERE(SELECT TIMEDIFF(exit_datetime, entry_datetime) > 3600)")
    perf_t_60_more = cur.fetchall()

    return perf_t_0_10[0][0], perf_t_10_20[0][0], perf_t_20_30[0][0], perf_t_30_40[0][0], perf_t_40_50[0][0], perf_t_50_60[0][0], perf_t_60_more[0][0]

perf_t_0_10, perf_t_10_20, perf_t_20_30, perf_t_30_40, perf_t_40_50, perf_t_50_60, perf_t_60_more = get_performance_by_time_in_position()


 ###################################################################################################################################################  


# data for first row
equity =  go.Scatter(
    x = cum_pl_trade_id,
    y = cum_pl_result, 
    mode = "lines", 
    line = dict(color = ('rgb(0, 0, 0)'), width = 3),
    name = 'Equity'
)

profitloss = go.Bar( 
    x = pl_trade_id,
    y = pl_trade_result,
    name = 'Profitloss',
    opacity = 0.6,
    marker = dict(color='rgb(0, 0, 255)')
)

runup = go.Bar(
    x = pl_trade_id,
    y = runups,
    name='Runups',
    opacity = 0.6,
    marker=dict(color='rgb(0, 255, 0)')
)

drawdown = go.Bar(
    x = pl_trade_id,
    y = drawdowns,
    name='Drawdowns',
    opacity = 0.6,
    marker=dict(color='rgb(255, 0, 0)')
)

data = [equity, profitloss, runup, drawdown]

layout = go.Layout(
    title='Equity',
    xaxis=dict(
        title='Number of trades',
        tickfont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        )
    ),
    yaxis=dict(
        title='USD',
        titlefont=dict(
            size=12,
            color='rgb(107, 107, 107)'
        ),
        tickfont=dict(
            size=14,
            color='rgb(107, 107, 107)'
        )
    ),
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.1,
    bargroupgap=0.0
)










import numpy as np

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N)+5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-5

trace0 = go.Scatter(
    x = random_x,
    y = random_y0,
    mode = 'lines',
    line = dict( color = ('rgb(22, 96, 167)'), width = 4,),
    name = 'one'
)
trace1 = go.Scatter(
    x = random_x,
    y = random_y1,
    mode = 'lines+markers',
    name = 'two'
)
trace2 = go.Scatter(
    x = random_x,
    y = random_y2,
    mode = 'markers',
    name = 'three'
)


testingdata = [trace0, trace1, trace2]









# data for table
table_rows = ['Closed Trades Result', 'Closed Trades Profit', 'Closed Trades Loss', 'Profit Factor', " ",
              'Equity Peak', 'Maximum Runup', 'Maximum Drawdown', " ",
             "Total Trades", "Long Trades", "Short Trades", "Winning Trades", "Loosing Trades", "Percet Profitable", " ",
             "Average Trade Result", "Average Winning Trade", "Average Loosing Trade", "Largest Winning Trade", "Largest Loosing Trade", " ",
             "Average Time in Trades", "Average Time in Winning Trade", "Average Time in Loosing Trade","Longest Held Winning Trade", "Longest Held Loosing Trade", " ", 
             "Average Qty Per Trade", "Largest Trade Qty" ]

nr_of_items = len(table_rows)


app = dash.Dash(__name__)

app.css.append_css({"external_url" : "https://codepen.io/amyoshino/pen/jzXypZ.css"})

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.title = "AOS Dashboard"

app.layout = html.Div(children=[
    
    #  --------------------------------------------------- 0 row: headings ----------------------------------------------------
    html.Div(
    [ 
        html.H3(children='web data visualisation test in python', style={"text-align":"center"}),
        html.H5(children='sample of plotting data from a running SC AOS study using realtime updates', style={"text-align":"center"}),
    ],  className = "row"),

#  --------------------------------------------------- 1 row alternative: equity chart using PLOTY GO.SCATTER --------------------------------------------------

    html.Div([
        dcc.Graph(
            id = 'equity',
            figure = go.Figure(
                                data = data,                     
                                layout = layout
                            )
                )], className = "row"),

   # ---------------------------------------------------  2 row: table stats PLOTLY TABLE ---------------------------------------------------
       html.Div([ 
            dcc.Graph(
                id='table',
                figure=go.Figure(
                                 data = [ 
                                            go.Table(
                                            header=dict(values=['Metric', 'All Trades', 'Long Trades', 'Short Trades']),
                                            cells=dict(values=[[*table_rows], [], [], []]))
                                        ],      
                                layout = go.Layout(title="Trade Statistics"))
                        )], className = "row"),

    # ---------------------------------------------------  3 row: barchart daily perf + winloss ratio -----------------------------------
       
    html.Div([ 
        html.Div([ # bar chart daily performance 
                dcc.Graph(
                id = 'dailyperf',
                figure = {
                        'data': [
                                    {'x': daily_dt, 'y': daily_pl_sum, 'type': 'bar', 'name': 'Daily Performance'}, 
                                ], 
                        'layout': {'title': 'Daily Performance', "color": '#7FDBFF' }
                        }
                    )
        ],  className = "nine columns"),

        html.Div([# pie win/loss ratio 
                    dcc.Graph(
                        id='piechart-daily_winloss',
                        figure=go.Figure(
                                            data = [
                                                    go.Pie(labels=['Winnig Days', 'Losing Days'],
                                                    values=[winning_days, loosing_days])
                                                ],      
                        layout = go.Layout(title='Daily Win/Loss Ratio')))

        ], className = "three columns"),
        ], className = "row"),

 #  --------------------------------------------------- 4 row: Long/Short, Time in pos ---------------------------------------------------
     html.Div([   
             html.Div([ # pie chart long short 
                        dcc.Graph(
                        id='piechart-direction',
                        figure=go.Figure(
                                         data = [
                                                    go.Pie(
                                                                labels=['Long', 'Short'],
                                                                values=[long, short],
                                                               
                                                           )
                                                ],      
                                         layout = go.Layout(title='Distribution by Direction')))
                            ], className = "three columns"),      
   
             html.Div([# bar chart long short performance
                        dcc.Graph(
                        id='barchart-winloss',
                         figure={
                            'data': [
                                        {'x': ["long"], 'y': [win_long], 'type': 'bar', 'name': 'Long'}, 
                                        {'x': ["short"], 'y': [win_short], 'type': 'bar', 'name': 'Short'}, 
                                    ], 
                            'layout': {'title': 'Performance by direction'}
                           }
                      )], className = "three columns"),  

               html.Div([# bar chart long short performance
                        dcc.Graph(
                        id='testingdata',
                        figure=go.Figure(data = testingdata, layout = go.Layout(title = "Heat Map (testing module)"))
                         )], className = "six columns")
             
             ], className = "row"),

 #    --------------------------------------------------- 5 row: daily profitloss ---------------------------------------------------
 html.Div([html.Div([
         dcc.Graph(
             id='piechart-distr_by_instr',
             figure=go.Figure(
                 data = [
                         go.Pie(
                                 labels=['YM', 'NQ', 'ES', 'RTY'],
                                 values=[ym, nq, es, rty],
                                 hole=0.4
                                )
                        ],      
                 layout = go.Layout(title='Distribution by Instrument')))
                            ], className = "four columns"),

        html.Div([# bar chart long short performance
                            dcc.Graph(
                            id='barchart-performance_by_instrument',
                             figure={
                                'data': [
                                            {'x': ["YM"], 'y': [pl_ym], 'type': 'bar', 'name': 'YM'}, 
                                            {'x': ["NQ"], 'y': [pl_nq], 'type': 'bar', 'name': 'NQ'}, 
                                            {'x': ["ES"], 'y': [pl_es], 'type': 'bar', 'name': 'ES'}, 
                                            {'x': ["RTY"], 'y': [pl_rty], 'type': 'bar', 'name': 'RTY'}, 

                                        ], 
                                'layout': {'title': 'Performance by Instrument'}
                               }
                          )], className = "three columns"),
 
     ], className = "row"),

  #    --------------------------------------------------- 5 row: daily profitloss ---------------------------------------------------
  
  html.Div([ html.Div([ # horizontal bars based on time in position
                    dcc.Graph(
                    id='hor-barchar',
                    figure=go.Figure(
                                     data = [
                                                go.Bar(
                                                    x =[t_0_5, t_6_10, t_11_15, t_16_20, t_21_25, t_26_30, t_31_35, t_36_40, t_41_45, t_46_50, t_51_55, t_56_60, t_61_more],
                                                    y =["< 5 mins ","5-10 mins ","10-15 mins ","15-20 min ","20-25 min ","25-30 mins ","30-35 mins ","35-40 mins ","40-45 min ","45-50 min ","50-55 mins ", "55-60 mins ", "> 60 mins "],
                                                    orientation = "h"
                                                    )],      
                                     layout = go.Layout(title='Trade Duration')))
                     ], className = "six columns"),
    
   html.Div([ # horizontal bars based perfromance by time in position
                    dcc.Graph(
                    id='hor-barchar_perf_by_time',
                    figure=go.Figure(
                                     data = [
                                                go.Bar(
                                                    x =[perf_t_0_10, perf_t_10_20, perf_t_20_30, perf_t_30_40, perf_t_40_50, perf_t_50_60, perf_t_60_more],
                                                    y =["< 10 mins ","10-20 mins ","20-30 mins ","30-40 min ","40-50 min ","50-60 mins ", "> 60 mins "],
                                                    orientation = "h"
                                                    )],      
                                     layout = go.Layout(title='Performance by Trade Duration')))
                     ], className = "six columns"),
            ], className = "row")
  
       
       
 
 
 
 
 
 
 
 
 
 
 ])
        

          
  
 
          

             











if __name__ == '__main__':
    app.run_server(debug=True)
