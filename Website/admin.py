from flask import Blueprint, render_template



admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")
#from models import users


@admin.route("/")
def randomfunction():
    pass

#def for homepage for admin
#@admin.route("/view")
#def view():
    #return render_template("view.html", values=users.query.all())
#need to pass the class users to this blueprint so that it can store the info
