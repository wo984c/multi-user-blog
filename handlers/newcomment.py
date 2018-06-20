from handlers.handler import *
from helper import *
from models.post import *
from models.comment import *


# Renders the form for new comments if user is logged in.
# Renders the login form if not logged in.
# Post the comment.

class NewComment(Handler):

    @login_required
    def get(self, post_id):
        post = Post.get_by_id(int(post_id), parent=blog_key())

        if not post:
            self.error(404)
            return

        subject = post.subject
        content = post.content
        self.render("newcomment.html", subject=subject, content=content,
                pkey=post.key())

    @login_required
    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return

        comment = self.request.get('comment')

        if comment:
            author = self.request.get('author')
            c = Comment(comment=comment, post=post_id, parent=comm_key(),
                        author=author, post_subj=post.subject)
            c.put()

            self.render("delete.html", action="created", type="Comment",
                            post_id=c.post)

        else:
            error = "please provide a comment!"
            self.render("permalink.html", post=post, content=content,
                        error=error)
