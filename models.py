import json

from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

upvotes = db.Table('upvotes',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('sub_id', db.Integer, db.ForeignKey('subtitle.id')))

class Video(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    subtitles = db.relationship('Subtitle', backref='videoIdLink', lazy='dynamic')

    def __repr__(self):
        return '<Video {}>'.format(self.id)

class Subtitle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    languageCode = db.Column(db.String(4), index=True)
    text = db.Column(db.Text())
    isDefault = db.Column(db.Boolean())
    videoId = db.Column(db.String, db.ForeignKey('video.id'))

    def __repr__(self):
        return '<Video {} - {}>'.format(self.videoId, self.languageCode)

    @staticmethod
    def dictToString(inDict):
        #todo! remove!
        return json.dumps(inDict)

    def getTextDict(self):
        return json.loads(self.text)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    passwordHash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def setPassword(self, inPassword):
        self.passwordHash = generate_password_hash(inPassword)

    def checkPassword(self, inPassword):
        return check_password_hash(self.passwordHash, inPassword)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
