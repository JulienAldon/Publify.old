import sys
import spotipy
import spotipy.util as util
import datetime

def setAuth(client_id, client_secret, username, scope, redirect_url='http://localhost/'):
	"""
	Authenticate the user <username>, using <client_id>,
	<client_secret> and <redirect_url> and providing the <scope>
	`client_id`: Spotify application client_id.
	`client_secret`: Spotify application client_secret.
	`redirect_url`: Dont know what it is default : localhost).
	`username`: User id from spotify on which the application will get the privileges.
	`scope`: Scope of the application.
	"""
	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_url)
	if token:
		return token
	else:
		print("Can't get token for", username)

class Playlist:
	def __init__(self, token):
		self._client = spotipy.Spotify(auth=token)

	def add_track(self, playlist_id, track_ids, user):
		"""
		Add tracks from <track_ids> to the playlist <playlist_id> using the <token> for authentication
		The user must be logged in with the function setAuth().
		`token` : authentication token given by setAuth() function.
		`playlist_id` : playlist where tracks will be added.
		`track_ids` : tuple list containing [("to_add", <trackId>), ("to_del", <trackId>)]
		This list is given by getTrackDiff() function.
		"""
		self._client.trace = False
		add = [a[1] for a in track_ids if a[0] == 'to_add']
		dele = [a[1] for a in track_ids if a[0] == 'to_del']
		if add:
			results = self._client.user_playlist_add_tracks(user, playlist_id, add)
		if dele:
			results = self._client.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id, dele)
	
	def getTrackDiff(self, l1, l2):
		"""
		Get the difference between track_id list <l1> and track_id <l2>
		l1 : track_id list of collaborative playlist
		l2 : track_id list of a public playlist
		Return : list of tuple l[0][0] = to_add or to_del l[0][1] = track id
		[('to_add', <track_id>), ('to_del', <track_id>)]
		"""
		l = []
		for i in l1:
			if not i in l2:
				l.append(('to_add', i))
		for i in l2:
			if not i in l1:
				l.append(('to_del', i))
		return(l)

	def show_tracks(self, results):
		"""
		Add tracks id in a list and return it
		`result`: Json format of the playlist request
		returns 
		"""
		tracks = []
		for item in results['items']:
			track = item['track']
			tracks.append(track['id'])
		return(tracks)

	def show_artist(self, results):
		artists = []
		for item in results['items']:
			track = item['track']
			artists.append(track['artists'][0]['id'])
		return(artists)

	def getUserPlaylist(self, user):
		p = []
		c = []
		playlists = self._client.user_playlists(user)
		for playlist in playlists['items']:
			if playlist['collaborative'] == False:
				p.append((playlist['name'], playlist['id']))
			else:
				c.append((playlist['name'], playlist['id']))
		return p, c

	def getTracksid(self, playlist_id, user_id):
		"""
		using <token> get the list of tracks id given a <playlist> id
		`playlist`: Id of a playlist
		"""
		results = self._client.user_playlist(user_id, playlist_id, fields="tracks,next")
		tracks = results['tracks']
		t = self.show_tracks(tracks)
		while tracks['next']:
			tracks = self._client.next(tracks)
			t += self.show_tracks(tracks)
		return(t)

	def getArtistsAlbums(self, artists_id):
		"""
		artists_id : list of artists_id
		"""
		albums_id = []
		albums = []
		for a in artists_id:
			albums.append(self._client.artist_albums(a))
		for album in albums:
			for al in album['items']:
				albums_id.append(al['id'])
		return(albums_id)

	def getAlbumsReleaseDate(self, albums_id):
		"""
		albums_id : list of album id's
		"""
		dates = []
		for a in albums_id:
			albums = self._client.album(a)
			dates.append((a, albums['release_date']))
		result = self.sortAlbumsByDate(dates) 
		return(result)

	def getLastAlbums(self, rg, albums_date):
		"""
		rg: range of the time search (in days)
		albums_date format: [('%Y-%m-%d', 'album_id'), ...]
		"""
		dates = self.generateRangeofDates(rg)
		res = [(a[0], a[1]) for a in albums_date if a[0] in dates]
		if res is None:
			print('No songs found!')
		l = []
		for a in res:
			album = self._client.album_tracks(a[1])
			l.append(album['items'][0]['id'])
		return(l)

	def generateRangeofDates(self, rg):
		"""
		rg: range of the wanted generation
		"""
		date = datetime.datetime.now()
		a = date.strftime('%Y-%m-%d')
		dt = datetime.datetime.strptime(a, "%Y-%m-%d")
		step = datetime.timedelta(days=1)
		l = []
		for i in range(0, rg):
			l.append(dt.strftime('%Y-%m-%d'))
			dt -= step
		return(l)

	def createReleasePlaylist(self, user_id, pl_name, tracks):
		a = self.generateRangeofDates(1)
		print(a[0])
		b = '[Releasify] ' + a[0] + ' ' + pl_name
		print(b)
		self._client.trace = False
		playlist = self._client.user_playlist_create(user_id, b, public=True)
		results = self._client.user_playlist_add_tracks(user_id, playlist['id'], tracks)

	def sortAlbumsByDate(self, albums_date):
		"""
		sort the albums_date list by date
		albums_date format: [('%Y-%m-%d', 'album_id'), ...]
		"""
		fixed_dates = []
		for b in albums_date:
			if len(b[1]) == 4:
				fixed_dates.append((b[0], b[1] + '-01-01'))
			else:
				fixed_dates.append((b[0], b[1]))
		a = [(datetime.datetime.strptime(ts[1], "%Y-%m-%d"), ts[0]) for ts in fixed_dates]
		a.sort(key=lambda tup: tup[0])
		newa = [(datetime.datetime.strftime(ts[0], "%Y-%m-%d"), ts[1]) for ts in a]
		return(newa)

	def getArtistsIdInPlaylist(self, userid, playlistid):
		"""
		get all the artists of a playlist
		"""
		results = self._client.user_playlist(userid, playlistid, fields="tracks,next")
		artist = results['tracks']
		t = self.show_artist(artist)
		while artist['next']:
			artist = self._client.next(artist)
			t += self.show_artist(artist)
		t = list(set(t))
		return(t)
