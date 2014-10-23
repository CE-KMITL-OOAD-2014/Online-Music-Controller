import os.path
from module import User,Player,Command

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)

 
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
        


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/ws", WebSocketHandler),
    (r"/return", TestHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
	debug=True)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()