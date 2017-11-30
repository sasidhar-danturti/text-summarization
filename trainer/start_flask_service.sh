openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

python prediction_service.py


#FLASK_APP=prediction_service.py python -m   flask run --host 0.0.0.0
