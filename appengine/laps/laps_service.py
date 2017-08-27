"""Laps microservice."""

import os
import logging
from google.appengine.api import urlfetch
from flask import Flask


app = Flask(__name__)

print os.environ.get('SERVER_SOFTWARE','')
BASE_URL = 'https://8083-dot-3036522-dot-devshell.appspot.com'
from google.appengine.api import app_identity
#server_url_base = 'https://%s' % app_identity.get_default_version_hostname()
#print server_url_base
#print os.path.join(server_url_base, 'barcodes', 'increment_lap_count')
print os.path.join(BASE_URL, 'barcodes', 'increment_lap_count')

@app.route('/laps/increment/<barcode_number>')
def increment_laps(barcode_number):
  """Increments the number of laps for the specified barcode by one."""
  result = urlfetch.fetch(
      url=os.path.join(BASE_URL, 'barcodes', 'increment_lap_count'),
      payload={'barcode_number': int(barcode_number)},
      method=urlfetch.POST,
      headers={'Content-Type': 'application/json'})
  print result
  print dir(result)
  print result.status_code
  #print result.content
  return 'Hello laps increment %s' % barcode_number
      

@app.errorhandler(500)
def server_error(e):
	# Log the error and stacktrace.
	logging.exception('An error occurred during a request.')
	return 'An internal error occurred.', 500

