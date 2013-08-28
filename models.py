from google.appengine.ext import db

class User(db.Model):
    fullname = db.StringProperty(required=True)
    salt = db.TextProperty()
    password_hash = db.TextProperty(required=True)
    email = db.TextProperty(required=True)
    
    @classmethod
    def create_new_user(cls, fullname,salt, password_hash, email):
        user_check = User.gql('where fullname=:1 and password_hash=:2 and email=:3', fullname,password_hash, email).count()
        if fullname and password_hash and email:
            if user_check == 0:
                new_user = User(fullname=fullname,salt = salt,password_hash = password_hash, email=email)
                new_user.put()
                return new_user.key().id()
            else:
                return ('Username already exists.')
        else:
            return ('Empty fields.')
    
                


      
            
            
