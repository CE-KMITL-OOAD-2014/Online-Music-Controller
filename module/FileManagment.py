import os
import subprocess
from FileRepo import FileRepo

class FileManagment():
    def __init__(self):
        self.file = FileRepo()

    # upload file from server to player 
    def add(self,fileinfo,player_address):
        cwd = subprocess.Popen('pwd', stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
        location = cwd.communicate()[0]
        newline_location = location.find("\n")
        location = location[:newline_location]+"/upload/"
        fname = fileinfo['filename']
        print location + fname
        try:
            fh = open(location + fname, 'w')
            fh.write(fileinfo['body'])
            os.system("sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/song") #send file from server to player
            print "sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/song"
            print (fname + " is uploaded!! Check "+location+" folder")
            self.file.add(fname,player_address,"All")
        except :
            print "duplicate_file!!!"

    # delete file from player
    def remove(self,file_name,player_address):
        try:
            os.system("sshpass -p raspberry ssh -o StrictHostKeyChecking=no pi@"+player_address+" 'rm /home/pi/song/"+file_name+"'")
        except :
            print "remove is bug"
