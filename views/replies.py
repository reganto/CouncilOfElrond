'''
Created on Nov 6, 2021

@author: reganto
'''
import peewee

from views.base import BaseHandler
from tornado.web import addslash
from models import Reply


class ReplyHandler(BaseHandler):
    def post(self, slug, thread_id):
        if not self.request.headers.get('Cookie'):
            return
        try:
            body = self.get_argument('body') if self.get_argument(
                'body') != '' else None
            if body is None:
                raise ValueError('ValueError: None value is not acceptable!')
        except ValueError as e:
            self.write(f'{e}')
        else:
            Reply.create(
                body=body,
                user=self.current_user.decode(),
                thread=thread_id,
            )
            self.redirect(self.reverse_url('show-thread', slug, thread_id))

    @addslash
    def get(self, thread_id):
        self.set_status(200)
        self.write('reply number '+thread_id)
