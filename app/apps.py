from app.app.utils import normalize_app_name
from app.settings import ORG_MGMT_APPS, APP_TYPE_ORG_MGMT_APP, APP_TYPE_EXA_TEACHERS
from org_mgmt_app.elements.info import ORG_MGMT_APP_ELMS_INFO
from exa_teachers.elements.info import EXA_TEACHERS_APP_ELMS_INFO

oma_elms       = {}
exa_tchrs_elms = {}

def get_app_type(app):
    app = normalize_app_name(app)
    if app in ORG_MGMT_APPS:
        return APP_TYPE_ORG_MGMT_APP
    return APP_TYPE_EXA_TEACHERS
def get_app_element_set(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        return oma_elms
    return exa_tchrs_elms
def get_app_elms_info_source(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        return ORG_MGMT_APP_ELMS_INFO
    return EXA_TEACHERS_APP_ELMS_INFO