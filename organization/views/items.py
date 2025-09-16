from django.http import HttpResponse
from django.apps import apps
from app.responses import error, ok
from app.view import SecureView
from app.settings import ORG_MGMT_APP_EXAMPLE
from organization.elements.elements import get_org_elms_public_info, get_org_elms_public_info_str, get_org_elms_private_info, FIELD_PARAM_TYPE
from organization.views.utils.list_item_fields import get_items_list, get_item_list_section
import json
from abc import ABC

org_elms_private_info = get_org_elms_private_info()
org_elms_public_info  = get_org_elms_public_info()

def get_input_field_values(item_type, request):
    input_fields = json.loads(request.body)
    input_field_values = {}
    for field_name in input_fields:
        field_value = input_fields[field_name]
        field_info = org_elms_public_info[item_type]["fields"][field_name]
        if field_info[FIELD_PARAM_TYPE] in org_elms_public_info:
            field_name = f"{field_name}_id"
        input_field_values[field_name] = field_value
    return input_field_values

class ItemsInfoView(SecureView):
    def get(self, request, app):
        return HttpResponse(get_org_elms_public_info_str())
    
class ItemTypeView(SecureView, ABC):
    def validate_message(self, request):
        self.item_type = request.GET.get("item_type")
        self.item_private_info = org_elms_private_info.get(self.item_type)
        self.item_public_info  = org_elms_public_info .get(self.item_type)
        if None == self.item_private_info:
            return error(400, "invalid item type")
        model = self.item_private_info.get("model")
        if None == model:
            item_type = self.item_public_info["source"]["type"]
            model = org_elms_private_info[item_type]["model"]
        self.item_model = apps.get_model(*model.split("."))
        return None
class ItemListView(ItemTypeView):
    def get(self, request, app):
        list_item_fields = org_elms_public_info[self.item_type]["list_item_fields"].copy()
        if "id" not in list_item_fields:
            list_item_fields.append("id")
        return ok(
            items=list(self.item_model.objects.using(app).values(*list_item_fields)))
class ItemsSectionView(ItemTypeView):
    def get(self, request, app):
        return ok(
            section=get_item_list_section(app, self.item_type))
    
class CreateItemView(ItemTypeView):
    def post(self, request, app):
        if app == ORG_MGMT_APP_EXAMPLE:
            return ok()
        try:
            input_fields = get_input_field_values(self.item_type, request)
            created_item = self.item_model.objects.using(app).create(**input_fields)
            list_item_fields = org_elms_public_info[self.item_type]["list_item_fields"]
            created_item_fields = []
            for field in list_item_fields:
                created_item_fields.append(getattr(created_item, field))
            created_item_list_fields = get_items_list(app, self.item_type, [], list_item_fields, 
                self.item_model.objects.using(app).filter(id=created_item.id))
            # TODO: Add specific items updating logic (will require to transfer table generation logic from admin.html to a javascript file)
            return ok(created_item_fields=created_item_list_fields)
        except Exception as e:
            print("Error post CreateItemView:")
            print(e)
            return error(409, str(e))
class ItemView(ItemTypeView):
    def get(self, request, app):
        item_id = request.GET.get("item_id")
        value_types = request.GET.get("value_types")
        item_fields = None
        if value_types == "value":
            item_type_fields = org_elms_public_info[self.item_type].get("fields")
            if None == item_type_fields:
                item_type_fields = org_elms_public_info[self.item_public_info["source"]["type"]]["fields"]
            fields = list(item_type_fields.keys())
            item_fields = self.item_model.objects.using(app).values(*fields).get(id=item_id)
        elif value_types == "info":
            item_fields = get_items_list(app, self.item_type, [],
                list(self.item_public_info["fields"].keys()), self.item_model.objects.using(app).filter(id=item_id))
        else:
            return error(400, f"'{value_types}' value for 'value_type' field is not allowed.")
        return ok(item_fields=item_fields)
class UpdateItemView(ItemTypeView):
    def patch(self, request, app):
        if app == ORG_MGMT_APP_EXAMPLE:
            return ok()
        try:
            print('A')
            input_fields = get_input_field_values(self.item_type, request)
            print(input_fields)
            update_result = self.item_model.objects.using(app).filter(id=request.GET.get("item_id")).update(**input_fields)
            print("UPDATE RESULT")
            print(update_result)
            return ok()
        except Exception as e:
            print("Error post CreateItemView:")
            print(e)
            return error(409, str(e))
class DeleteItemView(ItemTypeView):
    def delete(self, request, app):
        if app == ORG_MGMT_APP_EXAMPLE:
            return ok()
        try:
            self.item_model.objects.using(app).filter(id=request.GET.get("item_id")).delete()
            return ok()
        except Exception as e:
            print("Error post CreateItemView:")
            print(e)
            return error(409, str(e))
