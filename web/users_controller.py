import sys
sys.path.append("../entity")
sys.path.append("../services")

from flask import render_template, Blueprint, request, redirect, url_for
from users import Users
from users_service import UsersService

usersBlueprint = Blueprint("usersBlueprint",__name__)

@usersBlueprint.route("/")
def home():
    return 'Home'

@usersBlueprint.route("/users")
def listAllUsers():
    usersList = Users.loadAll()
    return render_template("users/list.html", users=usersList)

@usersBlueprint.route("/users/form", methods = ["get"])
def addForm():
    return render_template("users/form.html")

@usersBlueprint.route("/users/form", methods = ["post"])
def addUser():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    UsersService.addUser(username,email, password)
    return redirect(url_for("usersBlueprint.listAllUsers"))