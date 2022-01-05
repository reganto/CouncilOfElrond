from .base import BaseHandler
from database.models import User
from tornado.web import addslash


class profilesHandler(BaseHandler):
    @addslash
    def get(self, username):
        user = User.select().where(User.username==username).first()
        self.render('profiles/show.html', profile_user=user)

