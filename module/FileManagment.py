import os
import subprocess

class FileManagment():
    def __init__(self):
        pass

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
            
            os.system("sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/code") #from server to player
            print "sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/code"
            return (fname + " is uploaded!! Check "+location+" folder")
        except :
            return "duplicate_file!!!"
            #self.finish("duplicate_file!!!")
