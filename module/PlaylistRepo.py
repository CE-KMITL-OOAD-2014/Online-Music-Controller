import torndb

class PlaylistRepo(object):
    """docstring for Repository"""
    def __init__(self):
        self.db = torndb.Connection(
            host="127.0.0.1:3306", database="myDB",
            user="root", password="root")

    def add(self,playlist_name,player_id):

        try:
            if self.db.execute("SELECT * FROM playlist WHERE playlist_name=%s AND player_id=%s",playlist_name,player_id) :
                print "duplicate playlist"

            else : 
                self.db.execute(
                    "INSERT INTO playlist (playlist_name,player_id) VALUES (%s,%s)",playlist_name,player_id
                    )
                print "succeed"
        except :
            print "bug"

    def get_all(self,player_id):

        return self.db.query("SELECT * FROM playlist WHERE player_id = %s ",player_id)

    





    
        
