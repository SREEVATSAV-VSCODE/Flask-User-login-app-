
from flask import Flask, render_template, request, mysql.connector
app=Flask(__name__)

@app.route("/login",methods=["POST","GET"])


def login():
 msg=""
 if request.method=="POST"and "Username" in request.form and "Password" in request.form:
    Username=request.form["Username"]
    Password=request.form["Password"]
    mydb=mysql.connector.connect(
    host="sql12.freesqldatabase.com",
    user="sql12766698",
    password="dZBHbB679p",
    database="sql12766698")
    mycursor=mydb.cursor()
    account=mycursor.execute("SELECT * FROM LoginDetails where name=%s and password=%s",(Username,Password))
    account=mycursor.fetchone()
    if account:
        id=account[0]
        name=account[1]
        msg="Logged in Successfully!"
        return render_template("login.html",msg=msg,id=id,name=name)
    else:
        msg="Incorrect Credentials. Plase check again"
        return render_template("login.html",msg=msg)
 else:
    return render_template("login.html")
 
@app.route("/logout")
def logout():
      msg=""
      id=""
      name=""
      msg="Logged out successfully"
      return render_template("login.html",msg=msg,name=name,id=id)
