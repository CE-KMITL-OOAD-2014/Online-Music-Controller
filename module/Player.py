from GetPlaylist import GetPlaylist
from File import File
from Remote import RemoteCommand
from FileManagment import FileManagment
from PlayerRepo import PlayerRepo
from FileRepo import FileRepo
from Playlist import Playlist

class Player():
    """docstring for Player"""
    def __init__(self,player_ip):
        self.player_id = ""
        self.player_ip = player_ip
        self.playlists = []

        self.remote = RemoteCommand(player_ip)
        
    def get_address(self):
        return self.player_ip
    
    def connect(self):
        self.remote.login()

    def player_status(self):
        return self.remote.get_status()

    def set_player_id(self,player_id):
        self.player_id = player_id

    def run_command(self,*args) :
        
        # args[0] is command 

        if args[0] == "play_pause" :
            return self.remote.play_pause()
        
        elif args[0] == "next":
            return self.remote.next()
        
        elif args[0] == "previous":
            return self.remote.previous()
        
        elif args[0] == "add_playlist":
            playlist_name = args[1]
            player_id = args[2]
            playlist_repo = GetPlaylist()
            playlist_repo.add_playlist(playlist_name,player_id)

        elif args[0] == "delete_file_pl":
            playlist_name = args[1]
            file_repo = FileRepo()
            file_repo.delete_from_playlist(self.player_ip,playlist_name)

        elif args[0] == "add_file_to_pl":
            file_name = args[1]
            playlist_name = args[2]
            file_repo = FileRepo()
            file_repo.add(file_name,self.player_ip,playlist_name)

        elif args[0] == "get_playlist_songs":
            playlist_name = args[1]
            player_id = args[2]
            pl = Playlist(playlist_name,player_id)
            pl.update_filelist(self.player_ip)
            file_list =  pl.get_filelist()
            return_list = []
            for song in file_list:
                return_list.append(song.get_file_name())
            return return_list

        elif args[0] == "remove":
            file_management = FileManagment()
            file_name = args[1]
            file_management.remove(file_name,self.player_ip)
            file_repo = FileRepo()
            file_repo.delete_file(file_name,self.player_ip)

        else:
            #Play Song 
            file_queue = []
            check = 1
            file_list = args[2]
            file_name = args[1]
            for file_ in file_list:
                if check and  file_.get_file_name() != file_name:
                    pass
                else:
                    check = 0
                    file_queue.append(file_.get_file_name())
            return self.remote.play_song(file_queue)


    def add_file(self,file):
        self.adder = FileManagment()
        self.adder.add(file,self.player_ip)

    def add(self,user) :
        self.player = PlayerRepo()   
        self.player.add(self.player_id,self.player_ip,user)

    def get_playlist(self):
        return self.playlists 

    def set_playlist(self,playlist_name):
        for playlist in self.playlists:
            if playlist.get_playlist_name() == playlist_name:
                return playlist
        return None

    def update_playlist(self):
        playlist_repo = GetPlaylist()
        self.playlists = playlist_repo.get_playlist(self.player_id)

    def __del__(self):
        self.remote.logout()

            