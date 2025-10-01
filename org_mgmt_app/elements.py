from app.app.common_elements.address import AddressAppElm
from app.app.element import NOTREQ, REQ, AppElm

ORG_MGMT_APP_ELMS_INFO = [
    AddressAppElm("org_mgmt_app"),
    AppElm("address_x_organization", {
        "private": {
            "model": "org_mgmt_app.AddressXOrganization"
        },
        "public": {
            "title": ["Sede de organización", "Sedes de organizaciones"],
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
            "title": ["Tipo de organización", "Tipos de organizaciones"],
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
            "title": ["Organización", "Organizaciones"],
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
            "title": ["Tipo de rol de persona", "Tipos de roles de personas"],
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
            "title": ["Rol de persona", "Roles de personas"],
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
            "list_item_sort_criteria": ["national_id"],
        },
        "public": {
            "title": ["Persona", "Personas"],
            "list_item_fields"  : ["national_id", "name", "surname"],
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
            "title": ["Moneda", "Monedas"],
            "list_item_fields": ["code"],
            "fields": {
                "code":[REQ, "str", "Código"],
            },
        },
    }),
    AppElm("money_donation", {
        "private": {
            "model": "org_mgmt_app.MoneyDonation",
            "list_item_sort_criteria": ["-date"],
        },
        "public": {
            "title": ["Donación de dinero", "Donaciones de dinero"],
            "list_item_fields": ["date","person","amount","currency"],
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
            "title": ["Tipo de object" ,"Tipos de objeto"],
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
            "title": ["Objeto", "Objetos"],
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
            "model": "org_mgmt_app.ObjectDonation",
            "list_item_sort_criteria": ["-date"],
        },
        "public": {
            "title": ["Donación de objeto", "Donación de objetos"],
            "list_item_fields": ["date", "donor", "object"],
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
            "title": ["Tipo de transferencia de objeto", "Tipos de transferencias de objetos"],
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
            "title": ["Transferencia de objeto", "Transferencias de objetos"],
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
            "title": ["Tipo de servicio", "Tipos de servicios"],
            "list_item_fields": ["value"],
            "fields": {
                "value":[REQ, "str", "Tipo"],
            },
        },
    }),
    AppElm("service_donation", {
        "private": {
            "model": "org_mgmt_app.ServiceDonation",
            "list_item_sort_criteria": ["-date"],
        },
        "public": {
            "title": ["Donación de servicio", "Donaciones de servicios"],
            "list_item_fields": ["date","type","donor","service_start_date"],
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
            "model": "org_mgmt_app.Expenditure",
            "list_item_sort_criteria": ["-date"],
        },
        "public": {
            "title": ["Gasto", "Gastos"],
            "list_item_fields": ["currency", "amount", "date"],
            "fields": {
                "currency":[REQ, "currency", "Moneda"],
                "amount"  :[REQ, "float"   , "Monto" ],
                "date"    :[REQ, "date"    , "Fecha" ],
            },
        },
    }),
]