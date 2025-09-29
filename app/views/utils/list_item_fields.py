from django.apps import apps
from django.db.models import Q
from app.app.elements import get_app_elms_private_info, get_app_elms_public_info
from app.app.element import FIELD_PARAM_TITLE, FIELD_PARAM_TYPE
from app.apps.info import get_user_app_elm_permissons
from user.models import User

def get_item_values_to_request(app, item_type_fields, field_name, final_fields, prefilter=""):
    field_type = ("int" if "id" == field_name
        else item_type_fields[field_name][FIELD_PARAM_TYPE])
    field_type_pub_info = get_app_elms_public_info(app).get(field_type)
    if None == field_type_pub_info:
        final_fields.append(field_name)
        return 1
    prefilter += f"{field_name}__"
    rel_list_item_fields = field_type_pub_info["list_item_fields"]
    field_type_subfields = field_type_pub_info["fields"]
    num_of_subfields = 0
    for rel_elm_field in rel_list_item_fields:
        rel_elm_field_type = ("int" if "id" == rel_elm_field
            else field_type_subfields[rel_elm_field][FIELD_PARAM_TYPE])
        if rel_elm_field_type in get_app_elms_public_info(app):
            num_of_subfields += get_item_values_to_request(
                app, field_type_subfields, rel_elm_field, final_fields, prefilter=prefilter)
        else:
            final_fields.append(f"{prefilter}{rel_elm_field}")
            num_of_subfields += 1
    return num_of_subfields
    
def setup_item_list_user_type_filter(request, app, user_item_type_permissons):
    final_filter = Q()
    _filter = user_item_type_permissons.get("filter")
    if None != _filter:
        final_filter = final_filter & _filter
    user_filter = user_item_type_permissons.get("user_filter")
    if None != user_filter:
        final_filter = final_filter & Q(**{user_filter:request.user})
    app_filter = user_item_type_permissons.get("app_filter")
    if None != app_filter:
        final_filter = final_filter & Q(**{f"{app_filter}__name":app})
    filter_getter = user_item_type_permissons.get("filter_getter")
    if None != filter_getter:
        final_filter = final_filter & filter_getter(request, app)
    return final_filter
def get_items_list(request, app, item_type, fields, queryset=None, user_type=None):
    # 'user_type' field is used to reduce queries
    item_type_model = apps.get_model(*get_app_elms_private_info(app)[item_type]["model"].split("."))
    if queryset == None:
        queryset = item_type_model.objects.using(app).filter()
    if user_type == None:
        user_type = User.objects.get_type(request)
    user_item_type_permissons = get_user_app_elm_permissons(app, user_type, item_type)
    if None == user_item_type_permissons:
        return None
    queryset = queryset.filter(
        setup_item_list_user_type_filter(request, app, user_item_type_permissons))
    final_fields = []
    field_x_num_of_subfields = {}
    item_type_info = get_app_elms_public_info(app)[item_type]
    item_type_fields = item_type_info["fields"]
    for field_name in fields:
        field_x_num_of_subfields[field_name] = (
            get_item_values_to_request(
            app, item_type_fields, field_name, final_fields))
    if "id" not in fields:
        final_fields.append("id")
    section_items = []
    for item in list(queryset.distinct().values_list(*final_fields)):
        item_fields = []
        item_field_counter = 0
        for field_name in fields:
            num_of_subfields = field_x_num_of_subfields.get(field_name)
            if None == num_of_subfields:
                value = item[field_name]
                item_field_counter += 1
            else:
                subvalues = []
                for subvalue in item[item_field_counter:item_field_counter+num_of_subfields]:
                    if subvalue != None:
                        subvalues.append(str(subvalue))
                value = " - ".join(subvalues)
                item_field_counter += num_of_subfields
            item_fields.append(value)
        section_items.append({
            "id": item[final_fields.index("id")],
            "fields": item_fields,
        })
    return section_items

def get_item_type_field_titles(item_type_fields, list_item_fields):
    field_titles = []
    for field in list_item_fields:
        field_titles.append("ID" if "id" == field
            else item_type_fields[field][FIELD_PARAM_TITLE])
    return field_titles
def get_item_list_section(request, app, item_type, user_type=None):
    if user_type == None:
        user_type = User.objects.get_type(request)
    app_elms_public_info = get_app_elms_public_info(app)
    list_item_fields = app_elms_public_info[item_type]["list_item_fields"]
    item_type_model = apps.get_model(*get_app_elms_private_info(app)[item_type]["model"].split("."))
    sort_criteria = app_elms_public_info[item_type].get("list_item_sort_criteria", ["id"])
    queryset = item_type_model.objects.order_by(*sort_criteria)
    items = get_items_list(request, app, item_type, list_item_fields,
        queryset=queryset, user_type=user_type)
    if None == items:
        return None
    return {
        "title"       : app_elms_public_info[item_type]["title"],
        "item_type"   : item_type,
        "actions"     : get_user_app_elm_permissons(app, user_type, item_type)["actions"],
        "field_titles": get_item_type_field_titles(app_elms_public_info[item_type]["fields"], list_item_fields),
        "items"       : items,
    }