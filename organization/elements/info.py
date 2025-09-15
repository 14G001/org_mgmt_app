FIELD_PARAM_IS_REQ = 0
FIELD_PARAM_TYPE   = 1
FIELD_PARAM_TITLE  = 2
FIELD_PARAM_EXTRA_INFO = 3

NOTREQ   = False
REQ      = True


class OrgElm:
    def __init__(self, type, info):
        self.type = type
        self.info = info

ORGANIZATION_ELEMENTS_INFO = [
    OrgElm("address", {
        "private": {
            "model": "organization.Address"
        },
        "public": {
            "title": {
                "singular": "Dirección"  ,
                "plural"  : "Direcciones",
            },
            "list_item_fields": ["street_address1", "city", "state_province"],
            "fields": {
                "street_address1":[REQ   , "str", "Dirección 1"],
                "street_address2":[NOTREQ, "str", "Dirección 2"],
                "city"           :[NOTREQ, "str", "Ciudad"          ],
                "state_province" :[NOTREQ, "str", "Estado/Provincia"],
                "postal_code"    :[NOTREQ, "str", "Código Postal"   ],
                "country"        :[REQ   , "str", "País"            ],
            },
        },
    }),
    OrgElm("branch", {
        "private": {
            "model": "organization.OrganizationBranch"
        },
        "public": {
            "title": {
                "singular": "Sede"  ,
                "plural"  : "Sedes",
            },
            "list_item_fields": ["address"],
            "fields": {
                "address":[REQ   , "address", "Dirección"],
                "since"  :[NOTREQ, "date"   , "Desde"    ],
            },
        },
    }),
    OrgElm("person_role_type", {
        "private": {
            "model": "organization.PersonRoleType"
        },
        "public": {
            "title": {
                "singular": "Tipo de rol de persona"    ,
                "plural"  : "Tipos de roles de personas",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value": [REQ, "str", "Tipo"],
            },
        },
    }),
    OrgElm("person_role", {
        "private": {
            "model": "organization.PersonRole"
        },
        "public": {
            "title": {
                "singular": "Rol de persona" ,
                "plural"  : "Roles de personas",
            },
            "list_item_fields": ["person", "type", "start_date", "end_date"],
            "fields": {
                "type"      :[REQ   , "person_role_type", "Tipo"],
                "person"    :[REQ   , "person"  , "Persona"     ],
                "start_date":[REQ   , "date"    , "Desde"       ],
                "end_date"  :[NOTREQ, "date"    , "Hasta"    , {"null_case":"Actualidad"}],
            },
        },
    }),
    OrgElm("person", {
        "private": {
            "model": "organization.Person",
        },
        "public": {
            "title": {
                "singular": "Persona" ,
                "plural"  : "Personas",
            },
            "list_item_fields"  : ["national_id", "name", "surname"],
            "list_item_sort_criteria": ["national_id"],
            "fields": {
                "national_id":[REQ  , "str"    , "DNI"       ],
                "name"      :[REQ   , "str"    , "Nombre/s"  ],
                "surname"   :[REQ   , "str"    , "Apellido/s"],
                "birth_date":[REQ   , "date"   , "Fecha de nacimiento"],
                "residence" :[NOTREQ, "address", "Dirección" ],
            },
        },
    }),
    OrgElm("currency", {
        "private": {
            "model": "organization.Currency"
        },
        "public": {
            "title": {
                "singular": "Moneda" ,
                "plural"  : "Monedas",
            },
            "list_item_fields": ["code"],
            "fields": {
                "code":[REQ, "str", "Código"],
            },
        },
    }),
    OrgElm("money_donation", {
        "private": {
            "model": "organization.MoneyDonation"
        },
        "public": {
            "title": {
                "singular": "Donación de dinero"  ,
                "plural"  : "Donaciones de dinero",
            },
            "list_item_fields": ["date","person","amount","currency"],
            "list_item_sort_criteria": ["-date"],
            "fields": {
                "person"  :[REQ, "person"  , "Persona"],
                "currency":[REQ, "currency", "Moneda" ],
                "amount"  :[REQ, "float"   , "Monto"  ],
                "date"    :[REQ, "date"    , "Fecha"  ],
            },
        },
    }),
    OrgElm("object_type", {
        "private": {
            "model": "organization.ObjectType"
        },
        "public": {
            "title": {
                "singular": "Tipo de object" ,
                "plural"  : "Tipos de objeto",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value":[REQ, "str", "Tipo"],
            },
        },
    }),
    OrgElm("object", {
        "private": {
            "model": "organization.Object"
        },
        "public": {
            "title": {
                "singular": "Objeto" ,
                "plural"  : "Objetos",
            },
            "list_item_fields": ["id", "type"],
            "fields": {
                "type":[REQ, "object_type", "Tipo de objeto"],
                "estimated_cost_currency":[REQ, "currency", "Moneda del costo estimado"],
                "estimated_cost_amount"  :[REQ, "float"   , "Monto del costo estimado" ],
            },
        },
    }),
    OrgElm("object_donation", {
        "private": {
            "model": "organization.ObjectDonation"
        },
        "public": {
            "title": {
                "singular": "Donación de objeto" ,
                "plural"  : "Donación de objetos",
            },
            "list_item_fields": ["date", "donor", "object"],
            "list_item_sort_criteria": ["-date"],
            "fields": {
                "object":[REQ, "object", "Objeto" ],
                "donor" :[REQ, "person", "Donador"],
                "date"  :[REQ, "date"  , "Fecha"  ],
            },
        },
    }),
    OrgElm("object_pass_type", {
        "private": {
            "model": "organization.ObjectPassType"
        },
        "public": {
            "title": {
                "singular": "Tipo de pase de objeto" ,
                "plural"  : "Tipos de pase de objeto",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value": [REQ, "str", "Tipo"],
            },
        },
    }),
    OrgElm("object_pass", {
        "private": {
            "model": "organization.ObjectPass"
        },
        "public": {
            "title": {
                "singular": "Pase de objeto"  ,
                "plural"  : "Pases de objetos",
            },
            "list_item_fields": ["object", "new_person", "datetime", "type"],
            "fields": {
                "object"    :[REQ, "object"  , "Objeto"      ],
                "new_person":[REQ, "person"  , "Dueño nuevo" ],
                "datetime"  :[REQ, "datetime", "Fecha y hora"],
                "type"      :[REQ, "object_pass_type", "Tipo de pase de objeto"],
            },
        },
    }),
    OrgElm("expenditure", {
        "private": {
            "model": "organization.Expenditure"
        },
        "public": {
            "title": {
                "singular": "Gasto" ,
                "plural"  : "Gastos",
            },
            "list_item_fields": ["currency", "amount", "date"],
            "list_item_sort_criteria": ["-date"],
            "fields": {
                "currency":[REQ, "currency", "Moneda"],
                "amount"  :[REQ, "float"   , "Monto" ],
                "date"    :[REQ, "date"    , "Fecha" ],
            },
        },
    }),
]