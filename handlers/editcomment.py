from handlers.handler import *
from helper import *
from models.post import *

# Renders the form to edit a comment.
# Comment can only be edited by its author.

class EditComment(Handler):
    def get(self, post_id):
        error = ""
        if self.user:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            comment = db.get(key)
            author = comment.author
            loggedUser = self.user.username
            if author == loggedUser:
                key = db.Key.from_path('Comment', int(post_id),
                                       parent=comm_key())
                comment = db.get(key)
                self.render("editform.html", subject=comment.post_subj,
                            content=comment.comment, error=error,
                            post_id=post_id, parent_id=comment.post)
            else:
                error = "only the author is authorized to perform \
                        this operation"
                self.render("error.html", username=loggedUser, error=error)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.redirect("/login")
        else:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            c = db.get(key)
            c.comment = self.request.get('content')
            post_id = c.post
            c.put()

            self.render("delete.html", action="edited", type="Comment",
                            post_id=post_id)