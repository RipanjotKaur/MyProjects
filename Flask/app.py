from flask import Flask, render_template, request, redirect, session
from db import Database

app = Flask(__name__)
app.secret_key = "mysecretkey"  ###this for using/setup session
database = Database()


@app.route("/") #we can consider it as url, url ch slash marange tn thale vala index function execute ho jauga
def index ():
    return render_template('login.html') ##import render temp at top, this is use to integrate html file with flask
    # return "<h1> Hello Ripanjot </h1> "
##jo v website te show ho reha oh client nu show ho reha, HTML/CSS files v client nu show kron laii bniya, so assi css /html add kr skde flask ch

@app.route("/register")
def register():
    return render_template("register.html")

##client gives its data to html(at frontend) that data will go to app.py(Flask) >>> then ceck on database

@app.route("/perform_registration", methods = ["post"]) #telling it HTML to data post toh aa reha
def perform_registration():
    ##jdo user Register ch click kruga, eh function call hau bcz oh register alle form code ch action ch es functio/route da link aa 
    name = request.form.get("user_name")
    email = request.form.get("user_email")
    password = request.form.get("user_password")

    response = database.insert(name, email, password)
    if response:
        return render_template("login.html", message = "Registration Successfull.Kindly login to proceed")
    else:
        return render_template("register.html", message = "Email already exists")

@app.route("/perform_login", methods = ["post"])
def perform_login():
    email = request.form.get("user_email")
    password = request.form.get("user_password")
    response = database.search(email, password)
    if response:
        session["logged_in"] = 1 ###eh session vala esli laii, to be safe from hacking, je kise ne login kitta, logged in 1 bn gya te pta lg gya k kise ne credentials nal sahi login

        return redirect ("/profile")
    else:
        return"Wrong Credentials"
@app.route("/profile")
def profile():
    if session["logged_in"] == 1:
        return render_template ("profile.html")
    else:
        return redirect("/")

## Request is for receiving daat of htlm
app.run(debug=True) ##to run without click run again and again


