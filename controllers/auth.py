from flask import Flask, render_template,redirect,request,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask import current_app as app #if you directly import app it will leads to circular error
from Application.db import db
from models.models import User

@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        passwd = request.form.get("passward")
        this_user = User.query.filter_by(username=username).first()
        if this_user and check_password_hash(this_user.pass_hash, passwd):
            if this_user.is_superUser :
                return render_template("/adash")
            else:
                return render_template("/udash")
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html")
            
    return render_template("login.html")        
                

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name = request.form.get("name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not all([name, username, email, password]):
            flash("All fields are required", "danger")
            return render_template("register.html")
        
        pass_hash = generate_password_hash(password)

        user = User(name=name, username=username, u_email =email, pass_hash=pass_hash)

        try:
         db.session.add(user)
         db.session.commit()
        except IntegrityError:
            db.session.rollback()
        flash("Username or email already exists", "warning")
        return redirect(url_for("/register"))

        flash("Registered! Please log in.", "success")
        return render_template("/login")
       
    return render_template("/register")



"""

from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask import current_app as app #if you directly import app it will leads to circular error
from Application.db import db
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

auth = Blueprint("auth", __name__, static_folder="static", template_folder="templates")


@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    passwd = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.pass_hash, passwd):
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth.login"))

    session["user_id "] = user.user_id 
    session["username"] = user.username
    session["is_superUser"] = user.is_superUser

    flash("Logged in!", "success")
    return redirect(url_for("admin.dashboard") if user.is_superUser else url_for("user.dashboard"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not all([name, username, email, password]):
        flash("All fields are required", "danger")
        return redirect(url_for("auth.register"))

    pass_hash = generate_password_hash(password)

    user = User(name=name, username=username, u_email =email, pass_hash=pass_hash)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Username or email already exists", "warning")
        return redirect(url_for("auth.register"))

    flash("Registered! Please log in.", "success")
    return redirect(url_for("auth.login"))

"""
"""
from flask import Blueprint, render_template,request,redirect,session,url_for, flash
from extensions import db
from models import User
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
auth = Blueprint("auth", __name__,static_folder="static",template_folder="templates")

@auth.route("/",methods=['GET','POST'])
@auth.route("/login",methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    username=request.form.get("username")
    passwd=request.form.get("password")
    User = User.query.filter_by(username=username).first()
    if not User or not check_password_hash(User.password_hash, passwd):
        flash("Invalid username or password", "danger")
        return redirect(url_for("auth.login"))
    session["user_id"] = User.id
    session["username"] = User.username
    session["is_superuser"] = User.is_superuser
    if User.is_superuser:
        flash("Logged in!", "success")
        return redirect(url_for("admin.dashboard"))
    else:
        flash("Logged in!", "success")
        return redirect(url_for("user.dashboard"))
    #flash("Logged in!", "success")
   
@auth.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
        
    name=request.form.get('name')
    username=request.form.get('username')
    email=request.form.get('email')
    password=request.form.get('password')
    pass_hash = generate_password_hash(password)
    if not all([name, username, email, password]):
        flash("All fields are required", "danger")
        return redirect(url_for("auth.register"))
    User=User(name=name,username=username, u_email=email,pass_hash=pass_hash)
    try:
        db.session.add(User)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Username or email already exists", "warning")
        return redirect(url_for("auth.register"))

    flash("Registered! Please log in.", "success")
    return redirect(url_for("auth.login"))

"""