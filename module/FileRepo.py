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

    def get_all(self,player_id):

        return self.db.query("SELECT * FROM player WHERE owner = %s ",owner)