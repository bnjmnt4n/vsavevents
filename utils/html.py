import re

STRIP_REGEX = '</?(?:[A-Za-z][^\s>/]*)(?:[^>"\']|"[^"]*"|\'[^\']*\')*>'
ERROR_HTML = '<html><head><title>%s</title></head><body><h1>%s</h1></body></html>'

def strip_tags(html):
    return re.sub(STRIP_REGEX, '', html)

def handle_error(response, status, message):
    response.write(ERROR_HTML % (message, message))
    response.set_status(status)
