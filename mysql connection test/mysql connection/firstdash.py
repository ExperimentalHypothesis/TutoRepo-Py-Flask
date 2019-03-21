import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask, render_template
import pymysql
import plotly

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

host = "localhost"
user = "root"
password = "emeraldincubus"
db = "trading_discretionary"

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


app = dash.Dash(__name__ ) # external_stylesheets=external_stylesheets

app.css.append_css({"external_url" : "https://codepen.io/amyoshino/pen/jzXypZ.css"})


app.layout = html.Div(children=[
    html.Div([ 
       html.H3(children='web data visualisation test in python', style={"text-align":"center"}),
       html.H5(children='sample of plotting profit loss and cumulative profit from a running SC AOS study using realtime updates', style={"text-align":"center"}),
        ], className = "row"),
      html.Div(),
    html.Div([
        html.Div(dcc.Graph(
            id='profitloss',
            figure={
                    'data': [
                                {'x': pl_trade_id, 'y': pl_trade_result, 'type': 'bar', 'name': 'Profit Loss'}, 
                            ], 
                    'layout': {'title': 'Profit Loss'}
                   }
              ), className = "six columns"),

        html.Div(dcc.Graph(
            id='equity',
            figure={
                    'data': [
                                {'x': cum_pl_trade_id, 'y': cum_pl_result, 'type': 'line', 'name': 'Equity'}, 
                            ], 
                    'layout': {'title': 'Equity'}
                   }
                ), className = "six columns")],
            className = "row"),  
        
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
