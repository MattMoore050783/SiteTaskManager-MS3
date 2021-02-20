import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        flash("Registration Successful! Please Login to Continue")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You are logged out of Site Task Manager")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/get_sites")
def get_sites():
    sites = list(mongo.db.sites.find().sort("site_name", 1))
    return render_template("sites.html", sites=sites)


@app.route("/add_site", methods=["GET", "POST"])
def add_site():
    if request.method == "POST":
        site = {
            "site_name": request.form.get("site_name")
        }
        mongo.db.sites.insert_one(site)
        flash("New Site Added")
        return redirect(url_for("get_sites"))

    return render_template("add_site.html")


@app.route("/edit_site/<site_id>", methods=["GET", "POST"])
def edit_site(site_id):
    if request.method == "POST":
        submit = {
            "site_name": request.form.get("site_name")
        }
        mongo.db.sites.update({"_id": ObjectId(site_id)}, submit)
        flash("Site Successfully Updated")
        return redirect(url_for("get_sites"))

    site = mongo.db.sites.find_one({"_id": ObjectId(site_id)})
    return render_template("edit_site.html", site=site)


@app.route("/delete_site/<site_id>")
def delete_site(site_id):
    mongo.db.sites.remove({"_id": ObjectId(site_id)})
    flash("Site Successfully Deleted")
    return redirect(url_for("get_sites"))


@app.route("/get_tasktypes")
def get_tasktypes():
    tasktypes = list(mongo.db.tasktypes.find().sort("tasktype_name", 1))
    return render_template("tasktypes.html", tasktypes=tasktypes)


@app.route("/add_tasktype", methods=["GET", "POST"])
def add_tasktype():
    if request.method == "POST":
        tasktype = {
            "tasktype_name": request.form.get("tasktype_name")
        }
        mongo.db.tasktypes.insert_one(tasktype)
        flash("New Tasktype Added")
        return redirect(url_for("get_tasktypes"))

    return render_template("add_tasktype.html")


@app.route("/edit_tasktype/<tasktype_id>", methods=["GET", "POST"])
def edit_tasktype(tasktype_id):
    if request.method == "POST":
        submit = {
            "tasktype_name": request.form.get("tasktype_name")
        }
        mongo.db.tasktypes.update({"_id": ObjectId(tasktype_id)}, submit)
        flash("Tasktype Successfully Updated")
        return redirect(url_for("get_tasktypes"))

    tasktype = mongo.db.tasktypes.find_one({"_id": ObjectId(tasktype_id)})
    return render_template("edit_tasktype.html", tasktype=tasktype)


@app.route("/delete_tasktype/<tasktype_id>")
def delete_tasktype(tasktype_id):
    mongo.db.tasktypes.remove({"_id": ObjectId(tasktype_id)})
    flash("Tasktype Successfully Deleted")
    return redirect(url_for("get_tasktypes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

        