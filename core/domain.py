from abc import ABCMeta, abstractmethod

#############################----Command Class----###################################
class Command:
    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self):
        pass

class PlayPause(Command):
    def execute(self,address) : 
        print "play/pause at "+address

class Previous(Command):
    def execute(self,address) : 
        print "Previous at "+address

class Next(Command):
    def execute(self,address) : 
        print "Next at "+address

class PlaySong(Command):
    def execute(self,address,song_name) : 
        print "play "+song_name+" now at "+address

####################################################################################
#############################----GetPlayerStatus Class----##########################
class GetPlayerStatus():
	"""docstring for GetPlayerStatus"""
	__metaclass__ = ABCMeta
    
    @abstractmethod
	def get_status(self) :
		pass

class ControlStatus(GetPlayerStatus):
	"""docstring for ControlStatus"""
	def get_status(self,address):
		print "get Control status"

class MemoryStatus(GetPlayerStatus):
	"""docstring for ControlStatus"""
	def get_status(self,address):
		print "get Memory status"		
		
class QueueStatus(GetPlayerStatus):
	"""docstring for ControlStatus"""
	def get_status(self,address):
		print "get Queue status"		
	





####################################################################################
#############################----GetPlaylist Class----##############################
class GetPlaylist():
    def __init__(self):
        self.playlist_list = Playlist[]
    def get_playlist(self,name):
        return self.playlist_list[0]
    def add_playlist(self,name):
        self.playlist_list[arr(self.playlist_list)] = Playlist(name)
    
class Playlist():
    def __init__(self,name):
        self.playlist_name = name 
        self.file_list = File[]
    
    def get_playlist_name(self):
        return self.playlist_name   
    
    def get_filelist(self):
        return self.file_list
    
    def update_playlist(self,songs_name):
        for song in songs_name :
            self.file_list[len(self.file_list] = File(song)
    
    def remove(self):
        self.close()

class File():
    def __init__(self,name):
        self.file_name = name
    def get_file_name(self):
        return self.file_name
####################################################################################
#############################----Player Class----###################################
class Player():
	"""docstring for Player"""
	def __init__(self, player_id):
		self.player_id = player_id
		self.player_list = [] 
		self.status = ""

	def get_address(self):
		return self.player_id
    
	def run_command(self,*args):
		if len(args) == 1:
			args[0].execute(self.get_address())
		elif len(args) == 2:
			args[0].execute(self.get_address(),args[1])    

####################################################################################
#############################----User Class----###################################
class User(object):
	"""docstring for User"""
	def __init__(self, name):
		self.name = name
		self.user_player = Player("1234")

	def get_player_stat(self):

		print self.user_player.get_address()

####################################################################################


if __name__ == '__main__':
	print "HHH"
	user_temp = User("Sukrit")
	user_temp.get_player_stat()

	player = Player("1234")
	play_command = PlayPause()
	next_command = Next()
	play_song_command = PlaySong()
	player.run_command(play_command)
	player.run_command(play_song_command,"lalala")

		
		
		
