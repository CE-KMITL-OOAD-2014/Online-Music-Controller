import paramiko

# send real command to control player 
class RemoteCommand(object):
    def __init__(self, player_ip):
        self.player_ip = player_ip
        self.cmd = "sudo /etc/init.d/mediatomb restart"
        self.remote = paramiko.SSHClient()
        self.remote.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def login(self):
        self.remote.connect(self.player_ip,username = "pi",password = "raspberry")
        stdin, stdout, stderr = self.remote.exec_command('mpc update')
    def logout(self):
        self.remote.close()

    def play_song(self,songs):
        stdin, stdout, stderr = self.remote.exec_command('mpc clear')
        for song in songs:
            comm = "mpc add "+song
            stdin, stdout, stderr = self.remote.exec_command(comm)
        stdin, stdout, stderr = self.remote.exec_command('mpc play')

    def play_pause(self):
        stdin, stdout, stderr = self.remote.exec_command('mpc status')
        print stdout.readline()
        status = stdout.read()
        if status.find("[playing]") != -1:
            stdin, stdout, stderr = self.remote.exec_command('mpc pause')
        elif status.find("[paused]") != -1:
            stdin, stdout, stderr = self.remote.exec_command('mpc play')

    def previous(self):
        stdin, stdout, stderr = self.remote.exec_command('mpc prev')
        stdin, stdout, stderr = self.remote.exec_command('mpc status')
        print stdout.readline()

    def next(self):
        stdin, stdout, stderr = self.remote.exec_command('mpc next')
        stdin, stdout, stderr = self.remote.exec_command('mpc status')
        print stdout.readline()  

    def get_status(self):
        stdin, stdout, stderr = self.remote.exec_command('mpc status')
        status = stdout.readline()
        print status
        if status.find(".mp3") != -1:
            return status
        elif status.find(".wav") != -1:
            return status
        return "Idle"
