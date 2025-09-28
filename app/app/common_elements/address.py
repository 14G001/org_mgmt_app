from app.app.element import REQ, NOTREQ, AppElm

class AddressAppElm(AppElm):
    def __init__(self, app_name):
        super().__init__("address", {
            "private": {
                "model": f"{app_name}.Address"
            },
            "public": {
                "title": {
                    "singular": "Dirección de lugar físico"  ,
                    "plural"  : "Direcciones de lugares físicos",
                },
                "list_item_fields": ["street_address1", "city", "state_province"],
                "fields": {
                    "street_address1":[REQ   , "str", "Dirección"],
                    "street_address2":[NOTREQ, "str", "Dirección 2"],
                    "city"           :[NOTREQ, "str", "Ciudad"          ],
                    "state_province" :[NOTREQ, "str", "Estado/Provincia"],
                    "postal_code"    :[NOTREQ, "str", "Código Postal"   ],
                    "country"        :[REQ   , "str", "País"            ],
                },
            },
        })