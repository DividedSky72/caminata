"""Model definitions for app users."""

from google.appengine.ext import ndb

class CaminataInvitedUser(ndb.Model):
  """Invited users of the app."""
  email = ndb.StringProperty(indexed=True)
  dashboard_access = ndb.BooleanProperty(indexed=False)
  students_access = ndb.BooleanProperty(indexed=False)
  laps_access = ndb.BooleanProperty(indexed=False)

class CaminataUser(CaminataInvitedUser):
  """Users of the app."""
  user_id = ndb.StringProperty(required=True)

  @classmethod
  def from_invited_user(cls, invited_user, user_id):
    return cls(
        user_id=user_id,
        email=invited_user.email,
        dashboard_access=invited_user.dashboard_access,
        students_access=invited_user.students_access,
        laps_access=invited_user.laps_access)
    