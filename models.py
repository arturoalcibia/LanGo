from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Language(db.Model):
    shortCode = db.Column(db.String(2), primary_key=True)
    userId = db.Column(db.String, db.ForeignKey('user.id'))
    subtitles = db.relationship('Subtitle', backref='languageLink', lazy='dynamic')

    def __repr__(self):
        return '<Language {}>'.format(self.shortCode)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user_sub_score'))
    subtitleId = db.Column(db.Integer, db.ForeignKey('subtitle.id'))
    subtitle = db.relationship('Subtitle', backref=db.backref('all_sub_scores'))
    score = db.Column(db.Integer)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('user_sub_votes'))
    subtitleId = db.Column(db.Integer, db.ForeignKey('subtitle.id'))
    subtitle = db.relationship('Subtitle', backref=db.backref('all_sub_votes'))
    upvote = db.Column(db.Boolean, nullable=False)


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
    knownWordsIndexList = db.Column(db.Text(), nullable=True)
    isDefault = db.Column(db.Boolean())
    videoId    = db.Column(db.String, db.ForeignKey('video.id'))
    language_id = db.Column(db.String, db.ForeignKey('language.shortCode'))

    def __repr__(self):
        return '<Subtitle {} - {}>'.format(self.videoId, self.languageCode)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    passwordHash = db.Column(db.String(128))
    languages = db.relationship('Language', backref='userLanguagesLink', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def setPassword(self, inPassword):
        self.passwordHash = generate_password_hash(inPassword)

    def checkPassword(self, inPassword):
        return check_password_hash(self.passwordHash, inPassword)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
