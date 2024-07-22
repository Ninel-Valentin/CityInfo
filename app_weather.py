from flask import Flask, render_template, make_response
from flask_restful import Api

from utils.config import Config
from utils.models import db
from resources.weather import WeatherEndpoint

import os
cd = os.path.dirname(os.path.realpath(__file__))

app = Flask('WeatherInfo', template_folder=f'{cd}\\templates', static_folder=f'{cd}\\static')
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

api.add_resource(WeatherEndpoint, '/weather')

headers = {'Content-Type': 'text/html'}

@app.route('/')
def index():
    return make_response(render_template('index.html', found=True), 200, headers)

with app.app_context():
    try:
        db.create_all()
    except Exception:
        print("Can't connect to the database! Program will close now...")
        exit(0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
