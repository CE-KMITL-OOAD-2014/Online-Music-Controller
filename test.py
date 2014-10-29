import unittest
from mock import Mock
from module import GetPlaylist,Player

class Foo(object):
    # instance properties    
    def next(self):
        return "next"    
    def play_song(self, argValue):
        return "play "+argValue
    def play_pause(self):
        return "pp"
    def previous(self):
        return "prev"
    def logout(self):
        pass

class TestCase(unittest.TestCase):
    def test_get_playlist(self):
        self.playlist = GetPlaylist.GetPlaylist()

        mockPL1 = Mock(get_playlist_name = "Rock")
        mockPL2 = Mock(get_playlist_name = "Pop")
        mockPL3 = Mock(get_playlist_name = "Country")
        mockPL4 = Mock(get_playlist_name = "Jazz")

        self.playlist.playlist_list.append(mockPL1)
        self.playlist.playlist_list.append(mockPL2)
        self.playlist.playlist_list.append(mockPL3)
        self.playlist.playlist_list.append(mockPL4)

        test =["Rock","Pop","Country","Jazz"]

        self.assertEqual(test, self.playlist.get_playlist())


    def test_run_command(self):
        self.player = Player.Player("1234")
        mock_remote = Foo()
        self.player.remote = mock_remote
        self.assertEqual("next", self.player.run_command("next"))
        self.assertEqual("pp", self.player.run_command("play_pause"))
        self.assertEqual("prev", self.player.run_command("previous"))
        self.assertEqual("play lalala", self.player.run_command("play","lalala"))
        self.assertRaises(IndexError,lambda:self.player.run_command())



if __name__ == '__main__':
    unittest.main()