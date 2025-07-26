from extensions import db
from sqlalchemy import UniqueConstraint

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
    loc_id    = db.Column(db.Integer, db.ForeignKey("locations.loc_id"), nullable=True)
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




# parking lot table
#def PLotTable(cur):
#    cur.execute("""
#        CREATE TABLE IF NOT EXISTS ParkingLots (
#            lot_id INTEGER PRIMARY KEY AUTOINCREMENT,
#            lot_name TEXT NOT NULL,
#            loc_id INTEGER,
#            max_spot INTEGER,
#            lot_price REAL NOT NULL,
#            FOREIGN KEY(loc_id) REFERENCES Locations(loc_id)
#        );
#    """)
#
## parking spot table
#def PSportTable(cur):
#    cur.execute("""
#        CREATE TABLE IF NOT EXISTS PSpots (
#            spot_id INTEGER PRIMARY KEY,
#            lot_id INTEGER,
#            sport_no INTEGER UNIQUE,
#            is_avilabe BOOLEAN DEFAULT 1,
#            FOREIGN KEY(lot_id) REFERENCES ParkingLots(lot_id)
#        );
#    """)
#
## location table
#def LocTable(cur):
#    cur.execute("""
#        CREATE TABLE IF NOT EXISTS Locations (
#            loc_id INTEGER PRIMARY KEY,
#            loc_address TEXT NOT NULL,
#            city TEXT NOT NULL,
#            state TEXT NOT NULL,
#            pincode TEXT NOT NULL
#        );
#    """)
#