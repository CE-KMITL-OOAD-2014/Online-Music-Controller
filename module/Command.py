from Abstract import Command

class PlayPause(Command):
    def execute(self,address) : 
        return "play/pause at "+address

class Previous(Command):
    def execute(self,address) : 
        return "Previous at "+address

class Next(Command):
    def execute(self,address) : 
        return "Next at "+address

class PlaySong(Command):
    def execute(self,address,song_name) : 
        return "play "+song_name+" now at "+address