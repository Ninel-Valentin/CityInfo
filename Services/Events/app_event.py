from flask import Flask, render_template, make_response
from flask_restful import Api

from utils.config import Config
from utils.models import db
from endpoints.event import EventEndpoint

import time
import os

HOST = os.environ.get('HOST') or '0.0.0.0'
PORT = os.environ.get('PORT') or '5001'

cd = os.path.dirname(os.path.realpath(__file__))

app = Flask('EventInfo', template_folder=f'{cd}\\templates', static_folder=f'{cd}\\static')
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

api.add_resource(EventEndpoint, '/events')

headers = {'Content-Type': 'text/html'}

@app.route('/')
def index():
    return make_response(render_template('index.html', found=True), 200, headers)

time.sleep(30)
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Can't connect to the database! Program will close now...\nMessage:\n{repr(e)}")
        exit(0)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
