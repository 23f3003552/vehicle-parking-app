
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from extensions import db
from models import *
from sqlalchemy.exc import IntegrityError

userdash = Blueprint("userdash", __name__, static_folder="static", template_folder="templates")

@userdash.route("/", methods=["GET", "POST"])
def userdash():
    return render_template("userdash.html")