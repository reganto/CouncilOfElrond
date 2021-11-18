'''
Created on Nov 6, 2021

@author: reganto
'''
from app import Application
from database.models import migrator, Thread, User
from database.model_factory import Factory
from tests.base import BaseTest


class ParticipateTest(BaseTest):
    def get_app(self) -> Application:
        return Application()

    def setUp(self) -> None:
        super().setUp()
        migrator.upgrade()
        self.thread = Factory(Thread).create()
        self.user = Factory(User).create()

    def tearDown(self) -> None:
        super().tearDown()
        migrator.downgrade()

    def test_an_authenticated_user_may_participated_in_forum(self):
        # self.skipTest('I don\'t know but I think Tornado doesn\'t have facilities to make a user verified in tests!') # noqa E501
        # https://groups.google.com/g/python-tornado/c/6HW30emjops/m/_xqoNzeoTyUJ
        self.fetch(
            self.thread.path + '/replies/',
            method='POST',
            body="body=A fancy reply",
            headers={
                'Cookie': self.be.headers['Set-Cookie'],
                'Content-Type': 'application/x-www-form-urlencoded',
                }
            )
        response = self.fetch(self.thread.path)
        self.assertIn(b'A fancy reply', response.body)

    def test_unauthenticated_user_may_not_add_replies(self):
        # self.skipTest('Tornado don\'t raise an error for unauthenticated users it just redirect them') # noqa E501
        with self.assertRaises((PermissionError, AssertionError)):
            self.fetch(
                self.thread.path + '/replies/',
                method='POST',
                body="body=A fancy reply",
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    }
                )
            response = self.fetch(self.thread.path)
            self.assertIn(b'A fancy reply', response.body)
