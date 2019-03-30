import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, render_template
import pymysql
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas


################## getting data from mysql for profitloss ---> for making histogram  ##################  
def select_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT profit_loss from iml_aos")
    result = cur.fetchall()
    return result

pl_tuple =  select_pl()

# clearing out the tuple data returned from db
pl = []
for i in pl_tuple:
    pl.append(i[0]) 

numbered_pl = list(enumerate(pl, 1))

# split trade resuls and ids
pl_trade_id = []
pl_trade_result = []
for i in numbered_pl:
   
    pl_trade_id.append(i[0])
    pl_trade_result.append(i[1])

 #imitating random numbers as runups and drawdowns (because i dont have these in database)
import random
runups = []
drawdowns = []
for i in pl_trade_result:
    runups.append(random.randint(0,190))
    drawdowns.append(random.randint(-200,0))
    




  
################## getting the cummulative profitloss ---> for making equity chart ##################
def select_cum_pl():
    con = pymysql.connect(host="vmi239120.contaboserver.net", user="nirvikalpa", password="password", db="trading_automatic")
    cur = con.cursor()
    cur.execute("SELECT cummulative_pl from iml_aos")
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
       
    



################## getting % nr of trades for each symbol -> for making  piechart ##################
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



# -------------------------> here starts the dashapp <-------------------- #

app = dash.Dash(__name__ ) # external_stylesheets=external_stylesheets
app.css.append_css({"external_url" : "https://codepen.io/amyoshino/pen/jzXypZ.css"})
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.layout = html.Div(children=[
    
    #  --------------------------------------------------- first row: headings ----------------------------------------------------
    html.Div(
    [ 
        html.H3(children='web data visualisation test in python', style={"text-align":"center"}),
        html.H5(children='sample of plotting data from a running SC AOS study using realtime updates', style={"text-align":"center"}),
    ],  className = "row"),

    #  --------------------------------------------------- second row: equity chart --------------------------------------------------
    html.Div([
            dcc.Graph(
            id='equity',
            figure={
                    'data': [
                                {'x': cum_pl_trade_id, 'y': cum_pl_result, 'type': 'line', 'name': 'Equity'}, 
                            ], 
                    'layout': {'title': 'Equity'}
                   }
              )
    ], className = "row"),

    # ---------------------------------------------------  third row: barchart and piechard ---------------------------------------------------
     html.Div([  
         html.Div([ # bar chart
                    dcc.Graph( 
                    id='profitloss',
                    figure={
                            'data': [
                                        {'x': pl_trade_id, 'y': pl_trade_result, 'type': 'bar', 'name': 'Equity'}, 
                                        {'x': pl_trade_id, 'y': runups, 'type': 'bar', 'name': 'Runup'},
                                        {'x': pl_trade_id, 'y': drawdowns, 'type': 'bar', 'name': 'Drawdown'}
                                    ], 
                            'layout': {'title': 'Profit Loss'}
                            }
                        )], className = "eight columns"),
    
     html.Div([ # pie chart
                    dcc.Graph(
                    id='piechart',
                    figure=go.Figure(
                                     data = [
                                                go.Pie(labels=['YM', 'NQ', 'ES', "RTY"],
                                                values=[ym, nq, es, rty])
                                            ],      
                                     layout = go.Layout(title='Instruments')))
                        ], className = "four columns")
         ], className = "row")


     ])
   

if __name__ == '__main__':
    app.run_server(debug=True)