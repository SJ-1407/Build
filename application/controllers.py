from flask import Flask, request,redirect,url_for,session
from flask import render_template
from flask import current_app as app
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from application.models import *
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route("/",methods=["GET","POST"])
def index():
    venue=Venue.query.all()
    if "username" in session and session["user_role"]=='admin':
         return (render_template("admin.html",user=session["username"],role=session["user_role"]))
    elif  "username" in session:

        return render_template("index.html", user = session["username"], signed=True,role=session["user_role"],venue=venue)
    else:
        return render_template("index.html", user = "", signed=False,venue=venue)



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
      if "username" in session:
         return(redirect(url_for("index")))
      error_message=request.args.get("error")  
      return (render_template("login.html",error_message=error_message))
    else:
     if request.method=="POST":
        user=User.query.filter_by(email=request.form["email"]).first()
   
        if user:
            if bcrypt.check_password_hash(user.password,request.form["password"]):
                session["username"]= user.username
                session["user_role"]=user.roles[0].name
                session["user_email"]=user.email
                return redirect(url_for('index'))
            else:
              error_message = "Invalid email or password."
              return render_template('login.html', error_message=error_message)
      



@app.route("/register",methods=["GET","POST"])
def register():
    if "username" in session:
         return(redirect(url_for("index")))
    if request.method=='GET':
     return (render_template("register_user.html"))
    elif request.method=='POST':
        username=request.form["username"]
        email = request.form["email"]
        if "@" in email:
            user=User.query.filter_by(email=request.form["email"]).first()
            password=request.form["password"]
            if user:
               error="Email already registered"
               return (render_template("register_user.html", error=error))
            else:
               if(password!=request.form["confirm_password"]):
                  error="Password does not match with Confirm Password"
                  return(render_template("register_user.html",error=error))
               password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
              
               role = Role.query.filter_by(id=request.form['options']).first()
               
               user=User(username=username,email=email,password=password_hash)
               user.roles.append(role)
               user.tickets=[]
               db.session.add(user)
               db.session.commit()
               session["username"]=username  #maintaining cookie
               session["user_role"]=role.name
               session["user_email"]=user.email
               return redirect(url_for("login"))
        else:
           error = "Enter a valid email"
           return render_template("register_user.html", error = error)
        
@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
        session.pop("user_role")
        session.pop("user_email")
    return redirect("/")



