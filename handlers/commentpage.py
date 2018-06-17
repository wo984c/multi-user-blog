from handlers.handler import *
from helper import *


class CommentPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comment', post_id, parent=comm_key())
        comments = db.get(key)
        print comments.author
        self.render("permalink1.html", comments=comments)
