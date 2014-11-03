from GetPlaylist import GetPlaylist
from File import File
import Status
from Remote import RemoteCommand

class Player():
    """docstring for Player"""
    def __init__(self, player_id):
        self.player_id = player_id
        self.playlists = GetPlaylist() 
        self.mem_status = ""
        self.ctrl_status = ""
        self.remote = RemoteCommand(player_id)
        
    def get_address(self):
        return self.player_id
    
    def connect(self):
        self.remote.login()

    def player_status(self,status):
        status.get_status(self.get_address())

    def run_command(self,*args) :

        if args[0] == "play_pause" :
            #self.com = Command.PlayPause()
            self.remote.play_pause()
        elif args[0] == "next":
            #self.com = Command.Next() 
            self.remote.next()
        elif args[0] == "previous":
            self.remote.previous()
        
        elif args[0] == "get_playlist":
            return self.playlists.get_playlist()   

        elif args[0] == "add_playlist":
            print "add_playlist"+args[1]
            self.playlists.add_playlist(args[1])

        else:
            self.remote(args[1])   


    def __del__(self):
        self.remote.logout()

            