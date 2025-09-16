from django.apps import apps
from organization.elements.elements import get_org_elms_private_info, get_org_elms_public_info, FIELD_PARAM_TITLE, FIELD_PARAM_TYPE

org_elms_private_info = get_org_elms_private_info()
org_elms_public_info  = get_org_elms_public_info()

def get_item_values_to_request(item_type_fields, field_name, final_fields, prefilter=""):
    print(f"item type field: {field_name}")
    print(item_type_fields.keys())
    field_type = ("int" if "id" == field_name
        else item_type_fields[field_name][FIELD_PARAM_TYPE])
    field_type_pub_info = org_elms_public_info.get(field_type)
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
        if rel_elm_field_type in org_elms_public_info:
            print("ENTRB")
            num_of_subfields += get_item_values_to_request(
                field_type_subfields, rel_elm_field, final_fields, prefilter=prefilter)
        else:
            final_fields.append(f"{prefilter}{rel_elm_field}")
            num_of_subfields += 1
    return num_of_subfields
    
def get_items_list(app, item_type, order_by, fields, queryset):
    item_type_model = apps.get_model(*org_elms_private_info[item_type]["model"].split("."))
    if queryset == None:
        queryset = item_type_model.objects.using(app).filter()
    final_fields = []
    field_x_num_of_subfields = {}
    item_type_info = org_elms_public_info[item_type]
    item_type_fields = item_type_info["fields"]
    print(f"item type: {item_type}")
    print(fields)
    for field_name in fields:
        print("ENTRA")
        field_x_num_of_subfields[field_name] = (
            get_item_values_to_request(
            item_type_fields, field_name, final_fields))
    if "id" not in fields:
        final_fields.append("id")
    section_items = []
    print("FINAL FIELDS")
    print(final_fields)
    for item in list(queryset.order_by(*order_by).values_list(*final_fields)):
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
def get_item_list_section(app, item_type):
    queryset = None
    source = org_elms_public_info[item_type].get("source")
    original_item_type = item_type
    if source != None:
        source_type =  source["type"]
        source_model = apps.get_model(*org_elms_private_info[source_type]["model"].split("."))
        queryset = source_model.objects.using(app).filter(**org_elms_private_info[item_type]["source"]["characteristics"])
        item_type = source_type
    sort_criteria = org_elms_public_info[item_type].get("list_item_sort_criteria", ["id"])
    list_item_fields = org_elms_public_info[item_type]["list_item_fields"]
    items = get_items_list(app, item_type, sort_criteria, list_item_fields, queryset)
    return {
        "title": org_elms_public_info[original_item_type]["title"],
        "item_type": original_item_type,
        "field_titles": get_item_type_field_titles(org_elms_public_info[item_type]["fields"], list_item_fields),
        "items": items,
    }