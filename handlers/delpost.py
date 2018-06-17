from handlers.handler import *
from helper import *


# Deletes post from the post kind.
# Post can only be deleted by its author.

class DelPost(Handler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id),
                                   parent=blog_key())
            post = db.get(key)
            author = post.author
            loggedUser = self.user.username
            ctodel = db.GqlQuery("SELECT * FROM Comment \
                WHERE post_subj = :1", post.subject)

            if author == loggedUser:
                key = db.Key.from_path('Post', int(post_id),
                                       parent=blog_key())
                post = db.get(key)
                post.delete()

                if ctodel:
                    results = ctodel.fetch(10)
                    db.delete(results)
                    ltodel = db.GqlQuery("SELECT * FROM Like WHERE \
                        post = :1", post_id)
                    l_results = ltodel.fetch(ltodel.count())
                    db.delete(l_results)
                self.render("delete.html", action="deleted", type="Post")

            else:
                error = "only the author is authorized to perform this \
                        operation"
                self.render("error.html", username=loggedUser, error=error,
                            post_id=post_id)

        else:
            self.redirect("/login")
