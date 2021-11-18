'''
Created on Nov 6, 2021

@author: reganto
'''
from views.base import BaseHandler
from tornado.web import authenticated
from models import Reply, db


class AddAReply(BaseHandler):
    @authenticated
    def post(self, slug, thread_id):
        if not self.request.headers.get('Cookie'):
            return
        try:
            body = self.get_argument('body') if self.get_argument(
                'body') != '' else None
            if body is None:
                raise ValueError('ValueError: None value is not acceptable!')
            Reply.create(
                body=body,
                user=self.current_user.decode(),
                thread=thread_id,
            )
        except ValueError as e:
            self.write(f'{e}')
            db.rollback()
        else:
            self.redirect(self.reverse_url('show-thread', slug, thread_id))
