from flask import Flask
from Application.db import db  
from config import Config
app= None
def create_app():
    app=Flask(__name__)
     
    app.debug = True
    app.config.from_object(Config) 
    db.init_app(app)
   
    app.app_context().push()
    return app

app= create_app()
from controllers.auth import *
if __name__=='__main__':
    app.run()

