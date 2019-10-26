
from flask_moment import Moment
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import ARRAY

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    seeking_artist = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<Venue shows: {self.city}, id: {self.id}>'


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='artist', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'<artist shows: {self.genres}>'

class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id', ondelete='CASCADE'))
    Artist_id = db.Column(db.Integer, db.ForeignKey('artist.id', ondelete='CASCADE'))

    def __repr__(self):
       return f'<Shows time: {self.time}>'