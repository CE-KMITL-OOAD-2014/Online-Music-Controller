from File import File
from FileRepo import FileRepo

class Playlist():
    def __init__(self,name,player_id):
        self.playlist_name = name 
        self.player_id = player_id
        self.file_list = []
    
    def get_playlist_name(self):
        return self.playlist_name   
    

    def get_filelist(self):
        return self.file_list

    
    def update_filelist(self,player_ip):
      self.repo = FileRepo()
      self.file_list = []
      self.files = self.repo.get_all(self.playlist_name,player_ip)
      for file_ in self.files:
        self.file_list.append(File(file_["name"]))
    
    def remove(self):
        self.close()

