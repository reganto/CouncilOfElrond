from filters.base import BaseFilter
import database.models as models


class ThreadFilter(BaseFilter):
    def __init__(self, upcoming_filters):
        super().__init__(upcoming_filters)
        self.expected_filters = ['by', 'channel', 'popular']

    def by(self, username):
        threads = models.Thread.select().join(models.User) \
                        .where(models.User.username == username) \
                        .order_by(models.Thread.created_at.desc())
        return threads

    def channel(self, channel_slug):
        threads = models.Thread.select().join(models.Channel) \
                        .where(models.Channel.slug == channel_slug) \
                        .order_by(models.Thread.created_at.desc())
        return threads

    def popular(self, state=1):
        """Popular threads filter

        :param state: state parameter has no thing to do it's value
         of `popular` query string, defaults to 1
        :type state: int, optional
        :return: this filter returns threads based on popularity of them
         popularity measure is number of thread's replies.
        :rtype: models.Thread
        """
        from peewee import fn
        threads = (
            models.Thread.select(
                models.Thread.id,
                models.Thread.title,
                models.Thread.body,
                models.Thread.created_at,
                models.Thread.user_id,
                models.Thread.channel_id,
                fn.COUNT(models.Reply.thread_id)).join(models.Reply).where(
                    models.Thread.id == models.Reply.thread_id
                ).group_by(
                    models.Thread.id,
                    models.Reply.thread_id
                ).order_by(fn.COUNT(models.Reply.thread_id).desc()))
        return threads
