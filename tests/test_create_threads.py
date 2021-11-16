'''
Created on Nov 6, 2021

@author: reganto
'''
import peewee
from app import Application
from models import migrator
from model_factory import Factory
from models import User, Thread
from tests.base import BaseTest


class ParticipateTest(BaseTest):
    def get_app(self) -> Application:
        return Application()

    def setUp(self) -> None:
        super().setUp()
        migrator.upgrade()
        self.user = Factory(User).create()
        self.thread = Factory(Thread).create()

    def tearDown(self) -> None:
        super().tearDown()
        migrator.downgrade()

    def test_an_authenticated_user_can_create_new_forum_thread(self):
        self.fetch(
            '/threads/',
            method='POST',
            body=f"title={self.thread.title}&body={self.thread.body}&user={self.thread.creator}",  # noqa E501
            headers={
                'Cookie': self.be.headers['Set-Cookie'],
                'Content-Type': 'application/x-www-form-urlencoded',
                }
            )
        response = self.fetch(self.thread.path)
        self.assertIn(self.thread.title.encode(), response.body)

    def test_guests_may_not_create_threads(self):
        with self.assertRaises(AssertionError):
            self.fetch(
                '/threads/',
                method='POST',
                body=f"title={self.thread.title}&body={self.thread.body}&user={self.thread.creator}",  # noqa E501
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    }
                )
            response = self.fetch('/threads/1/')
            self.assertIn(self.thread.title.encode(), response.body)

        response = self.fetch(
            '/threads/?page=create',
            )
        self.assertNotIn(b'Create New Thread', response.body)

    def test_a_thread_requires_title(self):
        with self.assertRaises(peewee.IntegrityError):
            self.thread.title = None
            self.thread.save()

    def test_a_thread_requires_body(self):
        with self.assertRaises(peewee.IntegrityError):
            self.thread.body = None
            self.thread.save()

    def test_a_thread_requires_a_valid_channel(self):
        with self.assertRaises(peewee.IntegrityError):
            self.thread.channel = None
            self.thread.save()
