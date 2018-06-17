from google.appengine.ext import db
from helper import *

# Comment Model

class Comment(db.Model):
    comment = db.TextProperty(required=True)
    post = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    post_subj = db.StringProperty()

    def render(self):
        return render_str("comment.html", p=self)
