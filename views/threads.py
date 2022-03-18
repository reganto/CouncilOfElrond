from database.models import Thread, Reply, db
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


class ThreadsManager(BaseHandler):
    """Threads manager. [get, post, delete, update] threads

    :param BaseHandler: Base handler for our route handler classes
    :type BaseHandler: tornado.web.RequestHandler
    :raises ValueError: [description]
    """
    @addslash
    def get(self, slug, thread_id):
        try:
            thread = Thread.get_by_id(thread_id)
        except Exception:
            self.write('Thread does not exist')
        else:
            # reset replies pagination cookie
            if self.get_cookie('current_reply_page_number'):
                self.set_cookie('current_reply_page_number', '1'.encode())
            self.render('show-thread.html', thread=thread)

    @addslash
    @authenticated  # unauthenticated user
    def delete(self, slug: str, thread_id: int):
        """Delete a thread

        :param slug: slug of thread's channel
        :type slug: str
        :param thread_id: simply thread's id
        :type thread_id: int
        :raises ValueError: [description]
        """

        # unauthorized user
        # TODO: can we abstract user authorization
        # to single authorize function?
        self.current_user = int(self.request.headers.get('Uid', 0))
        thread = Thread.get_by_id(thread_id)
        if thread.user_id != self.current_user:
            self.set_status(302)
            return

        replies = Reply.select().join(Thread) \
            .where(Thread.id == thread_id)
        # TODO: can we delete all replies in one transaction?
        # TODO: can we abstract thread deletion in a single
        # Thread delete method?
        for reply in replies:
            reply.delete().execute()
        thread.delete().where(Thread.id == thread_id).execute()
        self.set_status(204)


class CreateAThread(BaseHandler):
    @addslash
    @authenticated
    def get(self):
        self.render('create-thread.html')

    def post(self):
        if not self.request.headers.get('Cookie'):  # NOTE: Just for testing
            return
        try:
            title = self.get_body_argument('title')
            body = self.get_body_argument('body')
            channel = self.get_argument('channel')
        except ValueError as e:
            self.write('An Error occured. please try again.')
            print('Error: ', e)
            db.rollback()
        else:
            thread = Thread.create(
                title=title,
                body=body,
                channel=channel,
                user=int(self.current_user),
            )
            self.redirect(thread.path)
