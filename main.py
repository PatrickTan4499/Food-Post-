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

    #input from checkboxes
    vegetables = ndb.StringProperty()
    grains = ndb.StringProperty()
    protiens = ndb.StringProperty()
    fruits = ndb.StringProperty()

    #input from textarea
    vegetable = ndb.StringProperty()
    grain = ndb.StringProperty()
    protien = ndb.StringProperty()
    fruit = ndb.StringProperty()

class Bank(ndb.Model):
    #creates recipient class to store all their info
    name = ndb.StringProperty()
    address = ndb.StringProperty()
    city = ndb.StringProperty()
    zipcode = ndb.StringProperty()
    phone = ndb.StringProperty()
    email = ndb.StringProperty()
    post_key = ndb.KeyProperty()

    #input from checkboxes
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
        name = self.request.get("name")
        city = self.request.get("city")
        address = self.request.get("streetname")
        zipcode = self.request.get("zipcode")
        phone = self.request.get("phone")
        email = users.get_current_user().email()
        protiens = self.request.get("protein")
        grains = self.request.get("grain")
        vegetables = self.request.get("vegetable")
        fruits = self.request.get("fruit")
        protien = self.request.get("protiens")
        grain = self.request.get("grains")
        vegetable = self.request.get("vegetables")
        fruit = self.request.get("fruits")

        donor = Donor(name = name, city = city, address = address, zipcode = zipcode, phone = phone, email = email, protiens = protiens, grains = grains, vegetables = vegetables, fruits = fruits, protien = protien, grain = grain, vegetable = vegetable, fruit = fruit)
        donor.put()

        #puts donor in datastore and redirects to home page
        self.redirect('/map')
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

class BankFormHandler(webapp2.RequestHandler):
    def get(self):
        #load the form page
        template = jinja_environment.get_template("templates/form2.html")
        self.response.write(template.render())
    def post(self):
        #create a recipient to save to datastore
        name = self.request.get("name")
        city = self.request.get("city")
        address = self.request.get("streetname")
        zipcode = self.request.get("zipcode")
        phone = self.request.get("phone")
        email = users.get_current_user().email()
        protiens = self.request.get("protein")
        grains = self.request.get("grain")
        vegetables = self.request.get("vegetable")
        fruits = self.request.get("fruit")

        bank = Bank(name = name, city = city, address = address, zipcode = zipcode, phone = phone, email = email, protiens = protiens, grains = grains, vegetables = vegetables, fruits = fruits )
        bank.put()

        #puts recipient in datastore and redirects to home page
        self.redirect('/map')
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


class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/about.html")
        self.response.write(template.render())


class MatchHandler(webapp2.RequestHandler):
    def get(self):

        sortedBanks = []
        results = []
        user_email = users.get_current_user().email()
        current_user_donor = Donor.query(Donor.email==user_email).get()
        current_user_bank = Bank.query(Bank.email==user_email).get()
        banks = Bank.query().fetch()
        donors = Donor.query().fetch()

        if current_user_donor:
            for bank in banks:
                similarity = 0;
                if current_user_donor.protiens == bank.protiens:
                    similarity += 1
                if current_user_donor.grains == bank.grains:
                    similarity += 1
                if current_user_donor.vegetables == bank.vegetables:
                    similarity += 1
                if current_user_donor.fruits == bank.fruits:
                    similarity += 1
                result = (bank, similarity)
                results.append(result)
        elif current_user_bank:
            for donor in donors:
                similarity = 0;
                if current_user_bank.protiens == donor.protiens:
                    similarity += 1
                if current_user_bank.grains == donor.grains:
                    similarity += 1
                if current_user_bank.vegetables == donor.vegetables:
                    similarity += 1
                if current_user_bank.fruits == donor.fruits:
                    similarity += 1
                result = (donor, similarity)
                results.append(result)

        results.sort(key=lambda result: result[1], reverse=True)
        for result in results:
            sortedBanks.append(result[0])

        print sortedBanks
        template_vars = {
            "list": sortedBanks,
            "currdonor": current_user_donor,
            "currbank": current_user_bank
        }
        template = jinja_environment.get_template("templates/map.html")
        self.response.write(template.render(template_vars))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', DonorFormHandler),
    ('/result', ResultHandler),
    ('/form2', BankFormHandler),
    ('/about', AboutHandler),
    ('/map', MatchHandler)

], debug=True)
