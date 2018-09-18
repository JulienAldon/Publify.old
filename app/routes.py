#!/usr/bin/env python3
from app import app
from app import db
import app.utility as util
from app.models import User, PlaylistLink
import app.myspotylib as msptlib
from datetime import datetime
import flask as fk
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import current_user, login_user, logout_user, login_required
from flask_oauthlib.client import OAuth
import json
import uuid
from urllib.parse import unquote

app.config.from_pyfile('myconfig.py')
oauth = OAuth(app)
spotify = oauth.remote_app(
    'spotify',
	consumer_key=app.config['CLIENTKEY'],
	consumer_secret=app.config['CLIENTSECRET'],
	request_token_params={'scope': 'playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative'},
	base_url='https://api.spotify.com/v1/',
	access_token_method='POST',
	access_token_url='https://accounts.spotify.com/api/token',
	request_token_url=None,
	authorize_url='https://accounts.spotify.com/authorize'
)

@spotify.tokengetter
def spotify_get_token():
	return fk.session.get('access_token'), ''

@app.before_request
def before_request():
	""" Last seen function """
	g.spotify = spotify

@app.route('/radio')
def radio():
	return render_template('radio.html', **util.get_radio_dict())

@app.route('/load_radio', methods=['POST'])
def load_radio():
	if request.method == "POST":
		res = request.data
	a = unquote(str(res.decode('utf-8')))
	play = a.replace('play=', '')
	print(play)
	if not 'access_token' in fk.session:
		return redirect(url_for('radio'))
	usr = fk.g.spotify.get('me')
	usr_id = usr.data['id']
	print(usr_id)
	P = msptlib.Playlist(fk.session['access_token'])
	usr_playlists = P.getUserPlaylist(usr_id)
	pl_id = util.getPlaylistIdfromName(play, usr_playlists)
	artists = P.getArtistsIdInPlaylist(usr_id, pl_id)
	albums_id = P.getArtistsAlbums(artists)
	dates = P.getAlbumsReleaseDate(albums_id)		
	tracks = P.getLastAlbums(7, dates)
	if tracks == []:
		print('No tracks found!')
		return render_template('radio.html', answer='No new tracks found!')
	P.createReleasePlaylist(usr_id, play, tracks)
	print("load_radio/", tracks)
	return redirect(url_for('radio'))

@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index():
	return render_template('index.html', **util.get_user_dict())

@app.route('/load_ajax', methods=('GET', 'POST'))
def load_index():
	if request.method == "POST":
		res = request.data
	a = unquote(str(res.decode('utf-8')))
	a = a.split('&')
	pub, col = [], []
	pub.append(a[0].replace('pub=', ''))
	col.append(a[1].replace('col=', ''))
	if not 'access_token' in fk.session:
		return redirect(url_for('index'))
	usr = fk.g.spotify.get('me')
	usr_id = usr.data['id']
	P = msptlib.Playlist(fk.session['access_token'])
	usr_playlists = P.getUserPlaylist(usr_id)
	if None in pub or None in col:
		print('Error pub and col are None')
		# "please select one colaborative and one public playlist"
	print (pub, col)
	try:
		col_id, pub_id = util.getIdfromName(col, pub, usr_playlists)
		util.syncPlaylists(col_id, pub_id, usr_id)
	except:
		print('Can\'t get if from names')
	link = PlaylistLink(pub_id, col_id)
	p = PlaylistLink.query.filter_by(collab_playlist_id=col_id, public_playlist_id=pub_id).first()
	if p is None:
		current_user = User.query.filter_by(username=usr_id).first()
		current_user.playlist_link.append(link)
		db.session.add(link)
		db.session.commit()
	return redirect(url_for('index'))

@app.route('/api/auth/login')
def spotify_api_login():
	fk.session.permanent = True
	if 'access_token' in fk.session:
		return redirect(url_for('index'))		
	state = fk.session['state'] = str(uuid.uuid4())
	callback = 'https://spot.xxx.epi.codes/api/auth/authorized'
	return g.spotify.authorize(callback=callback, state=state)

@app.route('/api/auth/logout')
def spotify_api_logout():
	if 'access_token' not in fk.session:
		return redirect(url_for('index'))
	del fk.session['access_token']
	return redirect(url_for('index'))

@app.route('/api/auth/authorized')
def spotify_api_authorized():
	if fk.session['state'] != str(fk.request.args['state']):
		return redirect(url_for('index'))		
	response = g.spotify.authorized_response()
	fk.session['access_token'] = response['access_token']
	usr = g.spotify.get('me').data['id']
	u = User.query.filter_by(username=usr).first()
	if u is None:
		u = User(usr, 0)
		db.session.add(u)
		db.session.commit()
	return redirect(url_for('index'))
