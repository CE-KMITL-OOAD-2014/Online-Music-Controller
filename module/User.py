from Player import Player

class User(object):
	"""docstring for User"""
	def __init__(self, name):
		self.name = name
		self.user_player = Player("1234")

	def get_player_stat(self):

		return self.user_player.get_address()