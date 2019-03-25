import dash
import dash_table
import pandas as pd
import pymysql

con = pymysql.connect(host=" ", 
                      user=" ", 
                      password=" ", 
                      db=" ", 
                      cursorclass=pymysql.cursors.DictCursor)

sql = "SELECT * FROM IML_AOS"
df = pd.read_sql(sql, con)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id='table',
    columns=[{"column": i, "id": i} for i in df.columns],
    data=df.to_dict("row"),
)

if __name__ == '__main__':
    app.run_server(debug=True)