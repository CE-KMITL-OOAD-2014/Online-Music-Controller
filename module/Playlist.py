from File import File
from FileRepo import FileRepo
class Playlist():
	def __init__(self,name):
		self.playlist_name = name 
		self.file_list = []
    
	def get_playlist_name(self):
		return self.playlist_name   
    
	def get_filelist(self,player_ip):
		file_repo = FileRepo()
		return file_repo.get_from_playlist(player_ip,self.playlist_name)

    
	def update_playlist(self,songs_name):
		for song in songs_name :
			self.file_list[len(self.file_list)] = File(song)
    
	def remove(self):
		self.close()

