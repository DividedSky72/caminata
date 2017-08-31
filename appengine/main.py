"""Main app."""

import logging
import flask
import utils


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
def caminata():
	return flask.render_template('index.html', user='user')


'''
@app.route('/')
def hello():
  return 'Hello main!'
    
@app.route('/<foo>')
def hello_foo(foo):
  return 'Hello %s!' % foo
'''



@app.errorhandler(500)
def server_error(e):
  # Log the error and stacktrace.
  logging.exception('An error occurred during a request.')
  return 'An internal error occurred.', 500

