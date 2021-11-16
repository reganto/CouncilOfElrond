'''
Created on Nov 6, 2021

@author: reganto
'''
import peewee

from model_factory import Factory
from models import migrator, User, Reply
from tests.base import BaseTest
from tornado.web import Application


class ReplisTest(BaseTest):
    def get_app(self):
        return Application()

    def setUp(self):
        super().setUp()
        migrator.upgrade()
        self.reply = Factory(Reply).create()

    def tearDown(self):
        super().tearDown()
        migrator.downgrade()

    def test_a_reply_has_an_owner(self):
        self.assertIsInstance(self.reply.user, User)

    def test_a_reply_requires_body(self):
        with self.assertRaises(peewee.IntegrityError):
            self.reply.body = None
            self.reply.save()
