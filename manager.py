
from module import User,Player,Command

import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket

import os
import subprocess
import hashlib

from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="myDB", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="root", help="blog database password")

clients = []


class Application(tornado.web.Application):
    def __init__(self): 
        handlers = [
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler),
            (r"/upload", FileManagment),             
            (r"/regis", RegisterHandler),               
            (r"/auth/login", LoginHandler),
            (r"/auth/logout", LogoutHandler),
            (r"/playlist", PlaylistHandler),     
            (r"/test",TestHandler)
        ]
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/auth/login",
            debug=True,
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


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html",playlist = "")

class TestHandler(BaseHandler):
    """docstring for test"""
    def get(self):
        self.render("base.html")
        


# class PlayerManagment():
#     def __init__(self,command,receiver) :
#         if command == "play_pause" :
#             #self.com = Command.PlayPause()
#             receiver.play_pause()
#         elif command == "next":
#             #self.com = Command.Next() 
#             receiver.next()
#         elif command == "previous":
#             receiver.prev()
#             #self.com = Command.Previous()
#         #self.user = User.User("Sukrit")
#         #print self.user.user_player.run_command(self.com)

"""class PlaylistManagment():
    def __init__(self):
        playlist_list =  GetPlaylist()

    def run_command(self,command):
        if command[:3] == "add" :
            try :
                playlist_list.add_playlist(command[3:])
            except :
                print "maybe to long playlist name "
        elif command[:3] == "get" :
            try :
                playlist_list.get_playlist(command[3:])
            except :
                print "can't find any playlist name "+command[3:]


"""
class PlaylistHandler(tornado.web.RequestHandler):
    def get(self):
        self.play = Player.Player("161.246.6.118")
        self.play.connect()
        renderStr = "<select>"
        playlists = self.play.run_command("get_playlist")
        for playlist in playlists :
            renderStr = renderStr+"<option value="+str(playlist)+">"+str(playlist)+"</option>"
            renderStr = renderStr+'</select><button name="selected_playlist value"="selected_playlist" onclick="OnClick("selected_playlist")"> selected_playlist </button>'
        self.render("index.html",
                playlist = renderStr
            )
    def set_render_str(self,renderString):
        self.renderStr = renderString

class FileManagment(tornado.web.RequestHandler):
    def post(self): #upload from host to server
        cwd = subprocess.Popen('pwd', stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
        location = cwd.communicate()[0]
        newline_location = location.find("\n")
        location = location[:newline_location]+"/upload/"

        player_address = "161.246.6.118"

        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        try:
            fh = open(location + fname, 'w')
            fh.write(fileinfo['body'])
            self.finish(fname + " is uploaded!! Check "+location+" folder")
            os.system("sshpass -p raspberry scp "+location+fname+" pi@"+player_address+":/home/pi/code") #from server to player
            print "sshpass -p raspberry scp /home/westlife/Desktop/scpTest/"+fname+" pi@"+player_address+":/home/pi/code"

        except :
            self.finish("duplicate_file!!!")


class RegisterHandler(BaseHandler):

    def get(self):
        self.render("regis.html")

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
            self.redirect("/")

        self.redirect("/")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.name = self.get_argument("name")
        self.password = self.get_argument("password")
        self.hash = hashlib.sha224()
        self.hash.update(self.password)
        user = self.db.get("SELECT * FROM user WHERE name = %s AND password = %s",self.name,self.hash.hexdigest())
        if not user:
            self.redirect("/")
        else:
            user_id = user["id"]
            self.set_secure_cookie("user",str(user_id))
            self.write(user["name"])

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.write("test1234")
            
class WebSocketHandler(tornado.websocket.WebSocketHandler): # Data Managment
    def open(self):
        clients.append(self)
        print 'new connection'
        self.write_message("connected")
        self.play = Player.Player("161.246.6.118")
        self.play.connect()
    
    def on_message(self, message):
        print 'message received %s' % message
        self.write_message('message received %s' % message)
        """if message != "get_playlist":
            self.play.run_command(message)
        else :
            renderStr = "<select>"
            playlists = self.play.run_command(message)
            for playlist in playlists :
                renderStr = renderStr+"<option value="+str(playlist)+">"+str(playlist)+"</option>"
            renderStr = renderStr+'</select><button name="selected_playlist value"="selected_playlist" onclick="OnClick("selected_playlist")"> selected_playlist </button>'
            plHandler = PlaylistHandler()
            plHandler.set_render_str(renderStr)
            self.redirect("/playlist")"""
        self.play.run_command(message)

    def post(self):
        var = self.get_argument('var')
        self.play_song(var)
        #self.man = User.User(var)
        #self.com = Command.PlaySong()
        #self.result =  self.man.user_player.run_command(self.com,"lalala")
        #self.write(self.result)


    def on_close(self):
        
        clients.remove(self)
        print 'connection closed' 

 

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
            
                 
if __name__ == "__main__":
    main()
