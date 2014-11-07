import torndb

class PlayerRepo(object):
    """docstring for Repository"""
    def __init__(self):
        self.db = torndb.Connection(
            host="127.0.0.1:3306", database="myDB",
            user="root", password="root")

    def add(self,mac,ip,owner):

        try:
            self.db.execute(
                "INSERT INTO player (mac,ip,owner) VALUES (%s,%s,%s)",mac,ip,owner
                )
            self.db.execute(
                "INSERT INTO playlist (playlist_name,player_id) VALUES ('All',%s)",mac
                )
        except :
            print "bug"

    def get_all(self,owner):

        return self.db.query("SELECT * FROM player WHERE owner = %s ",owner)






    
        
