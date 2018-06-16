import webapp2
from google.appengine.ext import db
from helper import *
from handler import *
from model import *


# Renders posts and comments to main page.

class MainPage(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC ")
        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created DESC ")
        self.render('main.html', posts=posts, comments=comments)


### Users Registration ###
# Validations 
#  1. Username does not exist in User Kind
#  2. password and verification match
#  3. password restrictions defined in valid_password
#  
# Email property is optional.
###

class RegisterPage(Handler):
    def get(self):
        self.render('register_main.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        val_username = valid_username(username)
        val_password = valid_password(password)
        val_email = valid_email(email)

        u = User.by_name(username)

        if u:
            error_u = "username already exist"
            self.render("register_main.html", username=username,
                        error_username=error_u)

        elif (val_username):
            if (val_password and verify == password and valid_email):
                p = User(parent=register_key(), username=username,
                         password=make_pw_hash(username, password),
                         email=email)
                p.put()
                self.set_secure_cookie('user_id', str(p.key().id()))
                self.redirect('/welcome')

            else:
                if not val_password or verify != password:
                    error_p = "invalid password"
                    self.render("register_main.html", username=username,
                                error_password=error_p)
                if not valid_email:
                    error_e = "invalid email address"
                    self.render("register_main.html", username=username,
                                error_email=error_e)

        else:
            error_u = "invalid username"
            self.render("register_main.html", username=username,
                        error_username=error_u)


# Renders the login page
# Redirects to the welcome page if user authenticates

class LoginPage(Handler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'invalid login or password'
            self.render('login.html', error_password=msg)


# Logout the user, clear the cookie, and redirects to the
# Home page.

class Logout(Handler):
    def get(self):
        self.logout()
        self.redirect('/')


# Renders the welcome page or redirects to the reqistration
# page.

class RegisterPostPage(Handler):
    def get(self):
        if self.user:
            self.render("welcome.html", username=self.user.username,
                ip=self.request.headers.get('X-AppEngine-City'))

        else:
            self.redirect("/signup/")


# Renders the form for new post if user is logged in.
# Redirects to the login form if not logged in.

class NewPost(Handler):
    def get(self):
        if self.user:
            self.render("form.html", type="New")

        else:
            self.render("login.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        author = str(self.user.username)

        if subject and content:
            p = Post(parent=blog_key(), subject=subject, content=content,
                     author=author, like=0)
            p.put()
            self.redirect('%s' % str(p.key().id()))

        else:
            error = "subject and content, please!"
            self.render("form.html", subject=subject, content=content,
                        error=error)


# Renders the post permalink page with related comments.

class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created DESC ")

        if not post:
            self.error(404)
            return

        self.render("permalink.html", post=post, comments=comments)


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
 #                   self.redirect("/")
                    self.render("delete.html", action="liked", type="Post",
                            post_id="")
                else:
                    error = "you already like this post."
                    self.render("error.html", username=current_user,
                                error=error, post_id=post_id)
            else:
                    error = "the author can't like his/her own page."
                    self.render("error.html", username=current_user,
                                error=error, post_id=post_id)
        else:
            self.redirect("/login")


# Renders the form for new comments if user is logged in.
# Renders the login form if not logged in.
# Post the comment.

class NewComment(Handler):
    def get(self, post_id):
        if not self.user:
            self.redirect("/login")
            return

        else:
            post = Post.get_by_id(int(post_id), parent=blog_key())
            subject = post.subject
            content = post.content
            self.render("newcomment.html", subject=subject, content=content,
                    pkey=post.key())

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            self.error(404)
            return

        if not self.user:
            self.redirect('login')

        comment = self.request.get('comment')

        if comment:
            author = self.request.get('author')
            c = Comment(comment=comment, post=post_id, parent=comm_key(),
                        author=author, post_subj=post.subject)
            c.put()
#            self.redirect('/%s' % str(post_id))
            self.render("delete.html", action="created", type="Comment",
                            post_id=c.post)

        else:
            error = "please provide a comment!"
            self.render("permalink.html", post=post, content=content,
                        error=error)


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


# Deletes comment from the comment kind.
# Comment can only be deleted by its author.

class DelComment(Handler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            comment = db.get(key)
            author = comment.author
            loggedUser = self.user.username

            if author == loggedUser:
                key = db.Key.from_path('Comment', int(post_id),
                                       parent=comm_key())
                comment = db.get(key)
                post_id = comment.post
                comment.delete()
                self.render("delete.html", action="deleted", type="Comment",
                            post_id=post_id)
            else:
                self.redirect("/")

        else:
            self.redirect("/login")


# Renders the form to edit a comment.
# Comment can only be edited by its author.

class EditComment(Handler):
    def get(self, post_id):
        error = ""
        if self.user:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            comment = db.get(key)
            author = comment.author
            loggedUser = self.user.username
            if author == loggedUser:
                key = db.Key.from_path('Comment', int(post_id),
                                       parent=comm_key())
                comment = db.get(key)
                self.render("editform.html", subject=comment.post_subj,
                            content=comment.comment, error=error,
                            post_id=post_id, parent_id=comment.post)
            else:
                error = "only the author is authorized to perform \
                        this operation"
                self.render("error.html", username=loggedUser, error=error)
        else:
            self.redirect("/login")

    def post(self, post_id):
        if not self.user:
            self.redirect("/login")
        else:
            key = db.Key.from_path('Comment', int(post_id), parent=comm_key())
            c = db.get(key)
            c.comment = self.request.get('content')
            post_id = c.post
            c.put()
#            self.redirect('/%s' % c.post)
            self.render("delete.html", action="edited", type="Comment",
                            post_id=post_id)

class CommentPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Comment', post_id, parent=comm_key())
        comments = db.get(key)
        print comments.author
        self.render("permalink1.html", comments=comments)


app = webapp2.WSGIApplication([('/?', MainPage),
                               ('/blog/?', MainPage),
                               ('/signup/?', RegisterPage),
                               ('/login/?', LoginPage),
                               ('/logout/?', Logout),
                               ('/welcome/?', RegisterPostPage),
                               ('/newpost/?', NewPost),
                               ('/([0-9]+)/delpost/?', DelPost),
                               ('/([0-9]+)/editpost/?', EditPost),
                               ('/([0-9]+)/newcomment/?', NewComment),
                               ('/editcomment/([0-9]+)/?', EditComment),
                               ('/delcomment/([0-9]+)/?', DelComment),
                               ('/([0-9]+)/likepost/?', LikePost),
                               ('/([0-9]+)/?', PostPage)], debug=True)
