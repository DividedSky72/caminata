"""Main app."""

import logging
import flask
import os
import utils
from google.appengine.api import users

class _CustomFlask(flask.Flask):
  jinja_options = flask.Flask.jinja_options.copy()
  # Override the template parameter {{ to {{{ for
  # the templating code because it conflicts with
  # Polymer notation.
  jinja_options.update(dict(
      block_start_string='{%',
      block_end_string='%}',
      variable_start_string='{{{',
      variable_end_string='}}}',
      comment_start_string='{#',
      comment_end_string='#}',
  ))

if utils.is_dev_server():
	template_folder = 'frontend'
else:
  template_folder = 'frontend/build/es5-bundled'
app = _CustomFlask(__name__, template_folder=template_folder)


@app.route('/caminata')
def caminata_root():
  user = users.get_current_user()
  print user.nickname(), user.user_id()
  return flask.render_template('index.html')


@app.route('/')
def root():
  print users.create_logout_url('http://www.google.com')
  return flask.redirect(
      os.path.join(utils.get_server_base(), 'caminata'), code=302)





@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500

