#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from model import Venue, Show, Artist, app, db
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



today = datetime.now()
now = today.strftime("%Y-%m-%d %H:%M:%S")

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  artists = Artist.query.order_by(db.desc('id')).limit(10).all()
  venues = Venue.query.order_by(db.desc('id')).limit(10).all()
  return render_template('pages/home.html', artists = artists, venues = venues)

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = []
  try:
    venues = Venue.query.distinct(Venue.city).all() 
    for ven in venues:
      ven.venues = Venue.query.filter_by(city=ven.city).all()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally: 
    db.session.close()
  return render_template('pages/venues.html', areas=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  res = {}
  try:
    name = request.form['search_term']
    res['data'] = Venue.query.filter(Venue.name.ilike('%'+ name + '%')).all()
    res['count'] = Venue.query.filter(Venue.name.ilike('%'+ name + '%')).count()
    data = request.form 
  except:
    print(sys.exc_info())
    flash('error occured')
  return render_template('pages/search_venues.html', results=res, search_term=request.form.get('search_term', '')) 

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = {}
  up_shows = []
  past_show = []
  try:
    venue = Venue.query.get(venue_id)
    for show in venue.shows:
      sh = Show.query.get(show.id)
      show.artist_name = sh.artist.name
      show.artist_image_link = sh.artist.image_link
      if show.time > today:
        show.time = str(show.time)
        up_shows.append(show)
      else:
        show.time = str(show.time)
        past_show.append(show)
    setattr(venue, 'past_shows', past_show)
    setattr(venue, 'upcoming_shows', up_shows)
    setattr(venue, 'past_shows_count', len(past_show))
    setattr(venue, 'upcoming_shows_count', len(up_shows))
  except:
    print(sys.exc_info())
  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    data = request.form
    genres = data.getlist('genres')
    venue = Venue(name=data['name'], city=data['city'],
    state=data['state'], address=data['address'], phone=data['phone'], genres=genres,
    facebook_link=data['facebook_link'], image_link=data['image_link'], seeking_artist=str_to_bool(data['seeking_talents']),
    seeking_description=data['seeking_description'])
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + data['name'] + ' was successfully listed!')  
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('venues'))


@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('venue successfully deleted')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('venue could not deleted')
  finally:
    db.session.close()
  return redirect(url_for('venues'))


@app.route('/artists/<artist_id>/delete', methods=['GET'])
def delete_artist(artist_id):
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('artist successfully deleted')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('artist could not deleted')
  finally:
    db.session.close()
  return redirect(url_for('artists'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  return render_template('pages/artists.html', artists=Artist.query.order_by('id').all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  res = {}
  try:
    name = request.form['search_term']
    res['data'] = Artist.query.filter(Artist.name.ilike('%'+ name + '%')).all()
    res['count'] = Artist.query.filter(Artist.name.ilike('%'+ name + '%')).count()
    data = request.form 
  except:
    print(sys.exc_info())
    flash('error occured')
  return render_template('pages/search_artists.html', results=res, search_term=request.form.get('search_term', '')) 
 
  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = {}
  up_shows = []
  past_show = []
  try:
    artist = Artist.query.get(artist_id)
    for show in artist.shows:
      sh = Show.query.get(show.id)
      show.venue_name = sh.venue.name
      show.venue_image_link = sh.venue.image_link
      if show.time > today :
        show.time = str(show.time)
        up_shows.append(show)
      else:
        show.time = str(show.time)
        past_show.append(show)
    setattr(artist, 'past_shows', past_show)
    setattr(artist, 'upcoming_shows', up_shows)
    setattr(artist, 'past_shows_count', len(past_show))
    setattr(artist, 'upcoming_shows_count', len(up_shows))
  except:
    print(sys.exc_info())
  return render_template('pages/show_artist.html', artist=artist)
 

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  art = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=art)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    data = request.form
    artist = Artist.query.get(artist_id)
    for art in data:
      if art == 'genres':
        genres = data.getlist('genres')
        setattr(artist, art, genres)
      else:
        setattr(artist, art, data[art])
    flash('artist ' + data['name'] + ' has been updated')
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('artist ' + data['name'] + ' could not be updated')
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))
  



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  ven = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=ven)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    data = request.form
    venue = Venue.query.get(venue_id)
    for art in data:
      if art == 'genres':
        genres = data.getlist('genres')
        setattr(venue, art, genres)
      elif art == 'seeking_talents':
        setattr(venue, 'seeking_artist', str_to_bool(data[art]))
      else:
        setattr(venue, art, data[art])
    flash('venue ' + data['name'] + ' has been updated')
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('venue ' + data['name'] + ' could not be updated')
  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    data = request.form
    genres = data.getlist('genres')
    artist = Artist(name=data['name'], city=data['city'],
    state=data['state'], phone=data['phone'], genres=genres,
    facebook_link=data['facebook_link'], image_link=data['image_link'], seeking_venue=str_to_bool(data['seeking_shows']),
    seeking_description=data['seeking_description'])
    db.session.add(artist)
    db.session.commit()
    flash('Artist was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('Sorry, artist could not listed!')
  finally:
    db.session.close()
  return redirect(url_for('artists'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  allshows = []
  try:
    allshows = Show.query.order_by('time').all()
    for sh in allshows:
      sh.artist_name = sh.artist.name
      sh.venue_name = sh.venue.name
      sh.artist_image_link = sh.artist.image_link
      sh.time = str(sh.time)
  except:
    print(sys.exec_info())
  return render_template('pages/shows.html', shows=allshows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  data = {}
  try:
    data = request.form
    show = Show(Artist_id=data['artist_id'], venue_id=data['venue_id'], time=data['start_time'] )
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  except:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  return redirect(url_for('shows'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
