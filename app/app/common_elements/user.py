from app.app.element import REQ, NOTREQ, AppElm

# WARNING: App that uses the following AppElms should be using "default" database.
# RECOMMENDED: Include AppElms in a single app that use "default" database using USER_APP_ELEMENTS macro.

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
class UserTypeAppElm(AppElm): # WARNING: App that uses this AppElm should be using "default" database
    def __init__(self):
        super().__init__("user_type", {
            "private": {
                "model"       : "user.UserType"
            },
            "public": {
                "title": {
                    "singular": "Tipo de usuario" ,
                    "plural"  : "Tipos de usuarios",
                },
                "list_item_fields": ["app","value"],
                "fields": {
                    "app"     : [REQ, "app", "Aplicación"],
                    "value"   : [REQ, "str", "Tipo"      ],
                },
            },
        })
class UserAppElm(AppElm): # WARNING: App that uses this AppElm should be using "default" database
    def __init__(self):
        super().__init__("user", {
            "private": {
                "model"       : "user.User"
            },
            "public": {
                "title": {
                    "singular": "Usuario" ,
                    "plural"  : "Usuarios",
                },
                "list_item_fields": ["username", "email", "type"],
                "fields": {
                    "email"   :[REQ, "str"      , "Email"            ],
                    "username":[REQ, "str"      , "Nombre de usuario"],
                    "type"    :[REQ, "user_type", "Tipo de usuario"  ],
                },
            },
        })

USER_APP_ELEMENTS = [
    AppAppElm     (),
    UserTypeAppElm(),
    UserAppElm    (),
]