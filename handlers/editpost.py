from handlers.handler import *
from helper import *


# Renders the form to edit a post.
# Post can only be edited by its author.

class EditPost(Handler):
    def get(self, post_id):
        error = ""
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            author = post.author
            loggedUser = self.user.username

            if author == loggedUser:
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                post = db.get(key)
                self.render("form.html", subject=post.subject, type="Edit",
                            content=post.content, error=error, post_id=post_id)
            else:
                error = "only the author is authorized to perform \
                        this operation"
                self.render("error.html", username=loggedUser, error=error,
                            post_id=post_id)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.redirect("/login")
        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            p.subject = self.request.get('subject')
            p.content = self.request.get('content')
            p.put()
            self.redirect('/%s' % str(p.key().id()))
