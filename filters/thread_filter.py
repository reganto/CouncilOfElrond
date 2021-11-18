from filters.base import BaseFilter
import database.models as models


class ThreadFilter(BaseFilter):
    def __init__(self, upcoming_filters):
        super().__init__(upcoming_filters)
        self.expected_filters = ['by', 'channel']

    def by(self, username):
        threads = models.Thread.select().join(models.User).where(
            models.User.username == username).order_by(models.Thread.created_at.desc())  # noqa E501
        return threads

    def channel(self, channel_slug):
        threads = models.Thread.select().join(models.Channel).where(
            models.Channel.slug == channel_slug).order_by(models.Thread.created_at.desc())  # noqa E501
        return threads
