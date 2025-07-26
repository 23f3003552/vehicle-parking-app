#models for parking app
from Application.db import db
from sqlalchemy import UniqueConstraint

class User(db.Model):
    __tablename__ = "users"   # use lowercase, conventional

    user_id      = db.Column(db.Integer, primary_key=True)
    username     = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash    = db.Column(db.String(255), nullable=False)
    name         = db.Column(db.String(120), nullable=False)
    u_email      = db.Column(db.String(255), unique=True)
    is_superUser = db.Column(db.Boolean, nullable=False, default=False)

    # Optional but recommended:
    created_at   = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    updated_at   = db.Column(db.DateTime, server_default=db.func.now(),
                             onupdate=db.func.now(), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


class Location(db.Model):
    __tablename__ = "locations"

    loc_id      = db.Column(db.Integer, primary_key=True)
    loc_address = db.Column(db.String(255), nullable=False)
    city        = db.Column(db.String(120), nullable=False)
    state       = db.Column(db.String(120), nullable=False)
    pincode     = db.Column(db.String(20), nullable=False)

    # Relationship with ParkingLots
    parking_lots = db.relationship("ParkingLot", back_populates="location", cascade="all, delete")

    def __repr__(self):
        return f"<Location {self.city}, {self.state}>"


class ParkingLot(db.Model):
    __tablename__ = "parking_lots"

    lot_id    = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_name  = db.Column(db.String(120), nullable=False)
    loc_id    = db.Column(db.Integer, db.ForeignKey("locations.loc_id"), nullable=False)
    max_spot  = db.Column(db.Integer)
    lot_price = db.Column(db.Float, nullable=False)

    # Relationship with Location and PSpots
    location = db.relationship("Location", back_populates="parking_lots")
    spots = db.relationship("PSpot", back_populates="lot", cascade="all, delete")

    def __repr__(self):
        return f"<ParkingLot {self.lot_name}>"


class PSpot(db.Model):
    __tablename__ = "pspots"
    __table_args__ = (UniqueConstraint("lot_id", "spot_no", name="uq_lot_spot"),)

    spot_id     = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lot_id      = db.Column(db.Integer, db.ForeignKey("parking_lots.lot_id"), nullable=False)
    spot_no     = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True, nullable=False)

    # Relationship with ParkingLot
    lot = db.relationship("ParkingLot", back_populates="spots")

    def __repr__(self):
        return f"<PSpot {self.spot_no} in Lot {self.lot_id}>"

class BookLot(db.Model):
    __tablename__ = "book_lot"
    
    b_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    veh_no= db.Column(db.String(32),nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey("pspots.spot_id"), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    b_status = db.Column(db.String(50), default="booked")

    # Relationships
    user = db.relationship("User", backref="bookings")
    spot = db.relationship("PSpot", backref="bookings")

    def __repr__(self):
        return f"<BookLot {self.b_id} user={self.u_id} spot={self.spot_id}>"


class Payment(db.Model):
    __tablename__ = "payment"

    p_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b_id = db.Column(db.Integer, db.ForeignKey("book_lot.b_id"), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    p_time = db.Column(db.DateTime(timezone=True), nullable=False)
    p_status = db.Column(db.Boolean, default=False)

    # Relationships
    booking = db.relationship("BookLot", backref="payments")
    user = db.relationship("User", backref="payments")

    def __repr__(self):
        return f"<Payment {self.p_id} booking={self.b_id}>"
