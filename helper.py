import os
import re
import random
import hashlib
import hmac
import webapp2
import jinja2
from string import letters
from google.appengine.ext import db


# JINJA Configuration

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


# Secret Key 

secret = 'oTTg3BzTyG2/wwJDi/Kfx/cDQ6Ar5AhUpkyFHioLL1WG+cmm6qAbDM3d/wvkzJdl'


# Validations

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{6}$")
PASS_RE = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# Model Keya

def blog_key(name='default'):
    return db.Key.from_path('Post', name)


def comm_key(name='default'):
    return db.Key.from_path('Comment', name)


def register_key(name='default'):
    return db.Key.from_path('User', name)


def like_key(name='default'):
    return db.Key.from_path('Like', name)


# Authentication

def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(username, password, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(username, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(username, password, salt)


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASS_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)
