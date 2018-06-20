from handlers.handler import *
from helper import *
from models.post import *


# Renders the form for new post if user is logged in.
# Redirects to the login form if not logged in.

class NewPost(Handler):
    def get(self):
        if self.user:
            self.render("form.html", type="New")

        else:
            self.render("login.html")

    def post(self):
        if self.user:
            subject = self.request.get('subject')
            content = self.request.get('content')
            author = str(self.user.username)

            if subject and content:
                p = Post(parent=blog_key(), subject=subject, content=content,
                         author=author, like=0)
                p.put()
                self.redirect('%s' % str(p.key().id()))

            else:
                error = "subject and content, please!"
                self.render("form.html", subject=subject, content=content,
                            error=error)
        else:
            self.render("login.html")
