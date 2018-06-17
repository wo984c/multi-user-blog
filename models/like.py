from google.appengine.ext import db

# Like Model

class Like(db.Model):
    post = db.StringProperty(required=True)
    user = db.StringProperty()
