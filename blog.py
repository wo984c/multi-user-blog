import webapp2

from handlers.handler import *
from handlers.commentpage import *
from handlers.delcomment import *
from handlers.delpost import *
from handlers.editcomment import *
from handlers.editpost import *
from handlers.likepost import *
from handlers.loginpage import *
from handlers.logout import *
from handlers.mainpage import *
from handlers.newcomment import *
from handlers.newpost import *
from handlers.postpage import *
from handlers.registerpage import *
from handlers.registerpostpage import *


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
