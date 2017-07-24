import webapp2
import os
import jinja2

from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Donor(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()

class Bank(ndb.Model):
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render())

class DonorFormHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

    def post(self):
        donor = Donor(name = self.request.get("name"), city = self.request.get("city"), address = self.request.get("streetname"), zipcode = self.request.get("zipcode"), phone = self.request.get("phone"), email = self.request.get("email") )
        donor.put()
        self.redirect('/')
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())


class ResultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/result.html")
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', DonorFormHandler),
    ('/result', ResultHandler),

], debug=True)
