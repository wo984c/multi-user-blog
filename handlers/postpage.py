from handlers.handler import *
from helper import *


# Renders the post permalink page with related comments.

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created DESC ")

        self.render("permalink.html", post=post, comments=comments)
