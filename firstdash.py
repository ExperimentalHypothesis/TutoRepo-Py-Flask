import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, render_template
import pymysql
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas

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

# enumerating trades
numbered_pl = list(enumerate(pl, 1))

# spliting trade resuls and ids
pl_trade_id = []
pl_trade_result = []
for i in numbered_pl:
    pl_trade_id.append(i[0])
    pl_trade_result.append(i[1])

import random
runups = []
drawdowns = []
for i in pl_trade_result:
    runups.append(random.randint(0,190))
    drawdowns.append(random.randint(-200,0))
    
       
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
       


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app.css.append_css({"external_url" : "https://codepen.io/amyoshino/pen/jzXypZ.css"})


app = dash.Dash(__name__ ) # external_stylesheets=external_stylesheets

app.layout = html.Div(children=[
    
    #  --------------------------------------------------- first row: headings ----------------------------------------------------
    html.Div(
    [ 
        html.H3(children='web data visualisation test in python', style={"text-align":"center"}),
        html.H5(children='sample of plotting data from a running SC AOS study using realtime updates', style={"text-align":"center"}),
    ],  className = "row"),

    #  --------------------------------------------------- second row: equity chart --------------------------------------------------
    html.Div(
    [
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
                                                go.Pie(labels=['Desktop', 'Mobile', 'Tablet'],
                                                values=['42344', '1864', '2390'])
                                            ],      
                                     layout = go.Layout(title='Device Usage')))
                        ], className = "four columns")
         ], className = "row")

    #  --------------------------------------------------- fourth row: barchart and piechard ---------------------------------------------------




     ])
   

          
          
       

             






       
    ##this is the second graph
    #    html.Div(
    #        dcc.Graph(
    #        id='equity',
    #        figure={
    #                'data': [
    #                            {
    #                                'labels': ['1st', '2nd', '3rd', '4th', '5th'],
    #                                'values': [38, 27, 18, 10, 7],
    #                                'type': 'pie',
    #                            }, 

    #                            #{'x': pl_trade_id, 'y': pl_trade_result, 'type': 'bar', 'name': 'Profit Loss'}, 
    #                            #{'x': pl_trade_id, 'y': runups, 'type': 'bar', 'name': 'Runup'},
    #                            #{'x': pl_trade_id, 'y': drawdowns, 'type': 'bar', 'name': 'Drawdown'}
    #                        ], 
    #                'layout': {'title': 'Equity'}
    #               }
    #            ), className = "six columns")], className = "row"),    

    #    html.Div([ 
    #        html.Div(
    #         [ 
    #            dcc.Checklist(
    #                        options=[ {'label': 'Runup', 'value': 'runup'}, {'label': 'Drawdown', 'value': 'Drawdown'}, ],
    #                        values=['MTL', 'SF'],
    #                        labelStyle={'display': 'inline-block'}
    #                       ), 
    #             ], className = "Six columns",),
            

    #     html.Div(
    #         [ 
    #            dcc.Checklist(
    #                        options=[ {'label': 'Runup', 'value': 'runup'}, {'label': 'Drawdown', 'value': 'Drawdown'}, ],
    #                        values=['MTL', 'SF'],
    #                        labelStyle={'display': 'inline-block'}
    #                       ), 
    #             ], className = "Six columns",)], className = "row"),
    #    ],)


# toto je piechart
#app.layout = html.Div(children=
#            dcc.Graph(id='device_usage',
#                           figure=go.Figure(
#                               data=[go.Pie(labels=['Desktop', 'Mobile', 'Tablet'],
#                                            values=['42344', '1864', '2390'])
#                                            ],
#                               layout=go.Layout(
#                                   title='Device Usage')
#                           )),
#            )














if __name__ == '__main__':
    app.run_server(debug=True)
