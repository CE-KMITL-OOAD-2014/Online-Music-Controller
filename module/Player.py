from GetPlaylist import GetPlaylist
from File import File
import Status
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

        if args[0] == "play_pause" :
            #self.com = Command.PlayPause()
            return self.remote.play_pause()
        elif args[0] == "next":
            #self.com = Command.Next() 
            return self.remote.next()
        elif args[0] == "previous":
            return self.remote.previous()
        
        # elif args[0] == "get_playlist":
        #     return self.playlists.get_playlist(args[1])   

        elif args[0] == "add_playlist":
            playlist_repo = GetPlaylist()
            print "add_playlist "+args[1]
            playlist_repo.add_playlist(args[1],args[2])

        elif args[0] == "delete_file_pl":
            file_repo = FileRepo()
            file_repo.delete_from_playlist(self.player_ip,args[1])

        elif args[0] == "add_file_to_pl":
            file_repo = FileRepo()
            file_repo.add(args[1],self.player_ip,args[2])

        elif args[0] == "get_playlist_songs":
            pl = Playlist(args[1],args[2])
            pl.update_filelist(self.player_ip)
            file_list =  pl.get_filelist()
            return_list = []
            for song in file_list:
                return_list.append(song.get_file_name())
            return return_list

        elif args[0] == "remove":
            file_management = FileManagment()
            file_management.remove(args[1],self.player_ip)

        else:
            file_qeue = []
            check = 1
            for file_ in args[2]:
                if check and  file_.get_file_name() != args[1]:
                    pass
                else:
                    check = 0
                    file_qeue.append(file_.get_file_name())
            return self.remote.play_song(file_qeue)


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

            