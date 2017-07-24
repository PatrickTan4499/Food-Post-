import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))



class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render())

class FormHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

class ResultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/result.html")
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', FormHandler),
    ('/result', ResultHandler),
    ('/Map', MapHandler),
    ('/camera', CameraHandler),
], debug=True)
