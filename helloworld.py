#imported libraries
import os
import webapp2
import jinja2
import logging
import random
import string
import hashlib
import urllib

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
#from models import User,TweetEntry
import datetime


class NewUsers(db.Model):
    name = db.StringProperty(required=True)
    password = db.StringProperty(required = True)
    email_address = db.StringProperty(required = True)
    company = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    company_url = db.StringProperty(required = False)
    company_location = db.StringProperty(required = False)
    company_location_Description = db.TextProperty(required = False)
    salt = db.StringProperty(required=True)



template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
#     Parent class for all other webpages
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    def set_cookie(self,name,value):
        expires = datetime.date(2013,3,1)
        cookie_val = self.make_signed_cookie(value)
        self.response.headers.add_header('Set-Cookie','%s=%s; expires=%s; Path=/' % (name, cookie_val, expires))
    
    def delete_cookie(self):
        self.response.headers.add_header('Set-Cookie','name=; Path=/' )
        
        
    def make_signed_cookie(self,value):
        hush_hush = 'the secret is Revlon.lol'
        signing = '%s|%s' % (value,hashlib.sha256(value + hush_hush).hexdigest())
        return signing
    
    
    def read_signed_cookie(self,name):
        check = self.request.cookies.get('name')
        value_check = check.split('|')[0]
        index = self.make_signed_cookie(value_check)
        if check == index:
            return int(value_check)
        else:
            return 0
        
    def hashPassword(self,plaintext,salt):
        pw_hash = plaintext+salt
        return hashlib.sha256(pw_hash).hexdigest()
    
    def getSalt(self):
        return ''.join(random.choice(string.letters) for i in range(5)) 
        
    
        
    
        
        
class HomePage(Handler):
    def get(self):
        self.render('dashboard.html')
        
    def post(self):
        action = self.request.get('header_nav')
        
        if action == 'register':
            self.redirect('/signup')
        elif action == 'signin':
            self.redirect('/signin')
            
     
class get_widget(Handler):
    def userExist(self,name,password):
        return NewUsers.gql("where name=:1 and password=:2",name,password).count()
    
    def usernameExist(self,name):
        return NewUsers.gql("where name=:1",name).count()
    
    
    def buildDashBoard(self,name='',company=''):
        with open('templates/dashboard.html','r') as f:
            welcome = f.read()
            self.response.out.write(welcome %{'name':name,'company':company})
    def buildSignUp(self,name='',company=''):
        with open('templates/signup.html','r') as f:
            welcome = f.read()
            self.response.out.write(welcome)
            
#    def buildsettings(self,name='',company='',email=''):
#        with open('templates/settings.html','r') as f:
#            welcome = f.read()
#            self.response.out.write(welcome %{'name':name,'company':company,'email':email})
    
    
    def get(self):
        self.buildSignUp()
        #self.render("signup.html") 
        
    def post(self):
        salt = self.getSalt()
        name = self.request.get('signup-name')
        password = self.hashPassword(self.request.get('signup-password'), salt)
        Repassword = self.hashPassword(self.request.get('signup-repassword'), salt)
        email_address = self.request.get('signup-email')
        company = self.request.get('signup-company')
        
        
#        names = db.GqlQuery('select * from NewUsers where name=:1', name).get()
#        email = db.GqlQuery('select * from NewUsers where email_address=:1', email_address).get()
        if (name and password and  email_address and company) and (password==Repassword):
            usernameExist=self.usernameExist(name)
            if (usernameExist==0):
                new_users = NewUsers(name=name, password=password, email_address=email_address,company=company,salt=salt)
                user = db.put(new_users)
                new_users.put()
                ID = user.id()
                self.redirect('/Dashhome/%d' %(ID))
                #self.redirect("add_location/%d", name=name,company=company,%(ID))
                #self.render("dashboard.html", name=name,company=company)
                #CurrentUser = db.GqlQuery('select * from NewUsers where ID=:1', ID).get()
                #self.buildDashBoard(name,company)
                #ID=CurrentUser.name 
                #self.render("dashboard.html" %(str(new_users.name)))
                #user_id = user.id()
                #self.render("dashboard.html")
            else:
                error = "Username or email already taken, please choose another one"
                self.render("signup.html", error=error)
        else:
            error = "Please fill in all fields."
            self.render("signup.html", error=error)
            
            
    def hashPassword(self,plaintext,salt):
        pw_hash = plaintext+salt
        return hashlib.sha256(pw_hash).hexdigest()
    
    def getSalt(self):
        return ''.join(random.choice(string.letters) for i in range(5))    

                  
      
class MapPage(Handler):
    def get(self):
        self.render('map.html')
        

class add_location(Handler):
    branches=[]
    descriptions =[]
    
    def add_info(self,branches,branch):
        branches = str(branches) + '|' + str(branch)
        return str(branches)
        
        
    def get(self,ID):
        branches=[]
        user = NewUsers.get_by_id(int(ID))
        user.company_location = str(branches)
        name=user.name
        company=user.company
        self.render('dashboard.html',name=name,company=company)
        
    def post(self,ID):
        #branches=[]Anothersave-changes  description
        user = NewUsers.get_by_id(int(ID))
        submitted = self.request.get('actions')
        name=user.name
        company=user.company
        Company_url = self.request.get('company-url')
        Company_locational = self.request.get('company-site')
        description = self.request.get('description')

        if submitted =='Another':
            branche = self.add_info(user.company_location,Company_locational)
            descrp =  self.add_info(user.company_location_Description,description)
            user.company_location = str(branche)
            user.company_location_Description =str(descrp)
            user.put()
            place = user.company_location.split('|')
            places = place[1:]
            self.render('dashboard.html',name=name,company=company,url= Company_url,location = '',
                        branche = places,description='')
            
        elif submitted =='save-changes': 
            user.company_url=Company_url
            user.company_location= Company_locational
            user.company_location_Description = description
            user.put()
            self.response.out.write('<H1> WIDGET PAGE</H1>')
            
        
    
    
#        branch = self.request.get('company-site')
#        BranchDescription = self.request.get('description')
#        self.add_info(branch, BranchDescription)
        


class SignUp(Handler):
    def get(self):
        cookie_check = self.request.cookies.get('')
        if not cookie_check:
            self.render('/signup.html')
        else:
            #value = cookie_check.split('|')[0]
            self.redirect('/')
            
def post(self):
    name = self.request.get('signup-name')
    password = self.request.get('signup-password')
    Repassword = self.request.get('signup-repassword')
    company = self.request.get('signup-company')
    email_address = self.request.get('signup-email')
    if name and password and Repassword and company and email_address:
        names = db.GqlQuery('select * from NewUsers where username=:1', username).get()
        email = db.GqlQuery('select * from NewUsers where email_address=:1', email_address).get()
        if not (name or email):
            new_users = NewUsers(name=name, password=newPass, email_address=email_address,company=company)
            user = db.put(new_user)
            user_id = user.id()
            self.response.out.write('<H1><b>DASHBOARD COMING SOON</b></H1>')
        else:
            error = "Username or email already taken, please choose another one"
            self.render("signup.html", error=error)
        
    else:
        self.response.out.write('<h1><b> 3RROR </b></h1>')
        



class CustomiseJscript(Handler):
    def get(self,user_id):
        UserScript = NewUsers.get_by_id(int(user_id))  
        self.response.headers.add_header('Content-Type',"application/javascript; charset=utf-8")
        self.render('page.js', location=UserScript.location)

       
#    def post(self):
#        action = self.request.get('action')
#        fullname = self.request.get('signup-name')
#        email = self.request.get('signup-email')
#        password = self.request.get('signup-password')
#        company = self.request.get('company')
#    
#        if action == 'signin':
#            self.redirect('/signin.html')
#        elif action == "register":
#            salt = self.make_salt()
#            make_hash = self.make_password_hash(password,salt)
#            password_hash = make_hash[0]
            
#                aUser = User(fullname=fullname,salt = salt,password_hash = password_hash,email=email)
#                list = User.gql('where fullname=:1',fullname).get()
#                
#                if list:
#                    self.redirect('/')
#                else:
#                    aUser.put()
#                    self.set_cookie('name',str(aUser.key().id()))
#                    self.redirect('/')            
#            else:
#                self.error(404)/Dashboard_Activities
class Dashboard_Activities(Handler):
    def get(self):
        self.render('dashboard.html')


class setting(Handler):
    def get(self):
        self.render('settings.html') 
  
                           
class SignIn(Handler):    
    def get(self):
        cookie_check = self.request.cookies.get('')
        if not cookie_check:
            self.render('signin.html')
        else:
            #value = cookie_check.split('|')[0]
            self.redirect('/')
    
    def post(self):
        #action = self.request.get('action')
        email_address = self.request.get('signin-email')
        salts = NewUsers.gql('where email_address=:1',email_address).get().salt
        password = self.hashPassword(self.request.get('signin-password'), salts)
        user = NewUsers.gql("where email_address=:1 and password=:2",email_address,password).get()
        
        if user:
            ID = user.key().id()
            self.redirect('/Dashhome/%d' %(ID))
        else:
            self.response.out.write("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
      
#ender('settings.html',name='name',Company='Company',signup-email='ghamil')        
            

app = webapp2.WSGIApplication([('/',HomePage),
                               ('/map',MapPage),
                               ('/signup',SignUp),
                               ('/setting',setting),
                                ('/get_widget',get_widget),
                                ('/Dashhome/(\d+)', add_location),
                               ('/sign_in',SignIn)
                               ],debug=True)