from module import Player,User,Command,Status

if __name__ == '__main__':
	print "HHH"
	user_temp = User.User("Sukrit")
	user_temp.get_player_stat()

	player = Player.Player("1234")
	play_command = Command.PlayPause()
	next_command =  Command.Next()
	play_song_command =  Command.PlaySong()
	player.run_command(play_command)
	player.run_command(play_song_command,"lalala")
	ctrl = Status.ControlStatus()
	mem = Status.MemoryStatus()
	player.player_status(ctrl)
	player.player_status(mem)