from Playlist import Playlist
from PlaylistRepo import PlaylistRepo

class GetPlaylist():
    def __init__(self):
        self.repo = PlaylistRepo()
        self.playlists = []

    def get_playlist(self,player_id):
        playlist_temp = self.repo.get_all(player_id)
        for playlist in playlist_temp:
            self.playlist_temp = Playlist(playlist["playlist_name"],playlist["player_id"])
            self.playlists.append(self.playlist_temp)
        return self.playlists

    

    # def add_playlist(self,playlist_name,player_id):
    #   pl_repo = PlaylistRepo()
    #   pl_repo.add(playlist_name,player_id)
