from flask import Flask, render_template, request
import mysql.connector
import re
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)


def connect_db():
    try:
        return mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12767924",
            password="Y6smNHwcUU",
            database="sql12767924"
        )
    except mysql.connector.Error as err:
        print("Database Connection Error:", err)
        return None


@app.route("/login", methods=["POST", "GET"])
def login():
    msg = ""
    if request.method == "POST" and "Username" in request.form and "Password" in request.form:
        Username = request.form["Username"]
        Password = request.form["Password"]


        mydb = connect_db()
        if not mydb:
            return render_template("error.html", msg="Database Connection Failed")


        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LoginDetails WHERE Username=%s", (Username,))
        account = mycursor.fetchone()


        if account and check_password_hash(account[2], Password):
            id = account[0]
            name = account[1]
            msg = "Logged in Successfully!"
            return render_template("login.html", msg=msg, id=id, name=name)
        else:
            msg = "Incorrect Credentials. Please check again"
    
    return render_template("login.html", msg=msg)


@app.route("/logout")
def logout():
    msg = "Logged out successfully"
    return render_template("login.html", msg=msg, name="", id="")


@app.route("/register", methods=["POST", "GET"])
def register():
    msg = ''
    if request.method == "POST" and "Username" in request.form and "Email" in request.form and "Password" in request.form:
        Username = request.form["Username"]
        Password = request.form["Password"]
        Email = request.form["Email"]


        mydb = connect_db()
        if not mydb:
            return render_template("error.html", msg="Database Connection Failed")


        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM LoginDetails WHERE Username=%s AND Email=%s", (Username, Email))
        account = mycursor.fetchone()


        if account:
            msg = "Already Exists"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            msg = "Invalid Email format"
        elif not re.match(r'[A-Za-z0-9]+', Username):
            msg = "Username should only contain letters and numbers"
        elif not Password or not Username or not Email:
            msg = "Kindly fill details"
        else:
            hashed_password = generate_password_hash(Password)
            mycursor.execute("INSERT INTO LoginDetails (Username, Email, Password) VALUES (%s, %s, %s)", (Username, Email, hashed_password))
            mydb.commit()
            msg = "Registration Successful"
            return render_template("welcome.html", name=Username, msg=msg)
    
    return render_template("register.html", msg=msg)


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)





