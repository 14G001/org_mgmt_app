from app.app.element import REQ, NOTREQ, AppElm

# WARNING: App that uses the following AppElms should be using "default" database.
# RECOMMENDED: Include AppElms in a single app that use "default" database using USER_APP_ELEMENTS macro.

DEBUG_ALL_APPS = False # Only for tests: shows all available apps appart of current app

class AppAppElm(AppElm):
    def __init__(self):
        super().__init__("app", {
            "private": {
                "model"       : "user.App"
            },
            "public": {
                "title": {
                    "singular": "Aplicación"  ,
                    "plural"  : "Aplicaciones",
                },
                "list_item_fields": ["name"],
                "fields": {
                    "name": [REQ, "str", "ID"],
                },
            },
        })
class UserTypeAppElm(AppElm):
    def get_info(self):
        info = {
            "private": {
                "model"       : "user.UserType"
            },
            "public": {
                "title": {
                    "singular": "Tipo de usuario" ,
                    "plural"  : "Tipos de usuarios",
                },
                "list_item_fields": ["title"],
                "fields": {
                    "title"   : [REQ, "str", "Tipo"],
                },
            },
        }
        if DEBUG_ALL_APPS:
            public_info = info["public"]
            public_info["list_item_fields"].insert(0, "app")
            public_info["fields"]["app"] = [REQ, "app", "Aplicación"]
        return info
    def __init__(self):
        super().__init__("user_type", self.get_info())
class UserAppElm(AppElm):
    def __init__(self):
        super().__init__("user", {
            "private": {
                "model"       : "user.User",
                "list_item_sort_criteria": ["type__title", "name", "surname"],
            },
            "public": {
                "title": {
                    "singular": "Usuario" ,
                    "plural"  : "Usuarios",
                },
                "list_item_fields": ["type", "name", "surname", "username", ],
                "fields": {
                    "email"   :[REQ, "str"      , "Email"            ],
                    "username":[REQ, "str"      , "Nombre de usuario"],
                    "name"    :[REQ, "str"      , "Nombre"           ],
                    "surname" :[REQ, "str"      , "Apellido"         ],
                    "type"    :[REQ, "user_type", "Tipo de usuario"  ],
                },
            },
        })

def get_user_app_elements():
    user_app_elements = []
    if DEBUG_ALL_APPS:
        user_app_elements.append(AppAppElm())
    user_app_elements += [
        UserTypeAppElm(),
        UserAppElm    (),
    ]
    return user_app_elements
USER_APP_ELEMENTS = get_user_app_elements()