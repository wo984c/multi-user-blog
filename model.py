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


# Post Model

class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
#    modified_on = db.DateTimeProperty(auto_now_add = True)
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


# Like Model

class Like(db.Model):
    post = db.StringProperty(required=True)
    user = db.StringProperty()


# Comment Model

class Comment(db.Model):
    comment = db.TextProperty(required=True)
    post = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    post_subj = db.StringProperty()

    def render(self):
        return render_str("comment.html", p=self)
