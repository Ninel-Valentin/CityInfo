from flask import Flask, render_template, make_response
from flask_restful import Api

from utils.config import Config
from resources.gateway import GatewayEndpoint

import os
cd = os.path.dirname(os.path.realpath(__file__))

app = Flask('CityInfo', template_folder=f'{cd}\\templates', static_folder=f'{cd}\\static')
app.config.from_object(Config)
api = Api(app)

api.add_resource(GatewayEndpoint, '/data')

headers = {'Content-Type': 'text/html'}
@app.route('/')
def index():
    return make_response(render_template('index.html', found=True), 200, headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
