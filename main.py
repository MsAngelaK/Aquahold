
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

#class NewUsers(db.Model):
#   name = db.StringProperty(required=True)
#   email_address = db.StringProperty(required = True)
#   salt = db.StringProperty(required=True)



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
    
        
        
class HomePage(Handler):
    def get(self):
        self.render('landing.html')

app = webapp2.WSGIApplication([('/',HomePage),
                               ],debug=True)