import jinja2
import os
from . import user

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../')),
    extensions=['jinja2.ext.autoescape'])

def send(jinja, name, options):
    template = JINJA_ENVIRONMENT.get_template('templates/' + name)
    jinja.response.out.write(
        template.render(
            configure(options, jinja.request)
        )
    )

def configure(options, request):
    curr_user = user.get_user()
    loginUrl, logoutUrl = user.create_login_urls(request.path)

    if not curr_user:
        options['loginUrl'] = loginUrl
    else:
        options['logoutUrl'] = logoutUrl

    options['user'] = curr_user

    return options
