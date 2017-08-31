"""Barcodes microservice."""

import utils
from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service


class IncrementLapRequest(messages.Message):
  """Request to increment the lap count."""
  barcode_number = messages.IntegerField(1)
  increment_by = messages.IntegerField(2, default=1)
  validate = messages.BooleanField(3, default=True)


class IncrementLapResponse(messages.Message):
  """Response from incrementing lap count."""
  student_last_name = messages.StringField(1)
  student_first_name = messages.StringField(2)
  student_photo_url = messages.StringField(3)
  lap_count = messages.IntegerField(4)


# Create the RPC service that handles barcodes.
class BarcodesService(utils.CaminataService):
  """RPC service that handles barcodes."""

  @remote.method(IncrementLapRequest, IncrementLapResponse)
  def increment_lap_count(self, request):
    return IncrementLapResponse(student_last_name='Foo')


# Map the RPC service.
app = service.service_mappings([('/barcodes', BarcodesService)])
