'''
Created on Nov 9, 2021

@author: reganto
'''
from tornado.testing import AsyncHTTPTestCase


class BaseTest(AsyncHTTPTestCase):
    @property
    def be(self):
        return self.fetch(
            '/auth/login/',
            method='POST',
            body=b'',
            follow_redirects=False
        )

    def login(self, url: str) -> dict:
        """Login test user

        :param url: login endpoint
        :type url: str
        :return: a dict consist of headers
        :rtype: dict
        """
        response = self.fetch(
            url,
            method="POST",
            body=b"",
            follow_redirects=False
        )
        # Users should NOT modify headers directly
        # To modify headers, users have to change it with `update` method.
        headers = {
            'Cookie': response.headers['Set-Cookie'],
            'Content-Type': 'application/x-www-form-urlencoded',
            'uid': response.headers['uid'],
        }
        return headers
