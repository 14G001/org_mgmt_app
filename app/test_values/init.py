from app.test_values.app.org_mgmt_app import init_org_mgmt_app_db_test_values
from app.settings import APP_TYPE_ORG_MGMT_APP
from app.apps import get_app_type

def init_db_test_values(app):
    if APP_TYPE_ORG_MGMT_APP == get_app_type(app):
        init_org_mgmt_app_db_test_values(app)
        return
    # else; is exa_teachers app
    return