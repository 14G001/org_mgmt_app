from app.app.elements import get_app_elms_public_info
from app.app.element import FIELD_PARAM_TYPE

def get_input_field_values(app, item_type, body):
    app_elms_public_info = get_app_elms_public_info(app)
    input_fields = body["values"]
    input_field_values = {}
    for field_name in input_fields:
        field_value = input_fields[field_name]
        field_info = app_elms_public_info[item_type]["fields"][field_name]
        if field_info[FIELD_PARAM_TYPE] in app_elms_public_info:
            field_name = f"{field_name}_id" # If orm was not this way this would not be necessary
        input_field_values[field_name] = field_value
    return input_field_values