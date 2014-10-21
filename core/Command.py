from Abstract import Command

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