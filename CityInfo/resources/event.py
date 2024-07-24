from flask import request, render_template, make_response
from flask_restful import Resource
from utils.models import db, Event
from utils.utils import parse_dict_array, json_stringify, json_parse, process_response, validate, update_fields

from copy import deepcopy
import datetime

headers = {'Content-Type': 'text/html'}

class EventEndpoint(Resource):
    event_fields = ['enabled', 'category', 'title', 'description', 'city', 'location', 'date', 'price']
    fields_validations = {
            # Values are added
            "price": {
                "type": float
            },
            "date": {
                "type": datetime.date
            }
        }

    def get_events(self):
        filters = {key: request.args.get(key) for key in self.event_fields if request.args.get(key) is not None}
        
        validation_instance = deepcopy(self.fields_validations)
        update_fields(validation_instance, filters)
        validation_results = validate(validation_instance)

        if len(validation_results) > 0:
            return validation_results, 422 # Unprocessable entity

        events = Event.query
        for key, value in filters.items():
            if(value):
                events = events.filter_by(**{key: value})
        return events.all(), 200

    def get(self):
        events, event_code = self.get_events()
        if event_code != 200:
            return {"error": events}, event_code
        
        content_type = request.headers.get('Content-Type') or 'text/html'

        if content_type.lower() == 'application/json':
            events = parse_dict_array(events)
            if events:
                return json_stringify(events), 200
            else:
                return [], 204

        elif content_type.lower() == 'text/html':
            results, status_code = process_response(events, self.event_fields)
            custom_response = render_template('event.html', found=True, results=results or [], fields=self.event_fields), status_code, headers
            return make_response(custom_response)
        else:
            return {"error": "Unknown content-type"}, 415

    def post(self):
        fields = {key: request.args.get(key) for key in self.event_fields if request.args.get(key) is not None}

        if len(fields) != len(self.event_fields):
            missing_fields = [field for field in self.event_fields if field not in fields.keys()]
            return {"missing_fields": missing_fields}, 422

        parsed_fields = json_parse(fields)
        new_event = Event(**parsed_fields)
        db.session.add(new_event)
        db.session.commit()
        return "OK", 200

    def delete(self):
        event_id = request.args.get('id')
        if not event_id:
            return {"error": "ID is required to delete an event"}, 400

        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return {"error": "Event not found"}, 404

        event.enabled = False
        db.session.commit()
        return "Event disabled", 200

    def put(self):
        event_id = request.args.get('id')
        if not event_id:
            return {"error": "ID is required to update an event"}, 400

        event = Event.query.filter_by(id=event_id).first()
        if not event:
            return {"error": "Event not found"}, 404

        fields = {key: request.args.get(key) for key in self.event_fields if request.args.get(key) is not None}
        parsed_fields = json_parse(fields)
        for key, value in parsed_fields.items():
            setattr(event, key, value)
        db.session.commit()
        return "Event updated", 200
