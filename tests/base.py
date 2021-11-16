'''
Created on Nov 9, 2021

@author: reganto
'''
from tornado.testing import AsyncHTTPTestCase


class BaseTest(AsyncHTTPTestCase):
    @property
    def be(self):
        return self.fetch(
            '/user/login/',
            method='POST',
            body=b'',
            follow_redirects=False
            )
