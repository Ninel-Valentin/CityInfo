from flask import request
from flask_restful import Resource
import requests

EVENT_URL = 'http://10.2.98.193:5001/events'
WEATHER_URL = 'http://10.2.98.193:5002/weather'
headers = {'Content-Type': 'application/json'}

class GatewayEndpoint(Resource):
    filter_fields = ['city', 'date']
    
    def get(self):
        filters = {key: request.args.get(key) for key in self.filter_fields if request.args.get(key) is not None}
        url_filter = "&".join(list(map(lambda entry : f"{entry[0]}={entry[1]}", filters.items())))
        
        event_url = f"{EVENT_URL}?{url_filter}" if url_filter else EVENT_URL
        weather_url = f"{WEATHER_URL}?{url_filter}" if url_filter else WEATHER_URL

        response = {}
        status_code = 200
        
        try:
            event_request = requests.get(event_url, headers=headers)
            status_code = event_request.status_code
            
            response.update({"events": event_request.json()})
        except:
            response.update({"events": {
                "error": "Unavailable service",
                "status_code": 503
            }});
        
        try:
            weather_request = requests.get(weather_url, headers=headers)
            status_code = status_code if status_code == weather_request.status_code else 200 # Return the common status, if not common return 200
            
            response.update({"weather": weather_request.json()})
        except:
            response.update({"weather": {
                "error": "Unavailable service",
                "status_code": 503
            }});
            
        return response, status_code
        
    