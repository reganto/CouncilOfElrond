"""
Created on Nov 6, 2021

@author: reganto
"""
from tornado.web import Application

from tests.base import BaseTest
from database.models import migrator, Thread, Channel
from database.model_factory import Factory


class ChannelTest(BaseTest):
    def get_app(self):
        return Application()

    def setUp(self):
        super().setUp()
        migrator.upgrade()

    def tearDown(self):
        super().tearDown()
        migrator.downgrade()

    def test_a_channel_consist_of_a_thread(self):
        thread = Factory(Thread).create()
        channel = Factory(Channel).create()
        thread.channel = channel
        thread.save()
        self.assertIsInstance(thread.channel, Channel)
