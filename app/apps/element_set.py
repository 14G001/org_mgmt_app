from app.apps.type import get_app_type, APP_TYPE_ORG_MGMT_APP

oma_elms = {}
exa_elms = {}

def get_app_element_set(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        return oma_elms
    return exa_elms