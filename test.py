import unittest
from module import Player,Command,User

class TestCase(unittest.TestCase):


    def test_player(self):
        # make sure the shuffled sequence does not lose any elements
        self.player = Player.Player("1612224")
        self.assertEqual("1612224", self.player.get_address())

        # should raise an exception for an immutable sequence
        #self.assertRaises(BaseException, self.player.get_address(1))

    def test_user(self):
        self.user = User.User("name")
        self.assertEqual("1234",self.user.get_player_stat())

    def test_playpause(self):
        self.pp = Command.PlayPause()
        self.assertEqual("play/pause at 12221",self.pp.execute("12221"))

    def test_playsong(self):
        self.pp = Command.PlaySong()
        self.assertEqual("play lalala now at 12221",self.pp.execute("12221","lalala"))

    def test_Next(self):
        self.pp = Command.Next()
        self.assertEqual("Next at 12221",self.pp.execute("12221"))

    def test_Previous(self):
        self.pp = Command.Previous()
        self.assertEqual("Previous at 12221",self.pp.execute("12221"))

    def test_command(self):
        self.com = Player.Player("12221")
        self.exCommand = Command.Previous()
        self.assertEqual("Previous at 12221",self.com.run_command(self.exCommand))



if __name__ == '__main__':
    unittest.main()