from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

upvotes = db.Table('upvotes',
                   db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                   db.Column('sub_id', db.Integer, db.ForeignKey('post.id')))

class Video(db.Model):
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    subtitleTracks = db.relationship('SubtitleTrack', backref='videoIdLink', lazy='dynamic')

    def __repr__(self):
        return '<Video {}>'.format(self.id)

class SubtitleTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    languageCode = db.Column(db.String(4), index=True)
    isDefault = db.Column(db.Boolean())
    videoId = db.Column(db.String, db.ForeignKey('video.id'))

    def __repr__(self):
        return '<Video {} - {}>'.format(self.videoId, self.languageCode)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<User {}'.format(self.username)

    def setPassword(self, inPassword):
        self.passwordHash = generate_password_hash(inPassword)

    def checkPassword(self, inPassword):
        return check_password_hash(self.passwordHash, inPassword)