from flask import Flask, redirect, render_template, request, session,url_for
from werkzeug.security import generate_password_hash , check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="@123456789#neha#12345789@"

#routes
@app.route('/',methods=['GET','POST'])
def login():
    #if "username" in session:
     #   return redirect(url_for('dashboard'))
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        name=request.form.get('name')
        return render_template("adashboard.html")
    
@app.route("/register")
def register():
    return render_template("register.html")
if __name__ in "__main__":
    app.run(debug=True)