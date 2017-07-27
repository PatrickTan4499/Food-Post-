import webapp2
import os
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users
#add users api

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Donor(ndb.Model):
    #creates donor class to store all their info
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    post_key = ndb.KeyProperty()
    vegetables = ndb.StringProperty()
    grains = ndb.StringProperty()
    protiens = ndb.StringProperty()
    fruits = ndb.StringProperty()

class Bank(ndb.Model):
    #creates recipient class to store all their info
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    post_key = ndb.KeyProperty()
    vegetables = ndb.StringProperty()
    grains = ndb.StringProperty()
    protiens = ndb.StringProperty()
    fruits = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        #loads the home page
        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        login_url = users.create_login_url('/')

        template_vars = {
            "current_user": current_user,
            "logout_url": logout_url,
            "login_url": login_url,
        }
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render(template_vars))

#link this up to result.html to show all the donors and banks
class DonorFormHandler(webapp2.RequestHandler):
    def get(self):
        #load the form page
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

    def post(self):
        #create a Donor to save to datastore

        donor = Donor(name = self.request.get("name"), city = self.request.get("city"), address = self.request.get("streetname"), zipcode = self.request.get("zipcode"), phone = self.request.get("phone"), email = self.request.get("email"), protiens = self.request.get("protien"), grains = self.request.get("grain"), vegetables = self.request.get("vegetable"), fruits = self.request.get("fruit"))

        donor.put()
        #puts donor in datastore and redirects to home page
        self.redirect('/')
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

class BankFormHandler(webapp2.RequestHandler):
    def get(self):
        #load the form page
        template = jinja_environment.get_template("templates/form2.html")
        self.response.write(template.render())
    def post(self):
        #create a recipient to save to datastore
        bank = Bank(name = self.request.get("name"), city = self.request.get("city"), address = self.request.get("streetname"), zipcode = self.request.get("zipcode"), phone = self.request.get("phone"), email = self.request.get("email"), protiens = self.request.get("protien"), grains = self.request.get("grain"), vegetables = self.request.get("vegetable"), fruits = self.request.get("fruit") )
        bank.put()
        #puts recipient in datastore and redirects to home page
        self.redirect('/')
        template = jinja_environment.get_template("templates/form2.html")
        self.response.write(template.render())

class ResultHandler(webapp2.RequestHandler):
    def get(self):
        banks = Bank.query().fetch()
        donor_query = Donor.query()
        donors = donor_query.fetch()
        template_vars = {
            "donors": donors,
            "banks": banks
        }
        template = jinja_environment.get_template("templates/result.html")
        self.response.write(template.render(template_vars))

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        #urlsafe_key = self.request.get('key')
        #post_key = ndb.Key(urlsafe=urlsafe_key)
        #post = post_key.get()
        template = jinja_environment.get_template("templates/profile.html")
        self.response.write(template.render())

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/about.html")
        self.response.write(template.render())


class MatchHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/map.html")
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', DonorFormHandler),
    ('/result', ResultHandler),
    ('/form2', BankFormHandler),
    ('/profile', ProfileHandler),
    ('/about', AboutHandler),
    ('/map', MatchHandler)

], debug=True)
