"""Caminata usrs microservice."""

import utils
from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service


class GetCaminataUserRequest(messages.Message):
  """Request to increment the lap count."""
  barcode_number = messages.IntegerField(1)
  increment_by = messages.IntegerField(2, default=1)
  validate = messages.BooleanField(3, default=True)


class GetCaminataUserResponse(messages.Message):
  """Response from incrementing lap count."""
  caminata_user_email = messages.StringField(1)
  caminata_user_id = messages.StringField(2)
  dashboard_access = messages.BooleanField(3)
  students_access = messages.BooleanField(4)
  lapsaccess = messages.BooleanField(5)


# Create the RPC service that handles caminata users.
class CaminataUsersService(utils.CaminataService):
  """RPC service that handles barcodes."""

  @remote.method(GetCaminataUserRequest, GetCaminataUserResponse)
  def get_caminata_user(self, request):
    pass


# Map the RPC service.
app = service.service_mappings([('/barcodes', BarcodesService)])
