from handlers.handler import *
from helper import *


# Renders the login page
# Redirects to the welcome page if user authenticates

class LoginPage(Handler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'invalid login or password'
            self.render('login.html', error_password=msg)
