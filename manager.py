import os.path
from module import User,Player,Command

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import torndb
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:8080", help="blog database host")
define("mysql_database", default="myDB", help="blog database name")
define("mysql_user", default="root", help="blog database user")
define("mysql_password", default="root", help="blog database password")
 
clients = []

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class TestHandler(tornado.web.RequestHandler): 
	def post(self):
		var = self.get_argument('var')
		self.man = User.User(var)
		self.com = Command.PlaySong()
		self.resualt =  self.man.user_player.run_command(self.com,"lalala")
		self.write(self.resualt)

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

class RegisterHandler(tornado.web.RequestHandler):
	self.db = torndb.Connection(
		host=options.mysql_host, database=options.mysql_database,
		user=options.mysql_user, password=options.mysql_password)

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
     		
     		     


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", WebSocketHandler),
    (r"/regis", RegisterHandler),
    (r"/return", TestHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
	debug=True)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()