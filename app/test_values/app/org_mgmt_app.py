from org_mgmt_app.models import (Address, AddressXOrganization, OrganizationType,
    Organization, PersonRoleType, PersonRole, Person, Currency, MoneyDonation,
    ObjectType, Object, ObjectDonation, ObjectPassType, ObjectPass,
    ServiceType, ServiceDonation, Expenditure)
from app.test_values.utils import get_person_id
from app.settings import EXAMPLE_APP_INDICATOR, AVAILABLE_APPS

def create_models(app, model, records):
    objects = [model(**record) for record in records]
    return model.objects.using(app).bulk_create(objects)

def create_test_organization_addresses(app, addresses, organization):
    branches = create_models(app, AddressXOrganization, [
        {"address":addresses[0], "organization":organization[0]},
        {"address":addresses[1], "organization":organization[0]},
    ])
    return branches
def get_person_role_types(app):
    if app.startswith("ensenaxargentina"):
        return [
            {"value":"Docente/Participante"  },
            {"value":"Formadores de Docentes"},
            {"value":"Dirección/Gestión"     },
            {"value":"Aliado"                },
            {"value":"Estudiante"            },
        ]
    return [
        {"value":"Miembro"     },
        {"value":"Beneficiario"},
        {"value":"Empleado"    },
    ]

def create_test_organizations(app):
    organization_type = create_models(app, OrganizationType, [
        {"value":"ONG"                    },
        {"value":"Institución Académica"  },
        {"value":"Organización del Estado"},
        {"value":"Empresa"                },
        {"value":"Organismo Internacional"},
    ])

    organization = create_models(app, Organization, [
        {"type":organization_type[0], "name":AVAILABLE_APPS[app]["name"]},
        {"type":organization_type[0], "name":"ONG Externa 1"   },
        {"type":organization_type[0], "name":"ONG Externa 2"   },
        {"type":organization_type[3], "name":"Empresa 1"       },
        {"type":organization_type[3], "name":"Empresa 2"       },
    ])
    return organization

def add_test_person_role(person_roles, person, role_type):
    person_roles.append({
        "type": role_type,
        "person": person,
        "start_date": f"2024-01-{str(get_person_id(person)).rjust(2,'0')}",
    })
def create_test_persons(app, person_role_type):
    if Person.objects.using(app).exists():
        return Person.objects.using(app).all()
    NUM_OF_TEST_PERSONS = 10
    test_records = []
    for test_record_num in range(0, NUM_OF_TEST_PERSONS):
        test_records.append({
            "national_id":31200300 + test_record_num     ,
            "name"      :f"Persona{test_record_num + 1} nombre" ,
            "surname"   :f"Persona{test_record_num + 1} apellido",
            "birth_date":f"1990-03-2{test_record_num}"  ,
        })
    persons = create_models(app, Person, test_records)
    half_persons_len = int(NUM_OF_TEST_PERSONS / 2)
    person_roles = []
    for test_record_num in range(0, half_persons_len):
        add_test_person_role(person_roles, persons[test_record_num], person_role_type[0]) # add test members
    for test_record_num in range(half_persons_len, NUM_OF_TEST_PERSONS):
        add_test_person_role(person_roles, persons[test_record_num], person_role_type[1]) # add test beneficiaries
    create_models(app, PersonRole, person_roles)
    return persons

def create_test_money_donations(app, currency, persons):
    money_donations = create_models(app, MoneyDonation, [
        {"person":persons[0], "currency":currency[0], "amount": 3000.00, "date":"2025-11-20"},
        {"person":persons[1], "currency":currency[1], "amount": 7000.00, "date":"2025-11-21"},
        {"person":persons[5], "currency":currency[0], "amount":28000.00, "date":"2025-11-22"},
        {"person":persons[6], "currency":currency[1], "amount":14000.00, "date":"2025-11-23"},
    ])
    return money_donations

def create_test_object(app, object_type):
    _object = Object.objects.using(app).create(type=object_type)
    return _object
def create_test_object_donations(app, persons):
    object_types = create_models(app, ObjectType, [
        {"value":"Buzo"},{"value":"Cama"},{"value":"Horno"}
    ])
    object_donations = create_models(app, ObjectDonation, [
        {"object":create_test_object(app, object_types[0]), "donor":persons[0], "date":"2024-07-20"},
        {"object":create_test_object(app, object_types[1]), "donor":persons[0], "date":"2024-07-21"},
        {"object":create_test_object(app, object_types[1]), "donor":persons[1], "date":"2024-07-21"},
        {"object":create_test_object(app, object_types[2]), "donor":persons[5], "date":"2024-07-20"},
    ])
    object_pass_types = create_models(app, ObjectPassType, [
        {"value":"Transferencia a institución académica"},
        {"value":"Transferencia a organización"         },
        {"value":"Perdido"                              },
    ])
    object_owner_exchanges = create_models(app, ObjectPass, [
        {"type":object_pass_types[0], "object":object_donations[0].object, "new_person":persons[6], "datetime":"2025-09-20 15:40:40"},
        {"type":object_pass_types[1], "object":object_donations[0].object, "new_person":persons[3], "datetime":"2025-11-21 17:45:45"},
        {"type":object_pass_types[0], "object":object_donations[1].object, "new_person":persons[8], "datetime":"2025-11-21 17:45:45"},
        {"type":object_pass_types[2], "object":object_donations[2].object, "new_person":None      , "datetime":"2025-10-21 16:35:35"}
    ])
    return object_donations

def create_test_service_donations(app, persons):
    service_type = create_models(app, ServiceType, [
        {"value":"Educación y capacitación"      },
        {"value":"Asesoría legal"                },
        {"value":"Asesoría contable o impositiva"},
        {"value":"Diseño y contenido audiovisual"},
        {"value":"Transporte"                    },
        {"value":"Desarrollo o mantenimiento de sitios web"},
    ])
    service_donations = create_models(app, ServiceDonation, [
        {"type":service_type[0], "donor":persons[0], "date":"2025-11-20", "service_start_date":"2025-11-20", "service_end_date":"2026-11-20"},
        {"type":service_type[0], "donor":persons[1], "date":"2025-11-21", "service_start_date":"2025-11-21", "service_end_date":"2026-11-21"},
        {"type":service_type[3], "donor":persons[5], "date":"2025-11-22", "service_start_date":"2025-11-22", "service_end_date":"2026-11-22"},
        {"type":service_type[3], "donor":persons[6], "date":"2025-11-23", "service_start_date":"2025-11-23", "service_end_date":"2026-11-23"},
    ])
    return service_donations

def create_test_expenditures(app, currency):
    expenditures = create_models(app, Expenditure, [
        {"date":"2024-05-28", "amount":10000.00, "currency":currency[0]},
        {"date":"2024-09-28", "amount":10000.00, "currency":currency[1]},
        {"date":"2024-11-28", "amount":32000.00, "currency":currency[0]},
        {"date":"2025-09-28", "amount":15000.00, "currency":currency[1]},
    ])
    return expenditures

def init_org_mgmt_app_db_test_values(app):
    if PersonRoleType.objects.using(app).exists():
        return
    is_example_app = app.endswith(EXAMPLE_APP_INDICATOR)
    if is_example_app:
        addresses = create_models(app, Address, [
            {"street_address1":"San Martin 2382", "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
            {"street_address1":"Yrigoyen 1395"  , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        ])
        organization = create_test_organizations(app)
        create_test_organization_addresses(app, addresses, organization)
    person_role_type = create_models(app, PersonRoleType, get_person_role_types(app))
    if is_example_app:
        persons = create_test_persons(app, person_role_type)
        currency = create_models(app, Currency, [{"code":"USD"}, {"code":"ARS"}])
        create_test_money_donations(app, currency, persons)
        create_test_object_donations(app, persons)
        create_test_service_donations(app, persons)
        create_test_expenditures(app, currency)