from filters.base import BaseFilter
from models import User, Thread


class ThreadFilter(BaseFilter):
    def __init__(self, request):
        super().__init__(request)
        self.filters = ['by', 'popular']

    def by(self, username):
        threads = Thread.select().join(User).where(
            User.username == username).order_by(Thread.created_at.desc())
        return threads
