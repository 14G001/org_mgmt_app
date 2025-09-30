from django.http import HttpResponse
from django.apps import apps
from django.db.models import Q
from app.responses import error, ok, not_authorized
from app.view import SecureView
from app.apps.info import EXAMPLE_APP_INDICATOR, get_user_permissons
from app.app.elements import get_app_elms_public_info, get_app_elms_public_info_str, get_app_elms_private_info
from app.app.element import FIELD_PARAM_TYPE
from app.views.utils.list_item_fields import get_items_list, get_item_list_section, get_user_type_allowed_items_filter
from app.settings import DEBUG
import json
from abc import ABC

VALUE_TYPES_FIELD_NAME = "value_types"

def get_input_field_values(app, item_type, body):
    app_elms_public_info = get_app_elms_public_info(app)
    input_fields = body["values"]
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
        error_response = super().validate_message(request, app)
        if None != error_response:
            return error_response
        item_type = None
        self.body = None
        if b'' != request.body:
            self.body = json.loads(request.body)
            item_type = self.body["item_type"]
        else:
            item_type = request.GET.get("item_type")
        user_app_elm_permissons = (
            get_user_permissons(app, self.user_type)
            .get(item_type))
        if None == user_app_elm_permissons:
            return error(403, "Not authorized")
        self.user_app_elm_permissons = user_app_elm_permissons
        app_elms_private_info = get_app_elms_private_info(app)
        self.item_private_info = app_elms_private_info.get(item_type)
        self.item_public_info  = get_app_elms_public_info (app).get(item_type)
        self.item_type = item_type
        if None == self.item_private_info:
            return error(400, "Invalid item type")
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
        return ok(
            section=get_item_list_section(
            request, app, self.user_type, self.item_type))
    
class ItemView(ItemTypeView):
    def validate_message(self, request, app):
        error_response = super().validate_message(request, app)
        if None != error_response:
            return error_response
        item_id = None
        if None != self.body:
            item_id = self.body.get("id")
        else:
            item_id = request.GET.get("id")
        if item_id != None:
            can_user_access_that_item = (
                self.item_model.objects.filter(
                    Q(id=item_id)
                    & get_user_type_allowed_items_filter(request, app, self.user_app_elm_permissons))
                .exists())
            if not can_user_access_that_item:
                # You can test and ensure this works using campus_example app and choosing a teacher user; then you can try accessing the following endpoint and you will notice you will be able to receive information about student setting them user IDs on 'id' url field; but when you try to access some other user type settings its ID on 'id' url field it will not let you access it. url to test: /campus_example/item/?type=user&id=<SET_USER_ID_HERE>&value_types=info
                return not_authorized()
        self.item_id = item_id
        return None
    def post(self, request, app):
        if "c" not in self.user_app_elm_permissons["actions"]:            
            return not_authorized()        
        if not DEBUG and app.endswith(EXAMPLE_APP_INDICATOR):            
            return ok()        
        try:
            input_fields = get_input_field_values(app, self.item_type, self.body)
            created_item = self.item_model.objects.using(app).create(**input_fields)
            list_item_fields = get_app_elms_public_info(app)[self.item_type]["list_item_fields"]
            created_item_fields = []
            for field in list_item_fields:
                created_item_fields.append(getattr(created_item, field))
            created_item_list_fields = get_items_list(request, app, self.user_type, self.item_type, list_item_fields, 
                self.item_model.objects.using(app).filter(id=created_item.id))            
            # TODO: Add specific items updating logic (will require to transfer table generation logic from admin.html to a javascript file)
            return ok(created_item_fields=created_item_list_fields)
        except Exception as e:            
            print(e)
            return error(409, str(e))
    def get(self, request, app):
        item_id = self.item_id
        value_types = request.GET.get(VALUE_TYPES_FIELD_NAME)
        item_fields = None
        if value_types == "value":
            app_elms_public_info = get_app_elms_public_info(app)
            item_type_fields = app_elms_public_info[self.item_type].get("fields")
            if None == item_type_fields:
                item_type_fields = app_elms_public_info[self.item_public_info["source"]["type"]]["fields"]
            fields = list(item_type_fields.keys())
            item_fields = self.item_model.objects.using(app).values(*fields).get(id=item_id)
        elif value_types == "info":
            item_fields = get_items_list(request, app, self.user_type, self.item_type,
                list(self.item_public_info["fields"].keys()), self.item_model.objects.using(app).filter(id=item_id))
        else:
            return error(400, f"'{value_types}' value for '{VALUE_TYPES_FIELD_NAME}' field is not allowed.")
        return ok(item_fields=item_fields)
    def patch(self, request, app):
        if "u" not in self.user_app_elm_permissons["actions"]:
            return not_authorized()
        if not DEBUG and app.endswith(EXAMPLE_APP_INDICATOR):
            return ok()
        try:
            input_fields = get_input_field_values(app, self.item_type, self.body)
            update_result = self.item_model.objects.using(app).filter(id=self.item_id).update(**input_fields)
            print("UPDATE RESULT")
            print(update_result)
            return ok()
        except Exception as e:
            print(e)
            return error(409, str(e))
    def delete(self, request, app):
        if "d" not in self.user_app_elm_permissons["actions"]:
            return not_authorized()
        if not DEBUG and app.endswith(EXAMPLE_APP_INDICATOR):
            return ok()
        try:
            self.item_model.objects.using(app).filter(id=self.item_id).delete()
            return ok()
        except Exception as e:
            print(e)
            return error(409, str(e))
