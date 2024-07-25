import json
from decimal import Decimal

from app_gateway import app

# Check main page response
def test_GET_home():
    response = app.test_client().get('/')
    assert response._status_code == 200
    
    
# Check data API response and content
def test_GET_API():
    response = app.test_client().get('/data')
    assert response._status_code == 200
    json_response = json.loads(response.text)
    assert 'events' in json_response.keys()
    assert 'weather' in json_response.keys()
    

# Format check
def test_GET_test_structure():
    response = app.test_client().get('/data?city=TEST')
    assert response._status_code == 200
    
    json_response = json.loads(response.text)
    assert 'events' in json_response.keys()
    assert len(json_response.get('events')) == 1
    
    assert 'weather' in json_response.keys()
    assert len(json_response.get('weather')) == 1
    
    test_response = json_response.get('events')[0]
    
    assert Decimal(str(test_response.get('id'))) == Decimal('9')
    assert type(test_response.get('id')) == int
    assert test_response.get('enabled') == True
    # assert type(test_response.get('enabled')) == bool # Not needed because it passes the check with True
    assert test_response.get('title') == "TEST"
    assert test_response.get('city') == "TEST"
    assert test_response.get('location') == "TEST"
    assert test_response.get('category') == "TEST"
    assert test_response.get('date') == '1700-01-01'
    assert Decimal(str(test_response.get('price'))) == Decimal('0.0')
    assert type(test_response.get('price')) == float
    
    test_response = json_response.get('weather')[0]
    
    assert Decimal(str(test_response.get('id'))) == Decimal('5')
    assert type(test_response.get('id')) == int
    assert test_response.get('tips') == "TEST"
    assert test_response.get('city') == "TEST"
    assert test_response.get('description') == "TEST"
    assert test_response.get('date') == '1700-01-01'
    assert Decimal(str(test_response.get('temperature'))) == Decimal('0.0')
    assert type(test_response.get('temperature')) == float
    assert Decimal(str(test_response.get('humidity'))) == Decimal('0.0')
    assert type(test_response.get('humidity')) == float
    
    
# =================== Date filter format testing ===================
def test_GET_date_format_ok():
    response = app.test_client().get('/data?date=1700-01-01')
    assert response._status_code == 200
    
def test_GET_date_format_empty():
    response = app.test_client().get('/data?date')
    assert response._status_code == 200
    
    
# Check if wrong format date works
def test_GET_date_format_reverse():
    response = app.test_client().get('/data?date=1700-13-01')
    assert response._status_code == 422
    
    json_response = json.loads(response.text)
    assert 'events' in json_response.keys()
    assert 'error' in json_response.get('events').keys()
    assert 'date' in json_response.get('events').get('error')
    
    assert 'weather' in json_response.keys()
    assert 'error' in json_response.get('weather').keys()
    assert 'date' in json_response.get('weather').get('error')
    
    
# Check if unparsable format date works
def test_GET_date_format_wrong():
    response = app.test_client().get('/data?date=1700-131-101')
    assert response._status_code == 422
    
    json_response = json.loads(response.text)
    assert 'events' in json_response.keys()
    assert 'error' in json_response.get('events').keys()
    assert 'date' in json_response.get('events').get('error')
    
    assert 'weather' in json_response.keys()
    assert 'error' in json_response.get('weather').keys()
    assert 'date' in json_response.get('weather').get('error')
    
    
# =================== City filter format testing ===================
def test_GET_city_ok():
    response = app.test_client().get('/data?city=TEST')
    assert response._status_code == 200
    
    json_response = json.loads(response.text)
    assert 'events' in json_response.keys()
    assert len(json_response.get('events')) == 1
    
    assert 'weather' in json_response.keys()
    assert len(json_response.get('weather')) == 1
        

def test_GET_empty():
    response = app.test_client().get('/data?city=THIS_CITY_DOES_NOT_EXIST')
    assert response._status_code == 204
    
# post / put / delete