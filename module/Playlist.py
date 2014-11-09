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
    
    def update_filelist(self):
      self.repo = FileRepo()
      self.files = self.repo.get_all(self.playlist_name,"161.246.5.47")
      for file in self.files:
          self.file_list.append(File(file["name"]))
    
    def remove(self):
        self.close()

