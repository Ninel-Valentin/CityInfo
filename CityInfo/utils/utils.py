import datetime

def parse_dict_array(input_array):
    output_array = [entry.to_dict() for entry in input_array]
    return output_array

def json_stringify(input_arr):
    output_arr = []
    for input_dict in input_arr:
        output_dict = {}
        for key, value in input_dict.items():
            if isinstance(value, datetime.date):
                output_dict[key] = value.strftime("%Y-%m-%d")
            else:
                output_dict[key] = value
        output_arr.append(output_dict)
    return output_arr

def json_parse(input_dict):
    output_dict = {}
    for key, value in input_dict.items():
        if value.lower() == "true":
            output_dict[key] = True
        elif value.lower() == "false":
            output_dict[key] = False
        else:
            try:
                output_dict[key] = float(value)
            except ValueError:
                output_dict[key] = value
    return output_dict

def process_response(response):
    if not len(response):
        return None, 200  # Success but no content
    response_dict = parse_dict_array(response)
    return response_dict, 200

def validate(fields_validations):
        failed_fields = []
        
        for key, field in fields_validations.items():
            try:
                if(field.get('value')):
                    match field.get('type'):
                        case datetime.date: # Requires dotted notation to work in match
                            parsed_field = field.get('value').split('-')
                            parsed_field = map(lambda date_param: int(date_param), parsed_field)
                            datetime.date(*parsed_field)
                        case __:
                            field.get('type')(field.get('value'))
            except Exception:
                failed_fields.append(key)
                
        return failed_fields

def update_fields(fields_validations, filters):
    for key, value in filters.items():
        if key in fields_validations.keys():
            fields_validations[key].update({"value":value})
