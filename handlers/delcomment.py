from handlers.handler import *
from helper import *


# Deletes comment from the comment kind.
# Comment can only be deleted by its author.

class DelComment(Handler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            comment = db.get(key)
            author = comment.author
            loggedUser = self.user.username

            if author == loggedUser:
                key = db.Key.from_path('Comment', int(post_id),
                                       parent=comm_key())
                comment = db.get(key)
                post_id = comment.post
                comment.delete()
                self.render("delete.html", action="deleted", type="Comment",
                            post_id=post_id)
            else:
                self.redirect("/")

        else:
            self.redirect("/login")
