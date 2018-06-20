from handlers.handler import *
from helper import *
from models.post import *


# Renders the form to edit a comment.
# Comment can only be edited by its author.

class EditComment(Handler):

    @login_required
    def get(self, post_id):
        key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
        comment = db.get(key)

        if not comment:
            self.error(404)
            return

        author = comment.author
        loggedUser = self.user.username
        if author == loggedUser:
            key = db.Key.from_path('Comment', int(post_id),
                                   parent=comm_key())
            comment = db.get(key)
            self.render("editform.html", subject=comment.post_subj,
                        content=comment.comment, error="",
                        post_id=post_id, parent_id=comment.post)
        else:
            error = "only the author is authorized to perform \
                    this operation"
            self.render("error.html", username=loggedUser, error=error)


    @login_required
    def post(self, post_id):
        key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
        c = db.get(key)

        if not c:
            self.error(404)
            return

        author = c.author
        loggedUser = self.user.username

        if author == loggedUser:
            c.comment = self.request.get('content')
            post_id = c.post
            c.put()

            self.render("delete.html", action="edited", type="Comment",
                            post_id=post_id)

        else:
            error = "only the author is authorized to perform \
                    this operation"
            self.render("error.html", username=loggedUser, error=error)