from flask import Flask, request,redirect,url_for,session,flash
from flask import render_template
from flask import current_app as app
from application.database import db
from flask_sqlalchemy import SQLAlchemy
from application.models import *
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)



@app.route("/",methods=["GET","POST"])
def index():
    products = Product.query.all()  # Fetch all products and their associated images
    return render_template('index.html', products=products)



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
               #user.products=[]
               user.roles.append(role)
               
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

'''@app.route("/buy/<int:product_id>", methods=["GET", "POST"])
def buy(product_id):
    product = Product.query.get_or_404(product_id)  # Get the product or return 404 if not found
    if request.method == "GET":
        return render_template("buy_product.html", product=product)
    elif request.method == "POST":
        if 'user_email' not in session:
            flash("You need to log in to buy products.", "warning")
            return redirect(url_for('login'))  # Redirect to login page
        else:
           print(session["user_email"])

        user = User.query.filter_by(email=session['user_email']).first() # Retrieve user from session
        print(user)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('index'))  # Redirect to home page

        # Assuming 'products' is a relationship field on the User model
        u_p=user_product(user_id=user.id,product_id=product_id)
        print(u_p)
        db.session.add(u_p)
          # Add the product to the user's collection of bought products
        db.session.commit()  # Commit the transaction to the database

        flash('Purchase confirmed for ' + product.name, 'success')
        return redirect(url_for('index'))  # Redirect to the home page or confirmation page
    return render_template("buy_product.html", product=product)'''

@app.route("/buy/<int:product_id>", methods=["GET", "POST"])
def buy(product_id):
    product = Product.query.get_or_404(product_id)  # Get the product or return 404 if not found
    if request.method == "GET":
        return render_template("buy_product.html", product=product)
    elif request.method == "POST":
        if 'user_email' not in session:
            flash("You need to log in to buy products.", "warning")
            return redirect(url_for('login'))  # Redirect to login page

        user = User.query.filter_by(email=session['user_email']).first()  # Retrieve user from session
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('index'))  # Redirect to home page

        # Adding product to the user's list of products using the established relationship
       
        flash('Purchase confirmed for ' + product.name, 'success') 
        user.products.append(product)
        # Add the product to the user's collection of bought products
        db.session.commit()  # Commit the transaction to the database
          
        

        return redirect(url_for('index'))  # Redirect to the home page or confirmation page

    return render_template("buy_product.html", product=product)

'''@app.route("/cart/<int:product_id>", methods=["GET", "POST"])
def buy(product_id):
    product = Product.query.get_or_404(product_id)  # Get the product or return 404 if not found
    if request.method == "GET":
        return render_template("cart_product.html", product=product)
    elif request.method == "POST":
        if 'user_email' not in session:
            flash("You need to log in to buy products.", "warning")
            return redirect(url_for('login'))  # Redirect to login page

        user = User.query.filter_by(email=session['user_email']).first()  # Retrieve user from session
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('index'))  # Redirect to home page

        # Adding product to the user's list of products using the established relationship
       
        flash('Purchase confirmed for ' + product.name, 'success') 
        user.products.append(product)
        # Add the product to the user's collection of bought products
        db.session.commit()  # Commit the transaction to the database
          
        

        return redirect(url_for('index'))  # Redirect to the home page or confirmation page

    return render_template("buy_product.html", product=product)'''


@app.route('/orders')
def order_history():
    if 'user_email' not in session:
        flash("You need to log in to view order history.", "warning")
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user_email']).first()
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('index'))

    products = user.products  # Assuming this retrieves the list of ordered products
    return render_template('order_history.html', products=products)
