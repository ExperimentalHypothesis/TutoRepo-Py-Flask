from flask import Flask, render_template
import pymysql

app = Flask(__name__)

host = "localhost"
user = "root"
password = "------"
db = "xyz"

def select_from_db():
    con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
    cur = con.cursor()
    cur.execute("SELECT * from intraday")
    result = cur.fetchall()
    return result

@app.route("/")
def index():
    def query():
        elements = select_from_db()
        return elements
    res = query()
    return render_template("database.html", result=res)


if __name__ == "__main__":
    app.run(debug=True)
