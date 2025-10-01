TITLE_SINGULAR = 0
TITLE_PLURAL   = 1

FIELD_PARAM_IS_REQ = 0
FIELD_PARAM_TYPE   = 1
FIELD_PARAM_TITLE  = 2
FIELD_PARAM_EXTRA_INFO = 3

NOTREQ   = False
REQ      = True

class AppElm:
    def __init__(self, type, info):
        self.type = type
        self.info = info