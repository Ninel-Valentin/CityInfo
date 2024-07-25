from flask import Flask, render_template, make_response
from flask_restful import Api

from utils.config import Config
from endpoints.gateway import GatewayEndpoint

import logging
import time
import os

HOST = os.environ.get('HOST') or '0.0.0.0'
PORT = os.environ.get('PORT') or '5000'

cd = os.path.dirname(os.path.realpath(__file__))

app = Flask('CityInfo', template_folder=f'{cd}\\templates', static_folder=f'{cd}\\static')
app.config.from_object(Config)
api = Api(app)

# Logging into text file ! NOT TESTED !
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

api.add_resource(GatewayEndpoint, '/data')

headers = {'Content-Type': 'text/html'}
@app.route('/')
def index():
    return make_response(render_template('index.html', found=True), 200, headers)

time.sleep(30)
if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
