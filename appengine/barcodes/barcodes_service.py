"""Barcodes microservice."""

from protorpc import messages
from protorpc import remote
from protorpc.wsgi import service

package = ''

'''
curl -H \
   'content-type:application/json' \
   -d '{"barcode_number": 1}'\
   https://8080-dot-3036522-dot-devshell.appspot.com/barcodes/increment_lap_countx
   
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8080/barcodes/increment_lap_count
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8083/barcodes/increment_lap_count   
curl -X GET http://0.0.0.0:8080/laps/increment/1   
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8083/barcodes.increment_lap_count
'''

# Request to increment the lap count.
class IncrementLapRequest(messages.Message):
  barcode_number = messages.IntegerField(1)
  increment_by = messages.IntegerField(2, default=1)
  validate = messages.BooleanField(3, default=True)


# Response from incrementing lap count.
class IncrementLapResponse(messages.Message):
  student_last_name = messages.StringField(1)
  student_first_name = messages.StringField(2)
  student_photo_url = messages.StringField(3)
  lap_count = messages.IntegerField(4)


# Create the RPC service that handles barcodes.
class BarcodesService(remote.Service):

    @remote.method(IncrementLapRequest, IncrementLapResponse)
    def increment_lap_count(self, request):
      return IncrementLapResponse(student_last_name='Foo')

# Map the RPC service.
app = service.service_mappings([('/barcodes', BarcodesService)])
