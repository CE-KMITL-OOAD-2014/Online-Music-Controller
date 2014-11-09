import torndb

class FileRepo(object):
    """docstring for Repository"""
    def __init__(self):
        self.db = torndb.Connection(
            host="127.0.0.1:3306", database="myDB",
            user="root", password="root")

    def add(self,name,player_ip,playlist):

        try:
            self.db.execute(
                "INSERT INTO file (name,player_ip,playlist) VALUES (%s,%s,%s)",name,player_ip,playlist
                )
        except :
            print "bug"



    def get_from_playlist(self,player_ip,playlist_name):
        print player_ip
        print playlist_name
        try:
            return self.db.query("SELECT * FROM file WHERE player_ip = %s AND playlist = %s",player_ip,playlist_name)
        except Exception:
            print "bug"
            return "bug"
            

    def get_all(self,playlist_name,player_ip):

        return self.db.query("SELECT * FROM file WHERE playlist = %s AND  player_ip = %s ",playlist_name,player_ip)

