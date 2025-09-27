from utils.common_models import AddressModelBase
from django.db import models as m

class Address(AddressModelBase):
    pass

class OrganizationType(m.Model):
    value = m.TextField(null=False, unique=True)
class Organization(m.Model):
    type = m.ForeignKey(OrganizationType, null=False, on_delete=m.CASCADE)
    name = m.TextField(null=False, unique=True)

class AddressXOrganization(m.Model):
    address      = m.ForeignKey(Address     , null=False, on_delete=m.CASCADE)
    organization = m.ForeignKey(Organization, null=False, on_delete=m.CASCADE)
    class Meta:
        unique_together = (("address","organization",),)

class Person(m.Model):
    national_id     = m.TextField(null=False, unique=True) # Person identifier per country; for example: SSN in United States, DNI in Argentina, etc...
    name            = m.TextField(null=False)
    surname         = m.TextField(null=False)
    birth_date      = m.DateField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
class PersonRoleType(m.Model):
    value           = m.TextField(unique=True) # 'member','beneficiary'
class PersonRole(m.Model):
    type            = m.ForeignKey(PersonRoleType, null=False, on_delete=m.CASCADE)
    person          = m.ForeignKey(Person, null=False, related_name="roles", on_delete=m.CASCADE)
    start_date      = m.DateField(null=False)
    end_date        = m.DateField(null=True) # If it is NULL; it means person still has that role.
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)

class Currency(m.Model):
    code            = m.TextField(null=False, unique=True) # USD, ARS, ...
class MoneyDonation(m.Model):
    person          = m.ForeignKey(Person  , null=False, related_name='money_donations', on_delete=m.CASCADE)
    currency        = m.ForeignKey(Currency, null=False, related_name='donations'      , on_delete=m.CASCADE)
    amount          = m.FloatField(null=False)
    date            = m.DateField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)

class ObjectType(m.Model):
    value           = m.TextField(null=False, unique=True)
class Object(m.Model):
    type            = m.ForeignKey(ObjectType, null=False, on_delete=m.CASCADE)
    estimated_cost_currency = m.ForeignKey(Currency, null=True, on_delete=m.CASCADE)
    estimated_cost_amount   = m.FloatField(null=True)

class ObjectDonation(m.Model):
    object          = m.ForeignKey(Object    , null=False, related_name='donations'       , on_delete=m.CASCADE)
    donor           = m.ForeignKey(Person    , null=False, related_name='object_donations', on_delete=m.CASCADE)
    date            = m.DateField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)

class ObjectPassType(m.Model): # transfer to new beneficiary, transfer to organization, unknown (lost/stolen)
    value           = m.TextField(null=False, unique=True)
class ObjectPass(m.Model):
    type            = m.ForeignKey(ObjectPassType, null=False, on_delete=m.CASCADE)
    object          = m.ForeignKey(Object, null=False, related_name='owner_exchanges' , on_delete=m.CASCADE)
    new_person      = m.ForeignKey(Person, null=True , related_name='objects_received', on_delete=m.CASCADE) # If person is NULL; it means it was lost or stolen
    datetime        = m.DateTimeField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)

class ServiceType(m.Model):
    value = m.TextField(null=False)
class ServiceDonation(m.Model):
    type  = m.ForeignKey(ServiceType, null=False, on_delete=m.CASCADE)
    donor = m.ForeignKey(Person     , null=False, on_delete=m.CASCADE)
    date  = m.DateField(null=False)
    estimated_cost_currency = m.ForeignKey(Currency, null=True, on_delete=m.CASCADE)
    estimated_cost_amount   = m.FloatField(null=True)
    service_start_date      = m.DateField (null=True)
    service_end_date        = m.DateField (null=True)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)

class Expenditure(m.Model):
    date            = m.DateField(null=False)
    currency        = m.ForeignKey(Currency, on_delete=m.CASCADE)
    amount          = m.FloatField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
