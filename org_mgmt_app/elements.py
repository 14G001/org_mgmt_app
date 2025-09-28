from app.app.common_elements.common_elements import AddressAppElm
from app.app.element import NOTREQ, REQ, AppElm

ORG_MGMT_APP_ELMS_INFO = [
    AddressAppElm("org_mgmt_app"),
    AppElm("address_x_organization", {
        "private": {
            "model": "org_mgmt_app.AddressXOrganization"
        },
        "public": {
            "title": {
                "singular": "Sede de organización"  ,
                "plural"  : "Sedes de organizaciones",
            },
            "list_item_fields": ["address", "organization"],
            "fields": {
                "address"     :[REQ, "address"     , "Dirección"   ],
                "organization":[REQ, "organization", "Organización"],
            },
        },
    }),
    AppElm("organization_type", {
        "private": {
            "model": "org_mgmt_app.OrganizationType"
        },
        "public": {
            "title": {
                "singular": "Tipo de organización"   ,
                "plural"  : "Tipos de organizaciones",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value": [REQ, "str", "Tipo"],
            },
        }
    }),
    AppElm("organization", {
        "private": {
            "model": "org_mgmt_app.Organization"
        },
        "public": {
            "title": {
                "singular": "Organización"  ,
                "plural"  : "Organizaciones",
            },
            "list_item_fields": ["name", "type"],
            "fields": {
                "type": [REQ, "organization_type", "Tipo"  ],
                "name": [REQ, "str"              , "Nombre"],
            },
        }
    }),
    AppElm("person_role_type", {
        "private": {
            "model": "org_mgmt_app.PersonRoleType"
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
    AppElm("person_role", {
        "private": {
            "model": "org_mgmt_app.PersonRole"
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
    AppElm("person", {
        "private": {
            "model": "org_mgmt_app.Person",
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
            },
        },
    }),
    AppElm("currency", {
        "private": {
            "model": "org_mgmt_app.Currency"
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
    AppElm("money_donation", {
        "private": {
            "model": "org_mgmt_app.MoneyDonation"
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
    AppElm("object_type", {
        "private": {
            "model": "org_mgmt_app.ObjectType"
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
    AppElm("object", {
        "private": {
            "model": "org_mgmt_app.Object"
        },
        "public": {
            "title": {
                "singular": "Objeto" ,
                "plural"  : "Objetos",
            },
            "list_item_fields": ["id", "type"],
            "fields": {
                "type":[REQ, "object_type", "Tipo de objeto"],
                "estimated_cost_currency":[NOTREQ, "currency", "Moneda del costo estimado"],
                "estimated_cost_amount"  :[NOTREQ, "float"   , "Monto del costo estimado" ],
            },
        },
    }),
    AppElm("object_donation", {
        "private": {
            "model": "org_mgmt_app.ObjectDonation"
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
    AppElm("object_pass_type", {
        "private": {
            "model": "org_mgmt_app.ObjectPassType"
        },
        "public": {
            "title": {
                "singular": "Tipo de transferencia de objeto" ,
                "plural"  : "Tipos de transferencias de objetos",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value": [REQ, "str", "Tipo"],
            },
        },
    }),
    AppElm("object_pass", {
        "private": {
            "model": "org_mgmt_app.ObjectPass"
        },
        "public": {
            "title": {
                "singular": "Transferencia de objeto"  ,
                "plural"  : "Transferencias de objetos",
            },
            "list_item_fields": ["object", "new_person", "datetime", "type"],
            "fields": {
                "object"    :[REQ, "object"  , "Objeto"      ],
                "new_person":[REQ, "person"  , "Dueño nuevo" ],
                "datetime"  :[REQ, "datetime", "Fecha y hora"],
                "type"      :[REQ, "object_pass_type", "Tipo de transferencia de objeto"],
            },
        },
    }),
    AppElm("service_type", {
        "private": {
            "model": "org_mgmt_app.ServiceType"
        },
        "public": {
            "title": {
                "singular": "Tipo de servicio" ,
                "plural"  : "Tipos de servicios",
            },
            "list_item_fields": ["value"],
            "fields": {
                "value":[REQ, "str", "Tipo"],
            },
        },
    }),
    AppElm("service_donation", {
        "private": {
            "model": "org_mgmt_app.ServiceDonation"
        },
        "public": {
            "title": {
                "singular": "Donación de servicio" ,
                "plural"  : "Donaciones de servicios",
            },
            "list_item_fields": ["date","type","donor","service_start_date"],
            "list_item_sort_criteria": ["-date"],
            "fields": {
                "type" :[REQ, "service_type", "Tipo de servicio"],
                "donor":[REQ, "person"      , "Donador"         ],
                "date" :[REQ, "date"        , "Fecha"           ],
                "service_start_date":[NOTREQ, "date", "Fecha de inicio del servicio"],
                "service_end_date"  :[NOTREQ, "date", "Fecha de fin del servicio"   ],
                "estimated_cost_currency":[NOTREQ, "currency", "Moneda del costo estimado"],
                "estimated_cost_amount"  :[NOTREQ, "float"   , "Monto del costo estimado" ],
            },
        },
    }),
    AppElm("expenditure", {
        "private": {
            "model": "org_mgmt_app.Expenditure"
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