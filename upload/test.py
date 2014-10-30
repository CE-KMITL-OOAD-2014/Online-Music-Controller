from abc import ABCMeta, abstractmethod
class Animal:
    __metaclass__ = ABCMeta
    @abstractmethod
    def say_something(self) : 
        return "I'm sus"
        
class Cat(Animal):
    def say_something(self) : 
        s = super(Cat,self).say_something()
        return "%s - %s" % (s, "Miauuu")

class Dog(Animal):
    def say_something(self) : 
        s = super(Dog,self).say_something()
        return "%s - %s" % (s, "Hong Kong")

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



class Player():
	"""docstring for Player"""
	def __init__(self, player_id):
		self.player_id = player_id
		self.player_list = [] 
		self.status = ""

	def get_address(self):
		return self.player_id
    
	def run_command(self,command):
		command.execute(self.get_address())
        
	def run_command(self,command,song_name):
		command.execute(self,get_address,song_name)    

class User(object):
	"""docstring for User"""
	def __init__(self, name):
		self.name = name
		self.user_player = Player("1234")

	def get_player_stat(self):

		print self.user_player.get_address()


if __name__ == '__main__':
	print "HHH"
	user_temp = User("Sukrit")
	user_temp.get_player_stat()

	player = Player("1234")
	play_command = PlayPause()
	next_command = Next()
	player.run_command(play_command)

		
		
		
