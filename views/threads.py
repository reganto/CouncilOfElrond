from tornado.web import addslash
from views.base import BaseHandler
from models import Thread, Channel


class ThreadsHandler(BaseHandler):
    @addslash
    def get(self):
        page = self.get_query_argument('page', None)
        if page == 'create' and self.current_user:
            self.render('create-thread.html')
        try:
            threads = Thread.select().order_by(Thread.created_at.desc())
        except Exception:
            self.write('Threads does not exist!')
        else:
            self.render('threads.html', threads=threads)

    def post(self):
        if not self.request.headers.get('Cookie'):
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
        except ValueError as e:
            self.write(f'{e}')
        else:
            thread = Thread.create(
                title=title,
                body=body,
                channel=channel,
                user=self.current_user,
                )
            self.redirect(thread.path)


class SingleThreadHandler(BaseHandler):
    @addslash
    def get(self, slug, thread_id):
        try:
            thread = Thread.get(id=thread_id)
        except Exception:
            self.write('Thread does not exist')
        else:
            self.render('show-thread.html', thread=thread)


class ThreadsBelongsToAChannel(BaseHandler):
    def get(self, channel_slug=None):
        threads = None
        if channel_slug:
            try:
                threads = Thread.select().join(Channel).where(
                    Channel.slug == channel_slug).order_by(Thread.created_at.desc())  # noqa E501
            except AttributeError:
                print('Channel Does not exist!')
            else:
                self.render('threads.html', threads=threads)
