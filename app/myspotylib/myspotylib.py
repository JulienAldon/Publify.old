import sys
import spotipy
import spotipy.util as util

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
			artists.append(track['artists'][0]['name'])
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

	def getTracksid(self, playlist, user):
		"""
		using <token> get the list of tracks id given a <playlist> id
		`playlist`: Id of a playlist
		"""
		results = self._client.user_playlist(user, playlist, fields="tracks,next")
		tracks = results['tracks']
		t = self.show_tracks(tracks)
		while tracks['next']:
			tracks = self._client.next(tracks)
			t += self.show_tracks(tracks)
		return(t)

	def getArtistInPlaylist(self, user, playlist):
		"""
		get les artistes d'une playlist sans doublon
		"""
		results = self._client.user_playlist(user, playlist, fields="tracks,next")
		artist = results['tracks']
		t = self.show_artist(artist)
		while artist['next']:
			artist = self._client.next(artist)
			t += self.show_tracks(artist)
		t = list(set(t))
		return(t)
