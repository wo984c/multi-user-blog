from handlers.handler import *
from helper import *


# Renders the welcome page or redirects to the reqistration
# page.

class RegisterPostPage(Handler):
    def get(self):
        if self.user:
            self.render("welcome.html", username=self.user.username,
                ip=self.request.headers.get('X-AppEngine-City'))

        else:
            self.redirect("/signup/")
