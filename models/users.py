# user.py
from extensions import db

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






#user table
#def UserTable(cur):
#    cur.execute("""  
#        CREATE TABLE IF NOT EXISTS Users (
#            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
##            username TEXT UNIQUE NOT NULL,
#            pass_hash TEXT NOT NULL,
#            name TEXT NOT NULL,
#            u_email TEXT UNIQUE,
#            is_superUser BOOLEAN DEFAULT 0
#       ); """)
