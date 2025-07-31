from flask import Flask, render_template,redirect,request,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from sqlalchemy import func
from flask import current_app as app #if you directly import app it will leads to circular error
from Application.db import db
from sqlalchemy.orm import selectinload
from datetime import datetime
from models.models import *
#route for user login
@app.route("/",methods=["GET","POST"])
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        this_user = User.query.filter_by(username=username).first()
        if this_user and check_password_hash(this_user.pass_hash, password):
            flash("Login successful!", "success") 
            if this_user.is_superUser :
                return redirect(url_for("adash"))
            else:
                return redirect(url_for("userdash",username=username))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html")
            
    return render_template("login.html")        
                
#route for user registration

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
            return render_template("register.html")

        flash("Registered! Please log in.", "success")
        return render_template("login.html")
       
    return render_template("register.html")
#route for adding parking lot via admin dashboard
@app.route("/addlot",methods=["GET","POST"])
def addlot():
    user=User.query.filter_by(is_superUser=True).first()
    if request.method =="POST":
        lot_name= request.form.get("lot_name")
        address= request.form.get("address")
        state=request.form.get("state")
        city=request.form.get("city")
        pincode=request.form.get("pincode")
        price=float(request.form.get("price"))
        maxspot=int(request.form.get("maxspot"))
        location=Location(loc_address=address,city=city,state=state,pincode=pincode)
        db.session.add(location)
        db.session.flush()
        
        
        parkingLot=ParkingLot( loc_id=location.loc_id ,lot_name=lot_name,max_spot =maxspot ,lot_price=price)
        db.session.add(parkingLot)
        db.session.commit()
        spots = [PSpot(lot_id=parkingLot.lot_id, spot_no=i + 1) for i in range(maxspot)]
        db.session.add_all(spots)
        db.session.commit()
        return redirect(url_for("adash"))
    return render_template("addlot.html")

# route for admin dashboard
@app.route("/adash", methods=["GET","POST"])
def adash():
    user=User.query.filter_by(is_superUser=True).first()
    
    
    lots = (
          db.session.query(ParkingLot)
          .options(selectinload(ParkingLot.spots))   
          .all()
      )
  
    for lot in lots:
          total = lot.max_spot 
          occ_cnt = sum(1 for s in lot.spots if not s.is_available)   
          lot.tspot = total
          lot.occ_cnt = occ_cnt
          lot.avcspot = total - occ_cnt
          
    return render_template("adash.html", user=user, lots=lots)
#admin edit lot
@app.route("/editlot/<int:lot_id>",methods=["GET","POST"])
def editlot(lot_id):
    lot=db.session.query(ParkingLot).filter_by(lot_id=lot_id).first()
    loc=db.session.query(Location).filter_by(loc_id=lot.loc_id).first()
    if request.method=="POST":
        lot.lot_name=request.form.get("lotname")
        lot.lot_price=float(request.form.get("price"))
        lot.max_spot=int(request.form.get("maxspot"))
        
        db.session.commit()
        return redirect(url_for("adash"))
    return render_template("editlot.html",lot=lot,loc=loc)
# admin delete lot
@app.route("/deletelot/<int:lot_id>",methods=["POST"])
def deletelot(lot_id):
    lot = db.session.query(ParkingLot).filter_by(lot_id=lot_id).first()
    spot=db.session.query(PSpot).filter_by(lot_id=lot_id,is_available=False).first()
    if spot:
        return redirect(url_for("adash"))
    
    db.session.delete(lot)
    db.session.commit()
        
    
        
    return redirect(url_for("adash"))
#route for spot detail
@app.route("/spotdetail/<int:spot_id>",methods=["GET","POST"])
def spotdetail(spot_id):
    if request.method == "GET":
     booklot = db.session.query(BookLot).filter_by(spot_id=spot_id).first()
     return render_template("spotdetail.html",booklot=booklot)
    return render_template("spotdeyail.html",spot_id=spot_id)
#route for view/delete parking spot:
@app.route("/viewdeletespot/<int:spot_id>",methods=["GET","POST"])
def viewdeletespot(spot_id):
    if request.method == "GET":
        spot= PSpot.query.filter_by(spot_id=spot_id).first()
        return render_template("viewdeletespot.html",spot=spot)
    return render_template("viewdeletespot.html",spot_id=spot_id)
    
#route fro admin summary
@app.route("/asummary",methods=["GET","POST"])
def asummary():
    #bar graph
    al = db.session.query(func.count(PSpot.spot_id)).filter(PSpot.is_available==True).scalar()
    ol = db.session.query(func.count(PSpot.spot_id)).filter(PSpot.is_available==False).scalar()
    total = al + ol

  
    labels = ["Total Spots"]
    available = [al]
    occupied = [ol]

    plt.bar(labels, available, label="Available", color="green")
    plt.bar(labels, occupied, bottom=available, label="Occupied", color="red")

    plt.ylabel("Number of Spots")
    plt.title("Summary on avilable and occupied parking Spots")
    plt.legend()
    plt.savefig("static/images/bar.png")
    plt.clf()
    
    
    revd = (
        db.session.query(PSpot.lot_id, func.sum(BookLot.total_amount))
       .join(PSpot, BookLot.spot_id == PSpot.spot_id)
       .group_by(PSpot.lot_id)
       .all()
    )
    
    if revd:
        lot_ids = [str(lot_id) for lot_id, _ in revd]
        rev = [total for _ , total in revd]
        plt.pie(rev,labels=lot_ids,autopct='%1.1f%%',startangle=140)
        plt.title("Revenue Generated by parking lot")
        plt.savefig("static/images/pie.png")
        plt.clf()
        
        
    
    plt.title("revenue generated by parking lots")
    plt.savefig("static/images/pie.png")
    plt.clf()
    #pie chart on revenu
    
    return render_template("asummary.html")

   
#route for user detail!!
@app.route("/viewusers", methods=["GET","POST"])
def viewusers():
    if request.method == "GET":
        users=db.session.query(User).filter_by(is_superUser=False).all()
        return render_template("viewusers.html",users=users)
    return render_template("viewusers.html")
#route for user dashboard
@app.route("/userdash/<string:username>",methods=["GET","POST"])
def userdash(username):
    u_id = User.query.filter_by(username=username).first().user_id
    booking=BookLot.query.filter_by(u_id=u_id).all()
    for b in booking:
        spot = PSpot.query.get(b.spot_id)
        lot = ParkingLot.query.get(spot.lot_id)
        b.lname=lot.lot_name
        if b.total_amount == 0:
            b.pstat = "Unpaid"
        else:
            b.pstat= "paid"
    
    lots = []
    city = ""
    if request.method == "POST":
        city = request.form.get("city").lower()
        ids = [loc.loc_id for loc in Location.query.filter_by(city=city).all()]
        lots = ParkingLot.query.filter(ParkingLot.loc_id.in_(ids)).all()

        for lot in lots:
            total = lot.max_spot
            occ_cnt = sum(1 for s in lot.spots if not s.is_available)
            lot.tspot = total
            lot.occ_cnt = occ_cnt
            lot.avcspot = total - occ_cnt
            
        return render_template("userdash.html", username=username, booking=booking, lots=lots, city=city)
    return render_template("userdash.html",username=username,booking=booking)
#route for update booking
@app.route("/updatebooking/<int:b_id>/<string:username>",methods=["GET","POST"])
def updatebooking(b_id,username):
    book = BookLot.query.filter_by(b_id=b_id).first()
    s=PSpot.query.get(book.spot_id)
    lot = ParkingLot.query.get(s.lot_id)  
    amt = lot.lot_price 
    book.end_time = datetime.now()
    d = book.end_time - book.start_time
    hr = d.total_seconds() / 3600
    t_amt=round(hr*amt,2)
    book.total_amount=t_amt
    if request.method == "POST":
        print("okokokokokok from updatebooking")
        s=PSpot.query.get(book.spot_id)
        lot = ParkingLot.query.get(s.lot_id)  
        amt = lot.lot_price 
        book.end_time = datetime.now()
        book.b_status = "Released"
        spot = PSpot.query.filter_by(spot_id=book.spot_id).first()
        if spot:
            spot.is_available = True
       
      
        d = book.end_time - book.start_time
        hr = d.total_seconds() / 3600
        t_amt=round(hr*amt,2)
        book.total_amount=t_amt
        db.session.commit()
       
        return redirect(url_for("userdash",username=username))
    return render_template("updatebooking.html",b=book,username=username)