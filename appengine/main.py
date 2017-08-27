"""Main app."""

import logging

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
  return 'Hello main!'
    
@app.route('/foo')
def hello_foo():
  return 'Hello foo!'




@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500

