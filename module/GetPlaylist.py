from Playlist import Playlist
from PlaylistRepo import PlaylistRepo

class GetPlaylist():
	def __init__(self):
		pass
	def get_playlist(self,player_id):
		print "AAAA"
		try:
			print "BBBB"
			pl_repo = PlaylistRepo()
			returnPlaylist = pl_repo.get_all(player_id)

			return returnPlaylist
		except :
			return "no playlist"
		
		

	def add_playlist(self,playlist_name,player_id):
		pl_repo = PlaylistRepo()
		pl_repo.add(playlist_name,player_id)
