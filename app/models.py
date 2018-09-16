#!/usr/bin/env python3
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login

class PlaylistLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collab_playlist_id = db.Column(db.String(64))
    public_playlist_id = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='playlist_link')

    def __init__(self, public, private):
        self.collab_playlist_id, self.public_playlist_id = private, public

    def __repr__(self):
        return '<links {} {}>'.format(self.collab_playlist_id, self.public_playlist_id)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    level = db.Column(db.Integer)
    playlist_link = db.relationship('PlaylistLink', back_populates='user')
    def __init__(self, user, level):
        self.username, self.level = user, level

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))