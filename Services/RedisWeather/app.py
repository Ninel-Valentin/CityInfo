from flask import Flask, request
from flask_restful import Resource, Api

import json
import os
import logging
import time
import redis

app = Flask("weather")
api = Api(app)

time.sleep(30)

client = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis-weather'))

class Weather(Resource):
    def get(self):
        city = request.args.get('city')
        date = request.args.get('date')
        key = f'{city} - {date}' if date else city
        weather = client.get(key)
        if not weather:
            return 'No data', 204
        weather = json.loads(weather.decode('utf-8'))
        return weather, 200
        
    def post(self):
        keys = ('temperature', 'humidity', 'wind', 'city', 'date')
        weather = {k: request.args.get(k) for k in keys}
        city = request.args.get('city','Brasov')
        date = request.args.get('date', '')
        key = f'{city} - {date}' if date else city
        json_dump = json.dumps(weather)
        client.set(key, json_dump)
        return "OK", 201
    
    def put(self):
        self.post()
        
api.add_resource(Weather,'/weather')

weather = {
    "Brasov":{'temperature':20,"wind":15,"humidity":50},
    "Timisoara":{'temperature':22,"wind":65,"humidity":10},
}

if __name__ == '__main__':
    for city in weather.keys():
        client.set(city, json.dumps(weather[city]))
    app.run(host=os.environ.get('HOST','0.0.0.0'), port=os.environ.get('PORT','5002'))