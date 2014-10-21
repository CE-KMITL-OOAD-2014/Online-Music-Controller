from Playlist import Playlist

class GetPlaylist():
	def __init__(self):
		self.playlist_list = []

	def get_playlist(self,name):
		return self.playlist_list[0]

	def add_playlist(self,name):
		self.playlist_list[arr(self.playlist_list)] = Playlist(name)