"""
Created on Dec 9, 2021

@author: reganto
"""
from app import Application
from database.model_factory import Factory
from database.models import Reply, migrator

from tests.base import BaseTest


class FavoriteTest(BaseTest):
    def get_app(self):
        return Application()

    def setUp(self):
        super().setUp()
        migrator.upgrade()

    def tearDown(self):
        super().tearDown()
        migrator.downgrade()

    def test_unauthenticated_user_should_not_favorite_any_reply(self):
        reply = Factory(Reply).create()
        response = self.fetch(
            '/replies/'+str(reply.id)+'/favorites/',
            method='POST',
            body='',
            headers={
                # 'Cookie': self.be.headers['Set-Cookie'], # unauthorized user
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )
        self.assertEqual(response.code, 403)

    def test_an_authenticated_user_can_favorite_any_reply(self):
        reply = Factory(Reply).create()
        self.fetch(
            '/replies/'+str(reply.id)+'/favorites/',
            method='POST',
            body='',
            headers={
                'Cookie': self.be.headers['Set-Cookie'],
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )
        self.assertEqual(reply.favorites.count(), 1)

    def test_an_authenticated_user_may_only_favorite_a_reply_once(self):
        reply = Factory(Reply).create()
        authenticated_user = self.be.headers['Set-Cookie']
        self.fetch(  # Successfully done
            '/replies/'+str(reply.id)+'/favorites/',
            method='POST',
            body='',
            headers={
                'Cookie': authenticated_user,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )
        self.fetch(  # Integrity Error occured due to unique constraint
            '/replies/'+str(reply.id)+'/favorites/',
            method='POST',
            body='',
            headers={
                'Cookie': authenticated_user,
                'Content-Type': 'application/x-www-form-urlencoded',
            }
        )
        self.assertEqual(reply.favorites.count(), 1)
