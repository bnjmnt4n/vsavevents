import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../')),
    extensions=['jinja2.ext.autoescape'])

def send(response, name, options):
	template = JINJA_ENVIRONMENT.get_template(name)
	response.out.write(template.render(options))

def render(name, options):
	template = JINJA_ENVIRONMENT.get_template(name)
	return template.render(options)