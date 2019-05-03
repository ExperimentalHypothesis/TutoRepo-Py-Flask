from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route("/")
def home():
    return "home page"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "experimental"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "flask_form_test"

mysql = MySQL(app)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # get all the data from the form
        data = request.form

        # unpack them into single variables
        name = data["name"]
        surname = data["surname"]
        email = data["email"]
        password = data["pwd"]

        # make connection and put the data into database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (name, surname, email, password))
        mysql.connection.commit()
        cur.close()
        return "you have succesfully registered"

    return render_template("register.html")




@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # get all the data from the form
        data = request.form

        # unpack them into single variables
        email = data["email"]
        entered_password = data["pwd"]

        cur = mysql.connection.cursor() # make db connection
        stored_username = cur.execute("SELECT * FROM users WHERE email = %s", [email]) # find the stored email
        if stored_username: # if it is found
            row = cur.fetchone() # fetch the particular row where it sits
            stored_password = row[4]# and take its password
            if entered_password == stored_password: # check if matched and do the stuff.. 
                return "you are good to go"
            else:
                return "invalid password"
            cur.close()
        else:
            return "username does not exists"

    return render_template("login.html")











if __name__ == "__main__":
    app.run(debug=True)