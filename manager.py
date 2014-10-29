
from module import User,Player,Command

import torndb
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os
import subprocess
from tornado.options import define, options
define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="myDB", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="root", help="blog database password")

clients = []
__UPLOADS__ = "/home/westlife/Desktop/uploadTest/upload/"

class Application(tornado.web.Application):
    def __init__(self): 
        handlers = [
            (r"/", IndexHandler),
            (r"/ws", WebSocketHandler),
            (r"/regis", RegisterHandler),
            (r"/upload", FileManagment)               
        ]
        settings = dict(
            blog_title=u"Tornado Blog",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login",
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
        user_id = self.get_secure_cookie("cookie_user")
        if not user_id: return None
        return self.db.get("SELECT * FROM user WHERE id = %s", int(user_id))


class IndexHandler(BaseHandler):
    #@tornado.web.authenticated
    def get(self):
        self.render("index.html")


class PlayerManagment():
    def __init__(self,command) :
        if command == "play_pause" :
            self.com = Command.PlayPause()
        elif command == "next":
            self.com = Command.Next() 
        elif command == "previous":
            self.com = Command.Previous()
        self.user = User.User("Sukrit")
        print self.user.user_player.run_command(self.com)


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


class WebSocketHandler(tornado.websocket.WebSocketHandler): # Data Managment
    def open(self):
        clients.append(self)
        print 'new connection'
        self.write_message("connected")
    
    def on_message(self, message):
        print 'message received %s' % message
        self.write_message('message received %s' % message)
        PlayerManagment(message)

    def post(self):
        var = self.get_argument('var')
        self.man = User.User(var)
        self.com = Command.PlaySong()
        self.result =  self.man.user_player.run_command(self.com,"lalala")
        self.write(self.result)



class RegisterHandler(BaseHandler):

    def get(self):
        self.render("regis.html")

    def post(self):
        self.name = self.get_argument("name")
        self.mail = self.get_argument("email")
        self.password = self.get_argument("pass")
        self.db.execute(
            "INSERT INTO user (user,email,password) VALUES (self.name,self.mail,self.password)" 
            )   
        self.redirect("/")


        

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
            
                 
if __name__ == "__main__":
    main()
