from handlers.handler import *
from helper import *
from models.user import *

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
