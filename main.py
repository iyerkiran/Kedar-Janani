import os
import re
from google.appengine.ext import db
import webapp2
import jinja2
from google.appengine.api import mail
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
    def render_str(self, template, **params):
        return render_str(template, **params)
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
class Contact(db.Model):
    name = db.StringProperty(required = True)
    company = db.StringProperty(required = True)
    designation = db.StringProperty(required = True)
    block = db.StringProperty(required = True)
    contact = db.StringProperty(required = True)
    email = db.StringProperty(required = True)
    requirement = db.TextProperty(required = True)
#Delete this block after deploying this source code once.     
#c = Contact(name = "Manas Chaturvedi", ...)  
#c.put()
#End of block   

class ContactHandler(BlogHandler):    
    def get(self,p):
        self.render("enquiry.html")
    def post(self,p):
        name = self.request.get("name")
        company = self.request.get("company")
        designation = self.request.get("designation")
        block = self.request.get("block")
        contact = self.request.get("contact")
        email = self.request.get("email")
        requirement = self.request.get("requirement")
        if name and company and designation and block and contact and email and requirement:
            d = Contact(name = name, company = company,designation = designation, block = block, contact = contact, email = email,requirement = requirement)
            d.put()
            error = "Thank you for submitting your query we will get to you shortly."
            mail.send_mail(sender="kedar janani Support <kedarjananicc@gmail.com>",
              to="kedar janani chemplast <info@kjcp.in>",
              subject="New enquiry data",
              body="""name:%s 
              company:%s 
              designation:%s 
              address:%s 
              contact:%s 
              email:%s 
              requirement:%s""" % (name,company,designation,block,contact,email,requirement))
            mail.send_mail(sender="kedar janani Support <kedarjananicc@gmail.com>",
              to="Paras jain <jain.paras1210@gmail.com>",
              subject="New enquiry data",
              body="""name:%s 
              company:%s 
              designation:%s 
              address:%s 
              contact:%s 
              email:%s 
              requirement:%s""" % (name,company,designation,block,contact,email,requirement))
            self.render("enquiry.html", error=error)   
        else:
            error = '"ERROR"!!! Please fill all the information.'
            self.render("enquiry.html", error=error)    

class MainHandler(BlogHandler):
    def get (self, q):
        if q is None:
            q = 'index.html'
        self.response.headers ['Content-Type'] = 'text/html'
        self.render(q)
        
app = webapp2.WSGIApplication([('/enquiry(.*html)?', ContactHandler),('/(.*html)?', MainHandler)],debug=True)  