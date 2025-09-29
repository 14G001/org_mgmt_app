from app.apps.apps import get_app_elms_info_source
from app.apps.element_set import get_app_element_set
import json

def _get_app_elms_complete_info(app):
    app_element_set = get_app_element_set(app)
    app_elms_complete_info = app_element_set.get("complete_info")
    if None != app_elms_complete_info:
        return app_elms_complete_info
    app_elms_complete_info = {}
    for app_elm in get_app_elms_info_source(app):
        if app_elm.type in app_elms_complete_info:
            print(f"Error: organization element type '{app_elm.type}' is repeated.")
            quit(1)
        app_elms_complete_info[app_elm.type] = app_elm.info
    app_element_set["complete_info"] = app_elms_complete_info
    return app_elms_complete_info
    

def _get_app_elms_info_type(app, info_type):
    app_element_set = get_app_element_set(app)
    element_info = app_element_set.get(info_type)
    if None != element_info:
        return element_info
    element_info = {}
    app_elms_info = _get_app_elms_complete_info(app)
    for element_type in app_elms_info:
        element_info[element_type] = app_elms_info[element_type][info_type]
    app_element_set[info_type] = element_info
    return element_info

def get_app_elms_private_info(app):
    return _get_app_elms_info_type(app, "private")
def get_app_elms_public_info(app):
    return _get_app_elms_info_type(app, "public" )
def get_app_elms_public_info_str(app):
    app_element_set = get_app_element_set(app)
    app_elms_public_info_str = app_element_set.get("public_str")
    if None == app_elms_public_info_str:
        app_elms_public_info_str = (
            json.dumps(get_app_elms_public_info(app)))
        app_element_set["public_str"] = app_elms_public_info_str
    return app_elms_public_info_str