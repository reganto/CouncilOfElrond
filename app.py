import tornado.web
import tornado.ioloop
from tornado.options import parse_command_line, options, define

from routes import routes as Routes
from settings import SETTINGS

define("port", default=8000, type=int, help="run on the given port")


class Application(tornado.web.Application):
    def __init__(self):
        super().__init__(Routes, **SETTINGS)


if __name__ == "__main__":
    parse_command_line()
    Application().listen(options.port)
    tornado.ioloop.IOLoop.current().start()

