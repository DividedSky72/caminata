""" Laps microservice."""

import logging

from flask import Flask


app = Flask(__name__)

@app.route('/laps/increment/<badge_number>')
def increment_laps(badge_number):
  """Increments the number of laps for the specified badge by one."""
  return 'Hello laps increment %s' % badge_number


@app.errorhandler(500)
def server_error(e):
	# Log the error and stacktrace.
	logging.exception('An error occurred during a request.')
	return 'An internal error occurred.', 500

