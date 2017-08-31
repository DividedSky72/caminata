import os
import functools
from google.appengine.api import app_identity
from google.appengine.api import users
from protorpc import remote

JSON_MIME_TYPE = 'application/json'
INTERNAL_HEADER = 'X-Appengine-Inbound-Appid'
APP_ID = 'river-glen'


class CaminataService(remote.Service):
  """Superclass that all caminata sprotorpc ervices should inherit from.
  
  This is so we can use initialize_request_state easily.
  """
  def initialize_request_state(self, state):
    # Make sure header is internal.
    if state.headers[INTERNAL_HEADER] != APP_ID:
      raise remote.RequestError('Request did not come internally.')


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
