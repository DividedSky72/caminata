import os
import functools
from google.appengine.api import app_identity
from google.appengine.api import users

JSON_MIME_TYPE = 'application/json'
INTERNAL_HEADER = 'X-Appengine-Inbound-Appid'
APP_ID = 'river-glen'


def login_required(func):
  """Redirect to login if user isn't logged in."""
  print users.create_logout_url("/")
  @functools.wraps(func)
  def decorated_view(*args, **kwargs):
    if not users.get_current_user():
      return redirect(users.create_login_url(request.url))
    return func(*args, **kwargs)
  return decorated_view


def is_dev_server():
  return os.environ.get('SERVER_SOFTWARE','').startswith('Development')


def is_prod_server():
  return not is_dev_server()


def get_server_base():
  if is_dev_server():
    return 'http://localhost:8080'
  else:
    return 'https://%s' % app_identity.get_default_version_hostname()


def get_protorpc_headers():
  headers = {'Content-Type': JSON_MIME_TYPE}
  if is_dev_server():
    # https://stackoverflow.com/questions/41864284/how-to-authenticate-requests-across-internal-app-engine-modules
    # https://stackoverflow.com/questions/43197313/x-appengine-inbound-appid-header-is-not-added-in-gae-flexible-environment
    # https://issuetracker.google.com/issues/35899268
    
    # This should be getting set in a prod environment so need to add it in dev.
    headers[INTERNAL_HEADER] = APP_ID
  return headers
