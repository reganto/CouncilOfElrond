'''
Created on Nov 6, 2021

@author: reganto
'''
from views.base import BaseHandler
from tornado.web import authenticated
from database.models import Reply, Thread, db


class AddAReply(BaseHandler):
    @authenticated
    def post(self, slug, thread_id):
        if not self.request.headers.get('Cookie'):  # NOTE: Testing
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


class RepliesPagination(BaseHandler):
    def post(self):
        """Pagination for replies"""
        state = self.get_body_argument('state')
        thread_id = self.get_body_argument('thread_id')
        thread = Thread.get_by_id(int(thread_id))
        if self.get_cookie('current_reply_page_number'):
            page_number = int(self.get_cookie('current_reply_page_number'))
        else:
            self.set_cookie('current_reply_page_number', '1'.encode())
        replies = ''
        if int(state) == 1:  # Next Page
            replies = thread.replies.paginate(page_number + 1, 7)
            if len(replies) == 0:
                return
            number = int(self.get_cookie('current_reply_page_number'))
            number += 1
            self.set_cookie(
                'current_reply_page_number',
                str(number).encode())
        elif int(state) == -1:  # Prev Page
            number = int(self.get_cookie('current_reply_page_number'))
            if number == 1:  # First page of replies
                return
            replies = thread.replies.paginate(page_number-1, 7)
            number -= 1
            self.set_cookie(
                'current_reply_page_number',
                str(number).encode())
        else:
            return  # Unsupported state
        data = {}
        for reply in replies:
            data[reply.id] = {
                'body': reply.body,
                'user': reply.user.username.capitalize(),
                'thread': reply.thread.id,
                'created_at': reply.created_at.strftime("%d, %b %Y %H:%M")
            }
        self.write(data)
