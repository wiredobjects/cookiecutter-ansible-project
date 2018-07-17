import re
import sys

def sys_exit(msg):
    print(msg)
    sys.exit(1)

REGEX_PROJECT_SLUG = r'^[_a-zA-Z][-_a-zA-Z0-9]+$'
REGEX_EMAIL = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'

author_name = '{{ cookiecutter.author_name}}'
email = '{{ cookiecutter.email}}'
project_slug = '{{ cookiecutter.project_slug}}'

if author_name == '':
    sys_exit('[ERROR] No value for author name provided: %s - Please provide at least an alias name' % author_name)

if not re.match(REGEX_EMAIL, email):
    sys_exit('[ERROR] No valid email provided: %s' % email)

if not re.match(REGEX_PROJECT_SLUG, project_slug):
    sys_exit('[ERROR] The project slug (%s) is not a valid.' % project_slug)
