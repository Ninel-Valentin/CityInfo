from flask import request, render_template, make_response
from flask_restful import Resource
from utils.models import db, Weather
from utils.utils import parse_dict_array, json_stringify, json_parse, process_response, validate, update_fields

from copy import deepcopy
import datetime

headers = {'Content-Type': 'text/html'}

class WeatherEndpoint(Resource):
    weather_fields = ['humidity', 'temperature', 'tips', 'description', 'date', 'city']
    fields_validations = {
        # Values are added
        "humidity": {
            "type": float
        },
        "temperature": {
            "type": float
        },
        "date": {
            "type": datetime.date
        }
    }
    
    def get_weather(self):
        filters = {key: request.args.get(key) for key in self.weather_fields if request.args.get(key) is not None}

        validation_instance = deepcopy(self.fields_validations)
        update_fields(validation_instance, filters)
        validation_results = validate(validation_instance)

        if len(validation_results) > 0:
            return validation_results, 422 # Unprocessable entity

        weather = Weather.query
        for key, value in filters.items():
            if(value):
                weather = weather.filter_by(**{key: value})
        return weather.all(), 200

    def get(self):
        weather, weather_code = self.get_weather()
        if weather_code != 200:
            return {"error": weather}, weather_code
        
        content_type = request.headers.get('Content-Type') or 'text/html'

        if content_type.lower() == 'application/json':
            weather = parse_dict_array(weather)
            if weather:
                return json_stringify(weather), 200
            else:
                return [], 204

        elif content_type.lower() == 'text/html':
            results, status_code = process_response(weather, self.weather_fields)
            custom_response = render_template('weather.html', found=True, results=results or [], fields=self.weather_fields), status_code, headers
            return make_response(custom_response)
        else:
            return {"error": "Unknown content-type"}, 415

    def post(self):
        fields = {key: request.args.get(key) for key in self.weather_fields if request.args.get(key) is not None}

        if len(fields) != len(self.weather_fields):
            missing_fields = [field for field in self.weather_fields if field not in fields.keys()]
            return {"missing_fields": missing_fields}, 422

        parsed_fields = json_parse(fields)
        new_weather = Weather(**parsed_fields)
        db.session.add(new_weather)
        db.session.commit()
        return "OK", 200

    def delete(self):
        weather_id = request.args.get('id')
        if not weather_id:
            return {"error": "ID is required to delete a weather entry"}, 400

        weather = Weather.query.filter_by(id=weather_id).first()
        if not weather:
            return {"error": "Weather entry not found"}, 404

        db.session.delete(weather)
        db.session.commit()
        return "Weather entry deleted", 200

    def put(self):
        weather_id = request.args.get('id')
        if not weather_id:
            return {"error": "ID is required to update a weather entry"}, 400

        weather = Weather.query.filter_by(id=weather_id).first()
        if not weather:
            return {"error": "Weather entry not found"}, 404

        fields = {key: request.args.get(key) for key in self.weather_fields if request.args.get(key) is not None}
        parsed_fields = json_parse(fields)
        for key, value in parsed_fields.items():
            setattr(weather, key, value)
        db.session.commit()
        return "Weather entry updated", 200
