from datetime import datetime
from flask_login import UserMixin
from appinit import db




class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(35))
    email = db.Column(db.String(35), unique=True)
    notes = db.relationship('Note', backref='user', lazy='dynamic')
    image_file = db.Column(db.String(20), default='defaultpic.jpg')



class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


