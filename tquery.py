from Application.db import db
from app import create_app
from models.models import *
from sqlalchemy import func
from sqlalchemy.orm import selectinload 
from sqlalchemy.exc import IntegrityError

app = create_app()

with app.app_context():
    #lots = ParkingLot.query.all()
    b= BookLot.query().all()
    b.end_time = db.Column(db.DateTime, nullable=False)