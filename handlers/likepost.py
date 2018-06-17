from handlers.handler import *
from helper import *
from models.like import *


# Like post written by other user. 
# User can't like his/her own post.

class LikePost(Handler):
    def get(self, post_id):
        error = ""
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            author = post.author
            current_user = self.user.username

            if author != current_user:
                prev_like = db.GqlQuery("SELECT * FROM Like WHERE user =:1 \
                                AND post =:2", current_user, post_id)
                if prev_like.count() < 1:
                    like = Like(user=current_user, post=post_id)
                    like.put()
                    post.like += 1
                    post.put()

                    self.render("delete.html", action="liked", type="Post",
                            post_id="")
                else:
                    error = "you already like this post."
                    self.render("error.html", username=current_user,
                                error=error, post_id=post_id)
            else:
                    error = "the author can't like his/her own post."
                    self.render("error.html", username=current_user,
                                error=error, post_id=post_id)
        else:
            self.redirect("/login")
