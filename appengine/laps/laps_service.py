"""Laps microservice."""

import os
import json
import logging
import utils

from google.appengine.api import urlfetch
from flask import Flask, redirect, request

app = Flask(__name__)


@app.route('/laps/increment/<barcode_number>')
@utils.login_required
def increment_laps(barcode_number):
  """Increments the number of laps for the specified barcode by one."""
  url = os.path.join(utils.get_server_base(), 'barcodes.increment_lap_count')
  print url
  result = urlfetch.fetch(
      url=url,
      payload=json.dumps({'barcode_number': int(barcode_number)}),
      method=urlfetch.POST,
      headers=utils.get_protorpc_headers(),
      follow_redirects=False)
  print result.content
  return result.content
      

@app.errorhandler(500)
def server_error(e):
	# Log the error and stacktrace.
	logging.exception('An error occurred during a request.')
	return 'An internal error occurred.', 500

