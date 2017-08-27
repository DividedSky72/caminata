# Caminata Lap Tracking App

dev_appserver.py app.yaml dispatch.yaml laps/laps.yaml barcodes/barcodes.yaml

curl -H \
   'content-type:application/json' \
   -d '{"barcode_number": 1}'\
   https://8080-dot-3036522-dot-devshell.appspot.com/barcodes/increment_lap_countx
   
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8080/barcodes/increment_lap_count
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8083/barcodes/increment_lap_count   
curl -X GET http://0.0.0.0:8080/laps/increment/1   
curl -H 'content-type:application/json' -d '{"barcode_number": 1}' http://0.0.0.0:8083/barcodes.increment_lap_count