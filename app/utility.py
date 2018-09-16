#!/usr/bin/env python3
import flask as fk
from app import db
from app.forms import MyForm
import app.myspotylib as msptlib
from app.models import User, PlaylistLink

def json(code, message):
	"""
	Prepare a JSON response for API use, with the provided `code` and `message`.
	"""
	response = {'ok': code == 200, 'code': code}
	if message is not None:
		response['error' if code != 200 else 'message'] = message

	response = fk.json.jsonify(response)
	response.status_code = code
	return response

def getNameFromId(collab_id, public_id, usr_playlists):
	pub_name = []
	for b in public_id:
		for a in usr_playlists[0]: #public
			if a[1] == b:
				pub_name.append(a[0])
	collab_name = []
	for b in collab_id:
		for a in usr_playlists[1]: #collab
			if a[1] == b:
				collab_name.append(a[0])
	return collab_name, pub_name

def getIdfromName(collab, public, usr_playlists):
	pub_id = []
	col_id = []
	for a in usr_playlists[0]: #collab
		if (a[0] == public[0]):
			pub_id.append(a[1])
	for a in usr_playlists[1]: #pubic
		if (a[0] == collab[0]):
			col_id.append(a[1])
	return col_id[0], pub_id[0]

def getUserPlaylistLink(usr):
	try:
		usr_id = usr.data['id']
		usr_name = usr.data['display_name']
		user = User.query.filter_by(username=usr.data['id']).first()
		if user is None:
			user = User(usr, 0)
			db.session.add(user)
			db.session.commit()
	except Exception as e:
		raise Exception('Error when collecting db info!', e)
	pub_ids = [a.public_playlist_id for a in user.playlist_link]
	col_ids = [a.collab_playlist_id for a in user.playlist_link]
	P = msptlib.Playlist(fk.session['access_token'])
	usr_playlists = P.getUserPlaylist(usr_id)
	collab_name, pub_name = getNameFromId(col_ids, pub_ids, usr_playlists)
	return usr_name, pub_name, collab_name

def syncPlaylists(collab_id, public_id, usr_id):
	P = msptlib.Playlist(fk.session['access_token'])
	c = P.getTracksid(collab_id, usr_id)
	p = P.getTracksid(public_id, usr_id)
	track_ids = P.getTrackDiff(c, p)
	P.add_track(public_id, track_ids, usr_id)

def get_user():
	try:
		print(fk.session['access_token'])
		usr = fk.g.spotify.get('me')
		usr_id = usr.data['id']
		P = msptlib.Playlist(fk.session['access_token'])
		pub, col = [], []
		usr_playlists = P.getUserPlaylist(usr_id)
		usr_pl = [a[0] for a in usr_playlists[0]]
		usr_col = [a[0] for a in usr_playlists[1]]
		user = User.query.filter_by(username=usr_id).first()
		username, public, collab = getUserPlaylistLink(usr)
		if fk.request.method == 'POST':
			if fk.request.form['submit'] == 'sync':
				links = user.playlist_link
				if not links:
					return zip([], []), username, usr_pl, usr_col
				for l in links:
					syncPlaylists(l.collab_playlist_id, l.public_playlist_id, usr.data['id'])
				return zip(collab, public), username, usr_pl, usr_col
	except Exception as e:
		if e.args[0] == "name 'token' is not defined":
			raise e from None
		if e.args[0] == "name 'playlists' is not defined":
			raise e from None
		if 'access_token' in fk.session:
			print("updater error :", e)
			del fk.session['access_token']
		collab, public, username, usr_pl, usr_col = [], [], 'Anonymous', [], []
	return zip(collab, public), username, usr_pl, usr_col

def get_user_dict():
	"""
	Get The current user's collab, public, username and level as a dict
	"""
	return dict(zip(('PlaylistLinks', 'Username', 'SpotPublic', 'SpotCollab'), get_user()))

def get_radio():
	try:
		print(fk.session['access_token'])
		usr = fk.g.spotify.get('me')
		usr_id = usr.data['id']
		P = msptlib.Playlist(fk.session['access_token'])
		pub, col = [], []
		usr_playlists = P.getUserPlaylist(usr_id)
		usr_pl = [a[0] for a in usr_playlists[0]]
		usr_col = [a[0] for a in usr_playlists[1]]
		Playlists = usr_pl + usr_col
		print(Playlists)				
	except Exception as e:
		if e.args[0] == "name 'token' is not defined":
			raise e from None
		if e.args[0] == "name 'playlists' is not defined":
			raise e from None
		if 'access_token' in fk.session:
			print("radio error :", e)
			del fk.session['access_token']
		Playlists = []
	return Playlists


def get_radio_dict():
	return {'Playlists': get_radio()}