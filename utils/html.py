import re

STRIP_REGEX = '</?(?:[A-Za-z][^\s>/]*)(?:[^>"\']|"[^"]*"|\'[^\']*\')*>'

def strip_tags(html):
    return re.sub(STRIP_REGEX, '', html)
