from database.models import Thread, db
from tornado.web import addslash, authenticated

from views.base import BaseHandler


class ThreadsHandler(BaseHandler):
    @addslash
    def get(self):
        if self.request.query:
            threads = Thread.filter(self.request.query_arguments)
        else:
            threads = Thread.select().order_by(Thread.created_at.desc())
        self.render('threads.html', threads=threads)


class ShowAThread(BaseHandler):
    @addslash
    def get(self, slug, thread_id):
        try:
            thread = Thread.get_by_id(thread_id)
        except Exception:
            self.write('Thread does not exist')
        else:
            self.render('show-thread.html', thread=thread)


class CreateAThread(BaseHandler):
    @addslash
    @authenticated
    def get(self):
        self.render('create-thread.html')

    def post(self):
        if not self.request.headers.get('Cookie'):  # NOTE: Just for testing
            return
        try:
            title = self.get_body_argument(
                'title') if self.get_body_argument('title') != '' else None
            body = self.get_body_argument(
                'body') if self.get_body_argument('body') != '' else None
            channel = self.get_body_argument(
                'channel') if self.get_body_argument('channel') != '' else None
            if title is None or body is None or channel is None:
                raise ValueError(
                    'ValueError: None value is not acceptable!')
            thread = Thread.create(
                title=title,
                body=body,
                channel=channel,
                user=int(self.current_user),
            )
        except ValueError as e:
            self.write(f'{e}')
            db.rollback()
        else:
            self.redirect(thread.path)
