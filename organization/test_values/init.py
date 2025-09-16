from organization.models import (Address, OrganizationBranch, PersonRoleType,
    PersonRole, Person, Currency, MoneyDonation, ObjectType, Object,
    ObjectDonation, ObjectPassType, ObjectPass, Expenditure)
from organization.test_values.utils import get_person_id
from app.settings import ORG_MGMT_APP_EXAMPLE

def create_models(model, records):
    objects = [model(**record) for record in records]
    return model.objects.using(app).bulk_create(objects)

def create_test_branches(app, addresses):
    branches = create_models(OrganizationBranch, [
        {"address":addresses[0], "since":"2024-01-20"},
        {"address":addresses[1], "since":"2024-08-20"},
    ])
    return branches

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
    persons = create_models(Person, test_records)
    half_persons_len = int(NUM_OF_TEST_PERSONS / 2)
    person_roles = []
    for test_record_num in range(0, half_persons_len):
        add_test_person_role(person_roles, persons[test_record_num], person_role_type[0]) # add test members
    for test_record_num in range(half_persons_len, NUM_OF_TEST_PERSONS):
        add_test_person_role(person_roles, persons[test_record_num], person_role_type[1]) # add test beneficiaries
    create_models(PersonRole, person_roles)
    return persons

def create_test_money_donations(currency, persons):
    money_donations = create_models(MoneyDonation, [
        {"person":persons[0], "currency":currency[0], "amount": 3000.00, "date":"2025-11-20"},
        {"person":persons[1], "currency":currency[1], "amount": 7000.00, "date":"2025-11-21"},
        {"person":persons[5], "currency":currency[0], "amount":28000.00, "date":"2025-11-22"},
        {"person":persons[6], "currency":currency[1], "amount":14000.00, "date":"2025-11-23"},
    ])
    return money_donations

def create_test_object(object_type):
    _object = Object.objects.using(ORG_MGMT_APP_EXAMPLE).create(type=object_type)
    return _object
def create_test_object_donations(persons):
    object_types = create_models(ObjectType, [
        {"value":"Buzo"},{"value":"Cama"},{"value":"Horno"}
    ])
    object_donations = create_models(ObjectDonation, [
        {"object":create_test_object(object_types[0]), "donor":persons[0], "date":"2024-07-20"},
        {"object":create_test_object(object_types[1]), "donor":persons[0], "date":"2024-07-21"},
        {"object":create_test_object(object_types[1]), "donor":persons[1], "date":"2024-07-21"},
        {"object":create_test_object(object_types[2]), "donor":persons[5], "date":"2024-07-20"},
    ])
    object_pass_types = create_models(ObjectPassType, [
        {"value":"Transferencia a beneficiario"},
        {"value":"Transferencia a organización"},
        {"value":"Perdido"                     },
    ])
    object_owner_exchanges = create_models(ObjectPass, [
        {"type":object_pass_types[0], "object":object_donations[0].object, "new_person":persons[6], "datetime":"2025-09-20 15:40:40"},
        {"type":object_pass_types[1], "object":object_donations[0].object, "new_person":persons[3], "datetime":"2025-11-21 17:45:45"},
        {"type":object_pass_types[0], "object":object_donations[1].object, "new_person":persons[8], "datetime":"2025-11-21 17:45:45"},
        {"type":object_pass_types[2], "object":object_donations[2].object, "new_person":None      , "datetime":"2025-10-21 16:35:35"}
    ])
    return object_donations

def create_test_expenditures(currency):
    expenditures = create_models(Expenditure, [
        {"date":"2024-05-28", "amount":10000.00, "currency":currency[0]},
        {"date":"2024-09-28", "amount":10000.00, "currency":currency[1]},
        {"date":"2024-11-28", "amount":32000.00, "currency":currency[0]},
        {"date":"2025-09-28", "amount":15000.00, "currency":currency[1]},
    ])
    return expenditures

def init_organization_test_values(app):
    if PersonRoleType.objects.using(app).exists():
        return
    if app == ORG_MGMT_APP_EXAMPLE:
        addresses = create_models(Address, [
            {"street_address1":"San Martin 2382", "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
            {"street_address1":"Yrigoyen 1395"  , "city":"CABA", "state_province":"Buenos Aires", "country":"Argentina",},
        ])
        create_test_branches(app, addresses)
    person_role_type = create_models(PersonRoleType, [
        {"value":"Miembro"}, {"value":"Beneficiario"},
    ])
    if app == ORG_MGMT_APP_EXAMPLE:
        persons = create_test_persons(app, person_role_type)
        currency = create_models(Currency, [{"code":"USD"}, {"code":"ARS"}])
        create_test_money_donations(app, currency, persons)
        create_test_object_donations(app, persons)
        create_test_expenditures(app, currency)