def do_dictionaries_have_same_keys(dict1, dict2):
    if len(dict1) != len(dict2):
        return False
    for key in dict1:
        if key not in dict2:
            return False
    return True
def do_dictionary_group_have_same_keys(*args):
    dict_1 = args[0]
    for dict_n in args[1:]:
        if not do_dictionaries_have_same_keys(dict_1, dict_n):
            return False
    return True