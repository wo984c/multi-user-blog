from google.appengine.ext import db
from helper import *

# User Model

class User(db.Model):
    username = db.StringProperty(required=True)
    password = db.TextProperty(required=True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent=register_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('username =', name).get()
        return u

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.password):
            return u

    def render(self):
        return render_str("user_post.html", p=self)
