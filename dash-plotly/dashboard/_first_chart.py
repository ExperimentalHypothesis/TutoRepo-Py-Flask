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

host="localhost"
user="root"
password="password"
db="trading"
table=" "

 #########  getting data for equity, profitloss, drawdowns, rupun from mysql #########  
def get_data_for_equity(host, user, password, db, table):
    con = pymysql.connect(host=host, user=user, password=password, db=db)
    cur = con.cursor()

    cur.execute("SELECT profitloss from iut")
    pl = cur.fetchall()

    cur.execute("SELECT running_profitloss from iut")
    run_pl = cur.fetchall()

    cur.execute("SELECT runup from iut")
    ru = cur.fetchall()

    cur.execute("SELECT drawdown from iut")
    dd = cur.fetchall()

    return pl, run_pl, ru, dd

 #########  clearing the data to make i ready for plotting #########  
def clear_data_for_equity():
    pl, run_pl, ru, dd = get_data_for_equity()
          
    x=0
    indexes = []
    profitloss = []
    for i in pl:
        profitloss.append(i[0]) 
        x +=1
        indexes.append(x)
       
    running_profitloss = []
    for i in run_pl:
        running_profitloss.append(i[0])

    runup = []
    for i in ru:
        runup.append(i[0])

    drawdown = []
    for i in dd:
        drawdown.append(i[0])

    return indexes, profitloss, running_profitloss, runup, drawdown

 #########  plotting the data #########  
def make_first_chart():
    indexes, profitloss, running_profitloss, runup, drawdown = clear_data_for_equity()

    equity =  go.Scatter(
        x = indexes,
        y = running_profitloss, 
        name = 'Equity',
        mode = "lines", 
        line = dict(color = ('rgb(0, 0, 0)'), width = 3)
    )

    profitloss = go.Bar( 
        x = indexes,
        y = profitloss,
        name = 'Profitloss',
        opacity = 0.6,
        marker = dict(color='rgb(0, 0, 255)')
    )

    runup = go.Bar(
        x = indexes,
        y = runup,
        name='Runup',
        opacity = 0.7,
        marker=dict(color='rgb(0, 255, 0)')
    )

    drawdown = go.Bar(
        x = indexes,
        y = drawdown,
        name='Drawdown',
        opacity = 0.7,
        marker=dict(color='rgb(255, 0, 0)')
    )

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

    data = [equity, profitloss, runup, drawdown]
    layout = layout

    return data, layout


app = dash.Dash(__name__)

data, layout = make_first_chart()

app.layout = dcc.Graph(
    id = "first chart",
    figure = go.Figure(data = data, layout = layout))


if __name__ == "__main__":
    app.run_server(debug=True)


