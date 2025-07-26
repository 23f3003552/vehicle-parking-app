from extensions import db

class BookLot(db.Model):
    __tablename__ = "book_lot"

    b_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    spot_id = db.Column(db.Integer, db.ForeignKey("pspots.spot_id"), nullable=False)
    u_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    start_time = db.Column(db.String(120), nullable=False)
    end_time = db.Column(db.String(120), nullable=False)
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
    p_time = db.Column(db.String(120), nullable=False)
    p_status = db.Column(db.Boolean, default=False)

    # Relationships
    booking = db.relationship("BookLot", backref="payments")
    user = db.relationship("User", backref="payments")

    def __repr__(self):
        return f"<Payment {self.p_id} booking={self.b_id}>"
