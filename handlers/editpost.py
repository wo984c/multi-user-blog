from handlers.handler import *
from helper import *


# Renders the form to edit a post.
# Post can only be edited by its author.

class EditPost(Handler):

    @login_required
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return

        author = post.author
        loggedUser = self.user.username

        if author == loggedUser:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            self.render("form.html", subject=post.subject, type="Edit",
                        content=post.content, error="", post_id=post_id)
        else:
            error = "only the author is authorized to perform \
                    this operation"
            self.render("error.html", username=loggedUser, error=error,
                        post_id=post_id)


    @login_required
    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        p = db.get(key)

        if not p:
            self.error(404)
            return

        author = p.author
        loggedUser = self.user.username

        if author == loggedUser:
            p.subject = self.request.get('subject')
            p.content = self.request.get('content')
            p.put()
            self.redirect('/%s' % str(p.key().id()))

        else:
            error = "only the author is authorized to perform \
                    this operation"
            self.render("error.html", username=loggedUser, error=error,
                        post_id=post_id)
