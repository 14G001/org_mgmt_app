from app.settings import EXAMPLE_APP_INDICATOR

def normalize_app_name(app):
    if app.endswith(EXAMPLE_APP_INDICATOR):
        return app[:(-1)*len(EXAMPLE_APP_INDICATOR)]
    return app