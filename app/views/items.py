from django.http import HttpResponse
from django.apps import apps
from app.responses import error, ok
from app.view import SecureView
from app.apps.info import EXAMPLE_APP_INDICATOR
from app.app.elements import get_app_elms_public_info, get_app_elms_public_info_str, get_app_elms_private_info
from app.app.element import FIELD_PARAM_TYPE
from app.views.utils.list_item_fields import get_items_list, get_item_list_section
import json
from abc import ABC

def get_input_field_values(item_type, request, app):
    app_elms_public_info = get_app_elms_public_info(app)
    input_fields = json.loads(request.body)
    input_field_values = {}
    for field_name in input_fields:
        field_value = input_fields[field_name]
        field_info = app_elms_public_info[item_type]["fields"][field_name]
        if field_info[FIELD_PARAM_TYPE] in app_elms_public_info:
            field_name = f"{field_name}_id"
        input_field_values[field_name] = field_value
    return input_field_values

class ItemsInfoView(SecureView):
    def get(self, request, app):
        return HttpResponse(get_app_elms_public_info_str(app))
    
class ItemTypeView(SecureView, ABC):
    def validate_message(self, request, app):
        self.item_type = request.GET.get("item_type")
        app_elms_private_info = get_app_elms_private_info(app)
        self.item_private_info = app_elms_private_info.get(self.item_type)
        self.item_public_info  = get_app_elms_public_info (app).get(self.item_type)
        if None == self.item_private_info:
            return error(400, "invalid item type")
        model = self.item_private_info.get("model")
        self.item_model = apps.get_model(*model.split("."))
        return None
class ItemListView(ItemTypeView):
    def get(self, request, app):
        list_item_fields = get_app_elms_public_info(app)[self.item_type]["list_item_fields"].copy()
        if "id" not in list_item_fields:
            list_item_fields.append("id")
        return ok(
            items=list(self.item_model.objects.using(app).values(*list_item_fields)))
class ItemsSectionView(ItemTypeView):
    def get(self, request, app):
        print("B")
        return ok(
            section=get_item_list_section(
            request, app, self.item_type))
    
class CreateItemView(ItemTypeView):
    def post(self, request, app):
        if app.endswith(EXAMPLE_APP_INDICATOR):
            return ok()
        try:
            input_fields = get_input_field_values(self.item_type, request, app)
            created_item = self.item_model.objects.using(app).create(**input_fields)
            list_item_fields = get_app_elms_public_info(app)[self.item_type]["list_item_fields"]
            created_item_fields = []
            for field in list_item_fields:
                created_item_fields.append(getattr(created_item, field))
            created_item_list_fields = get_items_list(request, app, self.item_type, list_item_fields, 
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
            app_elms_public_info = get_app_elms_public_info(app)
            item_type_fields = app_elms_public_info[self.item_type].get("fields")
            if None == item_type_fields:
                item_type_fields = app_elms_public_info[self.item_public_info["source"]["type"]]["fields"]
            fields = list(item_type_fields.keys())
            item_fields = self.item_model.objects.using(app).values(*fields).get(id=item_id)
        elif value_types == "info":
            item_fields = get_items_list(request, app, self.item_type,
                list(self.item_public_info["fields"].keys()), self.item_model.objects.using(app).filter(id=item_id))
        else:
            return error(400, f"'{value_types}' value for 'value_type' field is not allowed.")
        return ok(item_fields=item_fields)
class UpdateItemView(ItemTypeView):
    def patch(self, request, app):
        if app.endswith(EXAMPLE_APP_INDICATOR):
            return ok()
        try:
            print('A')
            input_fields = get_input_field_values(self.item_type, request, app)
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
        if app.endswith(EXAMPLE_APP_INDICATOR):
            return ok()
        try:
            self.item_model.objects.using(app).filter(id=request.GET.get("item_id")).delete()
            return ok()
        except Exception as e:
            print("Error post CreateItemView:")
            print(e)
            return error(409, str(e))
