"""Caminata usrs microservice."""

import ast
import logging
import utils

from google.appengine.api import users
from google.appengine.ext import ndb

from flask import abort, Flask, redirect, request
from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service

import caminata_users_models


class GetCaminataUserRequest(messages.Message):
  """Request to get the current user."""


class GetCaminataUserResponse(messages.Message):
  """Response from incrementing lap count."""
  email = messages.StringField(1)
  nickname = messages.StringField(2)
  dashboard_access = messages.BooleanField(3)
  students_access = messages.BooleanField(4)
  laps_access = messages.BooleanField(5)


# Create the RPC service that handles caminata users.

class CaminataUsersService(utils.CaminataService):
  """RPC service that handles barcodes."""

  @remote.method(GetCaminataUserRequest, GetCaminataUserResponse)
  def get_caminata_user(self, _):
    user = user.get_current_user()
    if not user:
      raise remote.ApplicationError('User not logged in.')
      
    # Look for a user
    caminata_user_key = ndb.Key(
        caminata_users_models.CaminataUser, user.user_id())
    caminata_user = caminata_user_key.get()
    
    # If user not there, maybe they are invited, look them up
    # by email.
    if not caminata_user:
      invited_caminata_user_key = ndb.Key(
        caminata_users_models.InvitedCaminataUser, user.email().lower())
      invited_caminata_user = invited_caminata_user_key.get()
      if not invited_caminata_user:
        raise remote.ApplicationError('User not authorized.')
      caminata_user = caminata_users_models.CaminataUser.from_invited_user(
          invited_caminata_user, user.user_id())
      caminata_user.key = ndb.Key(caminata_users_models.CaminataUser, user.user_id())
      caminata_user.put()
      
    return GetCaminataUserResponse(
        email=caminata_user.email,
        nickname=caminata_user.nickname,
        dashboard_access=caminata_user.dashboard_access,
        students_access=caminata_user.students_access,
        laps_access=caminata_user.laps_access)

app = service.service_mappings([('/caminata_users/user', CaminataUsersService)])

"""
Below is the flask app for invited users. We keep it as a separate app since it can
handle a get request, which protorpc cannot, and we want to be able to invite users with a
GET in a browser.

To use the invited api you must be an admin. On the dev server log out with

/_ah/login?&action=logout

Then log back in as an admin.

Examples

https://8080-dot-3036522-dot-devshell.appspot.com/caminata_users/invite/?email=dashboard@caminata.com&dashboard=True
https://8080-dot-3036522-dot-devshell.appspot.com/caminata_users/invite/?email=students@caminata.com&students=True
https://8080-dot-3036522-dot-devshell.appspot.com/caminata_users/invite/?email=laps@caminata.com&laps=True
https://8080-dot-3036522-dot-devshell.appspot.com/caminata_users/invite/?email=all_access@caminata.com&laps=True&dashboard=True&students=True
"""


invite_app = Flask(__name__)

@invite_app.route('/caminata_users/invite/')
def invite():
  email = request.args.get('email')
  if not email:
    abort(400, 'No email supplied')
    
  email = email.lower()

  try:
    dashboard_access = ast.literal_eval(request.args.get('dashboard'))
  except ValueError:
    dashboard_access = False
    
  try:
    students_access = ast.literal_eval(request.args.get('students'))
  except ValueError:
    students_access = False
    
  try:
    laps_access = ast.literal_eval(request.args.get('laps'))
  except ValueError:
    laps_access = False

  invited_user_model = caminata_users_models.CaminataInvitedUser(
      email=email,
      dashboard_access=dashboard_access,
      students_access=students_access,
      laps_access=laps_access)
  invited_user_model.key = ndb.Key(caminata_users_models.CaminataInvitedUser, email)
  invited_user_model.put()
  logging.info('Invited %s' % email)
  return 'Invited %s' % email
