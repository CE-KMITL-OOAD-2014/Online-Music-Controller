import os
import subprocess
from FileRepo import FileRepo

class FileManagment():
    def __init__(self):
        self.file = FileRepo()

    def add(self,fileinfo,player_address):
        cwd = subprocess.Popen('pwd', stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
        location = cwd.communicate()[0]
        newline_location = location.find("\n")
        location = location[:newline_location]+"/upload/"
        # fileinfo = self.request.files['filearg'][0]
        #print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        print location + fname
        try:
            fh = open(location + fname, 'w')
            fh.write(fileinfo['body'])
            
            os.system("sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/song") #from server to player
            print "sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/song"
            print (fname + " is uploaded!! Check "+location+" folder")
            self.file.add(fname,player_address,"All")
        except :
            print "duplicate_file!!!"
            #self.finish("duplicate_file!!!")
       