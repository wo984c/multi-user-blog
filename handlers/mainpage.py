from handlers.handler import *


# Renders posts and comments to main page.

class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")
        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created DESC ")
        self.render('main.html', posts=posts, comments=comments)
