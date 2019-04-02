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
    opacity = 0.7,
    marker=dict(color='rgb(0, 255, 0)')
)

drawdown = go.Bar(
    x = pl_trade_id,
    y = drawdowns,
    name='Drawdowns',
    opacity = 0.7,
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


















  #{'x': pl_trade_id, 'y': pl_trade_result, 'type': 'bar', 'name': 'Profit Loss'}, 

# data for table
table_rows = ['Closed Trades Result', 'Closed Trades Profit', 'Closed Trades Loss', 'Profit Factor', " ",
              'Equity Peak', 'Maximum Runup', 'Maximum Drawdown', " ",
             "Total Trades", "Long Trades", "Short Trades", "Winning Trades", "Loosing Trades", "Percet Profitable", " ",
             "Average Trade Result", "Average Winning Trade", "Average Loosing Trade", "Largest Winning Trade", "Largest Loosing Trade", " ",
             "Average Time in Trades", "Average Time in Winning Trade", "Average Time in Loosing Trade","Longest Held Winning Trade", "Longest Held Loosing Trade", " ", 
             "Average Qty Per Trade", "Largest Trade Qty" ]

nr_of_items = len(table_rows)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__ ) # external_stylesheets=external_stylesheets
app.css.append_css({"external_url" : "https://codepen.io/amyoshino/pen/jzXypZ.css"})
app.title = "AOS Dashboard"

app.layout = html.Div(children=[
    
    #  --------------------------------------------------- 0 row: headings ----------------------------------------------------
    html.Div(
    [ 
        html.H3(children='web data visualisation test in python', style={"text-align":"center"}),
        html.H5(children='sample of plotting data from a running SC AOS study using realtime updates', style={"text-align":"center"}),
    ],  className = "row"),

    #  --------------------------------------------------- 1 row: equity chart using DASH --------------------------------------------------
    #html.Div([
    #        dcc.Graph(
    #        id='equity',
    #        figure={
    #                'data': [
    #                            {'x': cum_pl_trade_id, 'y': cum_pl_result, 'type': 'line', 'name': 'Equity'}, 
    #                            {'x': pl_trade_id, 'y': pl_trade_result, 'type': 'bar', 'name': 'Profit Loss'}, 
    #                            {'x': pl_trade_id, 'y': runups, 'type': 'bar', 'name': 'Runup'},
    #                            {'x': pl_trade_id, 'y': drawdowns, 'type': 'bar', 'name': 'Drawdown'}
    #                        ], 
    #                'layout': {'title': 'Equity, PL'}
    #               }
    #          )], className = "row"),

#  --------------------------------------------------- 1 row alternative: equity chart using PLOTY GO.SCATTER --------------------------------------------------

    html.Div([
        dcc.Graph(
            id='equity',
            figure=go.Figure(
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
                id='dailyperf',
                figure={
                        'data': [
                                    {'x': daily_dt, 'y': daily_pl_sum, 'type': 'bar', 'name': 'Daily Performance'}, 
                                ], 
                        'layout': {'title': 'Daily Performance', "color": '#7FDBFF' }
                        }
                    )
        ],  className = "nine columns"),

        html.Div([# pie win/loss ratio 
                    dcc.Graph(
                    id='piechart',
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
                            ], className = "six columns"),      
   
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
                      )], className = "six columns"),      
             ], className = "row"),

 #    --------------------------------------------------- 5 row: daily profitloss ---------------------------------------------------
 html.Div([
     dcc.Graph(
            id="donut-symbol-percentage",
            figure={
                        "data": [
                                    {
                                            "values": [16, 15, 12, 6, 5, 4, 42],
                                            "labels": [
                                                        "US",
                                                        "China",
                                                        "European Union",
                                                        "Russian Federation",
                                                        "Brazil",
                                                        "India",
                                                        "Rest of World"
                                                        ],
                                            "domain": {"x": [0, .48]},
                                            "name": "GHG Emissions",
                                            "hoverinfo":"label+percent+name",
                                            "hole": .4,
                                            "type": "pie"
                                        }
                                 ],
                        "layout": {"title": "Distribution by Instruments"}
                    }
            )
            ],)
    ],)

          
    
    #html.Div([  
    
          #html.Div([ # pie chart
          #          dcc.Graph(
          #          id='piechart',
          #          figure=go.Figure(
          #                           data = [
          #                                      go.Pie(labels=['NQ', 'YM', 'RTY', 'ES'],
          #                                      values=[nq, ym, rty, es])
          #                                  ],      
          #                           layout = go.Layout(title='Distribution by Instrument')))
          #              ], className = "four columns")
                      #], className = "row"),

 
            #html.Div([ # horizontal bars based on time in position
            #        dcc.Graph(
            #        id='hor-barchar',
            #        figure=go.Figure(
            #                         data = [
            #                                    go.Bar(
            #                                        x =[t_0_10, t_11_20, t_21_30, t_31_40, t_41_50, t_51_60, t_61_more],
            #                                        y =["les than 10","10 - 20","20 - 30","30 - 40","40 - 50","50 - 60", "60 and more"],
            #                                        orientation = "h"
            #                                        )],      
            #                         layout = go.Layout(title='Time in possition')))
            #         ], className = "four columns"),
       

             











if __name__ == '__main__':
    app.run_server(debug=True)
