from google.appengine.ext import db
from helper import *

# Post Model

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty(required=True)
    like = db.IntegerProperty()

    def render(self):
        return render_str("post.html", p=self)

    def vote(self, current_user):
        likes = db.GqlQuery("SELECT * FROM Like WHERE user= :1 and \
                            post= :2", current_user, self.subject)
        if likes.count < 1:
            l = Like(post=self.subject, user=current_user)
            l.put()
            self.likes += 1
            self.put()
