from handlers.handler import *


# Logout the user, clear the cookie, and redirects to the
# Home page.

class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')
