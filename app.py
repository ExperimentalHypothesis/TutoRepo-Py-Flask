from flask import Flask, render_template
from data import articles 
import pymysql

app = Flask(__name__)

# setting a variable var_articles which will hold all the list of dict from the foo articles
var_articles = articles()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/articles')
def articles():
    return render_template("articles.html", articles = var_articles) # passing data alongisde, which are in the variable var?articles

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


# setting up database
host = "localhost"
user = "root"
password = "emeraldincubus"
db = "trading_discretionary"

def select_from_db():
    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * from intraday")
    result = cur.fetchall()
    return result

@app.route("/database")
def index():
    def query():
        elements = select_from_db()
        return elements
    res = query()
    return render_template("database.html", result=res)

# not working correctly
@app.route('/article/<id>/')
def article():
    return render_template("articles.html", id = id) # passing data alongisde, which are in the variable var?articles

if __name__ == '__main__':
    app.run(debug=True)


#@app_flask.route('/plotly_dashboard') 
#def render_dashboard():
#    return flask.redirect('/pathname')