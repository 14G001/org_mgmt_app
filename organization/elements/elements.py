from organization.elements.info import (
    FIELD_PARAM_IS_REQ, FIELD_PARAM_TYPE, FIELD_PARAM_TITLE,
    ORGANIZATION_ELEMENTS_INFO)
import json

_org_elms_info = None
org_elms_private_info    = None
org_elms_public_info     = None
org_elms_public_info_str = None

def _get_org_elms_info():
    global _org_elms_info
    if None != _org_elms_info:
        return _org_elms_info
    _org_elms_info = {}
    for org_elm in ORGANIZATION_ELEMENTS_INFO:
        if org_elm.type in _org_elms_info:
            print(f"Error: organization element type '{org_elm.type}' is repeated.")
            quit(1)
        _org_elms_info[org_elm.type] = org_elm.info
    return _org_elms_info

def _get_org_elms_info_from_type(org_element_info_type):
    elements_info = {}
    org_elms_info = _get_org_elms_info()
    for element_type in org_elms_info:
        elements_info[element_type] = org_elms_info[element_type][org_element_info_type]
    return elements_info

def get_org_elms_private_info():
    global org_elms_private_info
    if None == org_elms_private_info:
        org_elms_private_info = _get_org_elms_info_from_type("private")
    return org_elms_private_info
def get_org_elms_public_info():
    global org_elms_public_info
    if None == org_elms_public_info:
        org_elms_public_info = _get_org_elms_info_from_type("public")
    return org_elms_public_info
def get_org_elms_public_info_str():
    global org_elms_public_info_str
    if None == org_elms_public_info_str:
        org_elms_public_info_str = (
            json.dumps(get_org_elms_public_info()))
    return org_elms_public_info_str