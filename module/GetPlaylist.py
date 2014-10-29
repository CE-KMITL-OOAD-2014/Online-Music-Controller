from Playlist import Playlist

class GetPlaylist():
	def __init__(self):
		self.playlist_list = []
		# self.playlist_list.append(Playlist("pl1"))
		# self.playlist_list.append(Playlist("pl2"))

	def get_playlist(self):
		try:
			returnPlaylist = []
			for playlist in self.playlist_list :
				returnPlaylist.append(playlist.get_playlist_name)

			return returnPlaylist
		except :
			return "no playlist"
		

	def add_playlist(self,name):
		self.playlist_list.append(Playlist(name))