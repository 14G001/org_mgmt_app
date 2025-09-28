from app.model import AppModel
import django.db.models as m

class AddressModelBase(AppModel):
    street_address1 = m.TextField(null=False)
    street_address2 = m.TextField(null=True )
    city            = m.TextField(null=True )
    state_province  = m.TextField(null=True )
    postal_code     = m.TextField(null=True )
    country         = m.TextField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
    class Meta:
        abstract = True

class PersonModelBase(AppModel):
    national_id     = m.TextField(null=False, unique=True) # Person identifier per country; for example: SSN in United States, DNI in Argentina, etc...
    name            = m.TextField(null=False)
    surname         = m.TextField(null=False)
    birth_date      = m.DateField(null=False)
    db_add_datetime = m.DateTimeField(null=False, auto_now_add=True)
    class Meta:
        abstract = True