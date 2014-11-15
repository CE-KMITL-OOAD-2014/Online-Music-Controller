import unittest
from mock import Mock
from module import Playlist,Player,File

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
    def test_get_file_list(self):
        self.playlist = Playlist.Playlist("test","1234")

        mockPL1 = Mock(get_file_name = "a")
        mockPL2 = Mock(get_file_name = "b")
        mockPL3 = Mock(get_file_name = "c")
        mockPL4 = Mock(get_file_name = "d")

        self.playlist.file_list.append(mockPL1)
        self.playlist.file_list.append(mockPL2)
        self.playlist.file_list.append(mockPL3)
        self.playlist.file_list.append(mockPL4)

        test =[mockPL1 ,mockPL2 ,mockPL3 ,mockPL4]

        self.assertEqual(test, self.playlist.get_filelist())


    def test_run_command(self):
        self.player = Player.Player("1234")
        mock_remote = Foo()
        self.player.remote = mock_remote
        self.assertEqual("next", self.player.run_command("next"))
        self.assertEqual("pp", self.player.run_command("play_pause"))
        self.assertEqual("prev", self.player.run_command("previous"))
        self.assertRaises(IndexError,lambda:self.player.run_command())



if __name__ == '__main__':
    unittest.main()