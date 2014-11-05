from Player import Player
from PlayerRepo import PlayerRepo

class User(object):
	"""docstring for User"""
	def __init__(self, user_id):
		self.name = ""
		self.user_id = user_id
		self.player_list = []

	def update_player_list(self):

		self.player_list[:] = []
		self.repo = PlayerRepo()
		self.players = self.repo.get_all(self.user_id)
		
		for player in self.players:
			player_temp = Player(player['ip'])
			player_temp.set_player_id(player['mac'])
			self.player_list.append(player_temp)

	def get_players(self):
		return self.player_list