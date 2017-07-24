import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/home.html")
        self.response.write(template.render())
<<<<<<< HEAD
    
=======


class FormHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/form.html")
        self.response.write(template.render())

class ResultHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template("templates/result.html")
        self.response.write(template.render())


>>>>>>> 601d02c46a104a242cbcb7305ad779e05ea3b21d
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/form', FormHandler),
    ('/result', ResultHandler),
    ('/Map', MapHandler),
    ('/camera', CameraHandler),
], debug=True)
