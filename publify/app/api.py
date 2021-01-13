from app import app
from app import db
import flask as fk
from flask import url_for, request, g, redirect
from flask_restful import Resource, Api
from flask_restful.reqparse import RequestParser
from app.models import User, PlaylistLink
from flask_sqlalchemy import SQLAlchemy
import app.spotifyWrapper as abc
from flask_cors import CORS, cross_origin
from authlib.integrations.flask_client import OAuth
# from flask_oauthlib.client import OAuth
import json
import uuid
import functools
#initialisation
# app.config.from_object(Config)
oauth = OAuth(app)

def fetch_spotify_token():
	# if not 'access_token' in fk.session:
	# 	return "no token
		# authorisation = request.headers['Authorization'].split(' ')
		# if authorisation[0] == 'Bearer':
		# 	return authorisation[1]
		# else:
	return fk.session['access_token']

spotify = oauth.register(
	'spotify',
	client_id=app.config['CLIENTKEY'],
	client_secret=app.config['CLIENTSECRET'],
	client_kwargs={'scope': 'playlist-read-private playlist-modify-private playlist-modify-public playlist-read-collaborative'},
	api_base_url='https://api.spotify.com/v1/',
	access_token_method='POST',
	access_token_url='https://accounts.spotify.com/api/token',
	request_token_url=None,
	authorize_url='https://accounts.spotify.com/authorize',
	fetch_token=fetch_spotify_token,
)
api = Api(app, prefix="/api/v1")

def isAuthorized(func):
	@functools.wraps(func)
	def fx(*args, **kwargs):
		try:
			usr = spotify.get('me').json()
			usr['display_name']
		except:
			return redirect('https://publify.aldon.info')
		return redirect('https://publify.aldon.info/app')
	return fx

# utility

def createError(msg, code, special=None):
	if special:
		return fk.jsonify({'error': msg , 'status': code, 'special': special})
	return fk.jsonify({'error': msg , 'status': code})

# resources
class Radio(Resource):
	def get(self):
		if fetch_spotify_token():
			return fk.jsonify({'data': 'You are connected'})
		return {'bite': 'couille'}

	def post(self):
		return {}

class Playlists(Resource):
	def get(self):
		try:
			usr = spotify.get('me').json()
		except:
			return createError('Unauthorized', 401, special='Spotify authentification required, please log in with spotify')
		name = usr['display_name']
		user = abc.User(token=fetch_spotify_token()['access_token'], id=usr['id'], name=name)
		user.getPlaylists()
		result = {
			'public': [{
				'name': a.name,
				'id' : a.id
			} for a in user.playlists['public']],
			'collaborative': [{
				 'name': b.name, 
				 'id': b.id
			} for b in user.playlists['collaborative']]
		}
		return fk.jsonify(result)

	def post(self):
		try:
			usr = spotify.get('me').json()
		except Exception:
			return createError('Unauthorized', 401, special='Spotify authentification required, please log in with spotify')
		response = request.get_json()
		if response is None:
			return createError('Bad Request', 400, special="No playlist provided please change the request's body")
		if not response['public'] or not response['collaborative']:
			return createError('Bad Request', 400, special="No playlist provided please change the request's body")
		name = usr['display_name']
		user = abc.User(token=fetch_spotify_token()['access_token'], id=usr['id'], name=name)

		link = PlaylistLink(response['public'], response['collaborative'])
		current_user = User.query.filter_by(username=usr['id']).first()
		current_user.playlist_link.append(link)
		db.session.add(link)
		db.session.commit()
		public = abc.Playlist(link.public_playlist_id, user, type="public")
		public.getTracks()
		collaborative = abc.Playlist(link.collab_playlist_id, user, type="collaborative")
		collaborative.getTracks()
		return fk.jsonify({'success': 'playlist link created', 
			'link': {
				'linkId': link.id,
				'collaborative': {'id': collaborative.id, 'name': collaborative.name},
				'public': {'id': public.id, 'name': public.name}
				}
			})

class PlaylistLinks(Resource):
	def get(self, id):
		try:
			usr = spotify.get('me').json()
		except:
			return createError('Unauthorized', 401, special='Spotify authentification required, please log in with spotify')
		p = PlaylistLink.query.filter_by(id=id).first()
		if p is None:
			return createError('Not Found', 404)
		return fk.jsonify({'collaborative': p.collab_playlist_id, 'public': p.public_playlist_id})	
	
	def put(self, id):
		if not 'access_token' in fk.session:
			return createError('Unauthorized', 401, special='Authentification required')
		p = PlaylistLink.query.filter_by(id=id).first()
		res = request.get_json()
		if p is None:
			return createError('Not Found', 404)
		p.collab_playlist_id = res['collaborative']
		p.public_playlist_id = res['public']
		db.session.commit()
		return fk.jsonify({'success': 'Playlist Link Updated'})

	def delete(self, id):
		if not 'access_token' in fk.session:
			return createError('Unauthorized', 401, special='Authentification required')
		p = PlaylistLink.query.filter_by(id=id).first()
		if p is None:
			return createError('Not Found', 404)
		db.session.delete(p)
		db.session.commit()
		return fk.jsonify({'success': 'Playlist Link Deleted'})
	
	def options(self, id):
		pass

class Synchronizer(Resource):
	def get(self, id):
		pass
	
	def put(self, id):
		response = request.get_json()
		if response is None:
			return createError('Bad Request', 400, special="No playlist provided please change the request's body")
		try:
			usr = spotify.get('me').json()
		except:
			return createError('Unauthorized', 401, special='Spotify authentification required, please log in with spotify')
		name = usr['display_name']
		user = abc.User(token=fetch_spotify_token()['access_token'], id=usr['id'], name=name)
		p = PlaylistLink.query.filter_by(id=id).first()
		if p is None:
			return createError('Not Found', 404)

		public = abc.Playlist(p.public_playlist_id, user, type="public")
		public.getTracks()
		collaborative = abc.Playlist(p.collab_playlist_id, user, type="collaborative")
		collaborative.getTracks()
		if response['direction'] == 'Forward':
			public.sync(collaborative)
		elif response['direction'] == 'Backward':
			collaborative.sync(public)
		else:
			return createError('Bad Request', 400, special="No playlist provided please change the request's body")
		return fk.jsonify({'success': 'Synchronization requested'})

class Links(Resource):
	def get(self):
		try:
			usr = spotify.get('me').json()
		except:
			return createError('Unauthorized', 401, special='Spotify authentification required, please log in with spotify')
		name = usr['display_name']
		usrId = usr['id']
		user = abc.User(token=fetch_spotify_token()['access_token'], id=usrId, name=name)
		p = PlaylistLink.query.all()
		if p is None:
			return createError('Not Found', 404)
		collab = []
		public = []
		ids = []
		for a in p:
			ids.append(a.id)
			collab.append(abc.Playlist(a.collab_playlist_id, user, type="collaborative"))
			public.append(abc.Playlist(a.public_playlist_id, user, type="public"))
		response = fk.jsonify({'links':[{
			'linkId': c,
			'collaborative': {'id': a.id, 'name': a.name},
			'public': {'id': b.id, 'name': b.name} 
		} for a, b, c in zip(collab, public, ids)]})
		return response
	
api.add_resource(Radio, '/radio')
api.add_resource(Playlists, '/playlist')
api.add_resource(PlaylistLinks, '/playlist/<int:id>')
api.add_resource(Synchronizer, '/playlist/<int:id>/sync')
api.add_resource(Links, '/playlist/all/links')

@app.before_request
def before_request():
	""" Last seen function """
	g.spotify = spotify

@app.route('/api/auth/login')
def spotify_api_login():
	fk.session.permanent = True
	if 'access_token' in fk.session:
		del fk.session['access_token']
		# return fk.redirect('https://front.localhost/')
		# return createError('Forbiden', 403)
	callback = 'http://auth.publify.aldon.info/api/auth/authorized'
	return g.spotify.authorize_redirect(callback)

@app.route('/api/auth/logout')
def spotify_api_logout():
	if 'access_token' in fk.session:
		del fk.session['access_token']
		return fk.redirect('https://publify.aldon.info/')
		# return fk.jsonify({'success': 'User logged out sucessfully'})
	return createError('Unauthorized', 401)

@app.route('/api/auth/authorized')
def spotify_api_authorized():
	token = oauth.spotify.authorize_access_token()
	fk.session['access_token'] = token
	print(token)
	usr = spotify.get('me').json()
	u = User.query.filter_by(username=usr['id']).first()
	if u is None:
		u = User(usr['id'], 0)
		db.session.add(u)
		db.session.commit()
	# result = {'data': 'User created sucessfully'}
	return fk.redirect('https://publify.aldon.info/app')

if __name__ == '__main__':
	db.create_all()
	app.run(Treaded=True)