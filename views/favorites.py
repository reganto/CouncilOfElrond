from tornado.web import authenticated

from views.base import BaseHandler
from database.models import Favorite, User, Reply, db


class RepliesFavorites(BaseHandler):
    @authenticated
    def post(self, reply_id):
        try:
            Favorite.create(
                favorite_type='Reply',
                user=User.get_by_id(int(self.current_user.decode())),
                reply=reply_id,
            )
            self.redirect(self.get_argument('pathname')) 
        except Exception as e:
            db.rollback()
            self.write('You already favorite this reply!')

