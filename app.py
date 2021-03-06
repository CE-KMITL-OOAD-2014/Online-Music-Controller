from module import User,Player
from module.PlayerRepo import PlayerRepo

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

import torndb
import json
import hashlib
import subprocess
import os


from tornado.options import define, options
define("port", default=443, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="myDB", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="root", help="blog database password")

clients = []

class Application(tornado.web.Application):
    def __init__(self): 

        # all route 
        handlers = [
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler),
            (r"/upload", FileManagment),             
            (r"/regis", RegisterHandler),               
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/edit", EditPlaylistHandler),     
            (r"/account",AccountHandler),
            (r"/setplayer",SetPlayerHandler),
            (r"/nowplay",SongAPIHandler),
            (r"/listplayer",PlayerAPIHandler),
            (r"/addplayer",AddPlayerHandler),
            (r"/remove",RemoveHandler),

        ]
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            
            xsrf_cookies=False,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/auth/login",
            debug=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = torndb.Connection(
            host=options.mysql_host, database=options.mysql_database,
            user=options.mysql_user, password=options.mysql_password) 


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("user")
        if not user_id: return None
        return self.db.get("SELECT * FROM user WHERE id = %s", int(user_id))

    def get_current_player(self):
        player_id = self.get_secure_cookie("player")
        if not player_id: return None
        return self.db.get("SELECT * FROM player WHERE id = %s", int(player_id))


# first page handler 
# render web page to user
class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        player =  self.get_current_player()
        if not player:
            self.redirect("/setplayer")
        else:
            player_temp = Player.Player(player.ip)
            player_temp.set_player_id(player.mac)
            player_temp.update_playlist()
            user = self.get_current_user()
            playlist_temp = player_temp.set_playlist("All")
            playlist_temp.update_filelist(player.ip)
            files = playlist_temp.get_filelist()
            self.render("index.html",page_title ="Controller",player_ip = player.ip,dest ="/account",brand = user.name,playlists = player_temp.get_playlist(),files = files,temp_id = player.mac)


# account page handler
# render account setting page
class AccountHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        player =  self.get_current_player()

        if not player:
            self.render("account.html",page_title = "Accout Manager",user="test",player_ip = "no player",dest ="/",brand = "Controller")
        else:
            self.render("account.html",page_title = "Accout Manager",user = "test",player_ip = player["ip"],dest ="/",brand = "Controller")


# remove file handler
# get method for render page to user so user can pick a file they want to remove from selected player
# post method for get a selected file's name and remove it 
class RemoveHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        player =  self.get_current_player()

        if not player:
            self.redirect("/setplayer")
        else:
            player_temp = Player.Player(player.ip)
            player_temp.set_player_id(player.mac)
            player_temp.update_playlist()
            user = self.get_current_user()
            playlist_temp = player_temp.set_playlist("All")
            playlist_temp.update_filelist(player.ip)
            files = playlist_temp.get_filelist()
            self.render("remove.html",page_title ="Controller",player_ip = player.ip,dest ="/account",brand = user.name,files = files)

    def post(self):
        player_ip = self.get_argument("player_ip")
        player_temp = Player.Player(player_ip)
        player_temp.run_command("remove",self.get_argument("filename"))
        self.redirect("/account")


# select player handler
# get method for render select player page 
## user with no player are redirect to add player page
# post method for add user's player to cookie

class SetPlayerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.get_secure_cookie("user")
        self.user = User.User(user_id)
        self.user.update_player_list()
        player_temp = self.user.get_players()
        if not player_temp:
            self.redirect("/account")
        else:
            self.render(
                    "player_list.html",
                    brand = "Controller",
                    page_title = "Choose Player",
                    players = player_temp,
                    dest ="/"
                )

    def post(self):
        player_ip =  self.get_argument("player")   
        player = self.db.get("SELECT * FROM player WHERE ip = %s ",player_ip)
        if not player:
            self.redirect("/")                                    #if dont have player in db
        else:
            player_id = player["id"]
            self.set_secure_cookie("player",str(player_id))        # have player in db and set player cookie
            self.redirect("/")


# post method for get file_name_list from user and update playlist 

class EditPlaylistHandler(tornado.web.RequestHandler):

    def post(self):
        player_ip = self.get_argument("edpl_ip")
        player_id = self.get_argument("edpl_id")
        self.play = Player.Player(player_ip)
        self.play.connect()
        player_id = player_id
        pl_name = self.get_argument("playlist_temp")
        try:
            song_list =  self.request.arguments['selected_song']
            self.play.run_command("delete_file_pl",pl_name)
            for song in song_list:
                self.play.run_command("add_file_to_pl",song,pl_name)
        except:
            self.play.run_command("delete_file_pl",pl_name)
        self.redirect("/")

# get playlist's files and return to user

class EditPlaylist():
    def __init__(self,player_ip,player_id):
        self.play = Player.Player(player_ip)
        self.play.connect()
        self.player_id = player_id


    def get_song_list(self,pl_name):
        playlist_name = pl_name
        song_list = self.play.run_command('get_playlist_songs',playlist_name,self.player_id)       
        return song_list

# post method use for get file from user and upload to player

class FileManagment(tornado.web.RequestHandler):
    def post(self): #upload from host to server
        fileinfo = self.request.files['filearg'][0]
        player_ip = self.get_argument("player")
        self.player = Player.Player(player_ip)
        self.player.add_file(fileinfo)
        self.redirect("/account")

# return now playing song to user

class SongAPIHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        player =  self.get_current_player()
        if not player:
            self.write("<script>alert('No current player');</script>")
            self.redirect("/")
        else:
            player_temp = Player.Player(player.ip)

            try:
                player_temp.connect()
            except:
                pass
            status = player_temp.player_status()
            self.write(status)

# return user's players information

class PlayerAPIHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = self.get_secure_cookie("user")
        self.user = User.User(user_id)
        self.user.update_player_list()
        player_temp = self.user.get_players()
        if not player_temp:
            self.write("<script>alert('No your own player');</script>")
            self.redirect("/")
        else:
            player_json = json.dumps(player_temp,default = jdefault)
            self.write(player_json)

# websocket handler
# open and close websocket between client and server
# get command from user and run process

class WebSocketHandler(tornado.websocket.WebSocketHandler): 
    def open(self):
        clients.append(self)
        print 'new connection'
        self.write_message("connected")
        self.isEdit = True
        self.pl_temp = ""
    
    def on_message(self, message):
        self.write_message('message received %s' % message)
        if message.find("open") == 0:
            self.play = Player.Player(message[5:])
            self.files = []
            try:
                self.play.connect()
            except:
                self.write_message('error')  #if player not online  send msg to redirect to setplayer

        elif message.find("#id: ") == 0:
            self.play.set_player_id(message[5:])
            self.play.update_playlist()
            playlist_temp = self.play.set_playlist("All")
            playlist_temp.update_filelist(self.play.get_address())
            self.files = playlist_temp.get_filelist()
        elif message.find("editpl") == 0:
            pl_name = message[6:]
            if (pl_name != self.pl_temp) and self.isEdit==False:
                self.isEdit = True
            if self.isEdit:
                self.isEdit = False
                self.pl_temp = pl_name
                edit_playlist = EditPlaylist(self.play.player_ip,self.play.player_id)
                song_list = edit_playlist.get_song_list(pl_name)
            
                all_song_list = edit_playlist.get_song_list("All")
                write_str = ""
                for song in all_song_list:
                    if song in song_list:
                        check = "checked"
                    else:
                        check = ""
                    write_str = write_str+"<input type='checkbox' name='selected_song' value='"+song+"'"+check+">"+song+"<br>"
                self.write_message("sos"+write_str)
                
            else:
                print "Duplicate"

        elif message.find("addpl") == 0:
            self.play.run_command("add_playlist",message[6:],self.play.player_id)

        elif message.find("loadpl") == 0:
            playlist_name = message[7:]
            playlist_temp = self.play.set_playlist(playlist_name)
            playlist_temp.update_filelist(self.play.get_address())
            self.files = playlist_temp.get_filelist()
            file_json = json.dumps(self.files,default = jdefault)
            self.write_message(file_json)
        
        elif message.find("#play") != 0:
            self.play.run_command(message)

        else:
            self.play.run_command("play",message[6:],self.files)

    def on_close(self):
        
        clients.remove(self)
        print 'connection closed' 


class AddPlayerHandler(BaseHandler):

    def post(self):
        self.mac =  self.get_argument("mac")
        self.ip =  self.get_argument("ip")
        user_id = self.get_secure_cookie("user")
        self.player = Player.Player(self.ip)
        self.player.set_player_id(self.mac)
        try:
            self.player.add(user_id)
        except:
            self.render("wrong.html")
        self.redirect("/account")



class RegisterHandler(BaseHandler):

    def get(self):
        self.render("regis.html",status="")

    def post(self):
        self.name = self.get_argument("name")
        self.mail = self.get_argument("email")
        self.password = self.get_argument("password")
        self.hash = hashlib.sha224()
        self.hash.update(self.password)
        try:
            self.db.execute(
                "INSERT INTO user (name,email,password) VALUES (%s,%s,%s)",self.name,self.mail,self.hash.hexdigest()
                )
        except :
            self.render("regis.html",status ="username or email has already taken !!")

        self.redirect("/")


class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html',status="")

    def post(self):
        self.name = self.get_argument("name")
        self.password = self.get_argument("password")
        self.hash = hashlib.sha224()
        self.hash.update(self.password)
        user = self.db.get("SELECT * FROM user WHERE name = %s AND password = %s",self.name,self.hash.hexdigest())
        if not user:
            self.render("login.html",status ="username or password invalid !!")
        else:
            user_id = user["id"]
            self.set_secure_cookie("user",str(user_id))
            self.redirect("/setplayer")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.clear_cookie("player")
        self.clear_cookie("playlist")
        self.render("logout.html")

def SendStatus():
    for c in clients:
        status =  c.play.player_status()
        c.write_message("status "+status)

def jdefault(o):
    if isinstance(o, set):
        return list(o)
    return o.__dict__


# run server and set SendStatus() period (1 sec)
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),ssl_options = {
            "certfile": os.path.join("../cert/","server.crt"),
            "keyfile": os.path.join("../cert/","server.key"),
            })
    http_server.listen(options.port)
    scheduler = tornado.ioloop.PeriodicCallback(SendStatus, 1000)
    scheduler.start()
    tornado.ioloop.IOLoop.instance().start()
            
                 
if __name__ == "__main__":
    main()
