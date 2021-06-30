from flask import redirect, url_for, render_template, request, flash, jsonify
from flask import Blueprint, render_template
from werkzeug.security import check_password_hash, generate_password_hash, check_password_hash
main = Blueprint("main", __name__, static_folder="static", template_folder="templates")
from models import users, Note
from appinit import db
from control import app
from flask_login import login_user, login_required, logout_user, current_user
import json
import secrets
import os
from PIL import Image


@main.route("/", methods=["GET", "POST"]) 
def homepage():
    if request.method == "POST":
        note = request.form.get('note')
         
        if len(note) < 1:
            flash('Note is too short!')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added')


    return render_template("index.html", signin = False, user=current_user, name = current_user.user)


        
@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        user = request.form.get("user")
        password = request.form.get("password")
        email = request.form.get("email")

        found_user = users.query.filter_by(user=user).first()
        found_email = users.query.filter_by(email=email).first()
        
        
        if found_user:
            flash("Username Already Taken")
        elif len(user) > 21:
            flash('Username must be 20 characters or less')
        elif len(password) < 6:
            flash('Password must be greater than 5 characters')
        elif found_email:
            flash("This email is already in use")

        else:
            usr = users(user=user, email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(usr)
            db.session.commit()
            login_user(usr, remember=True)
            flash('Account created succesfully!')
            return redirect(url_for("main.user"))
    
    return render_template("register.html", user=current_user)

@main.route("/login", methods=["POST", "GET"])   
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")

        found_user = users.query.filter_by(user=user).first()
        if found_user:
            if check_password_hash(found_user.password, password):
             # basicly this function checks the password in the db against what was submitted in the form
                flash('Logged in successfully')
                login_user(found_user, remember=True)
                return redirect(url_for("main.user"))
            else:
                flash('Incorrect Password')
        else:
            flash('There is no one registered under that username')
       #flash("Logged in succesfully")
        #return redirect(url_for("user"))
    #else:
        #if "user" in session:
            #flash("Welcome back.") 
            #return redirect(url_for("user"))

    return render_template("login.html", user=current_user)


def pictureshiz(image_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image_file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    i = Image.open(image_file)
    i.thumbnail(125,125)
    i.save(picture_path)
    
    return picture_fn


@main.route("/user", methods=["POST", "GET"])
@login_required
def user():
    
    if request.method == 'POST':
        image_file = request.form.get("image_file")
        profilepic = pictureshiz(image_file)
        current_user.image_file = profilepic

        profilepic = users(image_file=image_file)
        db.session.add(profilepic)
        db.session.commit()
        flash("Profile picture changed!")

    image_file = url_for('static', filename='pics/' + current_user.image_file)    
    return render_template("user.html", user = current_user, name = current_user.user, emails = current_user.email, image_file=image_file)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out successfully.")
    
    return redirect(url_for("main.login"))



@main.route('/delete', methods=['POST'])
def delete():
    note=json.loads(request.data)
    noteId = note['noteId']
    note=Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})