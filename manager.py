import os.path
from module import User,Player,Command

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


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


application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/return", TestHandler)],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
	static_path=os.path.join(os.path.dirname(__file__), "static"),
	debug=True)

if __name__ == "__main__":
    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()