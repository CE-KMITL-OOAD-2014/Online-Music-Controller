from GetPlaylist import GetPlaylist
from File import File
import Status
import Command

class Player():
	"""docstring for Player"""
	def __init__(self, player_id):
		self.player_id = player_id
		self.player_list = [] 
		self.mem_status = ""
		self.ctrl_status = ""

	def get_address(self):
		return self.player_id
    
	def run_command(self,*args):
		if len(args) == 1:
			return args[0].execute(self.get_address())
		elif len(args) == 2:
			return args[0].execute(self.get_address(),args[1])    

	def player_status(self,status):
		status.get_status(self.get_address())
		    