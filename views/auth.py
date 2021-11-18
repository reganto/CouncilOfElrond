'''
Created on Nov 7, 2021

@author: reganto
'''
from views.base import BaseHandler
from models import User
from random import choice


class AuthHandler(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        try:
            users = User.select()
            users = [user for user in users]
            user = choice(users)
            self.set_secure_cookie('user', str(user.id))
        except Exception:
            self.write('User does not exist!')
        else:
            self.redirect(self.get_argument('next', '/'))


class Logout(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.reverse_url('threads'))
